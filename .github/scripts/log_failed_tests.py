import os
import re
import requests

GITHUB_REPO = "HansVRP/pytest-github-actions"
GITHUB_TOKEN = os.getenv("ISSUE_TOKEN")
ISSUE_LABEL = "test-failure"

def get_existing_issues():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    issues = response.json()
    return {issue["title"] for issue in issues}

def create_issue(test_name, error_msg, file_name):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": f" Test Failure: {test_name}",
        "body": f" Error Message: `{error_msg}`\n File: `{file_name}`",
        "labels": [ISSUE_LABEL],
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def parse_failed_tests():
    with open("pytest_output.txt", "r") as f:
        log_data = f.read()

    failed_tests = re.findall(r"(tests/.*?):(\d+) in (\w+)", log_data)

    return [(match[2], match[0]) for match in failed_tests]

if __name__ == "__main__":
    existing_issues = get_existing_issues()
    failed_tests = parse_failed_tests()

    for test_name, file_name in failed_tests:
        if f" Test Failure: {test_name}" not in existing_issues:
            create_issue(test_name, "Test failed", file_name)