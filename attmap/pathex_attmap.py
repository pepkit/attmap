"""Canonical behavior for attmap in pepkit projects."""

from __future__ import annotations

from collections.abc import Mapping

from ubiquerg import expandpath

from .ordattmap import OrdAttMap

__all__ = ["PathExAttMap"]


class PathExAttMap(OrdAttMap):
    """Used in pepkit projects, with Mapping conversion and path expansion."""

    def __getattribute__(self, item: str, expand: bool = True) -> object:
        res = super().__getattribute__(item)
        return _safely_expand(res) if expand else res

    def __getattr__(
        self, item: str, default: object = None, expand: bool = True
    ) -> object:
        """Get attribute, accessing stored key-value pairs as needed.

        Args:
            item: Name of attribute/key.
            default: Value to return if requested attr/key is missing.
            expand: Whether to attempt path expansion of string value.

        Returns:
            Value bound to requested name.

        Raises:
            AttributeError: If requested item is unavailable.
        """
        try:
            v = super().__getattribute__(item)
        except AttributeError:
            try:
                return self.__getitem__(item, expand)
            except KeyError:
                raise AttributeError(item)
        else:
            return _safely_expand(v) if expand else v

    def __getitem__(
        self, item: str, expand: bool = True, to_dict: bool = False
    ) -> object:
        """Fetch the value of given key.

        Args:
            item: Key for which to fetch value.
            expand: Whether to expand string value as path.
            to_dict: Whether to recursively convert mappings to dicts.

        Returns:
            Value mapped to given key, if available.

        Raises:
            KeyError: If the requested key is unmapped.
        """
        v = super().__getitem__(item)
        return _safely_expand(v, to_dict) if expand else v

    def get(self, k: str, default: object = None, expand: bool = True) -> object:
        try:
            return self.__getitem__(k, expand)
        except KeyError:
            return default

    def items(self, expand: bool = False, to_dict: bool = False) -> list[tuple]:
        """Produce list of key-value pairs, optionally expanding paths.

        Args:
            expand: Whether to expand paths.
            to_dict: Whether to recursively convert mappings to dicts.

        Returns:
            Stored key-value pairs, optionally expanded.
        """
        return [(k, self.__getitem__(k, expand, to_dict)) for k in self]

    def values(self, expand: bool = False) -> list:
        """Produce list of values, optionally expanding paths.

        Args:
            expand: Whether to expand paths.

        Returns:
            Stored values, optionally expanded.
        """
        return [self.__getitem__(k, expand) for k in self]

    def _data_for_repr(self, expand: bool = False):
        """Hook for extracting the data used in the object's text representation.

        Args:
            expand: Whether to expand paths.

        Returns:
            Collection of key-value pairs to include in text representation.
        """
        return filter(
            lambda kv: not self._excl_from_repr(kv[0], self.__class__),
            self.items(expand),
        )

    def to_map(self, expand: bool = False) -> dict:
        """Convert this instance to a dict.

        Args:
            expand: Whether to expand paths.

        Returns:
            This map's data, in a simpler container.
        """
        return self._simplify_keyvalue(self.items(expand), self._new_empty_basic_map)

    def to_dict(self, expand: bool = False) -> dict:
        """Return a builtin dict representation of this instance.

        Args:
            expand: Whether to expand paths.

        Returns:
            Builtin dict representation of this instance.
        """
        return self._simplify_keyvalue(self.items(expand, to_dict=True), dict)

    @property
    def _lower_type_bound(self):
        return PathExAttMap


def _safely_expand(x: object, to_dict: bool = False) -> object:
    if isinstance(x, str):
        return expandpath(x)
    if to_dict and isinstance(x, Mapping):
        return {k: _safely_expand(v, to_dict) for k, v in x.items()}
    return x
