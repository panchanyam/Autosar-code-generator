"""
autosar_codegen.simulator.base
==============================

Base simulation framework.

Provides common infrastructure for
AUTOSAR runtime simulation.
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from dataclasses import dataclass, field


from enum import Enum


from typing import Any



# ============================================================================
# Simulation State
# ============================================================================


class SimulationState(Enum):
    """
    Simulator lifecycle state.
    """

    CREATED = "created"

    INITIALIZED = "initialized"

    RUNNING = "running"

    STOPPED = "stopped"

    FAILED = "failed"



# ============================================================================
# Simulator Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class SimulatorMetadata:
    """
    Simulator identification.
    """

    name: str

    version: str = "1.0.0"

    description: str = ""

    priority: int = 100



# ============================================================================
# Simulation Event
# ============================================================================


@dataclass(slots=True)
class SimulationEvent:
    """
    Runtime simulation event.
    """

    timestamp: float

    event_type: str

    source: str = ""

    payload: Any = None



# ============================================================================
# Simulation Statistics
# ============================================================================


@dataclass(slots=True)
class SimulationStatistics:
    """
    Runtime statistics.
    """

    cycles: int = 0

    events: int = 0

    signals_processed: int = 0

    frames_processed: int = 0



# ============================================================================
# Simulation Context
# ============================================================================


@dataclass(slots=True)
class SimulationContext:
    """
    Shared simulation environment.
    """

    workspace: Any


    time: float = 0.0


    state: SimulationState = (
        SimulationState.CREATED
    )


    events: list[SimulationEvent] = field(
        default_factory=list
    )


    metadata: dict[str, Any] = field(
        default_factory=dict
    )


    statistics: SimulationStatistics = field(
        default_factory=SimulationStatistics
    )


    def emit(
        self,
        event_type: str,
        source: str = "",
        payload: Any = None,
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

        self.statistics.events += 1



    def advance(
        self,
        delta: float,
    ) -> None:
        """
        Advance simulation time.
        """

        self.time += delta

        self.statistics.cycles += 1



# ============================================================================
# Simulator Base Class
# ============================================================================


class Simulator(ABC):
    """
    Abstract AUTOSAR simulator.

    Implementations:

        NetworkSimulator
        EcuSimulator
        SignalSimulator
    """


    metadata = SimulatorMetadata(
        name="BaseSimulator"
    )


    def __init__(
        self,
    ) -> None:

        self.context: SimulationContext | None = None

        self.enabled = True



    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------


    @property
    def name(
        self,
    ) -> str:
        """
        Simulator name.
        """

        return self.metadata.name



    @property
    def priority(
        self,
    ) -> int:
        """
        Execution priority.
        """

        return self.metadata.priority



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def initialize(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Initialize simulator.
        """

        self.context = context

        context.state = SimulationState.INITIALIZED



    @abstractmethod
    def step(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Execute one simulation step.
        """

        raise NotImplementedError



    def start(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Start simulation.
        """

        self.initialize(context)

        context.state = SimulationState.RUNNING



    def stop(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Stop simulation.
        """

        context.state = SimulationState.STOPPED



    def fail(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Mark simulation failed.
        """

        context.state = SimulationState.FAILED