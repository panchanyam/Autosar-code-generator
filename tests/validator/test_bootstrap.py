"""
Tests validator bootstrap.
"""

from autosar_codegen.validator.bootstrap import (
    bootstrap_validators,
)



def test_bootstrap_creation():

    registry = bootstrap_validators()


    assert registry is not None



def test_default_validators_registered():

    registry = bootstrap_validators()


    validators = registry.all()


    assert len(
        validators
    ) > 0