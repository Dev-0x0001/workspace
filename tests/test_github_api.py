# Unit Tests for GitHub API Wrapper

import unittest
from github_api import GitHubClient
import httpretty

class TestGitHubClient(unittest.TestCase):
    def setUp(self):
        self.client = GitHubClient(token='test-token')
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()

    def test_create_repo_success(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api.github.com/user/repos',
            body='{"name": "test-repo", "full_name": "Dev-0x0001/test-repo", "html_url": "https://github.com/Dev-0x0001/test-repo"}',
            status=201
        )

        repo = self.client.create_repo('Dev-0x0001', 'test-repo')
        self.assertIsNotNone(repo)
        self.assertEqual(repo['name'], 'test-repo')

    def test_create_repo_failure(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api.github.com/user/repos',
            status=403
        )

        with self.assertRaises(Exception):
            self.client.create_repo('Dev-0x0001', 'test-repo')

    def test_create_pull_request_success(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api.github.com/repos/Dev-0x0001/test-repo/pulls',
            body='{"title": "Test PR", "html_url": "https://github.com/Dev-0x0001/test-repo/pull/1"}',
            status=201
        )

        pr = self.client.create_pull_request(
            'Dev-0x0001',
            'test-repo',
            'main',
            'feature-branch',
            'Test PR',
            'This is a test pull request.'
        )
        self.assertIsNotNone(pr)
        self.assertEqual(pr['title'], 'Test PR')

if __name__ == '__main__':
    unittest.main()