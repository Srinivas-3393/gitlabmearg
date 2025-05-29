from github import Github
import os

# Load your GitHub token from env or directly
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Or put your token here as string
REPO_NAME = "srinivas-3393/gitlabmerge"       # Change to your GitHub repo full name
BRANCH_NAME = "master"             # Branch with your changes
BASE_BRANCH = "main"                       # Branch you want to merge into

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Create Pull Request
pr = repo.create_pull(
    title="Automated PR: Feature Update",
    body="This PR was created automatically by script.",
    head=BRANCH_NAME,
    base=BASE_BRANCH
)

print(f"PR created: {pr.html_url}")
