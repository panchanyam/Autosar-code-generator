"""
Tests network resolver.
"""

from autosar_codegen.resolver.network import (
    NetworkResolver,
)



def test_network_resolver():

    resolver = NetworkResolver()

    assert resolver is not None



def test_network_resolution():

    resolver = NetworkResolver()


    result = resolver.resolve(None)


    assert result is not None