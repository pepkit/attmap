""" Test basic Mapping operations' responsiveness to underlying data change. """

import copy
import sys
import pytest
from helpers import make_mado

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(
    scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": {1: 2}}])
    #scope="function", params=[{}, {"a": 1}, {"c": {1: 2}}])
def entries(request):
    """ Data to store as entries in a mado. """
    return request.param


class BasicOpsDynamicTests:
    """ Tests of basic Mapping behavior, without complication of dynamism """

    def test_length_decrease(self, mado_type, entries):
        """ Length/size of a mado should match number of entries. """
        m = make_mado(mado_type, entries)
        assert len(entries) == len(m)
        ks = list(entries.keys())
        for i, k in enumerate(ks):
            del m[k]
            assert len(entries) - (i + 1) == len(m)

    def test_length_increase(self, mado_type, entries):
        """ Length/size of a mado should match number of entries. """
        m = make_mado(mado_type)
        for (i, (k, v)) in enumerate(entries.items()):
            assert i == len(m)
            m[k] = v
            assert (i + 1) == len(m)

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

    def test_repr(self, mado_type, entries):
        """ Formal text representation of a mado responds to data change. """

        def missing_items(r, data):
            missing_keys = [k for k in data if repr(k) not in r]
            missing_values = [v for v in data.values() if repr(v) not in r]
            return missing_keys, missing_values

        m = make_mado(mado_type)

        added = {}
        for k, v in entries.items():
            m[k] = v
            added[k] = v
            r = repr(m)
            miss_keys, miss_vals = missing_items(r, added)
            assert [] == miss_keys
            assert [] == miss_vals

        n = sys.maxsize
        for k in entries:
            del m[k]
            del added[k]
            r = repr(m)
            miss_keys, miss_vals = missing_items(r, added)
            assert [] == miss_keys
            assert [] == miss_vals
            assert len(r) < n
            n = len(r)

    @pytest.mark.skip("Not implemented")
    def test_str(self):
        """ Informal text representation of a mado responds to data change. """
        pass
