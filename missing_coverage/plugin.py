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
import os

log = logging.getLogger(__name__)


class MissingCoverage(Plugin):
    name = "missing_coverage"

    def readCoverageData(self, location=None):
        if not location:
            location = "./"
        with open(location + ".coverage", "rb") as f:
            rawdata = pickle.load(f)
            self.locations = rawdata["lines"].keys()

    def addModulesToCoverage(self, modules, location=None):
        if not location:
            location = "./"
        with open(location + ".coverage", "r+b") as f:
            rawdata = pickle.load(f)
            rawdata["lines"] = modules
            pickle.dump(rawdata, f, 2)
            
    def scanForAllModules(self, locations):
        output = []
        for location in locations:
            for (path, dirs, files) in os.walk(location):
                for f in files:
                    if ".py" == os.path.splitext(f)[1]:
                        output.append(os.path.join(path, f))
        return output

    def findRoots(self, locs=None):
        roots = []
        if locs is None:
            locs = list(self.locations)
            if len(locs) == 0:
                return roots

        def _condense(locs):
            results = []
            first = locs.pop(0)
            first_l = first.split("/")
            if first.endswith(".py"):
                first_l = first_l[:-1]
            if len(locs) == 0:
                results.append("/".join(first_l))
            for x in range(0, len(locs)):
                second = locs.pop(0)
                second_l = second.split("/")
                if second.endswith(".py"):
                    second_l = second_l[:-1]
                print("f: %s ---- s: %s " % (first, second))
                if len(first_l) > len(second_l):
                    shorter = second_l
                else:
                    shorter = first_l
                for y in xrange(1, len(shorter)):
                    if first_l[y] != second_l[y]:
                        if y == 1:
                            results.append("/".join(first_l))
                            results.append("/".join(second_l))
                        else:
                            results.append("/".join(first_l[0:y]))
                        break
                if len(results) == 0:
                    results.append("/".join(shorter))
                first = second
            return results
        roots = list(set(_condense(locs)))
        if len(roots) > 1:
            roots = list(set(_condense(roots)))
        return roots

    def main(self):
        self.readCoverageData()
        #Find roots
        roots = self.findRoots()

        self.scanForAllModules(roots)
