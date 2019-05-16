""" Canonical behavior for attmap in pepkit projects """

from .ordattmap import OrdAttMap
from ubiquerg import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["PathExAttMap"]


class PathExAttMap(OrdAttMap):
    """ Used in pepkit projects, with Mapping conversion and path expansion """

    def __getattr__(self, item, default=None, expand=True):
        try:
            v = super(PathExAttMap, self).__getattribute__(item)
        except AttributeError:
            try:
                return self.__getitem__(item, expand)
            except KeyError:
                # Requested item is unknown, but request was made via
                # __getitem__ syntax, not attribute-access syntax.
                raise AttributeError(item)
        else:
            return expandpath(v) if expand else v

    def __getitem__(self, item, expand=True):
        v = super(PathExAttMap, self).__getitem__(item)
        return self._finalize_value(v) if expand else v

    def _finalize_value(self, v):
        """
        Make any modifications to a retrieved value before returning it.

        This hook accesses an instance's declaration of value mutations, or
        transformations. That sequence may be empty (the base case), in which
        case any value is simply always returned as-is.

        If an instances does declare retrieval modifications, though, the
        declaration should be an iterable of pairs, in which each element's
        first component is a single-argument predicate function evaluated on
        the given value, and the second component of each element is the
        modification to apply if the predicate is satisfied.

        At most one modification function will be called, and it would be the
        first one for which the predicate was satisfied.

        :param object v: a value to consider for modification
        :return object: the finalized value
        """
        return expandpath(v) if isinstance(v, str) else v
