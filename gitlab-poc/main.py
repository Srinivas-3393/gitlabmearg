from dotenv import load_dotenv
import os

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