""" Ancillary functions """

from copy import deepcopy
import logging
import os


def copy(obj):

    def copy(self):
        """
        Copy self to a new object.
        """
        return deepcopy(self)

    obj.copy = copy
    return obj


def expandpath(p):
    """
    Expand environment and/or user variable(s) in a path.

    :param str p: path in which to populate variables for which value is
        available in current state
    :return str: variable-expanded path
    """
    return os.path.expanduser(os.path.expandvars(p))


def get_logger(name):
    """
    Return a logger equipped with a null handler.

    :param str name: name for the Logger
    :return logging.Logger: simple Logger instance with a NullHandler
    """
    log = logging.getLogger(name)
    log.addHandler(logging.NullHandler())
    return log
