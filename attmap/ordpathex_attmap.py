""" Canonical behavior for attmap in pepkit projects """

from .ordattmap import OrdAttMap
from ubiquerg import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["OrdPathExAttMap"]


class OrdPathExAttMap(OrdAttMap):
    """ Used in pepkit projects, with Mapping conversion and path expansion """

    @property
    def _transformations(self):
        """ Add path expansion behavior to more general attmap. """
        return super(OrdPathExAttMap, self)._transformations + \
            [(lambda obj: isinstance(obj, str), expandpath)]
