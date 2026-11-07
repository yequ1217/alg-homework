#!/usr/bin/env python3
"""抓取 ccc115a/_alg 的週次習題 issues，每份存成一個 HW 資料夾。"""

import json
import os
import re
import sys
import urllib.request

REPO = "ccc115a/_alg"
API = f"https://api.github.com/repos/{REPO}/issues"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ.get("GITHUB_TOKEN")

AUTHOR = "ccckmit"
WEEKLY_RE = re.compile(r"習題|第[0-9零一二三四五六七八九十百]+週")


def api_get(url):
    headers = {
        "User-Agent": "alg-homework-scraper",
        "Accept": "application/vnd.github+json",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp), resp.headers


def fetch_issues():
    items, url = [], f"{API}?state=all&per_page=100"
    while url:
        data, headers = api_get(url)
        items.extend(data)
        link = headers.get("Link", "")
        nxt = [p for p in link.split(",") if 'rel="next"' in p]
        url = re.search(r"<([^>]+)>", nxt[0]).group(1) if nxt else None
    return [i for i in items if "pull_request" not in i]


def week_label(title, number):
    m = re.search(r"第([0-9零一二三四五六七八九十百]+)週", title)
    if m:
        return f"第{m.group(1)}週"
    m = re.search(r"習題\s*([0-9]+)", title)
    if m:
        return f"習題{m.group(1)}"
    return f"#{number}"


def render_homework(issue):
    body = (issue.get("body") or "").strip() or "（此 issue 沒有內容）"
    return f"""# {issue['title']}

- 原始 issue: {issue['html_url']}
- 出題者: {issue['user']['login']}
- 發佈時間: {issue['created_at']}

---

{body}
"""


def render_readme(index, issue):
    return f"""# HW{index} - {issue['title']}

- 題目（ccckmit 出題）: [作業.md](作業.md)
- 原始 issue: {issue['html_url']}
- 發佈時間: {issue['created_at'][:10]}
- 狀態: 未完成

## 作答內容

- [ ] 程式碼
- [ ] 執行結果
- [ ] 說明 / 心得

## 筆記

（在這裡記錄解題思路）
"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    issues = [
        i for i in fetch_issues()
        if i["user"]["login"] == AUTHOR and WEEKLY_RE.search(i["title"])
    ]
    issues.sort(key=lambda i: i["number"])

    rows = []
    for index, issue in enumerate(issues, start=1):
        folder_name = f"HW{index}"
        folder = os.path.join(BASE_DIR, folder_name)
        os.makedirs(folder, exist_ok=True)

        with open(os.path.join(folder, "作業.md"), "w", encoding="utf-8") as f:
            f.write(render_homework(issue))
        readme_file = os.path.join(folder, "README.md")
        if not os.path.exists(readme_file):
            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(render_readme(index, issue))

        rows.append((folder_name, index, issue))
        print(f"[OK] {folder_name}/ 作業.md（README.md 已存在則保留）")

    readme = [
        f"# {REPO} 週次習題",
        "",
        f"共 {len(rows)} 份習題，每份一個資料夾（`作業.md` + `README.md`）。",
        "",
        "| 資料夾 | 週次 | 標題 | 原始 issue |",
        "| --- | --- | --- | --- |",
    ]
    for folder_name, index, issue in rows:
        readme.append(
            f"| [{folder_name}]({folder_name}/) "
            f"| {week_label(issue['title'], issue['number'])} "
            f"| {issue['title']} "
            f"| [#{issue['number']}]({issue['html_url']}) |"
        )
    root_readme = os.path.join(BASE_DIR, "README.md")
    if not os.path.exists(root_readme):
        with open(root_readme, "w", encoding="utf-8") as f:
            f.write("\n".join(readme) + "\n")

    print(f"\n完成：{len(rows)} 個資料夾")
    print(f"總覽：{os.path.join(BASE_DIR, 'README.md')}")


if __name__ == "__main__":
    main()
