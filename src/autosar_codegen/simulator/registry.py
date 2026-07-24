"""
autosar_codegen.simulator.registry
==================================

Simulator plugin registry.

Maintains available AUTOSAR simulators.
"""

from __future__ import annotations


from dataclasses import dataclass


from threading import RLock


from autosar_codegen.simulator.base import (
    Simulator,
)



# ============================================================================
# Registry Statistics
# ============================================================================


@dataclass(slots=True)
class RegistryStatistics:
    """
    Simulator registry statistics.
    """

    simulators: int = 0



# ============================================================================
# Simulator Registry
# ============================================================================


class SimulatorRegistry:
    """
    Registry for simulator plugins.
    """


    def __init__(
        self,
    ) -> None:

        self._simulators: list[Simulator] = []

        self._map: dict[str, Simulator] = {}

        self._lock = RLock()



    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------


    def register(
        self,
        simulator: Simulator,
    ) -> bool:
        """
        Register simulator.

        Returns:

            True  registered successfully

            False duplicate simulator
        """

        with self._lock:

            if simulator.name in self._map:

                return False



            self._simulators.append(

                simulator

            )


            self._map[

                simulator.name

            ] = simulator



            #
            # Lower priority executes first
            #
            self._simulators.sort(

                key=lambda item:

                item.priority

            )


        return True



    def unregister(
        self,
        simulator: Simulator,
    ) -> None:
        """
        Remove simulator.
        """

        with self._lock:

            self._map.pop(

                simulator.name,

                None

            )


            if simulator in self._simulators:

                self._simulators.remove(

                    simulator

                )



    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------


    def get(
        self,
        name: str,
    ) -> Simulator | None:
        """
        Retrieve simulator by name.
        """

        simulator = self._map.get(

            name

        )


        if simulator and simulator.enabled:

            return simulator


        return None



    def all(
        self,
    ) -> list[Simulator]:
        """
        Return enabled simulators.
        """

        return [

            simulator

            for simulator in self._simulators

            if simulator.enabled

        ]



    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------


    def enable(
        self,
        name: str,
    ) -> bool:
        """
        Enable simulator.
        """

        simulator = self._map.get(

            name

        )


        if simulator is None:

            return False



        simulator.enabled = True

        return True



    def disable(
        self,
        name: str,
    ) -> bool:
        """
        Disable simulator.
        """

        simulator = self._map.get(

            name

        )


        if simulator is None:

            return False



        simulator.enabled = False

        return True



    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Check simulator existence.
        """

        return name in self._map



    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------


    def statistics(
        self,
    ) -> RegistryStatistics:
        """
        Return registry information.
        """

        return RegistryStatistics(

            simulators=len(

                self._simulators

            )

        )



    def clear(
        self,
    ) -> None:
        """
        Remove all simulators.
        """

        with self._lock:

            self._simulators.clear()

            self._map.clear()



    def __iter__(
        self,
    ):
        """
        Iterate enabled simulators.
        """

        return iter(

            self.all()

        )