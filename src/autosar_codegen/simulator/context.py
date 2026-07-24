"""
autosar_codegen.simulator.context
=================================

Simulation runtime context.

Maintains runtime state during
AUTOSAR simulation execution.
"""

from __future__ import annotations


from dataclasses import dataclass, field


from typing import Any


from collections import deque


from autosar_codegen.simulator.base import (
    SimulationEvent,
    SimulationState,
)



# ============================================================================
# ECU Runtime Model
# ============================================================================


@dataclass(slots=True)
class EcuRuntime:
    """
    Runtime ECU representation.
    """

    name: str

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



# ============================================================================
# Frame Runtime
# ============================================================================


@dataclass(slots=True)
class FrameRuntime:
    """
    Runtime frame transmission object.
    """

    name: str

    payload: bytes = b""

    timestamp: float = 0.0



# ============================================================================
# Simulation Context
# ============================================================================


@dataclass(slots=True)
class SimulationContext:
    """
    Runtime simulation environment.
    """


    workspace: Any


    time: float = 0.0


    state: SimulationState = (
        SimulationState.CREATED
    )


    ecus: dict[str, EcuRuntime] = field(
        default_factory=dict
    )


    signals: dict[str, Any] = field(
        default_factory=dict
    )


    frame_queue: deque[FrameRuntime] = field(
        default_factory=deque
    )


    events: list[SimulationEvent] = field(
        default_factory=list
    )


    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # ------------------------------------------------------------------
    # ECU Handling
    # ------------------------------------------------------------------


    def add_ecu(
        self,
        name: str,
        **metadata,
    ) -> EcuRuntime:
        """
        Add ECU runtime node.
        """

        ecu = EcuRuntime(

            name=name,

            metadata=metadata,

        )


        self.ecus[name] = ecu


        return ecu



    def get_ecu(
        self,
        name: str,
    ) -> EcuRuntime | None:
        """
        Retrieve ECU.
        """

        return self.ecus.get(
            name
        )



    # ------------------------------------------------------------------
    # Signal Handling
    # ------------------------------------------------------------------


    def set_signal(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Update signal value.
        """

        self.signals[name] = value



    def get_signal(
        self,
        name: str,
        default=None,
    ):
        """
        Read signal value.
        """

        return self.signals.get(

            name,

            default

        )



    # ------------------------------------------------------------------
    # Frame Handling
    # ------------------------------------------------------------------


    def transmit_frame(
        self,
        name: str,
        payload: bytes = b"",
    ) -> None:
        """
        Queue frame transmission.
        """

        self.frame_queue.append(

            FrameRuntime(

                name=name,

                payload=payload,

                timestamp=self.time,

            )

        )



    def receive_frame(
        self,
    ) -> FrameRuntime | None:
        """
        Retrieve next frame.
        """

        if not self.frame_queue:

            return None


        return self.frame_queue.popleft()



    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------


    def emit_event(
        self,
        event_type: str,
        source: str = "",
        payload=None,
    ) -> None:
        """
        Add simulation event.
        """

        self.events.append(

            SimulationEvent(

                timestamp=self.time,

                event_type=event_type,

                source=source,

                payload=payload,

            )

        )



    # ------------------------------------------------------------------
    # Clock
    # ------------------------------------------------------------------


    def advance(
        self,
        delta: float,
    ) -> None:
        """
        Advance simulation time.
        """

        self.time += delta



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def start(
        self,
    ) -> None:
        """
        Start simulation.
        """

        self.state = SimulationState.RUNNING



    def stop(
        self,
    ) -> None:
        """
        Stop simulation.
        """

        self.state = SimulationState.STOPPED



    def fail(
        self,
    ) -> None:
        """
        Mark simulation failed.
        """

        self.state = SimulationState.FAILED



    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------


    def clear(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self.signals.clear()

        self.frame_queue.clear()

        self.events.clear()

        self.time = 0.0