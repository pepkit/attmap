"""The trait defining a multi-access data object."""

from __future__ import annotations

import abc
from collections.abc import Mapping, MutableMapping

from .helpers import get_data_lines, get_logger, is_custom_map

__all__ = ["AttMapLike"]

_LOGGER = get_logger(__name__)


class AttMapLike(MutableMapping):
    """Base class for multi-access-mode data objects."""

    def __init__(self, entries: "Mapping | None" = None) -> None:
        """Create a new instance, optionally with initial key-value pairs.

        Args:
            entries: Initial KV pairs to store.
        """
        self.add_entries(entries)

    def __getattr__(self, item: str, default: object = None) -> object:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            try:
                return self.__getitem__(item)
            except KeyError:
                raise AttributeError(item)

    @abc.abstractmethod
    def __delitem__(self, item: str) -> None:
        pass

    @abc.abstractmethod
    def __getitem__(self, item: str) -> object:
        pass

    @abc.abstractmethod
    def __setitem__(self, key: str, value: object) -> None:
        pass

    def __iter__(self):
        return iter([k for k in self.__dict__.keys()])

    def __len__(self) -> int:
        return sum(1 for _ in iter(self))

    def __repr__(self) -> str:
        return self._render(
            self._simplify_keyvalue(self._data_for_repr(), self._new_empty_basic_map)
        )

    def _render(self, data, exclude_class_list: list[str] = []) -> str:
        def _custom_repr(obj, prefix: str = "") -> str:
            """Call the ordinary repr on every object but list.

            Lists are converted to a block style string instead.

            Args:
                obj: Object to convert to string representation.
                prefix: String to prepend to each list line in block.

            Returns:
                Custom object representation.
            """
            if isinstance(obj, list) and len(obj) > 0:
                return f"\n{prefix} - " + f"\n{prefix} - ".join([str(i) for i in obj])
            return obj.strip("'") if hasattr(obj, "strip") else str(obj)

        class_name = self.__class__.__name__
        if class_name in exclude_class_list:
            base = ""
        else:
            base = class_name + "\n"

        if data:
            return base + "\n".join(get_data_lines(data, _custom_repr))
        else:
            return class_name + ": {}"

    def add_entries(self, entries) -> "AttMapLike":
        """Update this instance with provided key-value pairs.

        Args:
            entries: Collection of pairs of keys and values.

        Returns:
            This instance.
        """
        if entries is None:
            return
        if callable(entries):
            entries = entries()
        elif any("pandas.core" in str(t) for t in type(entries).__bases__):
            entries = entries.to_dict()
        try:
            entries_iter = entries.items()
        except AttributeError:
            entries_iter = entries
        for k, v in entries_iter:
            self[k] = (
                v
                if (
                    k not in self
                    or not isinstance(v, Mapping)
                    or not isinstance(self[k], Mapping)
                )
                else self[k].add_entries(v)
            )
        return self

    def get_yaml_lines(
        self,
        conversions: tuple = (
            (lambda obj: isinstance(obj, Mapping) and 0 == len(obj), None),
        ),
    ) -> list[str]:
        """Get collection of lines that define YAML text representation.

        Args:
            conversions: Collection of pairs in which first component is
                predicate function and second is what to replace a value
                with if it satisfies the predicate.

        Returns:
            YAML representation lines.
        """
        if 0 == len(self):
            return ["{}"]
        data = self._simplify_keyvalue(
            self._data_for_repr(), self._new_empty_basic_map, conversions=conversions
        )
        return self._render(data).split("\n")[1:]

    def is_null(self, item: object) -> bool:
        """Conjunction of presence in underlying mapping and value being None.

        Args:
            item: Key to check for presence and null value.

        Returns:
            True iff the item is present and has null value.
        """
        return item in self and self[item] is None

    def non_null(self, item: object) -> bool:
        """Conjunction of presence in underlying mapping and value not being None.

        Args:
            item: Key to check for presence and non-null value.

        Returns:
            True iff the item is present and has non-null value.
        """
        return item in self and self[item] is not None

    def to_map(self) -> dict:
        """Convert this instance to a dict.

        Returns:
            This map's data, in a simpler container.
        """
        return self._simplify_keyvalue(self.items(), self._new_empty_basic_map)

    def to_dict(self) -> dict:
        """Return a builtin dict representation of this instance.

        Returns:
            Builtin dict representation of this instance.
        """
        return self._simplify_keyvalue(self.items(), dict)

    def to_yaml(self, trailing_newline: bool = True) -> str:
        """Get text for YAML representation.

        Args:
            trailing_newline: Whether to add trailing newline.

        Returns:
            YAML text representation of this instance.
        """
        return "\n".join(self.get_yaml_lines()) + ("\n" if trailing_newline else "")

    def _data_for_repr(self):
        """Hook for extracting the data used in the object's text representation.

        Returns:
            Collection of key-value pairs to include in text representation.
        """
        return filter(
            lambda kv: not self._excl_from_repr(kv[0], self.__class__), self.items()
        )

    def _excl_from_eq(self, k) -> bool:
        """Hook for exclusion of particular value from comparison.

        Args:
            k: Key to consider for omission.

        Returns:
            Whether the given key should be omitted from comparison.
        """
        return False

    def _excl_from_repr(self, k, cls: type) -> bool:
        """Hook for exclusion of particular value from representation.

        Args:
            k: Key to consider for omission.
            cls: Data type on which to base the exclusion.

        Returns:
            Whether the given key should be omitted from text representation.
        """
        return False

    def _excl_classes_from_todict(self) -> tuple | None:
        """Hook for exclusion of particular class from a dict conversion."""
        return

    @property
    @abc.abstractmethod
    def _lower_type_bound(self):
        """Most specific type to which stored Mapping should be transformed."""
        pass

    @abc.abstractmethod
    def _new_empty_basic_map(self):
        """Return the empty collection builder for Mapping type simplification."""
        pass

    def _simplify_keyvalue(self, kvs, build, acc=None, conversions=None):
        """Simplify a collection of key-value pairs, reducing to simpler types.

        Args:
            kvs: Collection of key-value pairs.
            build: How to build an empty collection.
            acc: Accumulating collection of simplified data.
            conversions: Optional value conversion predicates.

        Returns:
            Collection of simplified data.
        """
        acc = acc or build()
        kvs = iter(kvs)
        try:
            k, v = next(kvs)
        except StopIteration:
            return acc
        if not isinstance(v, self._excl_classes_from_todict() or tuple()):
            if is_custom_map(v):
                v = self._simplify_keyvalue(v.items(), build, build())
            if isinstance(v, Mapping):
                for pred, proxy in conversions or []:
                    if pred(v):
                        v = proxy
                        break
            acc[k] = v
        return self._simplify_keyvalue(kvs, build, acc, conversions)
