"""
autosar_codegen.generator.base
==============================

Base generator framework.

Provides common infrastructure for all
AUTOSAR code generators.
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from dataclasses import dataclass, field


from pathlib import Path

from typing import Any



# ============================================================================
# Generator Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class GeneratorMetadata:
    """
    Generator identification information.
    """

    name: str

    version: str = "1.0.0"

    description: str = ""

    language: str = ""

    priority: int = 100



# ============================================================================
# Generator Statistics
# ============================================================================


@dataclass(slots=True)
class GeneratorStatistics:
    """
    Generation statistics.
    """

    files_generated: int = 0

    templates_processed: int = 0

    failed: int = 0



# ============================================================================
# Generation Context
# ============================================================================


@dataclass(slots=True)
class GeneratorContext:
    """
    Shared generator environment.
    """

    workspace: Any

    output_dir: Path

    templates_dir: Path | None = None


    metadata: dict[str, Any] = field(
        default_factory=dict
    )


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store generator state.
        """

        self.metadata[key] = value



    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve generator state.
        """

        return self.metadata.get(
            key,
            default
        )



# ============================================================================
# Generator Base
# ============================================================================


class Generator(ABC):
    """
    Abstract code generator.

    Example implementations:

        CGenerator
        CppGenerator
        PythonGenerator
        DocumentationGenerator

    """


    metadata = GeneratorMetadata(

        name="BaseGenerator"

    )


    def __init__(
        self,
    ) -> None:


        self.statistics = (
            GeneratorStatistics()
        )


        self.enabled = True



    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------


    @property
    def name(
        self,
    ) -> str:
        """
        Generator name.
        """

        return self.metadata.name



    @property
    def language(
        self,
    ) -> str:
        """
        Target language.
        """

        return self.metadata.language



    @property
    def priority(
        self,
    ) -> int:
        """
        Generator priority.
        """

        return self.metadata.priority



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def initialize(
        self,
        context: GeneratorContext,
    ) -> None:
        """
        Initialization hook.
        """



    @abstractmethod
    def generate(
        self,
        context: GeneratorContext,
    ) -> bool:
        """
        Execute generation.

        Returns:

            True  success
            False failure
        """

        raise NotImplementedError



    def finalize(
        self,
        context: GeneratorContext,
    ) -> None:
        """
        Finalization hook.
        """



    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------


    def file_generated(
        self,
    ) -> None:
        """
        Track generated file.
        """

        self.statistics.files_generated += 1



    def template_processed(
        self,
    ) -> None:
        """
        Track template usage.
        """

        self.statistics.templates_processed += 1



    def failure(
        self,
    ) -> None:
        """
        Track failure.
        """

        self.statistics.failed += 1