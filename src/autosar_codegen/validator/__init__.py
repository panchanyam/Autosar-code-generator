"""
AUTOSAR validation framework.
"""


from .base import (

    Validator,

    ValidatorMetadata,

    ValidationContext,

    ValidationMessage,

    ValidationSeverity,

    ValidationStatistics,

)

from .registry import (

    ValidatorRegistry,

    RegistryStatistics,

)

from .context import (

    ValidationContext,

    ValidationSummary,

)

from .dispatcher import (

    ValidatorDispatcher,

    DispatcherStatistics,

)


__all__ = [

    "Validator",

    "ValidatorMetadata",

    "ValidationContext",

    "ValidationMessage",

    "ValidationSeverity",

    "ValidationStatistics",

    "ValidatorRegistry",

    "RegistryStatistics",

    "ValidationSummary",

    "ValidatorDispatcher",

    "DispatcherStatistics",

]