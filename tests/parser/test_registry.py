"""
Tests parser registry.
"""

from autosar_codegen.parser.registry import (
    ParserRegistry,
)



class DummyParser:

    name = "dummy"



def test_register_parser():

    registry = ParserRegistry()


    parser = DummyParser()


    registry.register(
        parser
    )


    assert registry.get(
        "dummy"
    ) == parser



def test_registry_list():

    registry = ParserRegistry()


    registry.register(
        DummyParser()
    )


    assert len(
        registry.all()
    ) == 1



def test_unregister_parser():

    registry = ParserRegistry()


    registry.register(
        DummyParser()
    )


    registry.unregister(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None