""" Tests for conversion to base/builtin dict type """

import numpy as np
import pytest
from pandas import Series

from tests.helpers import get_att_map

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    "entries",
    [
        {},
        {"a": 1},
        {"b": {"c": 3}},
        {"A": [1, 2]},
        {"B": 1, "C": np.arange(3)},
        {"E": Series(["a", "b"])},
    ],
)
def test_to_dict_type(attmap_type, entries):
    """Validate to_dict result is a base dict and that contents match."""
    m = get_att_map(attmap_type, entries)
    assert type(m) is not dict
    d = m.to_dict()
    assert type(d) is dict
    assert d == entries
    assert entries == d
