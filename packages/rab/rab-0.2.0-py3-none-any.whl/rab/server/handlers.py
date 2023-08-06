"""Handlers

This module contains functions for manipulating REST API requests and
responses.
"""
# External Libraries
from flask import request
from flask import make_response

# Internal Libraries
from ..utils.constants import STATUS_MAP


def _get_request_json(flask_request=request):
    return flask_request.get_json(force=True, silent=True)


def return_error(code: int, detail: str) -> tuple:
    response = make_response({
        'detail': detail,
        'status': code,
        'title': STATUS_MAP[code],
    })
    response = {
        'body': {
            'detail': detail,
            'status': code,
            'title': STATUS_MAP[code],
        },
        'status': code,
        'headers': {"WWW-Authenticate": "Basic"} if code == 401 else [],
    }

    # return make_response()
    return tuple(v for k, v in response.items() if v)
