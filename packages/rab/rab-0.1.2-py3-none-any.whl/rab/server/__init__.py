"""REST API SERVER

This module defines the REST API server routes, functions for configuring the
server, and functions for running the server.
"""
# Standard Libraries
import shlex
import logging
import os

# External Libraries
import connexion
from flask_cors import CORS

# Internal Libraries
from ..utils.process import exec_cmd
from ..utils.discover import apis


_logger = logging.getLogger(__name__)


def _build_gunicorn_command(gunicorn_opts, host, port, workers):
    """Builds Gunicorn Command

    Args:
        gunicorn_opts (str): gunicorn options
        host (str): network interface to listen on
        port (int): port number
        workers (int): number of worker processes to spawn

    Returns:
        parsed and lexed gunicorn command
    """
    bind_address = f"{host}:{port}"
    opts = shlex.split(gunicorn_opts) if gunicorn_opts else []
    return (
        ["gunicorn"]
        + opts
        + ["-b", bind_address, "-w", f"{workers}", f"{__package__}:app"]
    )


def _run_server(gunicorn_opts, host, port, workers):
    """Start Server

    Args:
        gunicorn_opts (str): gunicorn options
        host (str): network interface to listen on
        port (int): port number
        workers (int): number of worker processes to spawn

    Returns:
        None
    """
    # add environment variables to `_run_server` function and add them to
    # subprocess here.
    env_map = {}
    full_command = _build_gunicorn_command(gunicorn_opts, host, port, workers or 4)
    _logger.critical(full_command)
    exec_cmd(
        full_command,
        env=env_map,
        stream_output=True,
    )


# WSGI Application
app = connexion.App(
    __name__,
    options={
        "openapi_url": "/",
        "swagger_ui": True,
    },
)

# Empty Default Blueprint
app.add_api("api.yaml")
CORS(app.app)

# Business Logic Blueprints
for name, module in apis.items():
    path = os.path.join(module.__path__[0], "api.yaml")
    app.add_api(path, base_path=module.BASE_PATH)
