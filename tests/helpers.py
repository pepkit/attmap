""" Helper functions for tests """

from mado._mado_like import MadoLike

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def make_mado(cls, data=None):
    """ Create a fresh, empty data object. """
    assert issubclass(cls, MadoLike)
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
