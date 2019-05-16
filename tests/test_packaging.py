""" Validate what's available directly on the top-level import. """

from abc import ABCMeta
from collections import OrderedDict
from inspect import isclass, isfunction
import itertools
import pytest
import attmap
from attmap import *

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def get_base_check(*bases):
    """
    Build function to validate an type's base classes.

    :param bases: sequence of base types.
    :return function(type) -> bool: function that checks a type's base classes
        for equivalence with the sequence given here.
    """
    return lambda obj: obj.__bases__ == bases


ECHO_TEST_FUNS = [isclass, get_base_check(PathExAttMap)]


@pytest.mark.parametrize(["obj_name", "typecheck"], itertools.chain(*[
    [("AttMapLike", f) for f in [isclass, lambda obj: obj.__metaclass__ == ABCMeta]],
    [("AttMap", f) for f in [isclass, get_base_check(AttMapLike)]],
    [("OrdAttMap", f) for f in [isclass, get_base_check(OrderedDict, AttMap)]],
    [("PathExAttMap", f) for f in [isclass, get_base_check(OrdAttMap)]],
    [("AttMapEcho", f) for f in ECHO_TEST_FUNS],
    [("EchoAttMap", f) for f in ECHO_TEST_FUNS],
    [("get_data_lines", isfunction)]
]))
def test_top_level_exports(obj_name, typecheck):
    """ At package level, validate object availability and type. """
    mod = attmap
    try:
        obj = getattr(mod, obj_name)
    except AttributeError:
        pytest.fail("Unavailable on {}: {}".format(mod.__name__, obj_name))
    else:
        assert typecheck(obj)
