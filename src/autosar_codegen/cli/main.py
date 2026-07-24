from __future__ import annotations

import typer
from rich.console import Console

from autosar_codegen.version import __version__

console = Console()

app = typer.Typer(
    name="autosar-codegen",
    help="AUTOSAR ARXML Parser and Code Generator",
    add_completion=False,
)


@app.command()
def version() -> None:
    """
    Print version.
    """

    console.print(
        f"[green]AUTOSAR Code Generator[/green] v{__version__}"
    )


@app.command()
def about() -> None:
    """
    Project information.
    """

    console.print(
        "[cyan]Generic AUTOSAR Code Generator[/cyan]"
    )

    console.print(
        "Supports AUTOSAR 4.2.2 / 4.3.1 / 4.4.0"
    )

    console.print(
        "Supports CAN / CAN FD / FlexRay / Ethernet"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()