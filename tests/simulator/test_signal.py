"""
Tests signal simulation.
"""

from autosar_codegen.simulator.signal import (
    SimSignal,
)



def test_signal_creation():

    signal = SimSignal(
        "Speed"
    )


    assert signal is not None



def test_signal_value():

    signal = SimSignal(
        "Speed"
    )


    signal.set_value(
        100
    )


    assert signal.value == 100