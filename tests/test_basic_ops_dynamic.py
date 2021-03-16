""" Test basic Mapping operations' responsiveness to underlying data change. """

import pytest
from hypothesis import given
from pandas import Series

from .helpers import get_att_map, rand_non_null, random_str_key

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.fixture(scope="function", params=[{}, {"a": 1}, {"b": [1, 2, 3], "c": (1, 2)}])
def entries(request):
    """ Data to store as entries in an attmap. """
    return request.param


def test_length_decrease(attmap_type, entries):
    """ Length/size of an attmap should match number of entries. """
    m = get_att_map(attmap_type, entries)
    assert len(entries) == len(m)
    ks = list(entries.keys())
    for i, k in enumerate(ks):
        del m[k]
        assert len(entries) - (i + 1) == len(m)


def test_length_increase(attmap_type, entries):
    """ Length/size of an attmap should match number of entries. """
    m = get_att_map(attmap_type)
    for (i, (k, v)) in enumerate(entries.items()):
        assert i == len(m)
        m[k] = v
        assert (i + 1) == len(m)


def test_positive_membership(attmap_type, entries):
    """ Each key is a member; a nonmember should be flagged as such """
    import random

    m = get_att_map(attmap_type)
    assert not any(k in m for k in entries)
    for k in entries:
        assert k not in m
        m[k] = random.random()
        assert k in m
    assert all(k in m for k in entries)


def test_negative_membership(attmap_type, entries):
    """ Object key status responds to underlying data change. """
    m = get_att_map(attmap_type, entries)
    for k in entries:
        assert k in m
        del m[k]
        assert k not in m


@pytest.mark.parametrize(
    "series", [Series(data) for data in [("a", 1), [("b", 2), ("c", 3)], []]]
)
def test_add_pandas_series(series, attmap_type):
    """ A pandas Series can be used as a simple container of entries to add. """
    m = get_att_map(attmap_type)
    raw_data = series.to_dict()
    keys = set(raw_data.keys())
    assert keys - set(m.keys()) == keys
    m.add_entries(series)
    assert raw_data == {k: m[k] for k in raw_data}


@pytest.mark.parametrize("seed_data", [{}, {"a": 1}, {"b": 2, "c": 3}])
@pytest.mark.parametrize("delkey", ["d", "e"])
def test_del_unmapped_key(attmap_type, seed_data, delkey):
    """ Attempt to remove unmapped key should not fail. """
    m = get_att_map(attmap_type, entries=seed_data)
    assert delkey not in m
    try:
        del m[delkey]
    except KeyError as e:
        pytest.fail("Attempt to remove unmapped key hit exception: {}".format(e))


@pytest.mark.xfail(reason="attmap text representations have changed.")
@pytest.mark.parametrize(
    "f_extra_checks_pair",
    [(repr, []), (str, [lambda s, dt: s.startswith(dt.__name__)])],
)
def test_text(attmap_type, entries, f_extra_checks_pair):
    """ Formal text representation of an attmap responds to data change. """

    get_rep, extra_checks = f_extra_checks_pair
    m = get_att_map(attmap_type)

    added = {}
    for k, v in entries.items():
        m[k] = v
        added[k] = v

    text = get_rep(m)
    lines = text.split("\n")
    assert len(lines) == 1 + len(entries)
    assert lines[0].startswith(attmap_type.__name__)

    def _examine_results(ls, items):
        def find_line(key, val):
            matches = [l for l in ls if l.startswith(k) and "{}".format(v) in l]
            if len(matches) == 0:
                raise Exception(
                    "No matches for key={}, val={} among lines:\n{}".format(
                        key, val, "\n".join(lines)
                    )
                )
            elif len(matches) == 1:
                return matches[0]
            else:
                raise Exception(
                    "Non-unique ({}) matched lines:\n{}".format(
                        len(matches), "\n".join(matches)
                    )
                )

        matched, missed = [], []
        for k, v in items.items():
            try:
                matched.append(((k, v), find_line(k, v)))
            except Exception as e:
                missed.append(((k, v), str(e)))
        return matched, missed

    goods, bads = _examine_results(lines, added)
    if bads:
        pytest.fail("Errors/failures by key-value pair:\n{}".format(bads))
    for (k, v), l in goods:
        assert l.startswith("{}".format(k))
        assert "{}".format(v) in l

    for k in entries:
        del m[k]
        del added[k]
        text = get_rep(m)
        goods, bads = _examine_results(text.split("\n"), added)
        if bads:
            pytest.fail("Errors/failures by key-value pair:\n{}".format(bads))
        for kv, l in goods:
            assert l.startswith("{}".format(kv[0]))
            assert "{}".format(kv[1]) in l
        for check in extra_checks:
            check(text, attmap_type)


class CheckNullTests:
    """ Test accuracy of the null value test methods. """

    DATA = [(("truly_null", None), True)] + [
        (kv, False)
        for kv in [
            ("empty_list", []),
            ("empty_text", ""),
            ("empty_int", 0),
            ("empty_float", 0),
            ("empty_map", {}),
        ]
    ]

    @pytest.fixture(scope="function")
    def entries(self):
        """ Provide some basic entries for a test case's attmap. """
        return dict([kv for kv, _ in self.DATA])

    @staticmethod
    @pytest.fixture(scope="function")
    def m(attmap_type):
        """ Build an AttMap instance of the given subtype. """
        return get_att_map(attmap_type)

    @pytest.mark.skip(reason="test appears broken")
    @staticmethod
    @given(v=rand_non_null())
    def test_null_to_non_null(m, v):
        """ Non-null value can overwrite null. """
        k = random_str_key()
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)

    @pytest.mark.skip(reason="test appears broken")
    @staticmethod
    @given(v=rand_non_null())
    def test_non_null_to_null(m, v):
        """ Null value can overwrite non-null. """
        k = random_str_key()
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)

    @staticmethod
    def test_null_to_absent(m):
        """ Null value for previously absent key is inserted. """
        k = random_str_key()
        m[k] = None
        assert m.is_null(k) and not m.non_null(k)
        del m[k]
        assert not m.is_null(k) and not m.non_null(k)

    @pytest.mark.skip(reason="test appears broken")
    @staticmethod
    @given(v=rand_non_null())
    def test_non_null_to_absent(m, v):
        """ Non-null value for previously absent key is inserted. """
        k = random_str_key()
        m[k] = v
        assert not m.is_null(k) and m.non_null(k)
        del m[k]
        assert not m.is_null(k) and not m.non_null(k)
