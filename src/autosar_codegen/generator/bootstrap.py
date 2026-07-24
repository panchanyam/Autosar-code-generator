"""
autosar_codegen.generator.bootstrap
===================================

Default generator registration.

Creates the standard generator environment.
"""

from __future__ import annotations


from autosar_codegen.generator.registry import (
    GeneratorRegistry,
)


from autosar_codegen.generator.c import (
    CGenerator,
)



# ============================================================================
# Default Generators
# ============================================================================


DEFAULT_GENERATORS = (

    CGenerator,

)



# ============================================================================
# Bootstrap
# ============================================================================


def create_default_registry() -> GeneratorRegistry:
    """
    Create generator registry with
    default AUTOSAR generators.

    Returns:
        GeneratorRegistry
    """

    registry = GeneratorRegistry()



    for generator_class in DEFAULT_GENERATORS:

        registry.register(

            generator_class()

        )


    return registry