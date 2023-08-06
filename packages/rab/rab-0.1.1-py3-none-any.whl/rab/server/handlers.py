"""Handlers

This module contains functions for manipulating REST API requests and
responses.
"""
# External Libraries
from flask import request


def _get_request_json(flask_request=request):
    return flask_request.get_json(force=True, silent=True)
