""" Mixin traits to specify particular behavior of AttMapLike """

import abc

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["EchoMixin"]


class EchoMixin(object):
    """ If a requested key/attr is unset, echo it back as return value. """

    __metaclass__ = abc.ABCMeta

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
            return super(EchoMixin, self).__getattribute__(item)
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
            return item
