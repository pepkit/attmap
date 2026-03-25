"""Ancillary functions."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from copy import deepcopy

__all__ = ["get_data_lines"]


def copy(obj):
    def copy(self):
        """Copy self to a new object."""
        return deepcopy(self)

    obj.copy = copy
    return obj


def get_data_lines(
    data: Mapping,
    fun_key: callable,
    space_per_level: int = 2,
    fun_val: callable | None = None,
) -> list[str]:
    """Get text representation lines for a mapping's data.

    Args:
        data: Collection of data for which to get repr lines.
        fun_key: Function to render key as text.
        space_per_level: Number of spaces per level of nesting.
        fun_val: Function to render value as text.

    Returns:
        Collection of lines.
    """
    fun_val = fun_val or fun_key

    def space(lev):
        return " " * lev * space_per_level

    def render(lev, key, **kwargs):
        ktext = fun_key(key) + ":"
        try:
            val = kwargs["val"]
        except KeyError:
            return space(lev) + ktext
        else:
            return space(lev) + "{} {}".format(
                ktext, "null" if val is None else fun_val(val, space(lev))
            )

    def go(kvs, curr_lev, acc):
        try:
            k, v = next(kvs)
        except StopIteration:
            return acc
        if not isinstance(v, Mapping) or len(v) == 0:
            acc.append(render(curr_lev, k, val=v))
        else:
            acc.append(render(curr_lev, k))
            acc.append("\n".join(go(iter(v.items()), curr_lev + 1, [])))
        return go(kvs, curr_lev, acc)

    return go(iter(data.items()), 0, [])


def get_logger(name: str) -> logging.Logger:
    """Return a logger equipped with a null handler.

    Args:
        name: Name for the Logger.

    Returns:
        Simple Logger instance with a NullHandler.
    """
    log = logging.getLogger(name)
    log.addHandler(logging.NullHandler())
    return log


def is_custom_map(obj: object) -> bool:
    """Determine whether an object is a Mapping other than dict.

    Args:
        obj: Object to examine.

    Returns:
        Whether the object is a Mapping other than dict.
    """
    return isinstance(obj, Mapping) and type(obj) is not dict


def safedel_message(key) -> str:
    """Create safe deletion log message.

    Args:
        key: Unmapped key for which deletion/removal was tried.

    Returns:
        Message to log unmapped key deletion attempt.
    """
    return "No key {} to delete".format(key)
