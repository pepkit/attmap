""" Canonical behavior for attmap in pepkit projects """

from .attmap import AttMap
from .helpers import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["PathExAttMap"]


class PathExAttMap(AttMap):
    """ Used in pepkit projects, with Mapping conversion and path expansion """

    @property
    def _transformations(self):
        """ Add path expansion behavior to more general attmap. """
        return super(PathExAttMap, self)._transformations + \
            [(lambda obj: isinstance(obj, str), expandpath)]
