"""
autosar_codegen.resolver.bootstrap
==================================

Default AUTOSAR resolver registration.

Creates the standard resolver environment.
"""

from __future__ import annotations


from autosar_codegen.resolver.registry import (
    ResolverRegistry,
)


from autosar_codegen.resolver.datatype import (
    DataTypeResolver,
)


from autosar_codegen.resolver.signal import (
    SignalResolver,
)


from autosar_codegen.resolver.pdu import (
    PduResolver,
)


from autosar_codegen.resolver.frame import (
    FrameResolver,
)


from autosar_codegen.resolver.network import (
    NetworkResolver,
)



# ============================================================================
# Default Resolver List
# ============================================================================


DEFAULT_RESOLVERS = (

    DataTypeResolver,

    SignalResolver,

    PduResolver,

    FrameResolver,

    NetworkResolver,

)



# ============================================================================
# Bootstrap
# ============================================================================


def create_default_registry() -> ResolverRegistry:
    """
    Create resolver registry containing
    all default AUTOSAR resolvers.

    Returns:
        ResolverRegistry
    """

    registry = ResolverRegistry()



    for resolver_class in DEFAULT_RESOLVERS:


        registry.register(

            resolver_class()

        )


    return registry