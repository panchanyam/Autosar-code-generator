"""
Tests for core configuration.
"""

from pathlib import Path


from autosar_codegen.core.config import (
    Config,
)



def test_default_config_creation():

    config = Config()


    assert config is not None



def test_config_output_directory():

    config = Config()


    directory = Path(
        "generated"
    )


    config.output_directory = directory


    assert config.output_directory == directory



def test_config_attributes_exist():

    config = Config()


    assert hasattr(
        config,
        "output_directory",
    )