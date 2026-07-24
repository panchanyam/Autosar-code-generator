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


__all__ = [
    "Parser",
    "ParserMetadata",
    "ParserStatistics",
    "ParserContext",
    "ParserRegistry",
    "RegistryStatistics",
    "ParserDispatcher",
    "DispatcherStatistics",
]