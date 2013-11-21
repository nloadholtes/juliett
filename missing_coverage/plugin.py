"""
missing_coverage - Looks for the modules that were completely missed
by the tests. It then adds them to the .coverage file. The reports
then show the spots that are missing coverage. Then the developers
weep as they add new tests.

"""
__test__ = False
__author__ = "Nick Loadholtes"

import logging
from nose.plugins import Plugin
from nose import loader
from inspect import isfunction, ismethod
from nose.case import FunctionTestCase, MethodTestCase
from nose.failure import Failure
from nose.util import isclass, isgenerator, transplant_func, transplant_class
import random
import unittest

log = logging.getLogger(__name__)

class MissingCoverage(Plugin):
    pass