""" Test basic Mapping operations' responsiveness to underlying data change. """

import random
import sys
from hypothesis import given
import pytest
from .helpers import get_att_map, random_str_key, rand_non_null

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
def entries(request):
    """ Data to store as entries in an attmap. """
    return request.param


def test_length_decrease(attmap_type, entries):
    """ Length/size of an attmap should match number of entries. """
    m = get_att_map(attmap_type, entries)
    assert len(entries) == len(m)
    ks = list(entries.keys())
    for i, k in enumerate(ks):
        del m[k]
        assert len(entries) - (i + 1) == len(m)


def test_length_increase(attmap_type, entries):
    """ Length/size of an attmap should match number of entries. """
    m = get_att_map(attmap_type)
    for (i, (k, v)) in enumerate(entries.items()):
        assert i == len(m)
        m[k] = v
        assert (i + 1) == len(m)


def test_positive_membership(attmap_type, entries):
    """ Each key is a member; a nonmember should be flagged as such """
    import random
    m = get_att_map(attmap_type)
    assert not any(k in m for k in entries)
    for k in entries:
        assert k not in m
        m[k] = random.random()
        assert k in m
    assert all(k in m for k in entries)


def test_negative_membership(attmap_type, entries):
    """ Object key status responds to underlying data change. """
    m = get_att_map(attmap_type, entries)
    for k in entries:
        assert k in m
        del m[k]
        assert k not in m


@pytest.mark.parametrize("f_extra_checks_pair",
    [(repr, []), (str, [lambda s, dt: s.startswith(dt.__name__)])])
def test_text(attmap_type, entries, f_extra_checks_pair):
    """ Formal text representation of an attmap responds to data change. """

    get_rep, extra_checks = f_extra_checks_pair
    m = get_att_map(attmap_type)

    added = {}
    for k, v in entries.items():
        m[k] = v
        added[k] = v
        text = get_rep(m)
        miss_keys, miss_vals = _missing_items(text, added)
        assert [] == miss_keys
        assert [] == miss_vals

    n = sys.maxsize
    for k in entries:
        del m[k]
        del added[k]
        text = get_rep(m)
        miss_keys, miss_vals = _missing_items(text, added)
        assert [] == miss_keys
        assert [] == miss_vals
        assert len(text) < n
        for check in extra_checks:
            check(text, attmap_type)
        n = len(text)


class CheckNullTests:
    """ Test accuracy of the null value test methods. """

    DATA = [(("truly_null", None), True)] + \
           [(kv, False) for kv in [
               ("empty_list", []), ("empty_text", ""), ("empty_int", 0),
               ("empty_float", 0), ("empty_map", {})
           ]]

    @pytest.fixture(scope="function")
    def entries(self):
        """ Provide some basic entries for a test case's attmap. """
        return dict([kv for kv, _ in self.DATA])

    @staticmethod
    @pytest.fixture("function", params=[k for ((k, _), _) in DATA])
    def k(request):
        return request.param

    @staticmethod
    @pytest.fixture("function")
    def m(attmap_type):
        return get_att_map(attmap_type)

    @staticmethod
    @given(v=rand_non_null())
    def test_null_to_non_null(m, v):
        k = random_str_key()
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)

    @staticmethod
    @given(v=rand_non_null())
    def test_non_null_to_null(m, v):
        k = random_str_key()
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)

    @staticmethod
    def test_null_to_absent(m):
        k = random_str_key()
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)
        del m[k]
        assert not m.is_null(k) and not m.non_null(k)

    @staticmethod
    @given(v=rand_non_null())
    def test_non_null_to_absent(m, v):
        k = random_str_key()
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)
        del m[k]
        assert not m.is_null(k) and not m.non_null(k)


def _missing_items(r, data):
    """
    Determine which keys and/or values are missing from Mapping representation.

    :param str r: representation of the mapping
    :param Mapping data: data expected to be represented in the provided text
    :return list[str], list[str]: list of keys and of values, respectively, for
        which are not represented in the given text
    """
    missing_keys = [k for k in data if repr(k) not in r]
    missing_values = [v for v in data.values() if repr(v) not in r]
    return missing_keys, missing_values
