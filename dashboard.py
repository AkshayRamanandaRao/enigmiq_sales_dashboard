"""Update the repository README from prospect issues; uses only the standard library."""

import base64
from datetime import datetime
import json
import os
import re
import textwrap
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


STAGES = ("research", "contacted", "replied", "meeting", "proposal", "won", "lost")
START = "<!-- DASHBOARD_START -->"
END = "<!-- DASHBOARD_END -->"


def api(path, data=None):
    request = Request(
        "https://api.github.com/repos/" + os.environ["GITHUB_REPOSITORY"] + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="PUT" if data is not None else "GET",
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def prospect_issues():
    page = 1
    while True:
        batch = api(f"/issues?state=all&per_page=100&page={page}")
        for issue in batch:
            if "pull_request" not in issue and re.match(r"^\[(?:" + "|".join(STAGES) + r")\] ", issue["title"], re.I):
                yield issue
        if len(batch) < 100:
            break
        page += 1


def safe_cell(value):
    value = re.sub(r"\s+", " ", value).replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
    return textwrap.shorten(value, width=120, placeholder="…")


def render(readme, issues, today):
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) >= readme.index(END):
        raise ValueError("README dashboard markers missing or duplicated")
    counts = {stage: 0 for stage in STAGES}
    actions = []
    for issue in issues:
        match = re.match(r"^\[([a-z]+)\] ", issue["title"], re.I)
        if not match or match.group(1).lower() not in counts:
            continue
        stage = match.group(1).lower()
        counts[stage] += 1
        if stage not in ("won", "lost"):
            next_action = re.search(r"^Next action:\s*(.+)$", issue.get("body") or "", re.M | re.I)
            if next_action:
                actions.append((issue["html_url"], safe_cell(issue["title"]), safe_cell(next_action.group(1))))
    old = readme.split(START, 1)[1].split(END, 1)[0]
    history = [line for line in old.splitlines() if re.match(r"^\| \d{4}-\d\d-\d\d \|", line) and not line.startswith("| " + today + " |")]
    row = "| " + today + " | " + " | ".join(str(counts[s]) for s in STAGES) + " |"
    history = ([row] + history)[:30]
    header = "| " + " | ".join(s.title() for s in STAGES) + " |"
    divider = "| " + " | ".join("---:" for _ in STAGES) + " |"
    action_lines = [f"- [{title}]({url}) — {next_action}" for url, title, next_action in actions[:10]] or ["No next actions recorded."]
    block = "\n".join([
        f"## Pipeline · updated {today} (Europe/Zagreb)", "", header, divider,
        "| " + " | ".join(str(counts[s]) for s in STAGES) + " |", "",
        "### Next actions", "", *action_lines, "", "### Daily history (Europe/Zagreb)", "",
        "| Date | " + " | ".join(s.title() for s in STAGES) + " |", "| --- | " + " | ".join("---:" for _ in STAGES) + " |",
        *history, "",
    ])
    return readme.split(START, 1)[0] + START + "\n" + block + END + readme.split(END, 1)[1]


def main():
    remote = api("/contents/README.md")
    current = base64.b64decode(remote["content"]).decode("utf-8")
    today = datetime.now(ZoneInfo("Europe/Zagreb")).date().isoformat()
    updated = render(current, list(prospect_issues()), today)
    if updated != current:
        api("/contents/README.md", {
            "message": "Update sales dashboard for " + today,
            "content": base64.b64encode(updated.encode()).decode(),
            "sha": remote["sha"],
        })


if __name__ == "__main__":
    main()

