""" Canonical behavior for attmap in pepkit projects """

from .ordattmap import OrdAttMap
from ubiquerg import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["PathExAttMap"]


class PathExAttMap(OrdAttMap):
    """ Used in pepkit projects, with Mapping conversion and path expansion """

    @property
    def _retrieval_mutations(self):
        """ Add path expansion behavior to more general attmap. """
        return super(PathExAttMap, self)._retrieval_mutations + \
               [(lambda obj: isinstance(obj, str), expandpath)]
