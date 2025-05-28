# GitLab AI Merge Request Assistant

## Overview

This project demonstrates how to **extend GitLab** by automating the creation of feature branches and merge requests (MRs) using a FastAPI-based service.  
It also supports automatic reviewer assignment and can be further extended for notifications and more.

---

## Features

- **Create a new branch and merge request in GitLab via API**
- **Auto-assign reviewers** to the merge request (optional)
- **Webhook endpoint** for handling GitLab MR events (for future automation)
- **Easily extensible** for notifications (e.g., Slack) and other workflow automations

---

## Why is this needed?

- **Saves time:** No need to manually create branches and MRs in the GitLab UI.
- **Reduces errors:** Ensures consistent branch naming and MR creation.
- **Enables automation:** Can be triggered from other tools, scripts, or CI/CD pipelines.
- **Foundation for more:** Can be extended to auto-assign reviewers, send notifications, and more.

---

## How to Use

### 1. Clone the repository and install dependencies

```sh
git clone https://gitlab.com/your-namespace/your-repo.git
cd your-repo
pip install -r requirements.txt
```

### 2. Set up your `.env` file

Create a `.env` file in the project root with:

```
GITLAB_TOKEN=your_gitlab_token_with_api_scope
SLACK_WEBHOOK=your_slack_webhook_url   # Optional
```

### 3. Run the FastAPI app

```sh
uvicorn main:app --reload
```

### 4. Open Swagger UI

Go to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

### 5. Use the `/create-feature` endpoint

- Click "Try it out" on `/create-feature`
- Enter JSON like:

```json
{
  "project_id": 70153406,
  "source_branch": "main",
  "feature_branch": "feature/ai-review-assistant",
  "title": "Add my new feature",
  "description": "This MR adds a new feature.",
  "reviewers": ["your-gitlab-username"]  // Optional
}
```

- Click "Execute"
- A new branch and merge request will be created in your GitLab project, and reviewers will be assigned if provided.

---

## How it Works

1. **/create-feature** endpoint receives a POST request with branch/MR details.
2. The app uses the GitLab API to:
   - Create a new branch from the specified source branch.
   - Create a merge request from the new branch to the source branch.
   - Assign reviewers if provided.
3. The response includes the MR details and a link to view it in GitLab.

---

## AI-Powered Merge Request Features

- **Automatic AI Code Review:** Every MR with code changes receives an AI-generated code review comment.
- **AI Label Suggestions:** The AI suggests and assigns relevant labels based on the code diff.
- **AI Risk Analysis:** The AI analyzes the code diff for potential risks and posts a summary.
- **AI Unit Test Suggestions:** The AI suggests possible unit tests for the new code.

**Proof:**  
See the merge request discussion/comments and labels for AI-generated feedback after creating an MR with real code changes.

---

## Extending This POC

- Add Slack or email notifications for new MRs.
- Automate merging, labeling, or other GitLab actions.
- Integrate with CI/CD or chatbots.

---

## License

MIT

---

**This project proves that you can extend GitLab with custom automation using its API and webhooks!**

