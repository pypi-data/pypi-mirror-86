"""Command Line Interface

This module defines top-level command line interface (CLI) commands.  It also
gathers and registers CLI commands of submodules within the package.
"""
# Standard Libraries
import sys
import logging

# External Libraries
import click

# Internal Libraries
from .utils import cli_args
from .utils.process import ShellCommandException
from .utils.logging_utils import eprint
from .server import _run_server


_logger = logging.getLogger(__name__)


CONTEXT_SETTINGS = dict(
    help_option_names=["--help"], max_content_width=80, auto_envvar_prefix="RAB"
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    pass


@cli.command()
@cli_args.HOST
@cli_args.PORT
@cli_args.WORKERS
@click.option(
    "--gunicorn-opts",
    default=None,
    help="Additional command line options forwarded to gunicorn processes.",
)
def server(host, port, workers, gunicorn_opts):
    """Run the REST API Server.

    The server listens on http://localhost:5000 by default, and only accepts
    connections from the local machine. To accept connections from other
    machines, you'll need to pass `--host 0.0.0.0` to listen on all network
    interfaces or provide a specific interface address.
    """
    try:
        _run_server(gunicorn_opts=gunicorn_opts, host=host, port=port, workers=workers)
    except ShellCommandException:
        eprint("Running the server failed. Please see the logs above for details.")
        sys.exit(1)


@cli.command(help="Initialize Database.")
@click.option(
    "--uri",
    required=True,
    default=None,
    help="SQLAlchemy uri connection string",
)
def database(uri):
    """Initialize Database."""
    click.echo("database")
