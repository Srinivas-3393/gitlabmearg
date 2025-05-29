# Minor change for AI MR demo: Added a harmless comment to trigger AI features.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
BASE_URL = "https://gitlab.com/api/v4"

def create_feature_branch_and_mr(project_id, source_branch, feature_branch, title, description, reviewers=None):
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}

    # 1. Create a new branch (ignore error if branch exists)
    branch_url = f"{BASE_URL}/projects/{project_id}/repository/branches"
    branch_data = {"branch": feature_branch, "ref": source_branch}
    branch_resp = requests.post(branch_url, headers=headers, data=branch_data)
    # If branch exists, GitLab returns 400, which is fine for our use case

    # 2. Create a merge request
    mr_url = f"{BASE_URL}/projects/{project_id}/merge_requests"
    mr_data = {
        "source_branch": feature_branch,
        "target_branch": source_branch,
        "title": title,
        "description": description
    }
    mr_resp = requests.post(mr_url, headers=headers, data=mr_data)
    if mr_resp.status_code != 201:
        return {"error": "Failed to create MR", "details": mr_resp.text}

    mr_info = mr_resp.json()
    mr_iid = mr_info["iid"]

    # 3. Get MR diff
    diff_url = f"{BASE_URL}/projects/{project_id}/merge_requests/{mr_iid}/changes"
    diff_resp = requests.get(diff_url, headers=headers)
    diff_text = ""
    if diff_resp.status_code == 200:
        diff_text = str(diff_resp.json())

    # 4. AI features (dummy for now)
    feedback = ai_code_review(diff_text)
    post_mr_comment(project_id, mr_iid, f"**AI Code Review:**\n{feedback}")

    return {"mr_url": mr_info["web_url"]}

def ai_code_review(diff_text):
    # Dummy implementation
    return "AI review: No issues found."

def post_mr_comment(project_id, mr_iid, comment):
    url = f"{BASE_URL}/projects/{project_id}/merge_requests/{mr_iid}/notes"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    requests.post(url, headers=headers, data={"body": comment})

