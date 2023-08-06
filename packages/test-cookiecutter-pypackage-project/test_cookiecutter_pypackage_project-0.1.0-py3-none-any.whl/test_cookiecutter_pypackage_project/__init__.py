"""test-cookiecutter-pypackage-project namespace."""

from importlib_metadata import PackageNotFoundError, version

__author__ = """Marco Gancitano"""
__email__ = "marco.gancitano@example.com"

# Used to automatically set version number from github actions
# as well as not break when being tested locally
try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "0.0.0"
