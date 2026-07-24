"""
autosar_codegen.simulator.ecu

ECU runtime simulation component.
"""

from __future__ import annotations


from dataclasses import dataclass, field


from typing import Any



@dataclass(slots=True)
class EcuState:
    """
    ECU runtime state.
    """

    name: str

    running: bool = False

    signals: dict[str, Any] = field(
        default_factory=dict
    )



class EcuSimulatorNode:
    """
    Represents an ECU runtime node.
    """


    def __init__(
        self,
        name: str,
    ) -> None:

        self.state = EcuState(

            name=name

        )



    def start(
        self,
    ) -> None:
        """
        Start ECU.
        """

        self.state.running = True



    def stop(
        self,
    ) -> None:
        """
        Stop ECU.
        """

        self.state.running = False



    def set_signal(
        self,
        name: str,
        value,
    ) -> None:
        """
        Update ECU signal.
        """

        self.state.signals[name] = value



    def get_signal(
        self,
        name: str,
        default=None,
    ):
        """
        Read ECU signal.
        """

        return self.state.signals.get(

            name,

            default

        )



    def step(
        self,
        context,
    ) -> None:
        """
        Execute ECU cycle.
        """

        if not self.state.running:

            return


        context.emit_event(

            "ECU_CYCLE",

            self.state.name

        )