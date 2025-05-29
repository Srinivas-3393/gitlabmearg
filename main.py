import logging
from dotenv import load_dotenv
import os
import subprocess
import gitlab
from fastapi import FastAPI, HTTPException
from gitlab_api import create_feature_branch_and_mr
from github_api import create_pull_request  # <-- Import the function

load_dotenv()  # Loads the .env file

github_token = os.getenv("GITHUB_TOKEN")
gitlab_token = os.getenv("GITLAB_TOKEN")
from fastapi import FastAPI, HTTPException
from gitlab_api import create_feature_branch_and_mr
from github_api import create_pull_request  # <-- Import the function

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/create-feature")
async def create_feature(data: dict):
    required_fields = [
        "project_id", "source_branch", "feature_branch", "title", "description"
    ]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")

    result = create_feature_branch_and_mr(
        project_id=data["project_id"],
        source_branch=data["source_branch"],
        feature_branch=data["feature_branch"],
        title=data["title"],
        description=data["description"],
        reviewers=data.get("reviewers")
    )
    return result

@app.get("/dummy")
def dummy_endpoint():
    return {"message": "This is a dummy endpoint for testing."}

@app.post("/create-github-pr")
async def create_github_pr(data: dict):
    required_fields = [
        "repo_name", "base_branch", "head_branch", "title", "body"
    ]
    for field in required_fields:
        if field not in data:
    
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")

    result = create_pull_request(
        repo_name=data["repo_name"],
        base_branch=data["base_branch"],
        head_branch=data["head_branch"],
        title=data["title"],
        body=data["body"]
    )
    return result

@app.post("/merge-github-to-gitlab")
async def merge_github_to_gitlab(
    github_repo: str,
    github_branch: str,
    gitlab_repo_url: str,
    gitlab_project_id: str,
    gitlab_target_branch: str = "main",
    mr_title: str = "Automated MR: GitHub branch to GitLab",
    mr_description: str = "This MR was created automatically by FastAPI."
):
    # Step 1: Fetch GitHub branch and push to GitLab
    try:
        # Add GitHub remote if not exists
        subprocess.run(["git", "remote", "add", "github", f"https://github.com/{github_repo}.git"], check=False)
        # Add GitLab remote if not exists
        subprocess.run(["git", "remote", "add", "gitlab", gitlab_repo_url], check=False)
        # Fetch the branch from GitHub
        subprocess.run(["git", "fetch", "github", github_branch], check=True)
        # Push the branch to GitLab
        subprocess.run(["git", "push", "gitlab", f"refs/remotes/github/{github_branch}:{github_branch}"], check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Git operation failed: {e}")

    # Step 2: Create Merge Request in GitLab
    try:
        GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
        gl = gitlab.Gitlab("https://gitlab.com", private_token=GITLAB_TOKEN)
        project = gl.projects.get(gitlab_project_id)
        mr = project.mergerequests.create({
            'source_branch': github_branch,
            'target_branch': gitlab_target_branch,
            'title': mr_title,
            'description': mr_description
        })
        return {"message": "Merge Request created", "mr_url": mr.web_url}
    except Exception as e:
        logging.exception("GitLab MR creation failed")
        raise HTTPException(status_code=500, detail=f"GitLab MR creation failed: {str(e)}")