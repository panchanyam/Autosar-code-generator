"""
autosar_codegen.simulator.network

Network bus simulation.
"""

from __future__ import annotations


from dataclasses import dataclass, field



@dataclass(slots=True)
class NetworkBus:
    """
    Runtime communication bus.
    """

    name: str

    frames: list = field(
        default_factory=list
    )



class NetworkSimulatorNode:
    """
    Simulates CAN/Ethernet network.
    """


    def __init__(
        self,
        name: str,
    ):

        self.bus = NetworkBus(

            name=name

        )



    def send(
        self,
        frame,
    ) -> None:
        """
        Add frame to network.
        """

        self.bus.frames.append(

            frame

        )



    def receive(
        self,
    ):
        """
        Receive frame.
        """

        if not self.bus.frames:

            return None


        return self.bus.frames.pop(0)



    def step(
        self,
        context,
    ) -> None:
        """
        Process network cycle.
        """

        frame = context.receive_frame()


        if frame:

            self.send(frame)


            context.emit_event(

                "FRAME_RECEIVED",

                self.bus.name,

                frame

            )