from ai_engine import suggest_reviewers
from gitlab_api import assign_reviewers
from slack_notifier import notify_slack

async def handle_merge_request(payload):
    mr = payload["object_attributes"]
    if mr["action"] == "open":
        project_id = mr["target_project_id"]
        mr_iid = mr["iid"]
        title = mr["title"]
        description = mr["description"]
        changes = [f["new_path"] for f in payload.get("changes", {}).get("files", [])]

        reviewers = suggest_reviewers(title, description, changes)
        assign_reviewers(project_id, mr_iid, reviewers)
        notify_slack(mr, reviewers)
