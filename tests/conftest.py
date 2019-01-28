
from mado import AttributeDict, AttributeDictEcho
import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


ALL_MADOS = [AttributeDict, AttributeDictEcho]


@pytest.fixture(scope="function", params=ALL_MADOS)
def mado_type(request, entries):
    """ A mado data type """
    return request.param
