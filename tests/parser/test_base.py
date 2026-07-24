"""
Tests parser base interface.
"""

from autosar_codegen.parser.base import (
    Parser,
)



class DummyParser(Parser):

    name = "dummy"


    def parse(
        self,
        context,
    ):

        return "parsed"



def test_parser_creation():

    parser = DummyParser()

    assert parser is not None



def test_parser_name():

    parser = DummyParser()

    assert parser.name == "dummy"



def test_parser_execution():

    parser = DummyParser()

    result = parser.parse(None)

    assert result == "parsed"