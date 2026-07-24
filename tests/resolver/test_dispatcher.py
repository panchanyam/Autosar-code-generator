"""
Tests resolver dispatcher.
"""

from autosar_codegen.resolver.dispatcher import (
    ResolverDispatcher,
)



def test_dispatcher_creation():

    dispatcher = ResolverDispatcher()

    assert dispatcher is not None



def test_dispatcher_registry():

    dispatcher = ResolverDispatcher()

    assert dispatcher.registry is not None