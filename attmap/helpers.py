""" Ancillary functions """

from copy import deepcopy
import logging
import sys
if sys.version_info < (3, 3):
    from collections import Mapping
else:
    from collections.abc import Mapping

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["get_data_lines", "is_custom_map"]


def copy(obj):

    def copy(self):
        """
        Copy self to a new object.
        """
        return deepcopy(self)

    obj.copy = copy
    return obj


def get_data_lines(data, fun_key, space_per_level=2, fun_val=None):
    """
    Get text representation lines for a mapping's data.

    :param Mapping data: collection of data for which to get repr lines
    :param function(object) -> str fun_key: function to render key as text
    :param function(object) -> str fun_val: function to render value as text
    :param int space_per_level: number of spaces per level of nesting
    :return Iterable[str]: collection of lines
    """

    # If no specific value-render function, use key-render function
    fun_val = fun_val or fun_key

    def space(lev):
        return " " * lev * space_per_level

    def render(lev, key, val):
        if key is None:
            return space(lev) + val
        valtext = val if val in ["{", "}"] else fun_val(val)
        return space(lev) + fun_key(key) + ": " + valtext

    def go(kvs, curr_lev, acc):
        try:
            k, v = next(kvs)
        except StopIteration:
            return acc
        if not isinstance(v, Mapping) or len(v) == 0:
            acc.append(render(curr_lev, k, v))
        else:
            acc.append(render(curr_lev, k, "{"))
            acc.append(",\n".join(go(iter(v.items()), curr_lev + 1, [])))
            acc.append(render(curr_lev, None, "}"))
        return go(kvs, curr_lev, acc)

    return go(iter(data.items()), 1, [])


def get_logger(name):
    """
    Return a logger equipped with a null handler.

    :param str name: name for the Logger
    :return logging.Logger: simple Logger instance with a NullHandler
    """
    log = logging.getLogger(name)
    log.addHandler(logging.NullHandler())
    return log


def is_custom_map(obj):
    """
    Determine whether an object is a Mapping other than dict.

    :param object obj: object to examine
    :return bool: whether the object is a Mapping other than dict
    """
    return isinstance(obj, Mapping) and type(obj) is not dict
