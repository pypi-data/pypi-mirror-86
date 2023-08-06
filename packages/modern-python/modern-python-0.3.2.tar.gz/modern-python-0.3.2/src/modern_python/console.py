"""Command-line interface."""

import textwrap

import click

from . import __version__
from . import wikipedia


@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Lanuage edition of wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """现代化python工程."""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
