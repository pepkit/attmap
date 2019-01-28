""" Tests of basic Mapping behavior, without complication of dynamism """

from mado import AttributeDict, AttributeDictEcho
import pytest
from helpers import make_mado

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ALL_MADOS = [AttributeDict, AttributeDictEcho]


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
def entries(request):
    """ Data to store as entries in a mado. """
    return request.param


@pytest.fixture(scope="function", params=["Z", 1, None])
def nonmember(request):
    """ Object that should not be present as key in a mapping. """
    return request.param


@pytest.fixture(scope="function", params=ALL_MADOS)
def mado_type(request, entries):
    """ A mado data type """
    return request.param


@pytest.mark.skip("Not implemented")
def test_length(mado_type, entries):
    """ Length/size of a mado should match number of entries. """
    assert len(entries) == len(make_mado(mado_type, entries))


@pytest.mark.skip("Not implemented")
def test_positive_membership(mado_type, entries):
    """ Each key is a member; a nonmember should be flagged as such """
    m = make_mado(mado_type, entries)
    assert [] == [k for k in entries if k not in m]


@pytest.mark.skip("Not implemented")
def test_negative_membership(mado_type, entries, nonmember):
    m = make_mado(mado_type, entries)
    assert nonmember not in m


@pytest.mark.skip("Not implemented")
def test_repr():
    pass


@pytest.mark.skip("Not implemented")
def test_str():
    pass

