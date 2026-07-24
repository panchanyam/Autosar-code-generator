"""
Tests network parser.
"""

from autosar_codegen.parser.network import (
    NetworkParser,
)



def test_network_parser():

    parser = NetworkParser()

    assert parser is not None



def test_network_parse():

    parser = NetworkParser()


    result = parser.parse(None)


    assert result is not None