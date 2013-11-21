"""
missing_coverage - Adds modules that are missing test coverage to the .coverage 
file so that they can be included in any reports.
"""
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='missing_coverage',
    version='1.0',
)
