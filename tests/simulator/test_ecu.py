"""
Tests ECU simulation.
"""

from autosar_codegen.simulator.ecu import (
    ECU,
)



def test_ecu_creation():

    ecu = ECU(
        "EngineECU"
    )


    assert ecu is not None



def test_ecu_name():

    ecu = ECU(
        "EngineECU"
    )


    assert ecu.name == "EngineECU"



def test_ecu_start():

    ecu = ECU(
        "EngineECU"
    )


    result = ecu.start()


    assert result is not None