"""
autosar_codegen.cli.integration
===============================

CLI application integration layer.

Creates and connects all AUTOSAR
processing services.
"""

from __future__ import annotations


from dataclasses import dataclass


from autosar_codegen.core.logger import (
    get_logger,
)


from autosar_codegen.cli.handlers import (
    WorkspaceHandler,
    ValidationHandler,
    GenerationHandler,
    SimulationHandler,
    ApplicationHandler,
)


logger = get_logger(
    __name__
)



# ============================================================================
# Application Services
# ============================================================================


@dataclass(slots=True)
class ApplicationServices:
    """
    Collection of application services.
    """

    parser: object | None = None

    resolver: object | None = None

    validator: object | None = None

    generator: object | None = None

    simulator: object | None = None



# ============================================================================
# Integration Builder
# ============================================================================


class IntegrationBuilder:
    """
    Builds AUTOSAR application pipeline.
    """


    def __init__(
        self,
    ) -> None:

        self.services = ApplicationServices()



    # ------------------------------------------------------------------
    # Service Registration
    # ------------------------------------------------------------------


    def register_parser(
        self,
        parser,
    ) -> "IntegrationBuilder":

        self.services.parser = parser

        return self



    def register_resolver(
        self,
        resolver,
    ) -> "IntegrationBuilder":

        self.services.resolver = resolver

        return self



    def register_validator(
        self,
        validator,
    ) -> "IntegrationBuilder":

        self.services.validator = validator

        return self



    def register_generator(
        self,
        generator,
    ) -> "IntegrationBuilder":

        self.services.generator = generator

        return self



    def register_simulator(
        self,
        simulator,
    ) -> "IntegrationBuilder":

        self.services.simulator = simulator

        return self



    # ------------------------------------------------------------------
    # Build Application
    # ------------------------------------------------------------------


    def build(
        self,
    ) -> ApplicationHandler:
        """
        Create application handler.
        """


        workspace_handler = WorkspaceHandler(

            parser=self.services.parser,

            resolver=self.services.resolver,

        )


        validation_handler = ValidationHandler(

            validator=self.services.validator,

        )


        generation_handler = GenerationHandler(

            generator=self.services.generator,

        )


        simulation_handler = SimulationHandler(

            simulator=self.services.simulator,

        )


        return ApplicationHandler(

            workspace_handler,

            validation_handler,

            generation_handler,

            simulation_handler,

        )



# ============================================================================
# Default Application Factory
# ============================================================================


def create_application(
    *,
    parser=None,
    resolver=None,
    validator=None,
    generator=None,
    simulator=None,
) -> ApplicationHandler:
    """
    Create fully configured CLI application.
    """


    builder = IntegrationBuilder()



    if parser:

        builder.register_parser(
            parser
        )


    if resolver:

        builder.register_resolver(
            resolver
        )


    if validator:

        builder.register_validator(
            validator
        )


    if generator:

        builder.register_generator(
            generator
        )


    if simulator:

        builder.register_simulator(
            simulator
        )


    return builder.build()