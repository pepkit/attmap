""" Tests absent the mutable operations, of basic Mapping operations """

import pytest
from helpers import make_mado

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
def entries(request):
    """ Data to store as entries in a mado. """
    return request.param


@pytest.fixture(scope="function", params=["Z", 1, None])
def nonmember(request):
    """ Object that should not be present as key in a mapping. """
    return request.param


def test_length(mado_type, entries):
    """ Length/size of a mado should match number of entries. """
    assert len(entries) == len(make_mado(mado_type, entries))


def test_positive_membership(mado_type, entries):
    """ Each key is a member; a nonmember should be flagged as such """
    m = make_mado(mado_type, entries)
    assert [] == [k for k in entries if k not in m]


def test_negative_membership(mado_type, entries, nonmember):
    m = make_mado(mado_type, entries)
    assert nonmember not in m


def test_repr(mado_type, entries):
    assert repr(entries) == repr(make_mado(mado_type, entries))


def test_str(mado_type, entries):
    m = make_mado(mado_type, entries)
    text = str(m)
    assert text.startswith(m.__class__.__name__)
    m.add_entries(entries)
    exp_data_text = "{}: {}".format(mado_type.__name__, str(entries))
    assert exp_data_text == text
