import unittest

from missing_coverage import MissingCoverage
from nose.plugins import PluginTester
from nose.tools import assert_equals


class TestMissingCoverage(PluginTester, unittest.TestCase):
    plugins = [MissingCoverage()]

    def test_findRoots(self):
        assert_equals(1, 2)
