'''
Utilities to help validate input.

Primitive types:
- is_float
- is_int

Files and directories:
- is_valid_file
- is_valid_dir
- is_readable
'''

import os


def is_float(value):
    '''
    Returns True if provided value is a float or can be converted into a float.
    Returns False otherwise.
    '''
    return _is_type(float, value)


def is_int(value):
    '''
    Returns True if provided value is an int or can be converted into an int.
    Returns False otherwise.
    '''
    return _is_type(int, value)


def _is_type(convert, value):
    ''' Returns True if provided value can be converted into provided type, or False otherwise. '''
    try:
        convert(value)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_file(path):
    ''' Returns True if provided file exists and is a file, or False otherwise. '''
    return os.path.exists(path) and os.path.isfile(path)


def is_valid_dir(path):
    ''' Returns True if provided directory exists and is a directory, or False otherwise. '''
    return os.path.exists(path) and os.path.isdir(path)


def is_readable(path):
    '''
    Returns True if provided file or directory exists and can be read with the current user.
    Returns False otherwise.
    '''
    return os.access(os.path.abspath(path), os.R_OK)
