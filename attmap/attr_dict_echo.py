""" AttributeDict that echoes an unset key/attr """

from .attr_dict import AttributeDict
from ._mixins import EchoMixin


class AttributeDictEcho(EchoMixin, AttributeDict):
    """ An AttributeDict that returns key/attr if it has no set value. """
    def __contains__(self, item):
        return item in self.__dict__
