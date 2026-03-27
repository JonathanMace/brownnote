"""Command-line interface for browntone."""

from __future__ import annotations

import click


@click.group()
@click.version_option()
def main() -> None:
    """Browntone: infrasound-induced abdominal resonance analysis."""


@main.command()
def info() -> None:
    """Print project information."""
    from browntone import __version__

    click.echo(f"browntone v{__version__}")
    click.echo("Computational investigation of infrasound-induced abdominal resonance")


if __name__ == "__main__":
    main()
