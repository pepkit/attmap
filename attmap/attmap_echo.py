"""AttMap that echoes an unset key/attr."""

from .pathex_attmap import PathExAttMap

__all__ = ["AttMapEcho", "EchoAttMap"]


class EchoAttMap(PathExAttMap):
    """An AttMap that returns key/attr if it has no set value."""

    def __getattr__(
        self, item: str, default: object = None, expand: bool = True
    ) -> object:
        """Fetch the value associated with the provided identifier.

        Args:
            item: Identifier for value to fetch.
            default: Default return value.
            expand: Whether to attempt variable expansion of string
                value, in case it's a path.

        Returns:
            Whatever value corresponds to the requested key/item.

        Raises:
            AttributeError: If the requested item appears to be protected
                (flanking double underscores).
        """
        try:
            return super().__getattr__(item, default, expand)
        except (AttributeError, TypeError):
            if self._is_od_member(item) or (
                item.startswith("__") and item.endswith("__")
            ):
                error_reason = "Protected-looking attribute: {}".format(item)
                raise AttributeError(error_reason)
            return default if default is not None else item

    @property
    def _lower_type_bound(self):
        """Most specific type to which an inserted value may be converted."""
        return AttMapEcho


AttMapEcho = EchoAttMap
