""" Test the basic mapping conversion functionality of an attmap """

import copy
from functools import partial
import random
import sys
if sys.version_info < (3, 3):
    from collections import Mapping
else:
    from collections.abc import Mapping
import pytest
from attmap import AttMap
from tests.helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(scope="function")
def entries():
    """ Basic data for a test case """
    return copy.deepcopy(
        {"arb_key": "text", "randn": random.randint(0, 10),
         "nested": {"ntop": 0, "nmid": {"list": ["a", "b"]},
                    "lowest": {"x": {"a": -1, "b": 1}}},
         "collection": {1, 2, 3}})


@pytest.fixture(scope="function")
def exp_num_raw(entries):
    """ Expected number of entries """
    return _get_num_raw(entries)


@pytest.fixture(scope="function")
def am(attmap_type, entries):
    """ Prepopulated attribute mapping of a particular subtype """
    return get_att_map(attmap_type, entries)


def test_type_conversion_completeness(am, attmap_type, exp_num_raw):
    """ Each nested mapping should be converted. """
    assert type(am) is attmap_type
    num_subtypes = _tally_types(am, AttMap)
    assert exp_num_raw == num_subtypes
    res = am.to_map()
    print("Object under test: {}".format(res))
    assert 0 == _tally_types(res, attmap_type)
    assert exp_num_raw == _get_num_raw(res)


def test_correct_size(am, entries):
    """ The transformed mapping should have its original size. """
    assert len(am) == len(entries), \
        "{} entries in attmap and {} in raw data".format(len(am), len(entries))
    assert len(am) == len(am.to_map()), \
        "{} entries in attmap and {} in conversion".format(len(am), len(am.to_map()))


def test_correct_keys(am, entries):
    """ Keys should be unaltered by the mapping type upcasting. """
    def text_keys(m):
        return ", ".join(m.keys())
    def check(m, name):
        assert set(m.keys()) == set(entries.keys()), \
            "Mismatch between {} and raw keys.\nIn {}: {}\nIn raw data: {}".\
            format(name, name, text_keys(m), text_keys(entries))
    check(am, "attmap")
    check(am.to_map(), "converted")


def test_values_equivalence(am, entries):
    """ Raw values should be equivalent. """
    def check(v1, v2):
        return all([check(v1[k], v2[k]) for k in set(v1.keys()) | set(v2.keys())]) \
            if isinstance(v1, Mapping) else v1 == v2
    assert check(am.to_map(), entries)


def _tally_types(m, t):
    """
    Tally the number of values of a particular type stored in a mapping.

    :param Mapping m: mapping in which to tally value types.
    :param type t: the type to tally
    :return int: number of values of the indicated type of interest
    """
    if not isinstance(m, Mapping):
        raise TypeError("Object in which to tally value types isn't a mapping: "
                        "{}".format(type(m)))
    if not issubclass(t, Mapping):
        raise ValueError("Type to tally should be a mapping subtype; got {}".
                         format(type(t)))
    def go(kvs, acc):
        try:
            head, tail = kvs[0], kvs[1:]
        except IndexError:
            return acc
        k, v = head
        extra = 1 + go(list(v.items()), 0) if isinstance(v, t) else 0
        return go(tail, acc + extra)
    return go(list(m.items()), 1 if isinstance(m, t) else 0)


_get_num_raw = partial(_tally_types, t=dict)
