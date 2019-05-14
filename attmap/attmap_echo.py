""" AttMap that echoes an unset key/attr """

from .ordpathex_attmap import OrdPathExAttMap


class AttMapEcho(OrdPathExAttMap):
    """ An AttMap that returns key/attr if it has no set value. """

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
            return super(self.__class__, self).__getattr__(item, default)
        except (AttributeError, TypeError):
            # If not, triage and cope accordingly.
            if item.startswith("_OrderedDict") or \
                    (item.startswith("__") and item.endswith("__")):
                # Accommodate security-through-obscurity approach of some libs.
                error_reason = "Protected-looking attribute: {}".format(item)
                raise AttributeError(error_reason)
            return default if default is not None else item

    @property
    def _lower_type_bound(self):
        """ Most specific type to which an inserted value may be converted """
        return AttMapEcho
