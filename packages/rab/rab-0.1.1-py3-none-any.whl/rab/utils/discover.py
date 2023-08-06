"""Discover

This module contains logic for resource discovery.
"""
# Standard Libraries
import pkgutil
import importlib

# Internal Libraries
import rab


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


try:
    importlib.import_module('rab.plugins')
except ModuleNotFoundError as error:
    pass

apis = (
    {
        name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(rab.plugins)
    }
    if hasattr(rab, "plugins")
    else {}
)
