"""
Tests PDU simulation.
"""

from autosar_codegen.simulator.pdu import (
    SimPdu,
)



def test_pdu_creation():

    pdu = SimPdu(
        "EngineData"
    )


    assert pdu is not None



def test_pdu_signal_addition():

    pdu = SimPdu(
        "EngineData"
    )


    pdu.add_signal(
        "Speed"
    )


    assert (
        "Speed"
        in pdu.signals
    )