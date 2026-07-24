"""
Tests simulator dispatcher.
"""

from autosar_codegen.simulator.dispatcher import (
    SimulatorDispatcher,
)



def test_dispatcher_creation():

    dispatcher = SimulatorDispatcher()


    assert dispatcher is not None



def test_dispatcher_registry():

    dispatcher = SimulatorDispatcher()


    assert dispatcher.registry is not None