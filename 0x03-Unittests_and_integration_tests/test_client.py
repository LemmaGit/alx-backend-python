#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Setup test payload
        test_payload = {"name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = test_payload

        # Create client instance
        client = GithubOrgClient(org_name)
        
        # Call the org property (should use get_json)
        result = client.org

        # Verify get_json was called exactly once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

        # Verify memoization - second call should not call get_json again
        result2 = client.org
        self.assertEqual(mock_get_json.call_count, 1)
        self.assertEqual(result2, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value"""
        # Setup test payload
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org', 
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            # Create client instance
            client = GithubOrgClient("google")

            # Access the property
            result = client._public_repos_url

            # Verify the org property was accessed
            mock_org.assert_called_once()

            # Verify the result matches expected URL
            self.assertEqual(result, test_payload["repos_url"])

def test_public_repos(self):
    """Test that public_repos returns correct list of repos"""
    # Setup test data
    test_payload = [
        {"name": "repo1", "license": {"key": "mit"}},
        {"name": "repo2", "license": {"key": "apache-2.0"}},
        {"name": "repo3", "license": None}
    ]
    test_url = "https://api.github.com/orgs/google/repos"

    # Mock get_json to return our test payload
    with patch('client.get_json', return_value=test_payload) as mock_get_json:
        # Mock _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url',
                 new_callable=PropertyMock,
                 return_value=test_url) as mock_public_repos_url:

            # Create client instance
            client = GithubOrgClient("google")

            # Call the method
            repos = client.public_repos()

            # Verify the property was accessed
            mock_public_repos_url.assert_called_once()

            # Verify get_json was called with correct URL
            mock_get_json.assert_called_once_with(test_url)

            # Verify the result matches expected repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
