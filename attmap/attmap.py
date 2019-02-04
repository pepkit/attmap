""" Dot notation support for Mappings. """

import sys
if sys.version_info < (3, 3):
    from collections import Mapping
else:
    from collections.abc import Mapping

from .helpers import copy
from ._att_map_like import AttMapLike


@copy
class AttMap(AttMapLike):
    """
    A class to convert a nested mapping(s) into an object(s) with key-values
    using object syntax (attmap.attribute) instead of getitem syntax
    (attmap["key"]). This class recursively sets mappings to objects,
    facilitating attribute traversal (e.g., attmap.attr.attr).
    """

    def __getattr__(self, item, default=None):
        """
        Fetch the value associated with the provided identifier.

        :param int | str item: identifier for value to fetch
        :return object: whatever value corresponds to the requested key/item
        :raises AttributeError: if the requested item has not been set,
            no default value is provided, and this instance is not configured
            to return the requested key/item itself when it's missing; also,
            if the requested item is unmapped and appears to be protected,
            i.e. by flanking double underscores, then raise AttributeError
            anyway. More specifically, respect attribute naming that appears
            to be indicative of the intent of protection.
        """
        try:
            return super(AttMap, self).__getattribute__(item)
        except (AttributeError, TypeError):
            # Handle potential failure from non-string or property request.
            pass
        try:
            # Route this dot notation request through the Mapping route.
            return self.__dict__[item]
        except KeyError:
            # If not, triage and cope accordingly.
            if item.startswith("__") and item.endswith("__"):
                # Accommodate security-through-obscurity approach used by some libraries.
                error_reason = "Protected-looking attribute: {}".format(item)
                raise AttributeError(error_reason)
            if default is not None:
                # For compatibility with ordinary getattr() call, allow default value.
                return default
            # Throw up our hands in despair and resort to exception behavior.
            raise AttributeError(item)

    def __setitem__(self, key, value):
        """
        This is the key to making this a unique data type. Flag set at
        time of construction determines whether it's possible for a null
        value to squash a non-null value. The combination of that flag and
        one indicating whether request for value for unset attribute should
        return the attribute name itself determines if any attribute/key
        may be set to a null value.

        :param str key: name of the key/attribute for which to establish value
        :param object value: value to which set the given key; if the value is
            a mapping-like object, other keys' values may be combined.
        """
        # TODO: consider enforcement of type constraint, that value of different
        # type may not overwrite existing.
        if isinstance(value, Mapping) and not isinstance(value, self.__class__):
            cls = self.__class__
            val = cls.__new__(cls)
            val.__init__(value)
            self.__dict__[key] = val
        else:
            self.__dict__[key] = value

    def __getitem__(self, item):
        try:
            # Ability to return requested item name itself is delegated.
            return self.__getattr__(item)
        except AttributeError:
            # Requested item is unknown, but request was made via
            # __getitem__ syntax, not attribute-access syntax.
            raise KeyError(item)

    def __repr__(self):
        return repr({k: v for k, v in self.__dict__.items()
                    if self._include_in_repr(k, klazz=self.__class__)})

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, repr(self))

    @staticmethod
    def _include_in_repr(attr, klazz):
        """
        Determine whether to include attribute in an object's text representation.

        :param str attr: attribute to include/exclude from object's representation
        :param str | type klazz: name of type or type itself of which the object
            to be represented is an instance
        :return bool: whether to include attribute in an object's
            text representation
        """
        # TODO: localize to peppy and subclass AttMap there for Project.
        exclusions_by_class = {
            "Project": ["_samples", "sample_subannotation",
                        "sheet", "interfaces_by_protocol"],
            "Subsample": ["sheet", "sample", "merged_cols"],
            "Sample": ["sheet", "prj", "merged_cols"]
        }
        classname = klazz.__name__ if isinstance(klazz, type) else klazz
        return attr not in exclusions_by_class.get(classname, [])
