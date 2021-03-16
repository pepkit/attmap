""" Tests for subclassing EchoAttMap """

import pytest

from attmap import EchoAttMap

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


class _SubEcho(EchoAttMap):
    """ Dummy class to derive from EchoAttMap """

    def __init__(self, entries=None):
        super(_SubEcho, self).__init__(entries)


@pytest.mark.parametrize("entries", [None, {}])
def test_echo_subclass_smoke(entries):
    """ Superclass ctor invocation avoids infinite recursion. """
    try:
        _SubEcho(entries)
    except RuntimeError as e:
        pytest.fail(str(e))
