"""
Tests validator dispatcher.
"""

from autosar_codegen.validator.dispatcher import (
    ValidatorDispatcher,
)



def test_dispatcher_creation():

    dispatcher = ValidatorDispatcher()


    assert dispatcher is not None



def test_dispatcher_registry():

    dispatcher = ValidatorDispatcher()


    assert dispatcher.registry is not None