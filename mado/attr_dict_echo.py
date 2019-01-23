""" AttributeDict that echoes an unset key/attr """

from .attr_dict import AttributeDict
from ._mixins import EchoMixin


class AttributeDictEcho(EchoMixin, AttributeDict):
    """ An AttributeDict that returns key/attr if it has no set value. """
    pass
