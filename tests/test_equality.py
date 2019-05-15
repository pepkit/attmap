""" Tests for attmap equality comparison """

import copy
import numpy as np
from pandas import DataFrame as DF, Series
import pytest
from attmap import AttMap, OrdAttMap, PathExAttMap, AttMapEcho
from .conftest import ALL_ATTMAPS
from .helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(scope="function")
def basic_data():
    """ Provide a test case with a couple of key-value pairs to work with. """
    return {"a": 1, "b": 2}


@pytest.mark.parametrize("attmap_type", ALL_ATTMAPS)
@pytest.mark.parametrize(["s1_data", "s2_data"], [
    ({"c": 3}, {"d": 4}), ({}, {"c": 3}), ({"d": 4}, {})])
def test_series_labels_mismatch_is_not_equal(
        basic_data, s1_data, s2_data, attmap_type):
    """ Maps with differently-labeled Series as values cannot be equal. """
    d1 = copy.copy(basic_data)
    d1.update(s1_data)
    d2 = copy.copy(basic_data)
    d2.update(s2_data)
    assert list(d1.keys()) != list(d2.keys())
    key = "s"
    m1 = get_att_map(attmap_type, {key: Series(d1)})
    m2 = get_att_map(attmap_type, {key: Series(d2)})
    assert m1 != m2


@pytest.mark.parametrize("attmap_type", ALL_ATTMAPS)
@pytest.mark.parametrize(["obj1", "obj2", "expected"], [
    (np.array([1, 2, 3]), np.array([1, 2, 4]), False),
    (np.array(["a", "b", "c"]), np.array(["a", "b", "c"]), True),
    (Series({"x": 0, "y": 0}), Series({"x": 0, "y": 1}), False),
    (Series({"x": 0, "y": 0}), Series({"x": 0, "y": 0}), True),
    (DF({"a": [1, 0], "b": [0, 1]}), DF({"a": [0, 0], "b": [0, 0]}), False),
    (DF({"a": [1, 0], "b": [0, 1]}), DF({"a": [1, 0], "b": [0, 1]}), True)
])
def test_eq_with_scistack_value_types(attmap_type, obj1, obj2, expected):
    """ Map comparison properly handles array-likes from scientific stack. """
    key = "obj"
    m1 = get_att_map(attmap_type, {key: obj1})
    m2 = get_att_map(attmap_type, {key: obj2})
    print("m1: {}".format(m1))
    assert (m1 == m2) is expected


@pytest.mark.parametrize("data", [{}, {"a": 1}])
@pytest.mark.parametrize(["this_type", "that_type", "exp"], [
    (AttMap, AttMap, True),
    (AttMap, AttMapEcho, False), (AttMap, OrdAttMap, False), (AttMap, PathExAttMap, False),
    (OrdAttMap, OrdAttMap, True),
    (OrdAttMap, PathExAttMap, False), (OrdAttMap, AttMapEcho, False),
    (PathExAttMap, PathExAttMap, True), (PathExAttMap, AttMapEcho, False),
    (AttMapEcho, AttMapEcho, True)])
def test_equality_is_strict_in_type(data, this_type, that_type, exp):
    """ Attmap equality requires exact type match. """
    m1 = get_att_map(this_type, data)
    m2 = get_att_map(that_type, data)
    assert type(m1) == this_type
    assert type(m2) == that_type
    assert (m1 == m2) is exp
    assert (m2 == m1) is exp
    assert (m1 != m2) is not exp
    assert (m2 != m1) is not exp


@pytest.mark.parametrize("maptype", ALL_ATTMAPS)
@pytest.mark.parametrize(["data", "delkey"], [
    ({"a": 1}, "a"), ({"b": 2, "c": 3}, "b"), ({"b": 2, "c": 3}, "c")])
def test_equality_fails_when_keysets_are_non_identical(maptype, data, delkey):
    """ Map comparison fails--unexceptionally--when operands differ in keys. """
    m1 = get_att_map(maptype, data)
    m2 = get_att_map(maptype, data)
    assert m1 == m2
    assert m2 == m1
    del m1[delkey]
    assert m1 != m2
    assert m2 != m1
