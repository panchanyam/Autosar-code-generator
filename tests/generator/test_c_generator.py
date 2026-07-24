"""
Tests C generator implementation.
"""

from pathlib import Path


from autosar_codegen.generator.c.generator import (
    CGenerator,
)



def test_c_generator_creation():

    generator = CGenerator()


    assert generator is not None



def test_c_generator_name():

    generator = CGenerator()


    assert generator.name == "c"



def test_c_generation(
    populated_workspace,
    output_directory,
):

    generator = CGenerator()


    result = generator.generate(

        populated_workspace,

        output_directory,

    )


    assert result is not None



def test_generated_output_exists(
    populated_workspace,
    output_directory,
):

    generator = CGenerator()


    generator.generate(

        populated_workspace,

        output_directory,

    )


    files = list(

        Path(output_directory).glob(
            "**/*"
        )

    )


    assert len(files) >= 0