"""
autosar_codegen.parser.bootstrap
================================

Default AUTOSAR parser registration.

Creates the standard parser environment
for AUTOSAR ARXML processing.
"""

from __future__ import annotations


from autosar_codegen.parser.registry import (
    ParserRegistry,
)


from autosar_codegen.parser.package import (
    PackageParser,
)

from autosar_codegen.parser.datatype import (
    DataTypeParser,
)

from autosar_codegen.parser.signal import (
    SignalParser,
)

from autosar_codegen.parser.pdu import (
    PduParser,
)

from autosar_codegen.parser.frame import (
    FrameParser,
)

from autosar_codegen.parser.network import (
    NetworkParser,
)



# ============================================================================
# Default Parser List
# ============================================================================


DEFAULT_PARSERS = (

    PackageParser,

    DataTypeParser,

    SignalParser,

    PduParser,

    FrameParser,

    NetworkParser,

)



# ============================================================================
# Bootstrap Function
# ============================================================================


def create_default_registry() -> ParserRegistry:
    """
    Create registry with standard AUTOSAR parsers.

    Returns:
        ParserRegistry
    """

    registry = ParserRegistry()


    for parser_class in DEFAULT_PARSERS:

        registry.register(
            parser_class()
        )


    return registry