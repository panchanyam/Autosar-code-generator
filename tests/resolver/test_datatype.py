"""
Tests datatype resolver.
"""

from autosar_codegen.resolver.datatype import (
    DatatypeResolver,
)



def test_datatype_resolver():

    resolver = DatatypeResolver()

    assert resolver is not None



def test_datatype_resolution():

    resolver = DatatypeResolver()


    result = resolver.resolve(None)


    assert result is not None