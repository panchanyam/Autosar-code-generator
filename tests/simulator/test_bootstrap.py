"""
Tests simulator bootstrap.
"""

from autosar_codegen.simulator.bootstrap import (
    bootstrap_simulators,
)



def test_bootstrap_creation():

    registry = bootstrap_simulators()


    assert registry is not None



def test_default_simulators_registered():

    registry = bootstrap_simulators()


    simulators = registry.all()


    assert len(
        simulators
    ) > 0