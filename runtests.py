import sys
import unittest
from tests import *


test_suite = [
    "tests"
]


def runtests(test_modules=None):
    # List of modules to test
    if (not test_modules):
        test_modules = test_suite

    # Construct and run test suite
    suite = unittest.TestSuite()

    for t in test_modules:
        try:
            mod = __import__(t, globals(), locals(), ["suite"])
            suitefn = getattr(mod, "suite")
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    test_modules = None

    if len(sys.argv) > 1:
        test_modules = [sys.argv[1]]

    runtests(test_modules)
