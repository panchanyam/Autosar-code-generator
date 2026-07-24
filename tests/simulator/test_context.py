"""
Tests simulation context.
"""

from autosar_codegen.simulator.context import (
    SimulationContext,
)



def test_context_creation():

    context = SimulationContext()


    assert context is not None



def test_context_storage():

    context = SimulationContext()


    context.set(
        "cycle",
        10,
    )


    assert context.get(
        "cycle"
    ) == 10



def test_missing_value():

    context = SimulationContext()


    assert context.get(
        "unknown"
    ) is None