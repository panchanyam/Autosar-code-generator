"""
Tests validator registry.
"""

from autosar_codegen.validator.registry import (
    ValidatorRegistry,
)



class DummyValidator:

    name = "dummy"



def test_register_validator():

    registry = ValidatorRegistry()


    validator = DummyValidator()


    registry.register(
        validator
    )


    assert registry.get(
        "dummy"
    ) == validator



def test_registry_items():

    registry = ValidatorRegistry()


    registry.register(
        DummyValidator()
    )


    assert len(
        registry.all()
    ) == 1



def test_remove_validator():

    registry = ValidatorRegistry()


    registry.register(
        DummyValidator()
    )


    registry.remove(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None