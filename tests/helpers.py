""" Helper functions for tests """

import random
import string

from hypothesis.strategies import *

from attmap._att_map_like import AttMapLike

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


# hypothesis strategies that generate a single value
# Note the arrangement by relative (increasing) complexity, as advised by the
# hypothesis docs: https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.one_of
ATOMIC_STRATEGIES = [
    booleans,
    binary,
    floats,
    integers,
    text,
    characters,
    uuids,
    emails,
    timedeltas,
    times,
    dates,
    datetimes,
    complex_numbers,
]


def get_att_map(cls, entries=None):
    """ Create a fresh, empty data object. """
    assert issubclass(cls, AttMapLike)
    return cls(entries or {})


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


def rand_non_null():
    """
    Generate a random non-null value

    :return object: randomized non-null value
    """
    return one_of(*[g() for g in ATOMIC_STRATEGIES])


def random_str_key():
    """
    Generate random (string) key.

    :return str: Randomized string key
    """
    return random.choice(string.ascii_letters)
