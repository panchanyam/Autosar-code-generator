"""
autosar_codegen.simulator.pdu

PDU packing and simulation.
"""

from __future__ import annotations


from dataclasses import dataclass, field



@dataclass(slots=True)
class PduRuntime:
    """
    Runtime PDU.
    """

    name: str

    signals: dict[str, object] = field(
        default_factory=dict
    )



class PduSimulator:
    """
    Simulates AUTOSAR PDU behaviour.
    """


    def __init__(
        self,
        name: str,
    ):

        self.pdu = PduRuntime(

            name=name

        )



    def set_signal(
        self,
        name: str,
        value,
    ) -> None:
        """
        Add signal value.
        """

        self.pdu.signals[name] = value



    def encode(
        self,
    ) -> bytes:
        """
        Simple runtime encoding.

        Production implementation will
        use bit-level AUTOSAR packing.
        """

        return str(

            self.pdu.signals

        ).encode()



    def transmit(
        self,
        context,
    ) -> None:
        """
        Send PDU.
        """

        context.transmit_frame(

            self.pdu.name,

            self.encode()

        )