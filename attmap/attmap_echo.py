""" AttMap that echoes an unset key/attr """

from .pepattmap import PepAttMap
from ._mixins import *


class AttMapEcho(EchoMixin, PepAttMap):
    """ An AttMap that returns key/attr if it has no set value. """

    def __contains__(self, item):
        return item in self.__dict__

    @property
    def _lower_type_bound(self):
        """ Most specific type to which an inserted value may be converted """
        return AttMapEcho
