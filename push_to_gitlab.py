import subprocess

github_branch = "main"  # Replace with your actual branch name if different

subprocess.run([
    "git", "push", "gitlab", f"refs/remotes/github/{github_branch}:{github_branch}"
], check=True)
