#!/usr/bin/env python3
"""Test utils module
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""
    
    @parameterized.expand([
        # First test case: simple dictionary
        ({"a": 1}, ("a",), 1),
        # Second test case: nested dictionary, first level
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        # Third test case: nested dictionary, full path
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # New test cases for exception handling
    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised with correct message"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        # Verify the exception message contains the expected key
        self.assertEqual(str(context.exception), expected_key)


class TestGetJson(unittest.TestCase):
    """Test class for get_json function"""
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns the expected result without making actual HTTP calls"""
        
        # Configure the mock to return a response with the test payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_json(test_url)
        
        # Assert that requests.get was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)
        
        # Assert that the output equals test_payload
        self.assertEqual(result, test_payload)