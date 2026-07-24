"""
Tests template rendering engine.
"""

from autosar_codegen.generator.template_engine import (
    TemplateEngine,
)



def test_template_engine_creation():

    engine = TemplateEngine()


    assert engine is not None



def test_render_template():

    engine = TemplateEngine()


    template = (
        "Hello {{name}}"
    )


    result = engine.render(

        template,

        {
            "name": "AUTOSAR"
        }

    )


    assert result == (
        "Hello AUTOSAR"
    )