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
]