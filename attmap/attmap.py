"""Dot notation support for Mappings."""

from __future__ import annotations

from collections.abc import Mapping

from ._att_map_like import AttMapLike
from .helpers import copy, get_logger, safedel_message

_LOGGER = get_logger(__name__)


@copy
class AttMap(AttMapLike):
    """A class to convert a nested mapping(s) into an object(s) with key-values
    using object syntax (attmap.attribute) instead of getitem syntax
    (attmap["key"]). This class recursively sets mappings to objects,
    facilitating attribute traversal (e.g., attmap.attr.attr).
    """

    def __delitem__(self, key: str) -> None:
        try:
            del self.__dict__[key]
        except KeyError:
            _LOGGER.debug(safedel_message(key))

    def __getitem__(self, item: str) -> object:
        return self.__dict__[item]

    def __setitem__(self, key: str, value: object) -> None:
        """Set the given key to the given value.

        Args:
            key: Name of the key/attribute for which to establish value.
            value: Value to which set the given key; if the value is a
                mapping-like object, other keys' values may be combined.
        """
        self.__dict__[key] = self._final_for_store(key, value)

    def __eq__(self, other: object) -> bool:
        if (type(self) != type(other)) or (len(self) != len(other)):
            return False
        for k, v in self.items():
            if self._excl_from_eq(k):
                _LOGGER.debug("Excluding from comparison: {}".format(k))
                continue
            if not self._cmp(v, other[k]):
                return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self == other

    @staticmethod
    def _cmp(a: object, b: object) -> bool:
        """Hook to tailor value comparison in determination of map equality."""
        try:
            import numpy as np
            import pandas as pd

            if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
                return bool(np.array_equal(a, b))
            if isinstance(a, pd.Series) and isinstance(b, pd.Series):
                return a.equals(b)
            if isinstance(a, pd.DataFrame) and isinstance(b, pd.DataFrame):
                return a.equals(b)
        except ImportError:
            pass
        try:
            return a == b
        except ValueError:
            return False

    def _final_for_store(self, k: str, v: object) -> object:
        """Before storing a value, apply any desired transformation.

        Args:
            k: Key for which to store value.
            v: Value to potentially transform before storing.

        Returns:
            Finalized value.
        """
        if isinstance(v, Mapping) and not isinstance(v, self._lower_type_bound):
            v = self._metamorph_maplike(v)
        return v

    @property
    def _lower_type_bound(self):
        return AttMap

    def _metamorph_maplike(self, m: Mapping) -> "AttMap":
        """Ensure a stored Mapping conforms with type expectation.

        Args:
            m: The mapping to which to apply type transformation.

        Returns:
            A (perhaps more specialized) version of the given map.

        Raises:
            TypeError: If the given value isn't a Mapping.
        """
        if not isinstance(m, Mapping):
            raise TypeError(
                "Cannot integrate a non-Mapping: {}\nType: {}".format(m, type(m))
            )
        return self._lower_type_bound(m.items())

    def _new_empty_basic_map(self) -> dict:
        """Return the empty collection builder for Mapping type simplification."""
        return dict()

    def _repr_pretty_(self, p, cycle: bool) -> str:
        """IPython display hook.

        Args:
            p: IPython PrettyPrinter instance.
            cycle: Whether a cyclic reference is detected.

        Returns:
            Text representation of the instance.
        """
        return p.text(repr(self) if not cycle else "...")
