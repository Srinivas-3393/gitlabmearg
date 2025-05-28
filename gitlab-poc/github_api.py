from github import Github
import os

def create_pull_request(repo_name, base_branch, head_branch, title, body):
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.create_pull(
        title=title,
        body=body,
        head=head_branch,
        base=base_branch
    )
    return {"pr_url": pr.html_url}