import sys
sys.path.append("..")
import unittest
from app.api import app

github_url = sys.argv[1]

class TestAPI(unittest.TestCase):

    def test_list_commits_success(self):
        # Arrange: Set up the Flask test client
        test_client = app.test_client()
        
        # Act: Make a request to the list-commits endpoint
        response = test_client.get('/list-commits', query_string={'url': github_url})

        
        # Assert: Check the response and status code
        self.assertEqual(response.status_code, 200)
        self.assertIn('commits', response.json)

    def test_list_commits_failure_500(self):
        # Arrange: Set up the Flask test client with a failing GitWrapper
        test_client = app.test_client()

        # Act: Make a request to the list-commits endpoint
        response = test_client.get(f'/list-commits', query_string={'url': github_url})

        # Assert: Check the response and status code
        self.assertEqual(response.status_code, 500)

    def test_list_commits_failure_404(self):
        # Arrange: Set up the Flask test client with a failing GitWrapper
        test_client = app.test_client()

        # Act: Make a request to the list-commits endpoint
        response = test_client.get(f'/list-commits', query_string={'url': github_url})

        # Assert: Check the response and status code
        self.assertEqual(response.status_code, 404)

    def test_list_commits_failure_400(self):
        # Arrange: Set up the Flask test client with a failing GitWrapper
        test_client = app.test_client()

        # Act: Make a request to the list-commits endpoint
        response = test_client.get(f'/list-commits', query_string={'url': github_url})

        # Assert: Check the response and status code
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)