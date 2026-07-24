"""
Tests generator base interface.
"""

from autosar_codegen.generator.base import (
    Generator,
)



class DummyGenerator(Generator):

    name = "dummy"


    def generate(
        self,
        context,
    ):
        return "generated"



def test_generator_creation():

    generator = DummyGenerator()

    assert generator is not None



def test_generator_name():

    generator = DummyGenerator()

    assert generator.name == "dummy"



def test_generate_execution():

    generator = DummyGenerator()


    result = generator.generate(
        None
    )


    assert result == "generated"