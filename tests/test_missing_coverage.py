import unittest

from missing_coverage import MissingCoverage
from nose.plugins import PluginTester
from nose.tools import assert_equals
from mock import patch


TEST_PATH_1 = ["/path/to/the/project/first/a.py",
            "/path/to/the/project/second/b.py"]


class TestMissingCoverage:
    def setUp(self):
        self.mc = MissingCoverage()

    def test_findRoots(self):
        self.mc.locations = TEST_PATH_1
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals("/path/to/the/project", results[0])

    def test_findRoots_none(self):
        self.mc.locations = []
        results = self.mc.findRoots()
        assert_equals([], results)

    def test_findRoots_nested(self):
        self.mc.locations = TEST_PATH_1 + ["/path/to/the/project/first/nested/c.py"]
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals("/path/to/the/project", results[0])

    def test_findRoots_higher_root(self):
        self.mc.locations = TEST_PATH_1 + ["/path/to/another/project/first/d.py"]
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals(["/path/to"], results)

    def test_findRoots_wildy_different(self):
        self.mc.locations = ["/a/b/c/e.py", "/path/to/another/project/first/d.py"]
        results = self.mc.findRoots()
        assert_equals(2, len(results))
        assert_equals(["/path/to/another/project/first", "/a/b/c"], results)

    def test_findRoots_one_root(self):
        self.mc.locations = ["/path/to/another/project/first/d.py"]
        results = self.mc.findRoots()
        assert_equals(1, len(results))
        assert_equals(["/path/to/another/project/first"], results)

    @patch("missing_coverage.plugin.os.walk")
    def test_scanForAllModules_one_root(self, mock_os):
        self.mc.locations = ["/path/to/another/project/first/d.py"]
        roots = ["/path/to/another/project/first"]
        mock_os.return_value = [("/path/to/another/project/first/", [],
            ["d.py", "a.py", "b.py"])]
        output = self.mc.scanForAllModules(roots)
        assert_equals(['/path/to/another/project/first/d.py',
            "/path/to/another/project/first/a.py",
            "/path/to/another/project/first/b.py"],
            output)

    @patch("missing_coverage.plugin.os.walk")
    def test_scanForAllModules_two_root(self, mock_os):
        self.mc.locations = ["/path/to/another/project/first/d.py",
            "/path/to/the/project/second/nested/c.py"]
        roots = ["/path/to/another/project/first"]
        mock_os.return_value = [("/path/to/another/project/first/", [],
            ["d.py", "a.py", "b.py"]),
            ("/path/to/another/project/second/", [], ["e.py", "f.py", "g.py"])]
        output = self.mc.scanForAllModules(roots)
        assert_equals(['/path/to/another/project/first/d.py',
            "/path/to/another/project/first/a.py",
            "/path/to/another/project/first/b.py",
            "/path/to/another/project/second/e.py",
            "/path/to/another/project/second/f.py",
            "/path/to/another/project/second/g.py"],
            output)

    @patch("missing_coverage.plugin.os.walk")
    def test_scanForAllModules_one_root_subdir(self, mock_os):
        self.mc.locations = ["/path/to/another/project/first/d.py",
            "/path/to/the/project/second/nested/c.py"]
        roots = ["/path/to/another/project/first"]
        mock_os.return_value = [("/path/to/another/project/first/", ["lib"],
            ["d.py", "a.py", "b.py"]),
            ("/path/to/another/project/first/lib", [], ["e.py", "f.py", "g.py"])]
        output = self.mc.scanForAllModules(roots)
        assert_equals(['/path/to/another/project/first/d.py',
            "/path/to/another/project/first/a.py",
            "/path/to/another/project/first/b.py",
            "/path/to/another/project/first/lib/e.py",
            "/path/to/another/project/first/lib/f.py",
            "/path/to/another/project/first/lib/g.py"],
            output)

if __name__ == '__main__':
    unittest.main()
