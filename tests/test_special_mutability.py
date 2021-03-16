""" Tests for mutability of AttributeDict """

import pytest

from attmap import AttributeDict, AttributeDictEcho

from .helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


OLD_ATTMAPS = [AttributeDict, AttributeDictEcho]
NULLABLE_ATTMAPS = OLD_ATTMAPS


@pytest.fixture(scope="function", params=["arbitrary", "random"])
def arb_key(request):
    """ Provide arbitrary key name for a test case. """
    return request.param


class UniversalMutabilityTests:
    """ Tests of attmap behavior with respect to mutability """

    @staticmethod
    @pytest.fixture(scope="function", params=OLD_ATTMAPS)
    def m(request):
        """ Provide a test case with a fresh empty data object. """
        return get_att_map(request.param)

    def test_null_can_always_be_set_if_key_is_absent(self, arb_key, m):
        """ When AttributeDict lacks a key, a null value can be set """
        assert arb_key not in m
        m[arb_key] = None
        assert arb_key in m
        assert m[arb_key] is None

    def test_empty_mapping_can_replace_nonempty(self, m, arb_key):
        """ Regardless of specific type, an empty map can replace nonempty. """
        assert arb_key not in m
        m[arb_key] = {}
        assert arb_key in m

    def test_inserted_mapping_adopts_container_type(self, m, arb_key):
        """ When mapping is inserted as value, it adopts its container's type. """
        assert arb_key not in m
        m[arb_key] = {}
        assert isinstance(m[arb_key], m.__class__)


class NullStorageTests:
    """ Tests for behavior of a attmap w.r.t. storing null value """

    @pytest.fixture(scope="function", params=NULLABLE_ATTMAPS)
    def m(self, request):
        """ Provide a test case with a fresh empty data object. """
        return get_att_map(request.param)

    def test_null_overwrites_existing(self, arb_key, m):
        """ Verify that a null value can replace a non-null one. """
        assert arb_key not in m
        arb_val = "placeholder"
        m[arb_key] = arb_val
        assert arb_val == m[arb_key]
        m[arb_key] = None
        assert arb_key in m
        assert m[arb_key] is None
