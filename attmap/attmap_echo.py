""" AttMap that echoes an unset key/attr """

from .attmap import AttMap
from ._mixins import EchoMixin


class AttMapEcho(EchoMixin, AttMap):
    """ An AttMap that returns key/attr if it has no set value. """
    def __contains__(self, item):
        return item in self.__dict__
