"""
Tests simulator base interface.
"""

from autosar_codegen.simulator.base import (
    Simulator,
)



class DummySimulator(Simulator):

    name = "dummy"


    def run(
        self,
        context,
    ):

        return True



def test_simulator_creation():

    simulator = DummySimulator()

    assert simulator is not None



def test_simulator_name():

    simulator = DummySimulator()

    assert simulator.name == "dummy"



def test_run_execution():

    simulator = DummySimulator()


    result = simulator.run(
        None
    )


    assert result is True