#!/usr/bin/env python3
"""Test utils module - contains unit tests for utility functions."""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),  # Simple dictionary
        ({"a": {"b": 2}}, ("a",), {"b": 2}),  # Nested dictionary
        ({"a": {"b": 2}}, ("a", "b"), 2),  # Full path
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test KeyError is raised with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_key)


class TestGetJson(unittest.TestCase):
    """Test class for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected result without HTTP calls."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result properly."""
        class TestClass:
            """Test class with memoized property."""

            def a_method(self):
                """Test method that returns value."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        test_instance = TestClass()
        with patch.object(test_instance, 'a_method') as mock_method:
            mock_method.return_value = 42

            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()