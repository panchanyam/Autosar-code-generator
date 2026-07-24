"""
Tests PDU parser.
"""

from autosar_codegen.parser.pdu import (
    PduParser,
)



def test_pdu_parser():

    parser = PduParser()

    assert parser is not None



def test_pdu_parse():

    parser = PduParser()

    result = parser.parse(None)


    assert result is not None