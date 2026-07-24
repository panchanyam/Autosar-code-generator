"""
autosar_codegen.generator.c.generator
=====================================

AUTOSAR C code generator.

Generates C header files from resolved
AUTOSAR workspace objects.
"""

from __future__ import annotations


from pathlib import Path


from autosar_codegen.generator.base import (
    Generator,
    GeneratorMetadata,
)


from autosar_codegen.generator.template_engine import (
    TemplateEngine,
)



class CGenerator(Generator):
    """
    AUTOSAR C source generator.
    """


    metadata = GeneratorMetadata(

        name="CGenerator",

        version="1.0.0",

        description=(

            "Generates AUTOSAR C headers"

        ),

        language="C",

        priority=10,

    )


    def __init__(

        self,

    ) -> None:

        super().__init__()


        self.template_engine = None



    # ------------------------------------------------------------------
    # Initialize
    # ------------------------------------------------------------------


    def initialize(
        self,
        context,
    ) -> None:
        """
        Initialize template engine.
        """

        template_path = (

            Path(__file__).parent

            /

            "templates"

        )


        self.template_engine = TemplateEngine(

            template_path

        )



    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------


    def generate(
        self,
        context,
    ) -> bool:
        """
        Generate AUTOSAR C headers.
        """

        try:

            self._generate_datatypes(
                context
            )


            self._generate_signals(
                context
            )


            self._generate_pdus(
                context
            )


            return True



        except Exception:


            self.failure()


            raise



    # ------------------------------------------------------------------
    # Datatype generation
    # ------------------------------------------------------------------


    def _generate_datatypes(
        self,
        context,
    ) -> None:
        """
        Generate datatype header.
        """


        content = self.template_engine.render(

            "datatype.h.j2",

            {

                "datatypes":
                    context.workspace.datatypes

            }

        )


        context.write_file(

            "include/datatypes.h",

            content,

            generator=self.name,

            description="AUTOSAR datatype definitions"

        )


        self.file_generated()



    # ------------------------------------------------------------------
    # Signal generation
    # ------------------------------------------------------------------


    def _generate_signals(
        self,
        context,
    ) -> None:
        """
        Generate signal header.
        """


        content = self.template_engine.render(

            "signal.h.j2",

            {

                "signals":
                    context.workspace.signals

            }

        )


        context.write_file(

            "include/signals.h",

            content,

            generator=self.name,

            description="AUTOSAR signal definitions"

        )


        self.file_generated()



    # ------------------------------------------------------------------
    # PDU generation
    # ------------------------------------------------------------------


    def _generate_pdus(
        self,
        context,
    ) -> None:
        """
        Generate PDU header.
        """


        content = self.template_engine.render(

            "pdu.h.j2",

            {

                "pdus":
                    context.workspace.pdus

            }

        )


        context.write_file(

            "include/pdus.h",

            content,

            generator=self.name,

            description="AUTOSAR PDU definitions"

        )


        self.file_generated()