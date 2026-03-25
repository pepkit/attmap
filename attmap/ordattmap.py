"""Ordered attmap."""

from __future__ import annotations

from collections import OrderedDict

from .attmap import AttMap
from .helpers import get_logger, safedel_message

__all__ = ["OrdAttMap"]

_LOGGER = get_logger(__name__)


class OrdAttMap(OrderedDict, AttMap):
    """Insertion-ordered mapping with dot notation access."""

    def __init__(self, entries=None) -> None:
        super().__init__(entries or {})

    def __setattr__(self, name: str, value: object) -> None:
        if not (self._is_od_member(name) or name.startswith("__")):
            self[name] = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, item: str) -> object:
        if not (self._is_od_member(item) or item.startswith("__")):
            return self[item]
        else:
            super().__getattr__(item)

    def __getitem__(self, item: str) -> object:
        """Attempt ordinary access, then access to attributes.

        Args:
            item: Key/attr for which to fetch value.

        Returns:
            Value to which given key maps.
        """
        try:
            return super().__getitem__(item)
        except KeyError:
            return AttMap.__getitem__(self, item)

    def __setitem__(self, key: str, value: object, finalize: bool = True) -> None:
        """Support hook for value transformation before storage."""
        super().__setitem__(
            key, self._final_for_store(key, value) if finalize else value
        )

    def __delitem__(self, key: str) -> None:
        """Make unmapped key deletion unexceptional."""
        try:
            super().__delitem__(key)
        except KeyError:
            _LOGGER.debug(safedel_message(key))

    def __eq__(self, other: object) -> bool:
        """Leverage base AttMap eq check, and check key order."""
        return AttMap.__eq__(self, other) and list(self.keys()) == list(other.keys())

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __repr__(self) -> str:
        """Leverage base AttMap text representation."""
        return AttMap.__repr__(self)

    def __reversed__(self):
        _LOGGER.warning("Reverse iteration as implemented may be inefficient")
        return iter(reversed(list(self.keys())))

    def keys(self) -> list:
        return [k for k in self]

    def values(self) -> list:
        return [self[k] for k in self]

    def items(self) -> list[tuple]:
        return [(k, self[k]) for k in self]

    def clear(self) -> None:
        raise NotImplementedError(
            "Clearance isn't implemented for {}".format(self.__class__.__name__)
        )

    __marker = object()

    def pop(self, key, default=__marker):
        try:
            return super().pop(key)
        except KeyError:
            try:
                return self.__dict__.pop(key)
            except KeyError:
                if default is self.__marker:
                    raise KeyError(key)
                return default

    def popitem(self, last: bool = True):
        raise NotImplementedError(
            "popitem isn't supported on a {}".format(self.__class__.__name__)
        )

    @staticmethod
    def _is_od_member(name: str) -> bool:
        """Assess whether name appears to be a protected OrderedDict member."""
        return name.startswith("_OrderedDict")

    def _new_empty_basic_map(self) -> OrderedDict:
        """For ordered maps, OrderedDict is the basic building block."""
        return OrderedDict()

    @property
    def _lower_type_bound(self):
        """OrdAttMap is the type to which nested maps are converted."""
        return OrdAttMap
