""" Ancillary functions """

from copy import deepcopy
import logging


def copy(obj):

    def copy(self):
        """
        Copy self to a new object.
        """
        return deepcopy(self)

    obj.copy = copy
    return obj


def get_logger(name):
    """
    Return a logger equipped with a null handler.

    :param str name: name for the Logger
    :return logging.Logger: simple Logger instance with a NullHandler
    """
    log = logging.getLogger(name)
    log.addHandler(logging.NullHandler())
    return log
