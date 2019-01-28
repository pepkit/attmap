""" Test basic Mapping operations' responsiveness to underlying data change. """

import pytest
from helpers import make_mado

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
def entries(request):
    """ Data to store as entries in a mado. """
    return request.param


class BasicOpsStaticTests:
    """ Tests of basic Mapping behavior, without complication of dynamism """

    def test_length(self, mado_type, entries):
        """ Length/size of a mado should match number of entries. """
        m = make_mado(mado_type, entries)
        assert len(entries) == len(m)
        ks = list(entries.keys())
        for i, k in enumerate(ks):
            del m[k]
            assert len(entries) - (i + 1) == len(m)

    def test_positive_membership(self, mado_type, entries):
        """ Each key is a member; a nonmember should be flagged as such """
        import random
        m = make_mado(mado_type)
        assert not any(k in m for k in entries)
        for k in entries:
            assert k not in m
            m[k] = random.random()
            assert k in m
        assert all(k in m for k in entries)

    def test_negative_membership(self, mado_type, entries):
        """ Object key status responds to underlying data change. """
        m = make_mado(mado_type, entries)
        for k in entries:
            assert k in m
            del m[k]
            assert k not in m

    @pytest.mark.skip("Not implemented")
    def test_repr(self):
        """ Formal text representation of a mado responds to data change. """
        pass

    @pytest.mark.skip("Not implemented")
    def test_str(self):
        """ Informal text representation of a mado responds to data change. """
        pass
