"""
autosar_codegen.parser.defaults
===============================

Default parser execution configuration.

Defines AUTOSAR parsing order and dependencies.
"""

from __future__ import annotations


from dataclasses import dataclass


# ============================================================================
# Parser Phase Definition
# ============================================================================


@dataclass(frozen=True, slots=True)
class ParserPhase:
    """
    Defines parser execution phase.
    """

    name: str

    order: int

    description: str



# ============================================================================
# Default AUTOSAR Parse Phases
# ============================================================================


PARSER_PHASES = (

    ParserPhase(

        name="package",

        order=10,

        description=(
            "Parse AUTOSAR package hierarchy"
        ),

    ),


    ParserPhase(

        name="datatype",

        order=20,

        description=(
            "Parse implementation datatypes"
        ),

    ),


    ParserPhase(

        name="signal",

        order=30,

        description=(
            "Parse communication signals"
        ),

    ),


    ParserPhase(

        name="pdu",

        order=40,

        description=(
            "Parse I-PDU definitions and mappings"
        ),

    ),


    ParserPhase(

        name="frame",

        order=50,

        description=(
            "Parse communication frames"
        ),

    ),


    ParserPhase(

        name="network",

        order=60,

        description=(
            "Parse CAN/Ethernet networks"
        ),

    ),

)



# ============================================================================
# Parser Dependency Map
# ============================================================================


PARSER_DEPENDENCIES = {

    "datatype": (

        "package",

    ),


    "signal": (

        "datatype",

    ),


    "pdu": (

        "signal",

    ),


    "frame": (

        "pdu",

    ),


    "network": (

        "frame",

    ),

}



# ============================================================================
# Helper Functions
# ============================================================================


def get_parser_order() -> list[str]:
    """
    Return parser execution order.

    """

    return [

        phase.name

        for phase in sorted(
            PARSER_PHASES,
            key=lambda item: item.order,
        )

    ]



def get_dependencies(
    parser_name: str,
) -> tuple[str, ...]:
    """
    Get parser dependencies.
    """

    return PARSER_DEPENDENCIES.get(
        parser_name,
        (),
    )