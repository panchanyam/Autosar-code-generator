"""
autosar_codegen.simulator.dispatcher
====================================

Simulation execution engine.

Coordinates registered AUTOSAR simulators.
"""

from __future__ import annotations


from dataclasses import dataclass


from autosar_codegen.simulator.registry import (
    SimulatorRegistry,
)


from autosar_codegen.simulator.context import (
    SimulationContext,
)


from autosar_codegen.simulator.base import (
    SimulationState,
)



# ============================================================================
# Dispatcher Statistics
# ============================================================================


@dataclass(slots=True)
class DispatcherStatistics:
    """
    Simulation execution statistics.
    """

    cycles: int = 0

    simulators_executed: int = 0

    failures: int = 0



# ============================================================================
# Simulator Dispatcher
# ============================================================================


class SimulatorDispatcher:
    """
    Executes simulator plugins.
    """


    def __init__(
        self,
        registry: SimulatorRegistry,
    ) -> None:

        self.registry = registry

        self.statistics = DispatcherStatistics()



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def initialize(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Initialize all simulators.
        """

        for simulator in self.registry.all():

            simulator.initialize(

                context

            )



    def start(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Start simulation.
        """

        self.initialize(

            context

        )


        context.start()



    def stop(
        self,
        context: SimulationContext,
    ) -> None:
        """
        Stop simulation.
        """

        context.stop()



    # ------------------------------------------------------------------
    # Simulation Execution
    # ------------------------------------------------------------------


    def step(
        self,
        context: SimulationContext,
    ) -> DispatcherStatistics:
        """
        Execute one simulation cycle.
        """

        if context.state != SimulationState.RUNNING:

            return self.statistics



        for simulator in self.registry.all():

            try:

                simulator.step(

                    context

                )


                self.statistics.simulators_executed += 1



            except Exception as exc:


                self.statistics.failures += 1


                context.emit_event(

                    event_type="SIMULATOR_FAILURE",

                    source=simulator.name,

                    payload=str(exc),

                )


        self.statistics.cycles += 1


        return self.statistics



    def run(
        self,
        context: SimulationContext,
        cycles: int,
        step_time: float = 0.01,
    ) -> DispatcherStatistics:
        """
        Execute multiple simulation cycles.
        """

        self.start(

            context

        )


        for _ in range(cycles):

            self.step(

                context

            )


            context.advance(

                step_time

            )


            if context.state == SimulationState.FAILED:

                break



        self.stop(

            context

        )


        return self.statistics



    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------


    def is_running(
        self,
        context: SimulationContext,
    ) -> bool:
        """
        Check simulation state.
        """

        return (

            context.state == SimulationState.RUNNING

        )