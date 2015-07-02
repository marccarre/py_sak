import logging
from threading import current_thread

def log_debug(f, args=None):
    ''' Wrap call of provided function with debug log statements. '''
    logging.debug('Starting "%s" in thread %s...' % (f.__name__, current_thread()))
    results = f(*args) if (args is not None) else f()
    logging.debug('Successfully finished "%s" in thread %s.' % (f.__name__, current_thread()))
    return results

def try_catch(f, args=None):
    ''' 
    Wrap call of provided function with try/except block and debug log statements. 
    If an instance of 'Exception' (or one of its subclasses) is thrown by 'f', 
    it is caught, and the exception object itself is return as a result.
    '''
    try:
        return log_debug(f, args)
    except Exception as e:
        logging.debug('Error in "%s" in thread %s: %s' % (f.__name__, current_thread(), e))
        return e
