""" Ordered attmap """

from collections import OrderedDict
from .attmap import AttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["OrdAttMap"]


class OrdAttMap(AttMap, OrderedDict):
    """ Insertion-ordered mapping with dot notation access """

    def __init__(self, entries=None):
        super(OrderedDict, self).__init__()
        super(AttMap, self).__init__(entries)
