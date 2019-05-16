""" Canonical behavior for attmap in pepkit projects """

from .ordattmap import OrdAttMap
from ubiquerg import expandpath

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["PathExAttMap"]


class PathExAttMap(OrdAttMap):
    """ Used in pepkit projects, with Mapping conversion and path expansion """

    def __getattr__(self, item, default=None, expand=True):
        """
        Get attribute, accessing stored key-value pairs as needed.

        :param str item: name of attribute/key
        :param object default: value to return if requested attr/key is missing
        :param bool expand: whether to attempt path expansion of string value
        :return object: value bound to requested name
        :raise AttributeError: if requested item is unavailable
        """
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
        """
        Fetch the value of given key.

        :param hashable item: key for which to fetch value
        :param bool expand: whether to expand string value as path
        :return object: value mapped to given key, if available
        :raise KeyError: if the requested key is unmapped.
        """
        v = super(PathExAttMap, self).__getitem__(item)
        return self._finalize_value(v) if expand else v

    def items(self, expand=False):
        """
        Produce list of key-value pairs, optionally expanding paths.

        :param bool expand: whether to expand paths
        :return Iterable[object]: stored key-value pairs, optionally expanded
        """
        return [(k, self.__getitem__(k, expand)) for k in self]

    def values(self, expand=False):
        """
        Produce list of values, optionally expanding paths.

        :param bool expand: whether to expand paths
        :return Iterable[object]: stored values, optionally expanded
        """
        return [self.__getitem__(k, expand) for k in self]

    def _data_for_repr(self, expand=False):
        """
        Hook for extracting the data used in the object's text representation.

        :param bool expand: whether to expand paths
        :return Iterable[(hashable, object)]: collection of key-value pairs
            to include in object's text representation
        """
        return filter(lambda kv: not self._excl_from_repr(kv[0], self.__class__),
                      self.items(expand))

    def to_map(self, expand=False):
        """
        Convert this instance to a dict.

        :return dict[str, object]: this map's data, in a simpler container
        """
        return self._simplify_keyvalue(self.items(expand), self._new_empty_basic_map)

    def to_dict(self, expand=False):
        """
        Return a builtin dict representation of this instance.

        :return dict: builtin dict representation of this instance
        """
        return self._simplify_keyvalue(self.items(expand), dict)

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
