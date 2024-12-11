#!/usr/bin/python3
"""API interface unit tests"""
import unittest
import inspect
import pycodestyle
from flask import json
import api.app
import api.core
import api.core.views
import api.core.views.interface
import api


class Test_interface(unittest.TestCase):
    """Test cases for views in interface module"""
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test environment."""
        cls.client = api.app.app.test_client()
        cls.correct_fun_names = [name for name, _ in
                         inspect.getmembers(api.core.views.interface.CorrectList,
                                            inspect.ismethod)]
        cls.predict_fun_names = [name for name, _ in
                         inspect.getmembers(api.core.views.interface.PredictList,
                                            inspect.ismethod)]

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        self.assertGreater(len(api.core.views.interface.__doc__), 0) # Module documentation test
        self.assertGreater(len(api.core.views.interface.PredictList.__doc__), 0)
        self.assertGreater(len(api.core.views.interface.CorrectList.__doc__), 0)
        # Test documentation for the correct class methods
        for func in self.correct_fun_names:
            with self.subTest(func):
                self.assertGreater(len(func.__doc__), 0,
                                   "Missing documentation of {} method".
                                   format(func))
        # Test documentation for the predict class methods
        for func in self.predict_fun_names:
            with self.subTest(func):
                self.assertGreater(len(func.__doc__), 0,
                                   "Missing documentation of {} method".
                                   format(func))
                
    def test_pep8_complaince(self) -> None:
        """Check if module is complaint when you run pycodestyle on it"""
        style_checker = pycodestyle.StyleGuide()
        result = style_checker.check_files(['api/core/views/interface.py'])
        self.assertEqual(result.total_errors, 0, "PEP 8 violations found")

    def test_predict_list_get(self) -> None:
        """Test the GET /api/predict endpoint."""
        response = self.client.get('/api/predict')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('connection to prediction endpoint is successful', data['message'])
    
    def test_correct_list_get(self):
        """Test the GET /api/correct/<id> endpoint."""
        response = self.client.get('/api/correct/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('connection to correction endpoint is successful', data['message'])

if __name__ == '__main__':
    unittest.main()
