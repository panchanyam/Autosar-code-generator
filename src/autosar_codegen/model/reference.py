"""
autosar_codegen.model.reference
===============================

AUTOSAR reference model.

Every <*-REF> element parsed from ARXML is represented by an
AutosarReference object.

References are intentionally kept unresolved until the
ReferenceResolver phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
from typing import Optional

from autosar_codegen.model.base import AutosarElement


# ============================================================================
# Reference Type
# ============================================================================


class ReferenceType(str, Enum):
    """
    AUTOSAR reference kind.
    """

    ABSOLUTE = "ABSOLUTE"

    RELATIVE = "RELATIVE"

    UUID = "UUID"


# ============================================================================
# Destination Type
# ============================================================================


class DestinationType(str, Enum):
    """
    Frequently used DEST values.

    Additional destination names may be used directly
    as strings when vendor extensions are encountered.
    """

    PACKAGE = "AR-PACKAGE"

    I_SIGNAL = "I-SIGNAL"

    I_SIGNAL_GROUP = "I-SIGNAL-GROUP"

    I_PDU = "I-PDU"

    CAN_FRAME = "CAN-FRAME"

    IMPLEMENTATION_DATA_TYPE = "IMPLEMENTATION-DATA-TYPE"

    APPLICATION_DATA_TYPE = "APPLICATION-DATA-TYPE"

    COMPU_METHOD = "COMPU-METHOD"

    UNIT = "UNIT"


# ============================================================================
# Autosar Reference
# ============================================================================


@dataclass(slots=True)
class AutosarReference:
    """
    Represents one AUTOSAR reference.

    The reference is intentionally unresolved until the
    resolver stage.
    """

    path: str

    destination: str | DestinationType

    reference_type: ReferenceType = ReferenceType.ABSOLUTE

    resolved: Optional[AutosarElement] = None

    # ------------------------------------------------------------------

    @property
    def is_resolved(self) -> bool:
        """
        True if resolver has linked this reference.
        """
        return self.resolved is not None

    # ------------------------------------------------------------------

    @property
    def is_absolute(self) -> bool:
        return self.reference_type == ReferenceType.ABSOLUTE

    # ------------------------------------------------------------------

    @property
    def is_relative(self) -> bool:
        return self.reference_type == ReferenceType.RELATIVE

    # ------------------------------------------------------------------

    @property
    def is_uuid(self) -> bool:
        return self.reference_type == ReferenceType.UUID

    # ------------------------------------------------------------------

    @property
    def parts(self) -> tuple[str, ...]:
        """
        Path split into components.

        Example
        -------
        "/Communication/Signals/VehicleSpeed"

        becomes

        ("Communication","Signals","VehicleSpeed")
        """

        p = PurePosixPath(self.path)

        return tuple(part for part in p.parts if part != "/")

    # ------------------------------------------------------------------

    @property
    def short_name(self) -> str:
        """
        Last component of the reference.
        """

        if not self.parts:
            return ""

        return self.parts[-1]

    # ------------------------------------------------------------------

    def bind(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Bind resolved object.
        """

        self.resolved = element

    # ------------------------------------------------------------------

    def unbind(self) -> None:
        """
        Remove binding.
        """

        self.resolved = None

    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.path

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"AutosarReference("
            f"path='{self.path}', "
            f"destination='{self.destination}', "
            f"resolved={self.is_resolved})"
        )