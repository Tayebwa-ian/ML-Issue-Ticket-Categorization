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
        cls.issue1 = {
            "title": "Contrast for Select files to upload button is too low",
            "body": "The contrast ratio for the Select files to upload \
                is on 2.69 and does not meet the minimum for WCAG AA.",
            "author": "MEMBER",
        }

        cls.issue2 = {
            "title": "Circular imports",
            "body": """Importing modules in multiple files will create circular dependencies, \
                in turn causing an infinite loop. 

            foo.sb:
            `import "bar"`

            foo:
            `import "foo"`

            ## Possible solution

            Modules could be analyzed beforehand to remove duplicate imports.""",
            "author": "COLLABORATOR",
        }
        cls.res1 = cls.client.post('/api/core/predict', json=cls.issue1)
        cls.res2 = cls.client.post('/api/core/predict', json=cls.issue2)

    def test_documentation(self) -> None:
        """Test if module, class and methods documentations exist"""
        # Module documentation test
        self.assertGreater(len(api.core.views.interface.__doc__), 0)
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
        """Test the GET /api/core/predict endpoint."""
        response = self.client.get('/api/core/predict')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    def test_correct_list_get(self):
        """Test the GET /api/core/issues/<id> endpoint."""
        response = self.client.get('/api/core/issues/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('author'), 'MEMBER')
        # Check if the prediction id not none
        self.assertTrue(data.get('prediction'))

    def test_correct_list_put(self):
        "Test the PUT /api/core/issues/<id> endpoint."
        self.issue1['actual_label'] = 'Enhancement'
        self.issue2['actual_label'] = 'Bug'
        resp1 = self.client.put(
            '/api/core/issues/1',
            json=self.issue1
        )
        resp2 = self.client.put(
            '/api/core/issues/2',
            json=self.issue2
        )
        data = json.loads(resp1.data)
        data2 = json.loads(resp2.data)
        self.assertEqual(data.get('actual_label'), 'Enhancement')
        self.assertEqual(data2.get('actual_label'), 'Bug')

if __name__ == '__main__':
    unittest.main()
