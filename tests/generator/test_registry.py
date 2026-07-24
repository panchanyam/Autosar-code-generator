"""
Tests generator registry.
"""

from autosar_codegen.generator.registry import (
    GeneratorRegistry,
)



class DummyGenerator:

    name = "dummy"



def test_register_generator():

    registry = GeneratorRegistry()


    generator = DummyGenerator()


    registry.register(
        generator
    )


    assert registry.get(
        "dummy"
    ) == generator



def test_registry_items():

    registry = GeneratorRegistry()


    registry.register(
        DummyGenerator()
    )


    assert len(
        registry.all()
    ) == 1



def test_remove_generator():

    registry = GeneratorRegistry()


    registry.register(
        DummyGenerator()
    )


    registry.remove(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None