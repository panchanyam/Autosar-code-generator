"""
AUTOSAR XML processing package.
"""

from .loader import (
    XmlLoader,
    XmlLoaderConfig,
    XmlDocument,
    XmlSource,
)

from .namespace import (
    NamespaceManager,
    NamespaceContext,
    AutosarVersion,
)

from .xpath import (
    XPathEngine,
    XPathResult,
)

from .walker import (
    XmlWalker,
    XmlNode,
    WalkerStatistics,
)

from .cache import (
    XmlCache,
    XmlCacheEntry,
)

__all__ = [
    "XmlLoader",
    "XmlLoaderConfig",
    "XmlDocument",
    "XmlSource",
    "NamespaceManager",
    "NamespaceContext",
    "AutosarVersion",
    "XPathEngine",
    "XPathResult",
    "XmlWalker",
    "XmlNode",
    "WalkerStatistics",
    "XmlCache",
    "XmlCacheEntry",
]