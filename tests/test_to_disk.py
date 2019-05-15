""" Tests for YAML representation of instances. """

from collections import namedtuple
import json
import sys
if sys.version_info < (3, 3):
    from collections import MutableMapping
else:
    from collections.abc import MutableMapping
import yaml
from attmap import *
import pytest
from tests.conftest import ALL_ATTMAPS

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

ENTRIES = [("b", 2), ("a", [("d", 4), ("c", [("f", 6), ("g", 7)])])]
EXPLINES = ["b: 2", "a:", "  d: 4", "  c:", "    f: 6", "    g: 7"]
FmtLib = namedtuple("FmtLib", ["parse", "write"])
YAML_NAME = yaml.__name__
JSON_NAME = json.__name__
FORMATTER_LIBRARIES = {
    YAML_NAME: FmtLib(lambda f: yaml.load(f, yaml.SafeLoader),
                   lambda m, f: f.write(m.to_yaml())),
    JSON_NAME: FmtLib(lambda f: json.load(f),
                   lambda m, f: json.dump(m.to_map(), f))
}


def pytest_generate_tests(metafunc):
    """ Dynamic test case generation and parameterization for this module """
    if "maptype" in metafunc.fixturenames:
        metafunc.parametrize("maptype", ALL_ATTMAPS)


def check_lines(m, explines, obs_fun, parse, check):
    """
    Check a YAML expectation against observation.

    :param attmap.AttMap m: the map to convert to YAML
    :param Iterable[str] explines: collection of expected lines
    :param str obs_fun: name of attmap function to call to get observation
    :param function(Iterable[str]) -> object parse: postprocess observed result
    :param function(object, object) -> bool check: validation function
    """
    obs = parse(getattr(m, obs_fun)())
    print("FUNCNAME: {}".format(obs_fun))
    print("EXPLINES (below):\n{}".format(explines))
    print("OBS (below):\n{}".format(obs))
    assert check(explines, obs)


@pytest.mark.parametrize(
    ["funcname", "exp"], [("get_yaml_lines", ["{}"]), ("to_yaml", "{}")])
def test_empty(funcname, exp, maptype):
    """ Verify behavior for YAML of empty attmap. """
    assert exp == getattr(maptype({}), funcname)()


@pytest.mark.parametrize(
    ["get_obs", "parse_obs"],
    [("get_yaml_lines", lambda ls: ls), ("to_yaml", lambda ls: ls.split("\n"))])
def test_yaml(maptype, get_obs, parse_obs):
    """ Tests for attmap repr as YAML lines or full text chunk. """
    eq = lambda a, b: a == b
    seteq = lambda a, b: len(a) == len(b) and set(a) == set(b)
    checks = {OrdAttMap: eq, PathExAttMap: eq, AttMapEcho: eq, AttMap: seteq}
    m = make_data(ENTRIES, maptype)
    check_lines(m, EXPLINES, get_obs, parse_obs, check=checks[maptype])


@pytest.mark.parametrize("fmtlib", [YAML_NAME, JSON_NAME])
def test_disk_roundtrip(maptype, tmpdir, fmtlib):
    """ Verify ability to parse, write, and reconstitute attmap. """
    m = make_data(ENTRIES, maptype)
    fp = tmpdir.join("disked_attmap.out").strpath
    fmtspec = FORMATTER_LIBRARIES[fmtlib]
    parse, write = fmtspec.parse, fmtspec.write
    with open(fp, 'w') as f:
        write(m, f)
    with open(fp, 'r') as f:
        recons = parse(f)
    assert recons == m.to_dict()


@pytest.mark.skip("not implemented")
def test_disk_path_expansion():
    pass


def make_data(entries, datatype):
    """
    Create the base data used to populate an attmap.

    :param Iterable[(str, object)] entries: key-value pairs
    :param type datatype: the type of mapping to build
    :return MutableMapping: the newly built/populated mapping
    """
    assert issubclass(datatype, MutableMapping)

    def go(items, acc):
        try:
            (k, v), t = items[0], items[1:]
        except IndexError:
            return acc
        if type(v) is list and all(type(e) is tuple and len(e) == 2 for e in v):
            v = go(v, datatype())
        acc[k] = v
        return go(t, acc)

    res = go(entries, datatype())
    assert len(res) > 0, "Empty result"
    return res
