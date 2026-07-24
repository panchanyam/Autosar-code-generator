"""
autosar_codegen.simulator.signal

Signal runtime simulation.
"""

from __future__ import annotations


from dataclasses import dataclass



@dataclass(slots=True)
class SignalValue:
    """
    Runtime signal value.
    """

    name: str

    value: object = None

    timestamp: float = 0.0



class SignalSimulatorNode:
    """
    Handles signal updates.
    """


    def __init__(
        self,
        name: str,
    ):

        self.signal = SignalValue(

            name=name

        )



    def update(
        self,
        value,
        timestamp: float,
    ) -> None:
        """
        Update signal value.
        """

        self.signal.value = value

        self.signal.timestamp = timestamp



    def read(
        self,
    ):
        """
        Read signal value.
        """

        return self.signal.value



    def publish(
        self,
        context,
    ) -> None:
        """
        Publish signal to simulation context.
        """

        context.set_signal(

            self.signal.name,

            self.signal.value

        )