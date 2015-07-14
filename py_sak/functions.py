'''
Utilities to help write functional code in Python and enhance existing functions.
- log_debug: add debug-level log statements before and after calling the provided function.
- try_catch: avoid the provided function to raise exception by handling and returning them.
'''

import logging
from threading import current_thread


def log_debug(func, *args, **kwargs):
    ''' Wrap call of provided function with debug log statements. '''
    logging.debug('Starting "%s" in thread %s...', func.__name__, current_thread())
    results = func(*args, **kwargs)
    logging.debug('Successfully finished "%s" in thread %s.', func.__name__, current_thread())
    return results


def try_catch(func, *args, **kwargs):
    '''
    Wrap call of provided function with try/except block and debug log statements.
    If an instance of 'Exception' (or one of its subclasses) is thrown by 'func',
    it is caught, and the exception object itself is return as a result.
    '''
    try:
        return log_debug(func, *args, **kwargs)
    except Exception as exc:
        logging.debug('Error in "%s" in thread %s: %s', func.__name__, current_thread(), exc)
        return exc
