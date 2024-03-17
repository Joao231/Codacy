#!/usr/bin/env python3
import argparse
import subprocess
import os
import tempfile


class GitWrapper:
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def list_commits(self):
 
        try:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Clone the repository to the temporary directory
            subprocess.run(["git", "clone", "--quiet", self.repo_url, temp_dir], check=True)

            # Change directory to the temporary repository
            os.chdir(temp_dir)

            # Get list of all branches
            git_branch_output = subprocess.check_output(["git", "branch", "--list", "--all"]).decode("utf-8").split("\n")
            # Retrieve commits for each branch
            commit_info = {}
    
            for branch in git_branch_output:
                if branch.strip() == "" or 'remotes/origin/HEAD -> origin/master' in branch or 'remotes/origin/master' in branch:
                    continue
                branch_name = branch.strip().replace("*", "").strip()
                subprocess.run(["git", "checkout", "--quiet", branch_name], check=True)
                commit_info[branch_name] = []
                git_log_output = subprocess.check_output(["git", "log", "--pretty=format:%H|%an|%ae|%cn|%ce|%ad|%cd|%s"])
                git_log_output = git_log_output.decode("utf-8").split("\n")
                for line in git_log_output:
                    if line.strip() == "":
                        continue
                    commit_hexsha, author_name, author_email, committer_name, committer_email, authored_date, committed_date, message = line.split("|", 7)
                    commit_info[branch_name].append({
                        'commit_hexsha': commit_hexsha,
                        'author_name': author_name,
                        'author_email': author_email,
                        'committer_name': committer_name,
                        'committer_email': committer_email,
                        'authored_date': authored_date,
                        'committed_date': committed_date,
                        'message': message
                    })


        except subprocess.CalledProcessError as e:
            # Handle 404 Not Found error
            if e.returncode == 128:
                return None, 404
            # Handle other errors
            return None, 500

        return commit_info
        
        

def main():
    parser = argparse.ArgumentParser(description='List commits from a GitHub repository.')
    parser.add_argument('--list-commits', metavar='URL', type=str, help='GitHub repository URL', required=True)
    args = parser.parse_args()

    github_url = args.list_commits
    git_wrapper = GitWrapper(github_url)
    commits_info = git_wrapper.list_commits()

    
    if isinstance(commits_info, tuple):
        print("Commits:", commits_info)
    else:
         # Print commit information for each branch
        for branch, commits in commits_info.items():
            print("=" * 50)
            print("Branch:", branch)
            print("=" * 50)
            for commit in commits:
                print("Commit Hexsha:", commit['commit_hexsha'])
                print("Author:", commit['author_name'], "<{}>".format(commit['author_email']))
                print("Committer:", commit['committer_name'], "<{}>".format(commit['committer_email']))
                print("Authored Date:", commit['authored_date'])
                print("Committed Date:", commit['committed_date'])
                print("Message:", commit['message'])
                print("-" * 50)
    

if __name__ == "__main__":
    main()