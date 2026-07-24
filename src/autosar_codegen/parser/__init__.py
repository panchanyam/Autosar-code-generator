"""
AUTOSAR parser framework.
"""

from .base import (
    Parser,
    ParserMetadata,
    ParserStatistics,
)

from .context import (
    ParserContext,
)

from .registry import (
    ParserRegistry,
    RegistryStatistics,
)

from .dispatcher import (
    ParserDispatcher,
    DispatcherStatistics,
)

from .package import (
    PackageParser,
)

from .datatype import (
    DataTypeParser,
)

from .signal import (
    SignalParser,
)

from .pdu import (
    PduParser,
)

from .frame import (
    FrameParser,
)

from .network import (
    NetworkParser,
)

from .bootstrap import (
    create_default_registry,
    DEFAULT_PARSERS,
)

from .defaults import (
    ParserPhase,
    PARSER_PHASES,
    PARSER_DEPENDENCIES,
    get_parser_order,
    get_dependencies,
)


__all__ = [
    "Parser",
    "ParserMetadata",
    "ParserStatistics",
    "ParserContext",
    "ParserRegistry",
    "RegistryStatistics",
    "ParserDispatcher",
    "DispatcherStatistics",
    "PackageParser",
    "DataTypeParser",
    "SignalParser",
    "PduParser",
    "FrameParser",
    "NetworkParser",
    "create_default_registry",
    "DEFAULT_PARSERS",
    "ParserPhase",
    "PARSER_PHASES",
    "PARSER_DEPENDENCIES",
    "get_parser_order",
    "get_dependencies",
]