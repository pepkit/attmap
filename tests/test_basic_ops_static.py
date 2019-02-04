""" Tests absent the mutable operations, of basic Mapping operations """

import pytest
from .helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
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
    assert repr(entries) == repr(get_att_map(attmap_type, entries))


def test_str(attmap_type, entries):
    """ Check informal text representation of an attmap. """
    m = get_att_map(attmap_type, entries)
    text = str(m)
    assert text.startswith(m.__class__.__name__)
    m.add_entries(entries)
    exp_data_text = "{}: {}".format(attmap_type.__name__, str(entries))
    assert exp_data_text == text
