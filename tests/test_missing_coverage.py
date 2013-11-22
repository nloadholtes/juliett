import unittest

from missing_coverage import MissingCoverage
from nose.plugins import PluginTester
from nose.tools import assert_equals


TEST_PATH_1 = ["/path/to/the/project/first/a.py",
            "/path/to/the/project/second/b.py"]

class TestMissingCoverage:
    def setUp(self):
        self.mc = MissingCoverage()

    def test_findRoots(self):
        self.mc.locations = TEST_PATH_1
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals("/path/to/the/project/", results[0])

    def test_findRoots_nested(self):
        self.mc.locations = TEST_PATH_1 + ["/path/to/the/project/first/nested/c.py"]
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals("/path/to/the/project/", results[0])

    def test_findRoots_higher_root(self):
        self.mc.locations = TEST_PATH_1 + ["/path/to/another/project/first/d.py"]
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals(["/path/to/"] , results)

if __name__ == '__main__':
    unittest.main()