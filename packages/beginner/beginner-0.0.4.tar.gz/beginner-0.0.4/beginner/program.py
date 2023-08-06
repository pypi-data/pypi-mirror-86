"""The module to let beginners in Python studies it more easily.

This module is mainly to make a program easily.

Import the module and call it."""


def error(exception: BaseException, *args, **kwargs):
    """Use raise for exceptions.
    Put the key-word into a function for use."""
    raise exception(args, kwargs)


if __name__ == '__main__':
    error(Exception, '123')
