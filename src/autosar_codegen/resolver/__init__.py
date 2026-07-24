"""
AUTOSAR resolver package.
"""

from .resolver import (
    Resolver,
    ResolverManager,
    ResolverStatistics,
)

from .base import (
    Resolver,
    ResolverMetadata,
    ResolverStatistics,
)

from .context import (
    ResolverContext,
)

from .registry import (
    ResolverRegistry,
    RegistryStatistics,
)

from .dispatcher import (
    ResolverDispatcher,
    DispatcherStatistics,
)

__all__ = [
    "Resolver",
    "ResolverManager",
    "ResolverStatistics",
    "ResolverMetadata",
    "ResolverContext",
    "ResolverRegistry",
    "RegistryStatistics",
    "ResolverDispatcher",
    "DispatcherStatistics",
]