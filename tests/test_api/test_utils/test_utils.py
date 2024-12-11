#!/usr/bin/python3
"""Test Utility Module"""
import unittest
import inspect
import pycodestyle
import api.core
import api.core.utils
from api.core.utils.utils import interpret_prediction
import api
import api.core.utils.utils

class TestUtilityModule(unittest.TestCase):

    def setUp(self):
        # Mocked input data
        self.fun_names = [name for name, _ in
                         inspect.getmembers(api.core.utils.utils,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(api.core.utils.utils.__doc__), 0) # Module documentation test

        for func in self.fun_names:
            with self.subTest(func):
                self.assertGreater(len(func.__doc__), 0,
                                   "Missing documentation of {} method".
                                   format(func))

    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['api/core/utils/utils.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")

    def test_interpret_prediction(self):
        # Test for valid predictions
        self.assertEqual(interpret_prediction(0), "Bug")
        self.assertEqual(interpret_prediction(1), "Enhancement")
        self.assertEqual(interpret_prediction(2), "Question")

        # Test for invalid prediction
        with self.assertRaises(AssertionError):
            self.assertEqual(interpret_prediction(3), "Unknown")


if __name__ == '__main__':
    unittest.main()
