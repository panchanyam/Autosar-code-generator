"""
autosar_codegen.validator.registry
==================================

Validator plugin registry.

Maintains available AUTOSAR validators.
"""

from __future__ import annotations


from dataclasses import dataclass


from threading import RLock


from autosar_codegen.validator.base import (
    Validator,
)



# ============================================================================
# Registry Statistics
# ============================================================================


@dataclass(slots=True)
class RegistryStatistics:
    """
    Validator registry statistics.
    """

    validators: int = 0



# ============================================================================
# Validator Registry
# ============================================================================


class ValidatorRegistry:
    """
    Registry for validator plugins.
    """


    def __init__(
        self,
    ) -> None:


        self._validators: list[Validator] = []


        self._map: dict[
            str,
            Validator
        ] = {}


        self._lock = RLock()



    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------


    def register(
        self,
        validator: Validator,
    ) -> bool:
        """
        Register validator.

        Returns:

            True  registered

            False duplicate
        """

        with self._lock:


            if validator.name in self._map:

                return False



            self._validators.append(

                validator

            )


            self._map[

                validator.name

            ] = validator



            #
            # Execute lower priority first
            #
            self._validators.sort(

                key=lambda item:

                item.priority

            )


        return True



    def unregister(
        self,
        validator: Validator,
    ) -> None:
        """
        Remove validator.
        """

        with self._lock:


            self._map.pop(

                validator.name,

                None

            )


            if validator in self._validators:

                self._validators.remove(

                    validator

                )



    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------


    def get(
        self,
        name: str,
    ) -> Validator | None:
        """
        Find validator by name.
        """

        validator = self._map.get(

            name

        )


        if validator and validator.enabled:

            return validator


        return None



    def all(
        self,
    ) -> list[Validator]:
        """
        Return enabled validators.
        """

        return [

            validator

            for validator in self._validators

            if validator.enabled

        ]



    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------


    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Check validator existence.
        """

        return name in self._map



    def enable(
        self,
        name: str,
    ) -> bool:
        """
        Enable validator.
        """

        validator = self._map.get(

            name

        )


        if validator is None:

            return False


        validator.enabled = True

        return True



    def disable(
        self,
        name: str,
    ) -> bool:
        """
        Disable validator.
        """

        validator = self._map.get(

            name

        )


        if validator is None:

            return False


        validator.enabled = False

        return True



    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------


    def statistics(
        self,
    ) -> RegistryStatistics:
        """
        Return registry statistics.
        """

        return RegistryStatistics(

            validators=len(

                self._validators

            )

        )



    def clear(
        self,
    ) -> None:
        """
        Remove all validators.
        """

        with self._lock:

            self._validators.clear()

            self._map.clear()



    def __iter__(
        self,
    ):
        """
        Iterate enabled validators.
        """

        return iter(

            self.all()

        )