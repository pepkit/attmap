""" Tests for mutability of AttributeDict """

from mado import AttributeDict, AttributeDictEcho
import pytest
from helpers import make_mado

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ALL_MADOS = [AttributeDict, AttributeDictEcho]
NULLABLE_MADOS = ALL_MADOS


@pytest.fixture(scope="function", params=["arbitrary", "random"])
def arb_key(request):
    """ Provide arbitrary key name for a test case. """
    return request.param


class UniversalMadoOptsTests:
    """ Tests for constant operations. """

    @pytest.fixture(scope="function")
    def entries(self):
        """ Provide raw key-value pairs as entries for an object. """
        return {"nnvk": "non-null",
                "number": 4,
                "nested": {"list": ["a", "b"], "sublevel": "arbitary"}}

    @staticmethod
    @pytest.fixture(scope="function", params=ALL_MADOS)
    def m(request):
        """ Return an empty, particular mado instance """
        make_mado(request.param)

    @pytest.mark.skip("Not implemented")
    def test_len(self, m, entries):
        """ Validate length operation's accuracy. """
        assert 0 == len(m)
        m.add_entries(entries)
        assert len(entries) == len(m)
    
    @pytest.mark.skip("Not implemented")
    def test_repr(self, m, entries):
        """ Validate raw text representation's accuracy. """
        pass
    
    @pytest.mark.skip("Not implemented")
    def test_str(self, m, entries):
        """ Validate refined text representation's accuracy. """
        text = str(m)
        assert text.startswith(m.__class__.__name__)
        m.add_entries(entries)
        exp_data_text = "{}: {}".format(
            self.__class__.__name__, str(entries))
        assert exp_data_text == str(m)


class UniversalMutabilityTests:
    """ Tests of mado behavior with respect to mutability """

    @staticmethod
    @pytest.fixture(scope="function", params=ALL_MADOS)
    def m(request):
        """ Provide a test case with a fresh empty data object. """
        return make_mado(request.param)

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
    """ Tests for behavior of a mado w.r.t. storing null value """

    @pytest.fixture(scope="function", params=NULLABLE_MADOS)
    def m(self, request):
        """ Provide a test case with a fresh empty data object. """
        return make_mado(request.param)

    def test_null_overwrites_existing(self, arb_key, m):
        """ Verify that a null value can replace a non-null one. """
        assert arb_key not in m
        arb_val = "placeholder"
        m[arb_key] = arb_val
        assert arb_val == m[arb_key]
        m[arb_key] = None
        assert arb_key in m
        assert m[arb_key] is None


class MembershipTests:
    """ Tests of determining whether a key is present in a data object. """

    @pytest.mark.skip("Not implemented")
    def test_echoer_key_absent(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_echoer_key_present(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_membership(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_membership_test_dynamism(self):
        pass


class EchoerTests:
    """ Tests of behavior of the echo-style  """
    pass


def is_missing(k, m):
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
