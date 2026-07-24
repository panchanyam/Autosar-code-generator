"""
Tests parser dispatcher.
"""

from autosar_codegen.parser.dispatcher import (
    ParserDispatcher,
)



def test_dispatcher_creation():

    dispatcher = ParserDispatcher()

    assert dispatcher is not None



def test_dispatcher_registry():

    dispatcher = ParserDispatcher()


    assert dispatcher.registry is not None