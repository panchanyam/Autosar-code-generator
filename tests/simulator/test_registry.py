"""
Tests simulator registry.
"""

from autosar_codegen.simulator.registry import (
    SimulatorRegistry,
)



class DummySimulator:

    name = "dummy"



def test_register_simulator():

    registry = SimulatorRegistry()


    simulator = DummySimulator()


    registry.register(
        simulator
    )


    assert registry.get(
        "dummy"
    ) == simulator



def test_registry_items():

    registry = SimulatorRegistry()


    registry.register(
        DummySimulator()
    )


    assert len(
        registry.all()
    ) == 1



def test_remove_simulator():

    registry = SimulatorRegistry()


    registry.register(
        DummySimulator()
    )


    registry.remove(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None