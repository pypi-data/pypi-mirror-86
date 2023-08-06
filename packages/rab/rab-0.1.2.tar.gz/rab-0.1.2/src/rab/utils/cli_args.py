"""CLI Arguments

This module contains definitions of click options shared by several CLI commands.
"""
# External Libraries
import click


HOST = click.option(
    "--host",
    "-h",
    metavar="HOST",
    default="127.0.0.1",
    help="The network address to listen on (default: 127.0.0.1). "
    "Use 0.0.0.0 to bind to all addresses if you need to access "
    "the server from other machines.",
)

PORT = click.option(
    "--port", "-p", default=5000, help="The port to listen on (default: 5000)."
)

WORKERS = click.option(
    "--workers",
    "-w",
    type=click.INT,
    default=None,
    help="Number of gunicorn worker processes to handle requests (default: 4).",
)
