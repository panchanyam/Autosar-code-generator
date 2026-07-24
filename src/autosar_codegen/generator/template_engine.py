"""
autosar_codegen.generator.template_engine
=========================================

Jinja2 based template rendering engine.

Responsible for loading and rendering
generator templates.
"""

from __future__ import annotations


from dataclasses import dataclass


from pathlib import Path


from typing import Any



from jinja2 import (

    Environment,

    FileSystemLoader,

    Template,

    TemplateNotFound,

)



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class TemplateStatistics:
    """
    Template engine statistics.
    """

    loaded: int = 0

    rendered: int = 0

    failed: int = 0



# ============================================================================
# Template Engine
# ============================================================================


class TemplateEngine:
    """
    Jinja2 template manager.
    """


    def __init__(
        self,
        template_dir: Path,
    ) -> None:


        self.template_dir = (

            Path(template_dir)

        )


        self.statistics = (
            TemplateStatistics()
        )


        self._cache: dict[
            str,
            Template
        ] = {}



        self.environment = Environment(

            loader=FileSystemLoader(

                str(
                    self.template_dir
                )

            ),

            autoescape=False,

            keep_trailing_newline=True,

        )



    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------


    def load(
        self,
        name: str,
    ) -> Template:
        """
        Load template.

        Uses cache.
        """

        if name in self._cache:

            return self._cache[name]



        try:

            template = (
                self.environment
                .get_template(name)
            )


            self._cache[name] = template


            self.statistics.loaded += 1


            return template



        except TemplateNotFound as exc:


            self.statistics.failed += 1


            raise FileNotFoundError(

                f"Template not found: {name}"

            ) from exc



    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------


    def render(
        self,
        name: str,
        variables: dict[str, Any],
    ) -> str:
        """
        Render template.

        Args:

            name:
                Template filename

            variables:
                Template data

        """

        try:

            template = self.load(
                name
            )


            result = template.render(
                **variables
            )


            self.statistics.rendered += 1


            return result



        except Exception:


            self.statistics.failed += 1


            raise



    # ------------------------------------------------------------------
    # Direct Rendering
    # ------------------------------------------------------------------


    def render_template(
        self,
        template: Template,
        variables: dict[str, Any],
    ) -> str:
        """
        Render already loaded template.
        """

        return template.render(
            **variables
        )



    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------


    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check template availability.
        """

        return (

            self.template_dir /

            name

        ).exists()



    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------


    def clear_cache(
        self,
    ) -> None:
        """
        Remove cached templates.
        """

        self._cache.clear()