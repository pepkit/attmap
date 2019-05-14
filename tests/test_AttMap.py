""" Tests for AttMap. """

import itertools
import os
import pickle

import numpy as np
import pytest
import yaml

from attmap import AttMap, AttMapEcho

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


# Provide some basic atomic-type data for models tests.
_BASE_KEYS = ("epigenomics", "H3K", "ac", "EWS", "FLI1")
_BASE_VALUES = \
    ("topic", "residue", "acetylation", "RNA binding protein", "FLI1")
_ENTRIES_PROVISION_MODES = ["gen", "dict", "zip", "list", "items"]
_SEASON_HIERARCHY = {
    "spring": {"February": 28, "March": 31, "April": 30, "May": 31},
    "summer": {"June": 30, "July": 31, "August": 31},
    "fall": {"September": 30, "October": 31, "November": 30},
    "winter": {"December": 31, "January": 31}
}

ADDITIONAL_NON_NESTED = {"West Complex": {"CPHG": 6}, "BIG": {"MR-4": 6}}
ADDITIONAL_NESTED = {"JPA": {"West Complex": {"CPHG": 6}},
                     "Lane": {"BIG": {"MR-4": 6}}}
ADDITIONAL_VALUES_BY_NESTING = {
    False: ADDITIONAL_NON_NESTED,
    True: ADDITIONAL_NESTED
}
COMPARISON_FUNCTIONS = ["__eq__", "__ne__", "__len__",
                        "keys", "values", "items"]


def pytest_generate_tests(metafunc):
    """ Centralize dynamic test case parameterization. """
    if "empty_collection" in metafunc.fixturenames:
        # Test case strives to validate expected behavior on empty container.
        collection_types = [tuple, list, set, dict]
        metafunc.parametrize(
                "empty_collection",
                argvalues=[ctype() for ctype in collection_types],
                ids=[ctype.__name__ for ctype in collection_types])


def basic_entries():
    """ AttMap data that lack nested structure. """
    for k, v in zip(_BASE_KEYS, _BASE_VALUES):
        yield k, v


def nested_entries():
    """ AttributeDict data with some nesting going on. """
    for k, v in _SEASON_HIERARCHY.items():
        yield k, v


@pytest.mark.parametrize("base", ["random", "irrelevant", "arbitrary"])
@pytest.mark.parametrize("protect", [False, True])
def test_echo_is_conditional(base, protect):
    """ Protected member isn't echoed. """
    m = AttMapEcho({})
    if protect:
        with pytest.raises(AttributeError):
            m.__getattr__("__{}__".format(base))
    else:
        assert base == m.__getattr__(base)


class AttributeConstructionDictTests:
    """Tests for the AttMap ADT.

    Note that the implementation of the equality comparison operator
    is tested indirectly via the mechanism of many of the assertion
    statements used throughout these test cases. Some test cases are
    parameterized by comparison function to test for equivalence, rather
    than via input data as is typically the case. This avoids some overhead,
    This is to ensure that the implemented `collections.MutableMapping`
    or `collections.abc.MutableMapping` methods are valid.
    """

    # Refer to tail of class definition for
    # data and fixtures specific to this class.

    def test_null_construction(self):
        """ Null entries value creates empty AttMap. """
        assert AttMap({}) == AttMap(None)

    def test_empty_construction(self, empty_collection):
        """ Empty entries container create empty AttMap. """
        m = AttMap(empty_collection)
        assert AttMap(None) == m
        assert m != dict()

    @pytest.mark.parametrize(
            argnames="entries_gen,entries_provision_type",
            argvalues=itertools.product([basic_entries, nested_entries],
                                        _ENTRIES_PROVISION_MODES),
            ids=["{entries}-{mode}".format(entries=gen.__name__, mode=mode)
                 for gen, mode in
                 itertools.product([basic_entries, nested_entries],
                                    _ENTRIES_PROVISION_MODES)]
    )
    def test_construction_modes_supported(
            self, entries_gen, entries_provision_type):
        """ Construction wants key-value pairs; wrapping doesn't matter. """
        entries_mapping = dict(entries_gen())
        if entries_provision_type == "dict":
            entries = entries_mapping
        elif entries_provision_type == "zip":
            keys, values = zip(*entries_gen())
            entries = zip(keys, values)
        elif entries_provision_type == "items":
            entries = entries_mapping.items()
        elif entries_provision_type == "list":
            entries = list(entries_gen())
        elif entries_provision_type == "gen":
            entries = entries_gen
        else:
            raise ValueError("Unexpected entries type: {}".
                             format(entries_provision_type))
        expected = AttMap(entries_mapping)
        observed = AttMap(entries)
        assert expected == observed

    @staticmethod
    def _validate_mapping_function_implementation(entries_gen, name_comp_func):
        data = dict(entries_gen())
        attrdict = AttMap(data)
        if __name__ == '__main__':
            if name_comp_func in ["__eq__", "__ne__"]:
                are_equal = getattr(attrdict, name_comp_func).__call__(data)
                assert are_equal if name_comp_func == "__eq__" \
                        else (not are_equal)
            else:
                raw_dict_comp_func = getattr(data, name_comp_func)
                attrdict_comp_func = getattr(attrdict, name_comp_func)
                expected = raw_dict_comp_func.__call__()
                observed = attrdict_comp_func.__call__()
                try:
                    # Most comparison methods are returning iterables.
                    assert set(expected) == set(observed)
                except TypeError:
                    # Could be int or other non-iterable that we're comparing.
                    assert expected == observed


class AttMapUpdateTests:
    """Validate behavior of post-construction addition of entries.

    Though entries may and often will be provided at instantiation time,
    AttMap is motivated to support inheritance by domain-specific
    data types for which use cases are likely to be unable to provide
    all relevant data at construction time. So let's verify that we get the
    expected behavior when entries are added after initial construction.

    """

    _TOTALLY_ARBITRARY_VALUES = [
        "abc", 123,
        (4, "text", ("nes", "ted")), list("-101")
    ]
    _GETTERS = ["__getattr__", "__getitem__"]
    _SETTERS = ["__setattr__", "__setitem__"]

    @pytest.mark.parametrize(
            argnames="setter_name,getter_name,is_novel",
            argvalues=itertools.product(_SETTERS, _GETTERS, (False, True)))
    def test_set_get_atomic(self, setter_name, getter_name, is_novel):
        """ For new and existing items, validate set/get behavior. """

        # Establish the AttMap for the test case.
        data = dict(basic_entries())
        ad = AttMap(basic_entries())

        # Establish a ground truth and select name/value(s) based on
        # whether or not the test case wants to test a new or existing item.
        if is_novel:
            item_name = "awesome_novel_attribute"
            assert item_name not in ad
            with pytest.raises(AttributeError):
                getattr(ad, item_name)
            item_values = self._TOTALLY_ARBITRARY_VALUES
        else:
            item_name = np.random.choice(a=list(data.keys()), size=1)[0]
            item_value = data[item_name]
            assert ad[item_name] == item_value
            assert getattr(ad, item_name) == item_value
            item_values = [item_value]

        # Determine which functions to use to make the set/get calls.
        setter = getattr(ad, setter_name)
        getter = getattr(ad, getter_name)

        # Validate set/get for each value.
        for value in item_values:
            setter(item_name, value)
            assert getter(item_name) == value


class AttMapCollisionTests:
    """ Tests for proper merging and type conversion of mappings. 
     AttMap converts a mapping being inserted as a value to an 
     AttMap. """

    @pytest.mark.parametrize(
            argnames="name_update_func",
            argvalues=["add_entries", "__setattr__", "__setitem__"])
    def test_squash_existing(self, name_update_func):
        """ When a value that's a mapping is assigned to existing key with 
        non-mapping value, the new value overwrites the old. """
        ad = AttMap({"MR": 4})
        assert 4 == ad.MR
        assert 4 == ad["MR"]
        new_value = [4, 5, 6]
        args = ("MR", new_value)
        setter = getattr(ad, name_update_func)
        if name_update_func == "add_entries":
            setter([args])
        else:
            setter(*args)
        assert new_value == ad.MR
        assert new_value == ad["MR"]


@pytest.mark.parametrize(
        argnames="name_update_func",
        argvalues=["add_entries", "__setattr__", "__setitem__"])
@pytest.mark.parametrize(
        argnames="name_fetch_func",
        argvalues=["__getattr__", "__getitem__"])
class AttMapNullTests:
    """ AttMap has configurable behavior regarding null values. """

    def test_new_null(self, name_update_func, name_fetch_func):
        """ When a key/item, isn't known, null is allowed. """
        ad = AttMap()
        setter = getattr(ad, name_update_func)
        args = ("new_key", None)
        self._do_update(name_update_func, setter, args)
        getter = getattr(ad, name_fetch_func)
        assert getter("new_key") is None

    def test_replace_null(self, name_update_func, name_fetch_func):
        """ Null can be replaced by non-null. """
        ad = AttMap({"lone_attr": None})
        assert getattr(ad, name_fetch_func)("lone_attr") is None
        setter = getattr(ad, name_update_func)
        non_null_value = AttMap({"was_null": "not_now"})
        self._do_update(name_update_func, setter,
                        ("lone_attr", non_null_value))
        assert non_null_value == getattr(ad, name_fetch_func)("lone_attr")

    @staticmethod
    def _do_update(name_setter_func, setter_bound_method, args):
        if name_setter_func == "add_entries":
            setter_bound_method([args])
        else:
            setter_bound_method(*args)


class AttMapItemAccessTests:
    """ Tests for access of items (key- or attribute- style). """

    @pytest.mark.parametrize(argnames="missing", argvalues=["att", ""])
    def test_missing_getattr(self, missing):
        attrd = AttMap()
        with pytest.raises(AttributeError):
            getattr(attrd, missing)

    @pytest.mark.parametrize(argnames="missing", argvalues=["", "b", "missing"])
    def test_missing_getitem(self, missing):
        attrd = AttMap()
        with pytest.raises(KeyError):
            attrd[missing]

    def test_numeric_key(self):
        """ Attribute request must be string. """
        ad = AttMap({1: 'a'})
        assert 'a' == ad[1]
        with pytest.raises(TypeError):
            getattr(ad, 1)


class AttMapSerializationTests:
    """ Tests for AttMap serialization. """

    DATA_PAIRS = [('a', 1), ('b', False), ('c', range(5)),
                  ('d', {'A': None, 'T': []}),
                  ('e', AttMap({'G': 1, 'C': [False, None]})),
                  ('f', [AttMap({"DNA": "deoxyribose", "RNA": "ribose"}),
                         AttMap({"DNA": "thymine", "RNA": "uracil"})])]

    @pytest.mark.parametrize(
            argnames="data",
            argvalues=itertools.combinations(DATA_PAIRS, 2),
            ids=lambda data: " data = {}".format(str(data)))
    @pytest.mark.parametrize(
            argnames="data_type", argvalues=[list, dict],
            ids=lambda data_type: " data_type = {}".format(data_type))
    def test_pickle_restoration(self, tmpdir, data, data_type):
        """ Pickled and restored AttMap objects are identical. """

        # Type the AttMap input data argument according to parameter.
        data = data_type(data)
        original_attrdict = AttMap(data)
        filename = "attrdict-test.pkl"

        # Allow either Path or raw string.
        try:
            dirpath = tmpdir.strpath
        except AttributeError:
            dirpath = tmpdir

        # Serialize AttMap and write to disk.
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'wb') as pkl:
            pickle.dump(original_attrdict, pkl)

        # Validate equivalence between original and restored versions.
        with open(filepath, 'rb') as pkl:
            restored_attrdict = AttMap(pickle.load(pkl))
        assert restored_attrdict == original_attrdict


class AttMapObjectSyntaxAccessTests:
    """ Test behavior of dot attribute access / identity setting. """

    DEFAULT_VALUE = "totally-arbitrary"
    NORMAL_ITEM_ARG_VALUES = \
            ["__getattr__", "__getitem__", "__dict__", "__repr__", "__str__"]
    PICKLE_ITEM_ARG_VALUES = ["__getstate__", "__setstate__"]
    ATTR_DICT_DATA = {"a": 0, "b": range(1, 3), "c": {"CO": 70, "WA": 5}}
    UNMAPPED = ["arb-att-1", "random-attribute-2"]

    @pytest.fixture(scope="function")
    def attrdict(self, request):
        """ Provide a test case with an AttMap. """
        d = self.ATTR_DICT_DATA
        return AttMapEcho(d) if request.getfixturevalue("return_identity") \
            else AttMap(d)

    @pytest.mark.parametrize(
            argnames="return_identity", argvalues=[False, True],
            ids=lambda ret_id: " identity setting={} ".format(ret_id))
    @pytest.mark.parametrize(
            argnames="attr_to_request",
            argvalues=NORMAL_ITEM_ARG_VALUES + PICKLE_ITEM_ARG_VALUES +
                      UNMAPPED + list(ATTR_DICT_DATA.keys()),
            ids=lambda attr: " requested={} ".format(attr))
    def test_attribute_access(
            self, return_identity, attr_to_request, attrdict):
        """ Access behavior depends on request and behavior toggle. """
        if attr_to_request == "__dict__":
            # The underlying mapping is still accessible.
            assert attrdict.__dict__ is getattr(attrdict, "__dict__")
        elif attr_to_request in self.NORMAL_ITEM_ARG_VALUES:
            # Request for common protected function returns the function.
            assert callable(getattr(attrdict, attr_to_request))
        elif attr_to_request in self.PICKLE_ITEM_ARG_VALUES:
            # We don't tinker with the pickle-relevant attributes.
            with pytest.raises(AttributeError):
                print("Should have failed, but got result: {}".
                      format(getattr(attrdict, attr_to_request)))
        elif attr_to_request in self.UNMAPPED:
            # Unmapped request behavior depends on parameterization.
            if return_identity:
                assert attr_to_request == getattr(attrdict, attr_to_request)
            else:
                with pytest.raises(AttributeError):
                    getattr(attrdict, attr_to_request)
        else:
            # A mapped attribute returns its known value.
            expected = self.ATTR_DICT_DATA[attr_to_request]
            if isinstance(expected, dict):
                expected = type(attrdict)(expected)
            observed = getattr(attrdict, attr_to_request)
            print("AD (below):\n{}".format(attrdict))
            assert expected == observed


class NullityTests:
    """ Tests of null/non-null values """

    _KEYNAMES = ["sample_name", "protocol", "arbitrary_attribute"]

    @pytest.mark.parametrize(argnames="item", argvalues=_KEYNAMES)
    def test_missing_is_neither_null_nor_non_null(self, item):
        """ Value of absent key is neither null nor non-null """
        ad = AttMap()
        assert not ad.is_null(item) and not ad.non_null(item)

    @pytest.mark.parametrize(argnames="item", argvalues=_KEYNAMES)
    def test_is_null(self, item):
        """ Null-valued key/item evaluates as such. """
        ad = AttMap()
        ad[item] = None
        assert ad.is_null(item) and not ad.non_null(item)

    @pytest.mark.parametrize(
        argnames=["k", "v"],
        argvalues=list(zip(_KEYNAMES, ["sampleA", "WGBS", "random"])))
    def test_non_null(self, k, v):
        """ AD is sensitive to value updates """
        ad = AttMap()
        assert not ad.is_null(k) and not ad.non_null(k)
        ad[k] = None
        assert ad.is_null(k) and not ad.non_null(k)
        ad[k] = v
        assert not ad.is_null(k) and ad.non_null(k)


@pytest.mark.usefixtures("write_project_files")
class SampleYamlTests:
    """ AttMap metadata only appear in YAML if non-default. """

    @staticmethod
    def _yaml_data(sample, filepath, section_to_change=None,
                   attr_to_change=None, newval=None):
        """
        Serialize a Sample, possibly tweaking it first, write, and parse.

        :param models.Sample sample: what to serialize and write
        :param str filepath: where to write the data
        :param str section_to_change: name of section
            in which to change attribute
        :param str attr_to_change: name of attribute to change
        :param object newval: value to set for targeted attribute
        :return (Iterable[str], dict): raw lines and parsed version (YAML)
        """
        if section_to_change:
            getattr(sample, section_to_change)[attr_to_change] = newval
        sample.to_yaml(filepath)
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return lines, data


@pytest.mark.parametrize(
    ["func", "exp"], [(repr, "AttMap: {}"), (str, "AttMap: {}")])
def test_text_repr_empty(func, exp):
    """ Empty AttMap is correctly represented as text. """
    assert exp == func(AttMap())
