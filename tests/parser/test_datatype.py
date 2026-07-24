"""
Tests datatype parser.
"""

from autosar_codegen.parser.datatype import (
    DatatypeParser,
)



def test_datatype_parser():

    parser = DatatypeParser()

    assert parser is not None



def test_parse_datatype():

    parser = DatatypeParser()


    result = parser.parse(None)


    assert result is not None