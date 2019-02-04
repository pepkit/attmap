""" Helper functions for tests """

from attmap._att_map_like import AttMapLike

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def get_att_map(cls, data=None):
    """ Create a fresh, empty data object. """
    assert issubclass(cls, AttMapLike)
    m = cls.__new__(cls)
    m.__init__(data or {})
    return m


def raises_keyerr(k, m):
    """
    Determine whether a mapping is missing a particular key.

    This helper is useful for explicitly routing execution through __getitem__
    rather than using the __contains__ implementation.

    :param object k: the key to check for status as missing
    :param Mapping m: the key-value collection to query
    :return bool: whether the requested key is missing from the given mapping,
        with "missing" determined by KeyError encounter during __getitem__
    """
    try:
        m[k]
    except KeyError:
        return True
    else:
        return False
