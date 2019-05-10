""" Validate what's available directly on the top-level import. """

from inspect import isclass, isfunction
import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    ["obj_name", "typecheck"],
    [("AttMap", isclass), ("OrdAttMap", isclass), ("OrdPathExAttMap", isclass),
     ("AttMapEcho", isclass), ("is_custom_map", isfunction),
     ("get_data_lines", isfunction)])
def test_top_level_exports(obj_name, typecheck):
    """ At package level, validate object availability and type. """
    import attmap
    mod = attmap
    try:
        obj = getattr(mod, obj_name)
    except AttributeError:
        pytest.fail("Unavailable on {}: {}".format(mod.__name__, obj_name))
    else:
        assert typecheck(obj)
