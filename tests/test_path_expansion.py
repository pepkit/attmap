""" Tests for path expansion behavior """

import itertools
import os
import random
import string
import pytest
from attmap import *
from ubiquerg import expandpath, TmpEnv

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


_ARB_VAR_NAMES = ["abc", "def"]
_ENV_VAR_NAMES = ["RANDOM_VARIABLE", "ARB_TEST_VAR"]
_RVS = _ARB_VAR_NAMES + _ENV_VAR_NAMES


@pytest.fixture(scope="function")
def pam():
    """ Provide a test case with a clean/fresh map. """
    return PathExAttMap()


def get_path_env_pair(perm):
    """
    Create path-like text and mapping of variable name substitutions.

    :param Sequence[str] perm: ordered array-like of path components
    :return (str, dict[str, str]): pair in which first component is the
        joined and env-var-adjusted ($ sign added) path, and the second is
        a mapping from env var name to value
    """
    def get_random_var():
        return "".join(random.choice(string.ascii_uppercase)
                       for _ in range(random.randint(3, 10)))
    parts, subs = [], {}
    for p in perm:
        if p.upper() == p:
            subs[p] = get_random_var()
            p = "$" + p
        parts.append(p)
    return os.path.join(*parts), subs


@pytest.mark.parametrize(["path", "env"],
    [get_path_env_pair(p) for p in itertools.chain(*[
        itertools.permutations(_RVS, k) for k in range(1, len(_RVS))])])
@pytest.mark.parametrize("fetch", [getattr, lambda m, k: m[k]])
def test_PathExAttMap_expands_available_variables(pam, path, env, fetch):
    """ Insertion of text encoding environment variables should expand. """
    k = random.choice(string.ascii_lowercase)
    with TmpEnv(**env):
        pam[k] = path
        assert expandpath(path) == fetch(pam, k)


def build_selective_substitution_space():
    """
    Create collection of test inputs and expected behaviors

    :return Iterable[(str, Iterable[str], Iterable[str], Mapping[str, str])]:
        collection of 4-tuples in which first component is path to store as
        value in map, second is collection of path parts expected to be
        unaltered, third is collection of path parts expected to be altered,
        and fourth is binding between temp env var and value expected to
        replace it
    """
    def part(vs):
        return set(_RVS) - vs, vs
    partitions = [part(set(c)) for c in itertools.chain(*[
        itertools.combinations(_ENV_VAR_NAMES, k)
        for k in range(1, len(_ENV_VAR_NAMES))])]
    get_sub = lambda: "".join(
        random.choice(string.ascii_lowercase) for _ in range(20))
    paths = [os.path.join(*perm) for perm in itertools.permutations(
        ["$" + v if v.upper() == v else v for v in _RVS], len(_RVS))]
    return [(path, pres, repl, {ev: get_sub() for ev in repl})
            for path in paths for pres, repl in partitions]


@pytest.mark.parametrize(
    ["path", "pres", "repl", "env"], build_selective_substitution_space())
@pytest.mark.parametrize("fetch", [getattr, lambda m, k: m[k]])
def test_PathExAttMap_substitution_is_selective(path, pres, repl, env, pam, fetch):
    """ Values that are environment variables are replaced; others aren't. """
    k = random.choice(string.ascii_lowercase)
    with TmpEnv(**env):
        pam[k] = path
        res = fetch(pam, k)
        print("Inserted path: {}".format(path))
        print("Retrieved path: {}".format(res))
        assert all(map(lambda s: s in res, pres))
        assert all(map(lambda s: s not in res, repl))


@pytest.mark.parametrize("path", itertools.chain(*[
    itertools.permutations(["$" + p for p in _ENV_VAR_NAMES] + _ARB_VAR_NAMES, k)
    for k in range(1, len(_ENV_VAR_NAMES) + len(_ARB_VAR_NAMES) + 1)]))
@pytest.mark.parametrize("fetch", [getattr, lambda m, k: m[k]])
@pytest.mark.parametrize("env",
    [{ev: "".join(string.ascii_lowercase for _ in range(20)) for ev in _RVS}])
def test_non_PathExAttMap_preserves_all_variables(path, fetch, env):
    """ Only a PathExAttMap eagerly attempts expansion of text as a path. """
    m = AttMap()
    k = random.choice(string.ascii_letters)
    with TmpEnv(**env):
        m[k] = path
        assert path == fetch(m, k)


@pytest.mark.parametrize(["path", "expected"], [
    ("http://localhost", "http://localhost"),
    ("http://lh/$HOME/page.html", "http://lh/{}/page.html".format(os.environ["HOME"]))])
@pytest.mark.parametrize("fetch", [lambda m, k: m[k], lambda m, k: getattr(m, k)])
def test_url_expansion(path, expected, fetch):
    key = "arbitrary"
    m = PathExAttMap({key: path})
    assert expected == fetch(m, key)
