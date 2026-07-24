"""
autosar_codegen.generator.context
=================================

Generation execution context.

Provides shared services for generators.
"""

from __future__ import annotations


from dataclasses import dataclass, field


from pathlib import Path


from typing import Any



# ============================================================================
# Generated Artifact
# ============================================================================


@dataclass(slots=True)
class GeneratedArtifact:
    """
    Represents a generated output file.
    """

    path: Path

    generator: str

    description: str = ""



# ============================================================================
# Generator Context
# ============================================================================


@dataclass(slots=True)
class GeneratorContext:
    """
    Shared environment for code generation.
    """


    workspace: Any


    output_dir: Path



    templates_dir: Path | None = None



    variables: dict[str, Any] = field(

        default_factory=dict

    )



    artifacts: list[GeneratedArtifact] = field(

        default_factory=list

    )



    metadata: dict[str, Any] = field(

        default_factory=dict

    )



    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------


    def initialize(
        self,
    ) -> None:
        """
        Prepare output environment.
        """

        self.output_dir.mkdir(

            parents=True,

            exist_ok=True

        )



    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------


    def set_variable(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Store template variable.
        """

        self.variables[name] = value



    def get_variable(
        self,
        name: str,
        default=None,
    ):
        """
        Retrieve template variable.
        """

        return self.variables.get(

            name,

            default

        )



    # ------------------------------------------------------------------
    # File Handling
    # ------------------------------------------------------------------


    def write_file(
        self,
        filename: str,
        content: str,
        generator: str = "",
        description: str = "",
    ) -> Path:
        """
        Write generated file.

        Returns:
            Generated file path
        """

        path = (

            self.output_dir /

            filename

        )


        path.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        path.write_text(

            content,

            encoding="utf-8"

        )


        self.artifacts.append(

            GeneratedArtifact(

                path=path,

                generator=generator,

                description=description,

            )

        )


        return path



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store runtime metadata.
        """

        self.metadata[key] = value



    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve runtime metadata.
        """

        return self.metadata.get(

            key,

            default

        )



    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------


    @property
    def generated_files(
        self,
    ) -> list[Path]:
        """
        Return generated file paths.
        """

        return [

            artifact.path

            for artifact in self.artifacts

        ]