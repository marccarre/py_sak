'''
Utilities to help write concurrent code in Python.
- concurrent_class_factory: helps to create a concurrent version of the provided class,
  by reflecting on the API, and wrapping around a thread-pool.
'''

import logging
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from threading import local, current_thread
from inspect import getmembers, ismethod, isfunction
from functools import partial
from py_sak.functions import log_debug, try_catch


_DOC_STRING = '''
    - factory and factory_args (Optional):
    Factory function and its arguments to create thread-local instances of
    the thread-unsafe class.
    These only need to be provided if the thread-unsafe class has a non-empty constructor,
    as instances of it are lazily and locally created in each thread/process.

    - pool (Optional):
    The pool of workers to parallelize processing on.
    It needs to conform to multiprocessing.Pool's API.
    If no pool is provided, default is a thread-pool (multiprocessing.pool.ThreadPool),
    which is only recommended for I/O-bound processes, as the GIL prevents true parallelism.

    - num_threads (Optional, Default: 4*cpu_count())
    The number of worker threads to allocate to the pool, if none is provided.
    N.B.: it is recommended to benchmark your client with various values for this parameter,
    as the optimal performance will depend on both your hardware and your workload.

    - raise_exceptions (Optional, Default: False):
    When set to False, exceptions will be caught and return as a resulting object.
    When set to True, concurrent processing will be interrupted and exception raised.
'''


def concurrent_class_factory(concurrent_class_name, thread_unsafe_class):
    '''
    Dynamically creates a thread-safe class which exposes the same API as
    the provided thread-unsafe class, but for which all public methods now:
    - accept an iterable of inputs,
    - parallelize processing of this iterable on a pool of workers.

    The resulting class's __init__ method optionally accepts: %s
    '''
    concurrent_class = _create_blank_concurrent_class(concurrent_class_name, thread_unsafe_class)
    for method_name, method in getmembers(thread_unsafe_class, lambda x: ismethod(x) or isfunction(x)):
        if not method_name.startswith('_'):
            setattr(concurrent_class, method_name, _mapper_for(method, method_name))
    return concurrent_class

concurrent_class_factory.__doc__ = concurrent_class_factory.__doc__ % _DOC_STRING


def _create_blank_concurrent_class(concurrent_class_name, thread_unsafe_class):
    def __init__(self, factory=None, factory_args=None, pool=None, num_threads=4 * cpu_count(), raise_exceptions=False):
        self._raise_exceptions = raise_exceptions
        self._local = local()
        self._pool = pool or _pool_for_io_bound_workload(self._local, factory or thread_unsafe_class, factory_args, num_threads)
    __init__.__doc__ = _DOC_STRING
    return type(concurrent_class_name, (object,), {'__init__': __init__})


def _pool_for_io_bound_workload(thread_local, factory, factory_args, num_threads):
    initializer = partial(_get_or_create_object, thread_local, factory)
    if factory_args is None:
        return ThreadPool(processes=num_threads, initializer=initializer)
    else:
        return ThreadPool(processes=num_threads, initializer=initializer, initargs=[factory_args])


def _get_or_create_object(thread_local, factory, factory_args=None):
    thread_unsafe_object = getattr(thread_local, 'thread_unsafe_object', None)
    if not thread_unsafe_object:
        logging.info('Creating thread-unsafe object in thread %s...', current_thread())
        thread_local.thread_unsafe_object = factory() if (factory_args is None) else factory(*factory_args)


def _mapper_for(method, method_name):
    def lazy_method(method_name, mapper_args):
        self, args = mapper_args
        func = getattr(self._local.thread_unsafe_object, method_name)
        args_type = type(args)
        if (args_type is list) or (args_type is tuple):
            return log_debug(func, *args) if self._raise_exceptions else try_catch(func, *args)
        elif args_type is dict:
            return log_debug(func, **args) if self._raise_exceptions else try_catch(func, **args)
        else:
            return log_debug(func, args) if self._raise_exceptions else try_catch(func, args)

    def mapper_method(self, iterable, chunk_size=None):
        return self._pool.map(
            partial(lazy_method, method_name),
            zip([self] * len(iterable), iterable),
            chunk_size
        )
    mapper_method.__doc__ = method.__doc__
    return mapper_method
