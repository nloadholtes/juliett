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
import pickle

log = logging.getLogger(__name__)


class MissingCoverage(Plugin):
    name = "missing_coverage"

    def readCoverageData(self, location=None):
        if not location:
            location = "./"
        with open(location + ".coverage", "rb") as f:
            rawdata = pickle.load(f)
            self.locations = rawdata["lines"].keys()

    def scanForAllModules(self, location):
        pass

    def findRoots(self, locs=None):
        roots = []
        #magic!
        #get the first path
        if locs is None:
            locs = list(self.locations)

        def _condense(locs):
            #get the next path
            results = []
            first = locs.pop(0)
            for x in range(0, len(locs)):
                second = locs.pop(0)
                first_l = first.split("/")[:-1]
                second_l = second.split("/")[:-1]
                print("f: %s ---- s: %s " % (first, second))
                for y in xrange(1, len(first_l)):
                    if first_l[y] != second_l[y]:
                        if y == 1:
                            results.append("/".join(first_l))
                            results.append("/".join(second_l))
                        else:
                            results.append("/".join(first_l[0:y]))
                        break
                first = second
            return results
        roots = list(set(_condense(locs)))
        return roots

    def main(self):
        self.readCoverageData()
        #Find roots

        self.scanForAllModules()
