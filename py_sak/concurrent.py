import logging
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from threading import local, current_thread
from inspect import getmembers, ismethod, isfunction, getargspec
from functools import partial


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
    for method_name, method in getmembers(thread_unsafe_class, ismethod):
        if not method_name.startswith('_'):
            setattr(concurrent_class, method_name, _mapper_for(method, method_name))
    return concurrent_class

concurrent_class_factory.__doc__ = concurrent_class_factory.__doc__ % _DOC_STRING


def _create_blank_concurrent_class(concurrent_class_name, thread_unsafe_class):
    def __init__(self, factory=None, factory_args=None, pool=None):
        self._local = local()
        self._pool = pool or _pool_for_io_bound_workload(self._local, factory or thread_unsafe_class, factory_args)
    __init__.__doc__ = _DOC_STRING
    return type(concurrent_class_name, (object,), {'__init__': __init__})

def _pool_for_io_bound_workload(thread_local, factory, factory_args, num_threads=4*cpu_count()):
    initializer = partial(_get_or_create_object, thread_local, factory)
    if factory_args is None:
        return ThreadPool(processes=num_threads, initializer=initializer)
    else: 
        return ThreadPool(processes=num_threads, initializer=initializer, initargs=factory_args)

def _get_or_create_object(thread_local, factory, factory_args=None):
    thread_unsafe_object = getattr(thread_local, 'thread_unsafe_object', None)
    if not thread_unsafe_object:
        logging.info('Creating thread-unsafe object in thread %s...' % current_thread())
        thread_local.thread_unsafe_object = factory() if (factory_args is None) else factory(factory_args)

def _mapper_for(method, method_name): 
    def lazy_method(method_name, mapper_args):
        logging.debug('Starting "%s" in thread %s...' % (method_name, current_thread()))
        self, args = mapper_args
        thread_unsafe_object = self._local.thread_unsafe_object
        thread_unsafe_method = getattr(thread_unsafe_object, method_name)
        results = thread_unsafe_method(args)
        logging.debug('Finished "%s" in thread %s...' % (method_name, current_thread()))
        return results

    mapper_method = lambda self, iterable, chunk_size=None: self._pool.map(
            partial(lazy_method, method_name), 
            zip([self]*len(iterable), iterable), 
            chunk_size
        )
    mapper_method.__doc__ = method.__doc__
    return mapper_method
