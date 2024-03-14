import sys
sys.path.append("..")
import unittest
import tempfile 
import shutil
from wrapper.wrapper import GitWrapper

github_url = sys.argv[1]


class TestGitWrapper(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.temp_dir)

    def test_list_commits_success(self):
        count = 0
        # Create an instance of GitWrapper
        git_wrapper = GitWrapper(github_url)

        # Use git CLI to retrieve the commit list
        result = git_wrapper.list_commits()

        for commits in result.values():
            for commit in commits:
                count += 1
                
        # Assert the result
        self.assertEqual(count, 854)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)