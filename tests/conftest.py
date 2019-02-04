
from attmap import *
import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ALL_ATTMAPS = [AttributeDict, AttributeDictEcho, AttMap, AttMapEcho]


@pytest.fixture(scope="function", params=ALL_ATTMAPS)
def attmap_type(request, entries):
    """ An AttMapLike subtype """
    return request.param
