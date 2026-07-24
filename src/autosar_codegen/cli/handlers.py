"""
autosar_codegen.cli.handlers
============================

CLI workflow handlers.

Coordinates parser, resolver,
validator, simulator and generator.
"""

from __future__ import annotations


from pathlib import Path

from typing import Any


from autosar_codegen.core.logger import (
    get_logger,
)


logger = get_logger(
    __name__
)



# ============================================================================
# Base Handler
# ============================================================================


class HandlerError(Exception):
    """
    CLI workflow execution error.
    """



# ============================================================================
# Workspace Handler
# ============================================================================


class WorkspaceHandler:
    """
    Loads and prepares AUTOSAR workspace.
    """


    def __init__(
        self,
        parser=None,
        resolver=None,
    ) -> None:

        self.parser = parser

        self.resolver = resolver



    def load(
        self,
        input_file: Path,
    ) -> Any:
        """
        Load AUTOSAR input file.
        """

        logger.info(
            "Loading AUTOSAR file: %s",
            input_file,
        )


        if self.parser is None:

            raise HandlerError(
                "Parser service not configured"
            )


        workspace = self.parser.parse(

            input_file

        )


        if self.resolver:

            workspace = self.resolver.resolve(

                workspace

            )


        return workspace



# ============================================================================
# Validation Handler
# ============================================================================


class ValidationHandler:
    """
    Executes validation workflow.
    """


    def __init__(
        self,
        validator=None,
    ) -> None:

        self.validator = validator



    def execute(
        self,
        workspace,
    ) -> bool:
        """
        Validate workspace.
        """

        logger.info(
            "Running validation"
        )


        if self.validator is None:

            raise HandlerError(
                "Validator service not configured"
            )


        result = self.validator.validate(

            workspace

        )


        return result



# ============================================================================
# Generation Handler
# ============================================================================


class GenerationHandler:
    """
    Executes source generation.
    """


    def __init__(
        self,
        generator=None,
    ) -> None:

        self.generator = generator



    def execute(
        self,
        workspace,
        output_directory: Path,
    ) -> bool:
        """
        Generate source code.
        """

        logger.info(
            "Generating source code"
        )


        if self.generator is None:

            raise HandlerError(
                "Generator service not configured"
            )


        self.generator.generate(

            workspace,

            output_directory,

        )


        return True



# ============================================================================
# Simulation Handler
# ============================================================================


class SimulationHandler:
    """
    Executes simulation workflow.
    """


    def __init__(
        self,
        simulator=None,
    ) -> None:

        self.simulator = simulator



    def execute(
        self,
        workspace,
        cycles: int = 100,
    ) -> bool:
        """
        Run simulation.
        """

        logger.info(
            "Starting simulation"
        )


        if self.simulator is None:

            raise HandlerError(
                "Simulator service not configured"
            )


        self.simulator.run(

            workspace,

            cycles,

        )


        return True



# ============================================================================
# Application Workflow Handler
# ============================================================================


class ApplicationHandler:
    """
    High-level application workflow.

    Used by CLI commands.
    """


    def __init__(
        self,
        workspace_handler: WorkspaceHandler,
        validation_handler: ValidationHandler,
        generation_handler: GenerationHandler,
        simulation_handler: SimulationHandler,
    ) -> None:

        self.workspace_handler = workspace_handler

        self.validation_handler = validation_handler

        self.generation_handler = generation_handler

        self.simulation_handler = simulation_handler



    def load_workspace(
        self,
        input_file: Path,
    ):
        """
        Load workspace.
        """

        return self.workspace_handler.load(

            input_file

        )



    def validate(
        self,
        workspace,
    ) -> bool:

        return self.validation_handler.execute(

            workspace

        )



    def generate(
        self,
        workspace,
        output_directory: Path,
    ) -> bool:

        return self.generation_handler.execute(

            workspace,

            output_directory,

        )



    def simulate(
        self,
        workspace,
        cycles: int = 100,
    ) -> bool:

        return self.simulation_handler.execute(

            workspace,

            cycles,

        )