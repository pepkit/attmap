""" Tests absent the mutable operations, of basic Mapping operations """

import pytest

from .helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ENTRY_DATA = [
    (),
    ("a", 1),
    ("b", [1, "2", 3]),
    ("c", {1: 2}),
    ("d", {"e": 0, "F": "G"}),
]


@pytest.fixture(
    scope="function",
    params=[{}, {"a": 1}, {"b": [1, "2", 3]}, {"c": {1: 2}}, {"d": {"F": "G"}}],
)
def entries(request):
    """ Data to store as entries in an attmap. """
    return request.param


@pytest.fixture(scope="function", params=["Z", 1, None])
def nonmember(request):
    """ Object that should not be present as key in a mapping. """
    return request.param


def test_length(attmap_type, entries):
    """ Length/size of an attmap should match number of entries. """
    assert len(entries) == len(get_att_map(attmap_type, entries))


def test_positive_membership(attmap_type, entries):
    """ Each key is a member; a nonmember should be flagged as such """
    m = get_att_map(attmap_type, entries)
    assert [] == [k for k in entries if k not in m]


def test_negative_membership(attmap_type, entries, nonmember):
    """ Check correctness of membership test for nonmember key. """
    m = get_att_map(attmap_type, entries)
    assert nonmember not in m


def test_repr(attmap_type, entries):
    """ Check raw text representation of an attmap. """
    obs = repr(get_att_map(attmap_type, entries))
    assert obs.startswith(attmap_type.__name__)


def test_str(attmap_type, entries):
    """ Check informal text representation of an attmap. """
    m = get_att_map(attmap_type, entries)
    assert repr(m) == str(m)


class CheckNullTests:
    """ Test accuracy of the null value test methods. """

    DATA = [(("truly_null", None), True)] + [
        (kv, False)
        for kv in [
            ("empty_list", []),
            ("empty_text", ""),
            ("empty_map", {}),
            ("empty_int", 0),
            ("empty_float", 0),
            ("bad_num", float("nan")),
            ("pos_inf", float("inf")),
            ("neg_inf", float("-inf")),
        ]
    ]

    @pytest.fixture(scope="function")
    def entries(self):
        """ Provide some basic entries for a test case's attmap. """
        return dict([kv for kv, _ in self.DATA])

    @staticmethod
    @pytest.fixture(scope="function", params=[k for ((k, _), _) in DATA])
    def k(request):
        """ Key to test """
        return request.param

    @staticmethod
    def test_present_is_null(attmap_type, entries, k):
        """ Null check on key's value works as expected. """
        m = get_att_map(attmap_type, entries)
        assert (entries[k] is None) == m.is_null(k)

    @staticmethod
    def test_present_non_null(attmap_type, entries, k):
        """ Non-null check on key's value works as expected. """
        m = get_att_map(attmap_type, entries)
        assert (entries[k] is not None) == m.non_null(k)

    @staticmethod
    @pytest.mark.parametrize("abs_key", ["missing", "absent"])
    def test_absent_is_neither_null_nor_non_null(attmap_type, entries, abs_key):
        m = get_att_map(attmap_type, entries)
        assert abs_key not in m
        assert not m.is_null(abs_key) and not m.non_null(abs_key)
