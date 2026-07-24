"""
Tests generator dispatcher.
"""

from autosar_codegen.generator.dispatcher import (
    GeneratorDispatcher,
)



def test_dispatcher_creation():

    dispatcher = GeneratorDispatcher()


    assert dispatcher is not None



def test_dispatcher_registry():

    dispatcher = GeneratorDispatcher()


    assert dispatcher.registry is not None