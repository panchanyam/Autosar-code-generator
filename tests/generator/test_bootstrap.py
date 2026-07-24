"""
Tests generator bootstrap.
"""

from autosar_codegen.generator.bootstrap import (
    bootstrap_generators,
)



def test_bootstrap_creation():

    registry = bootstrap_generators()


    assert registry is not None



def test_default_generators_registered():

    registry = bootstrap_generators()


    generators = registry.all()


    assert len(
        generators
    ) > 0