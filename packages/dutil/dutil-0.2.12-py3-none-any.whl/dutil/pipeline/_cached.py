import pyarrow
import functools
# from contextlib import contextmanager
# from contextvars import ContextVar
import numpy as np
import pandas as pd
import dill
from pathlib import Path
import shutil
import xxhash
from dask.delayed import Delayed
from typing import Optional, Union, List
from loguru import logger as _logger
import json

_ = pyarrow.__version__  # explicitly show pyarrow dependency

xxhasher = xxhash.xxh64(seed=42)


def _hash_obj(obj):
    if isinstance(obj, CachedResult):
        h = obj.get_hash()
    elif isinstance(obj, np.ndarray):
        xxhasher.update(obj.data)
        h = str(xxhasher.intdigest())
        xxhasher.reset()
    elif isinstance(obj, pd.Series):
        xxhasher.update(obj.values.data)
        h = str(xxhasher.intdigest())
        xxhasher.reset()
    elif isinstance(obj, pd.DataFrame):
        for c in obj:
            try:
                xxhasher.update(obj[c].values.data)
            except ValueError:
                xxhasher.update(obj[c].astype(str).values.data)
        h = str(xxhasher.intdigest())
        xxhasher.reset()
    else:
        h = str(obj)
    return h


def _get_cache_path(name, name_prefix, parameters, ignore_args, ignore_kwargs,
                    folder, ftype, kwargs_sep, foo, args, kwargs) -> Path:
    path = Path(folder)
    if ignore_args is None:
        ignore_args = parameters is not None
    if ignore_kwargs is None:
        ignore_kwargs = parameters is not None
    if name is None:
        name = foo.__name__
    _n = [name]
    if parameters is not None:
        _n.extend([str(k) + kwargs_sep + _hash_obj(v) for k, v in parameters.items()])
    if not ignore_args:
        _n.extend([_hash_obj(a) for a in args])
    if not ignore_kwargs:
        _n.extend([str(k) + kwargs_sep + _hash_obj(v) for k, v in kwargs.items()])
    elif isinstance(ignore_kwargs, list) or isinstance(ignore_kwargs, set):
        _n.extend([str(k) + kwargs_sep + _hash_obj(v) for k, v in kwargs.items()
                   if k not in ignore_kwargs])
    else:
        assert isinstance(ignore_kwargs, bool)
    full_name = '_'.join(_n) + '.' + ftype
    if name_prefix is not None:
        full_name = name_prefix + '__' + full_name
    path = path / full_name
    return path


def _cached_load(ftype, path):
    if ftype == 'parquet':
        data = pd.read_parquet(path)
    elif ftype == 'pickle':
        data = dill.load(open(path, 'rb'))
    else:
        raise ValueError('ftype {} is not recognized'.format(ftype))
    return data


def _cached_save(data, ftype, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if ftype == 'parquet':
        data.to_parquet(path, index=False, allow_truncated_timestamps=True)
    elif ftype == 'pickle':
        dill.dump(data, open(path, 'wb'))
    else:
        raise ValueError('ftype {} is not recognized'.format(ftype))


def _get_meta_path(cache_path: Path) -> Path:
    return cache_path.parent / (cache_path.name + '.meta')


class CacheMeta:
    """Cache meta data (incl. hash)"""

    def __init__(
        self,
        name: str,
        meta_path: Union[str, Path],
        cache_path: Union[str, Path],
        ftype: str,
        hash_value: Optional[str]
    ):
        self.name = name
        self.meta_path = Path(meta_path)
        self.cache_path = Path(cache_path)
        self.ftype = ftype
        self.hash_value = hash_value

    @classmethod
    def from_file(cls, meta_path: Path):
        with open(meta_path, 'rt') as f:
            fields = json.load(f)
        return cls(**fields)

    def dump_to_file(self):
        with open(self.meta_path, 'wt') as f:
            fields = {k: str(v) for k, v in self.__dict__.items()}
            json.dump(fields, f)


class CachedResult:
    """Lazy loader for cache data"""

    def __init__(self, name, name_prefix, parameters, ignore_args, ignore_kwargs,
                 folder, ftype, kwargs_sep, foo, args, kwargs, logger):
        cache_path = _get_cache_path(name, name_prefix, parameters,
                                     ignore_args, ignore_kwargs,
                                     folder, ftype, kwargs_sep, foo, args, kwargs)
        meta_path = _get_meta_path(cache_path)
        name = cache_path.name
        if meta_path.exists():
            self.meta = CacheMeta.from_file(meta_path)
        else:
            self.meta = CacheMeta(name, meta_path, cache_path, ftype, hash_value=None)
        self._cache_value = None
        self.logger = logger

    def load(self):
        """Load data from cache"""

        if self._cache_value is None:
            self._cache_value = _cached_load(self.meta.ftype, self.meta.cache_path)
            self.logger.debug('Task {}: data has been loaded from cache'.format(self.meta.name))
        return self._cache_value

    def dump(self, data):
        """Dump data to cache"""

        self._cache_value = data
        _cached_save(data, self.meta.ftype, self.meta.cache_path)
        self.logger.debug('Task {}: data has been saved to cache'.format(self.meta.name))
        self.meta.dump_to_file()

    def get_hash(self):
        """Get hash of cached data

        Used to construct a cache file name
        """

        # Hash may not be required, so it's not automatically computed from data
        if self.meta.hash_value is None:
            cache_obj = self.load()
            self.meta.hash_value = _hash_obj(cache_obj)
            self.meta.dump_to_file()
            self.logger.debug('Task {}: hash has been computed from data'.format(self.meta.name))
        return self.meta.hash_value

    def exists(self):
        return self.meta.cache_path.exists() and self.meta.meta_path.exists()


def cached(
    name: Optional[str] = None,
    name_prefix: Optional[str] = None,
    parameters: Optional[dict] = None,
    ignore_args: Optional[bool] = None,
    ignore_kwargs: Optional[Union[bool, List[str]]] = None,
    folder: Union[str, Path] = 'cache',
    ftype: str = 'pickle',
    kwargs_sep: str = '|',
    override: bool = False,
    logger=None,
):
    """Cache function output on the disk (advanced version)

    Features:
    - Pickle and parquet serialization
    - Special treatment for Delayed objects
    - Lazy cache loading
    - Hashing of complex arguments

    :param name: name of the cache file
        if none, name is constructed from the function name and args
    :param parameters: include these parameters in the name
        only meaningful when `name=None`
    :param ignore_args: if true, do not add args to the name
    :param ignore_kwargs: if true, do not add kwargs to the name
        it's also possible to specify a list of kwargs to ignore
    :param folder: name of the cache folder
    :param ftype: type of the cache file
        'pickle' | 'parquet'
    :param kwargs_sep: string separating a keyword parameter and its value
    :param override: if true, override the existing cache file
    :param logger: if none, use a new logger
    :return: new function
        output is lazily loaded from cache file if it exists, generated otherwise
        .load() to get data
    """

    logger = logger if logger is not None else _logger

    def decorator(foo):
        @functools.wraps(foo)
        def new_foo(*args, **kwargs):
            result = CachedResult(name, name_prefix, parameters,
                                  ignore_args, ignore_kwargs,
                                  folder, ftype, kwargs_sep,
                                  foo, args, kwargs,
                                  logger=logger)
            if not override and result.exists():
                # if the result (= cache OR cache + hash) exists, do nothing - just pass it on
                # the cache will be loaded only if required later
                logger.info('Task {}: skip (cache exists)'.format(result.meta.name))
            else:
                # if the result does not exist, generate data and save cache
                dask_args_detected = any(isinstance(a, Delayed) for a in args)
                dask_kwargs_detected = any(isinstance(v, Delayed) for k, v in kwargs.items())
                if not dask_args_detected and not dask_kwargs_detected:
                    # eager load cache for all arguments
                    args = [a.load() if isinstance(a, CachedResult) else a for a in args]
                    kwargs = {k: v.load() if isinstance(v, CachedResult) else v for k, v in kwargs.items()}
                    data = foo(*args, **kwargs)
                    result.dump(data)
                    logger.info('Task {}: data has been computed and saved to cache'.format(result.meta.name))
                else:
                    # if any of the arguments is a Delayed object, return anything
                    result = foo(*args, **kwargs)
            return result
        return new_foo
    return decorator


def clear_cache(
    folder: Union[str, Path] = 'cache',
    ignore_errors: bool = True,
):
    """Clear the cache folder

     :param folder: name of the cache folder
    """
    folder = Path(folder).absolute()
    shutil.rmtree(folder, ignore_errors=ignore_errors)
