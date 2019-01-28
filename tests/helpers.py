""" Helper functions for tests """

from mado._mado_like import MadoLike

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def make_mado(cls, data=None):
    """ Create a fresh, empty data object. """
    assert issubclass(cls, MadoLike)
    m = cls.__new__(cls)
    m.__init__(data or {})
    return m
