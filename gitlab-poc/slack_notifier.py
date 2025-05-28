import os
import requests

SLACK_URL = os.getenv("SLACK_WEBHOOK")

def notify_slack(mr, reviewers):
    message = f"🔔 *New MR* `{mr['title']}` needs review by: {', '.join(reviewers)}"
    payload = {"text": message}
    requests.post(SLACK_URL, json=payload)
