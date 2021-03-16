""" Fixtures and values shared among project's various test suites """

import pytest

from attmap import *

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ALL_ATTMAPS = [
    AttributeDict,
    AttributeDictEcho,
    AttMap,
    AttMapEcho,
    EchoAttMap,
    OrdAttMap,
    PathExAttMap,
]


@pytest.fixture(scope="function", params=ALL_ATTMAPS)
def attmap_type(request, entries):
    """ An AttMapLike subtype """
    return request.param
