#!/usr/bin/env python3
"""Build the site: copy site/ into dist/ and stamp in build information.

Placeholders like __COMMIT_SHORT__ inside .html files are replaced with real
values. On GitHub, the values come from environment variables that Actions sets
automatically. On your own computer, harmless "local" values are used instead.

Uses only Python's standard library, so there is nothing to install.
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site"
OUT = ROOT / "dist"


def main() -> None:
    if not SRC.is_dir():
        sys.exit("error: the site/ folder was not found. Run this from the project root.")

    # Start from a clean output folder every time, so old files never linger.
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)

    # Values provided by GitHub Actions (with fallbacks for local builds).
    commit_full = os.environ.get("GITHUB_SHA", "local-build")
    server = os.environ.get("GITHUB_SERVER_URL", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_number = os.environ.get("GITHUB_RUN_NUMBER", "")

    built_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if run_id and repo:
        run_url = f"{server}/{repo}/actions/runs/{run_id}"
        run_label = f"Workflow run {run_number}"
    else:
        run_url = "#"
        run_label = "Built on this computer"

    stamps = {
        "__COMMIT_SHORT__": commit_full[:7],
        "__COMMIT_FULL__": commit_full,
        "__BUILT_AT__": built_at,
        "__RUN_URL__": run_url,
        "__RUN_LABEL__": run_label,
    }

    changed = 0
    for page in OUT.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for placeholder, value in stamps.items():
            text = text.replace(placeholder, value)
        page.write_text(text, encoding="utf-8")
        changed += 1

    # A tiny file the page polls to learn whether a newer version has been published.
    (OUT / "version.json").write_text(
        json.dumps({"commit": commit_full, "built_at": built_at}, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Built {changed} page(s) into dist/  (commit {commit_full[:7]}, {built_at})")


if __name__ == "__main__":
    main()
