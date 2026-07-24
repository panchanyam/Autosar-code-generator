"""
AUTOSAR code generation framework.
"""


from .base import (

    Generator,

    GeneratorMetadata,

    GeneratorContext,

    GeneratorStatistics,

)

from .registry import (

    GeneratorRegistry,

    RegistryStatistics,

)

from .context import (

    GeneratorContext,

    GeneratedArtifact,

)

from .template_engine import (

    TemplateEngine,

    TemplateStatistics,

)

from .dispatcher import (

    GeneratorDispatcher,

    DispatcherStatistics,

)

from .bootstrap import (
    DEFAULT_GENERATORS,
    create_default_registry,
)


__all__ = [

    "Generator",

    "GeneratorMetadata",

    "GeneratorContext",

    "GeneratorStatistics",

    "GeneratorRegistry",

    "RegistryStatistics",

    "GeneratedArtifact",

    "TemplateEngine",

    "TemplateStatistics",

    "GeneratorDispatcher",

    "DispatcherStatistics",

    "DEFAULT_GENERATORS",
]