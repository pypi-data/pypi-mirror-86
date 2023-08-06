"""The module to let beginners in Python studies it more easily.

The module provides classes and functions which are common or important for beginners.
It includes code to do many kinds of Python goal.

Import the module and call it."""

import re  # This module is mainly to process strings.


def find_all(string: str, parent_string: str):
    """Find all the str in another longer str without "re" module."""
    return ((match.start(), match.end()) for match in re.finditer(string, parent_string))


def delete(string: str, parent_string: str) -> str:
    """Delete all the str in another longer str without "re" module or for/while loop.
    In fact, the func mainly uses "replace" method of class str."""
    return parent_string.replace(string, '')  # Let an empty string takes string's place.


def read_file(path: str) -> str:
    """When using function "open", it returns a file class object, then call "read" method to read it.
    Use this function without classes."""
    file = open(path, 'r')  # Open the file with mode 'r'(readonly).
    text = file.read()  # Read the file.
    file.close()  # Close the file.
    return text  # Return.


def try_running(code: str, *exceptions) -> bool:
    """Run code which is str type. While an exception happens, if it is in arg exceptions, return False,
    if not, raise CompileFailedError. If no exception happened, return True."""
    succeeded: bool = True
    try:
        exec(code)
    except exceptions:
        succeeded = False
    except BaseException:
        raise CompileFailedError()
    return succeeded


def write_file(path: str, text: str) -> None:
    """When using function "open", it returns a file class object, then call "write" method to write it.
    Use this function without classes."""
    file = open(path, 'w')
    file.write(text)
    file.close()


class CompileFailedError(Exception):
    def __str__(self):
        return 'Can not run the code because Python compiler cannot compile the code.'


def merge_dict(*dic):
    """Merge some dict. If they have the same key, the value is in the last dict.
    :return: Merged dict."""
    result = {}
    for dictionary in dic:
        for key in dictionary:
            result[key] = dictionary[key]
    return result


__globals__ = globals()

if __name__ == '__main__':
    print(__globals__)
