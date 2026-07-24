"""
Tests PDU resolver.
"""

from autosar_codegen.resolver.pdu import (
    PduResolver,
)



def test_pdu_resolver():

    resolver = PduResolver()

    assert resolver is not None



def test_pdu_resolution():

    resolver = PduResolver()


    result = resolver.resolve(None)


    assert result is not None