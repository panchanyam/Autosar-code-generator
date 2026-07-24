"""
Tests network simulation.
"""

from autosar_codegen.simulator.network import (
    SimNetwork,
)



def test_network_creation():

    network = SimNetwork(
        "CAN"
    )


    assert network is not None



def test_network_ecu_addition():

    network = SimNetwork(
        "CAN"
    )


    network.add_ecu(
        "EngineECU"
    )


    assert (
        "EngineECU"
        in network.ecus
    )