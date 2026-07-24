"""
autosar_codegen.cli.commands
============================

CLI command implementations.

Provides command abstraction for:

- generation
- validation
- simulation
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from dataclasses import dataclass


from pathlib import Path


from typing import Any



from autosar_codegen.core.logger import (
    get_logger,
)



logger = get_logger(
    __name__
)



# ============================================================================
# Command Context
# ============================================================================


@dataclass(slots=True)
class CommandContext:
    """
    Shared CLI execution context.
    """

    workspace: Any = None

    input_file: Path | None = None

    output_directory: Path | None = None

    config: Any = None



# ============================================================================
# Base Command
# ============================================================================


class Command(ABC):
    """
    CLI command interface.
    """


    name: str = "base"


    description: str = ""



    @abstractmethod
    def execute(
        self,
        context: CommandContext,
    ) -> int:
        """
        Execute command.

        Returns:

            0 success

            non-zero failure
        """

        raise NotImplementedError



# ============================================================================
# Generate Command
# ============================================================================


class GenerateCommand(Command):
    """
    Generate source code command.
    """


    name = "generate"


    description = (
        "Generate source code from AUTOSAR model"
    )



    def execute(
        self,
        context: CommandContext,
    ) -> int:

        logger.info(
            "Starting code generation"
        )


        #
        # Generator integration will be
        # connected in later commits.
        #

        return 0



# ============================================================================
# Validate Command
# ============================================================================


class ValidateCommand(Command):
    """
    Validate AUTOSAR model command.
    """


    name = "validate"


    description = (
        "Validate AUTOSAR model"
    )



    def execute(
        self,
        context: CommandContext,
    ) -> int:

        logger.info(
            "Starting validation"
        )


        #
        # Validator dispatcher integration
        # will be connected later.
        #

        return 0



# ============================================================================
# Simulate Command
# ============================================================================


class SimulateCommand(Command):
    """
    Run AUTOSAR simulation command.
    """


    name = "simulate"


    description = (
        "Execute AUTOSAR simulation"
    )



    def execute(
        self,
        context: CommandContext,
    ) -> int:

        logger.info(
            "Starting simulation"
        )


        #
        # Simulator dispatcher integration
        # will be connected later.
        #

        return 0



# ============================================================================
# Command Registry
# ============================================================================


class CommandRegistry:
    """
    Stores available CLI commands.
    """


    def __init__(
        self,
    ) -> None:

        self._commands: dict[str, Command] = {}



    def register(
        self,
        command: Command,
    ) -> None:
        """
        Register command.
        """

        self._commands[

            command.name

        ] = command



    def get(
        self,
        name: str,
    ) -> Command | None:
        """
        Retrieve command.
        """

        return self._commands.get(

            name

        )



    def all(
        self,
    ) -> list[Command]:
        """
        Return commands.
        """

        return list(

            self._commands.values()

        )



    def clear(
        self,
    ) -> None:
        """
        Remove commands.
        """

        self._commands.clear()