""" Tests for ordered AttMap behavior """

from collections import OrderedDict
from itertools import combinations
import pytest
from hypothesis import given
from hypothesis.strategies import *
from attmap import AttMap, AttMapEcho, OrdAttMap, OrdPathExAttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def pytest_generate_tests(metafunc):
    """ Test case generation and parameterization for this module """
    hwy_dat = [("Big Sur", 1), ("Jasper", 93), ("Sneffels", 62),
               ("Robson", 16), ("Garibaldi", 99)]
    keyhook, dathook = "hwy_dat_key", "raw_hwy_dat"
    if dathook in metafunc.fixturenames:
        metafunc.parametrize(dathook, [hwy_dat])
    if keyhook in metafunc.fixturenames:
        metafunc.parametrize(keyhook, [k for k, _ in hwy_dat])


def kv_lists_strategy(pool=(integers, text, characters, uuids), **kwargs):
    """
    Randomly select a strategy to generate list of pairs of keys and values.

    :return callable: hypothesis strategy with which to generate list of
        key-value pairs
    """
    kwds = {"min_size": 1, "unique_by": lambda kv: kv[0]}
    kwds.update(kwargs)
    return one_of(*[lists(tuples(ks(), vs()), **kwds)
                    for ks, vs in combinations(pool, 2)])


@pytest.mark.parametrize(["cls", "exp"], [
    (OrdAttMap, True), (OrderedDict, True), (AttMap, True),
    (OrdPathExAttMap, False), (AttMapEcho, False)])
def test_subclassing(cls, exp):
    """ Verify that OrdAttMap type has expected type memberships. """
    assert exp is issubclass(OrdAttMap, cls)


@pytest.mark.parametrize(["cls", "exp"], [
    (OrdAttMap, True), (OrderedDict, True), (AttMap, True),
    (OrdPathExAttMap, False), (AttMapEcho, False)])
def test_type_membership(cls, exp):
    """ Verify that an OrdAttMap instance passes type checks as expected. """
    assert exp is isinstance(OrdAttMap(), cls)


@given(kvs=kv_lists_strategy())
def test_ordattmap_insertion_order(kvs):
    """ Verify order preservation. """
    assert kvs == list(OrdAttMap(kvs).items())


@given(kvs=kv_lists_strategy())
def test_ordattmap_size(kvs):
    """ Verify size determination. """
    exp = len(kvs)
    assert exp > 0
    assert exp == len(OrdAttMap(kvs))


@given(kvs=kv_lists_strategy())
def test_ordattmap_contains(kvs):
    """ Verify key containment check. """
    m = OrdAttMap(kvs)
    missing = [k for k, _ in kvs if k not in m]
    if missing:
        pytest.fail("{} missing keys: {}".format(len(missing), missing))


@given(kvs=kv_lists_strategy(pool=(text, characters)))
@pytest.mark.parametrize("access", [lambda m, k: m[k], getattr])
def test_ordattmap_access(kvs, access):
    """ Verify dual value access modes. """
    m = OrdAttMap(kvs)
    bads = []
    for k, exp in kvs:
        obs = access(m, k)
        if exp != obs:
            bads.append((k, exp, obs))
    if bads:
        pytest.fail("{} mismatches: {}".format(len(bads), bads))


@given(kvs=kv_lists_strategy())
@pytest.mark.parametrize("other_type", [dict, OrderedDict])
def test_ordattmap_eq(kvs, other_type):
    """ Verify equality comparison behavior. """
    assert OrdAttMap(kvs) == other_type(kvs)


@pytest.mark.parametrize(["alter", "check"], [
    (lambda m, k: m.__delitem__(k), lambda _1, _2: True),
    (lambda m, k: m.pop(k), lambda x, o: x == o)])
def test_ordattmap_deletion(hwy_dat_key, raw_hwy_dat, alter, check):
    """ Validate key deletion behavior of OrdAttMap. """
    m = OrdAttMap(raw_hwy_dat)
    assert hwy_dat_key in m
    obs = alter(m, hwy_dat_key)
    assert hwy_dat_key not in m
    assert list(m.items()) == [(k, v) for k, v in raw_hwy_dat if k != hwy_dat_key]
    orig = [v for k, v in raw_hwy_dat if k == hwy_dat_key][0]
    assert check(orig, obs), "Expected {} but found {}".format(orig, obs)


@pytest.mark.parametrize("this_type", [OrdAttMap, OrdPathExAttMap])
@pytest.mark.parametrize("that_type", [dict, OrderedDict, OrdAttMap])
def test_ordattmap_overrides_eq_exclusion(
        hwy_dat_key, raw_hwy_dat, this_type, that_type):
    """ Verify ability to exclude key from comparisons. """
    class OrdSub(this_type):
        def _excl_from_eq(self, k):
            return super(OrdSub, self)._excl_from_eq(k) or k == hwy_dat_key
    msub = OrdSub(raw_hwy_dat)
    assert isinstance(msub, OrdAttMap)
    that = that_type(raw_hwy_dat)
    assert msub == that
    msub[hwy_dat_key] = None
    assert list(msub.items()) != list(that.items())
    assert msub == that


@pytest.mark.parametrize("that_type", [dict, OrderedDict, OrdAttMap])
def test_ordattmap_overrides_repr_exclusion(hwy_dat_key, raw_hwy_dat, that_type):
    """ Verify ability to exclude key from __repr__. """
    class OrdSub(OrdAttMap):
        def _excl_from_repr(self, k, cls):
            return super(OrdSub, self)._excl_from_repr(k, cls) or k == hwy_dat_key
    msub = OrdSub(raw_hwy_dat)
    assert isinstance(msub, OrdAttMap)
    that = that_type(raw_hwy_dat)
    assert msub == that
    assert hwy_dat_key in repr(that)
    assert hwy_dat_key not in repr(msub)


@pytest.mark.parametrize(["that_type", "exp"], [
    (OrdAttMap, True), (AttMapEcho, False), (AttMap, False),
    (OrdPathExAttMap, False), (OrderedDict, False), (dict, False)])
def test_ordattmap_repr(raw_hwy_dat, that_type, exp):
    """ Test __repr__ of OrdAttMap. """
    assert exp is (repr(OrdAttMap(raw_hwy_dat)) == repr(that_type(raw_hwy_dat)))


class BasicDataTests:
    """ Tests for some OrdAttMap behaviors on some very basic data. """

    BASIC_DATA = [("a", OrderedDict([("c", 3), ("b", 2)])), ("d", 4),
                  ("e", OrderedDict([("f", 6)]))]
    
    @pytest.fixture(params=[OrdAttMap, OrdPathExAttMap])
    def oam(self, request):
        return request.param(self.BASIC_DATA)
    
    @pytest.mark.parametrize(["get_value", "expected"], [
        (lambda m: type(m), OrderedDict),
        (lambda m: m["a"], OrderedDict([("c", 3), ("b", 2)])),
        (lambda m: m["d"], 4),
        (lambda m: m["e"], OrderedDict([("f", 6)]))
    ])
    def test_ordattmap_simplification_to_map(self, oam, get_value, expected):
        assert expected == get_value(oam.to_map())

    @pytest.mark.skip("not implemented")
    def test_ordattmap_repr(self, oam):
        pass
