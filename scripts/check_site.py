#!/usr/bin/env python3
"""Check the built site. Exits with an error (and fails the pipeline) if a problem is found.

Checks every .html file for:
  1. a non-empty <title>
  2. a lang attribute on <html> (helps screen readers)
  3. links and files (href / src) that point to something that does not exist
  4. links that start with "/" (these break on project sites hosted under /repo-name/)
  5. leftover __PLACEHOLDER__ text that the build step forgot to replace

Usage: python3 scripts/check_site.py dist
Uses only Python's standard library.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")
PLACEHOLDER = re.compile(r"__[A-Z][A-Z_]*__")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.lang = ""
        self.refs: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang") or ""
        if tag == "title":
            self.in_title = True
        for name in ("href", "src"):
            value = attrs.get(name)
            if value:
                self.refs.append(value)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check_page(page: Path, root: Path) -> list[str]:
    problems: list[str] = []
    name = page.relative_to(root).as_posix()
    text = page.read_text(encoding="utf-8")

    parser = PageParser()
    parser.feed(text)

    if not parser.title.strip():
        problems.append(f"{name}: missing or empty <title>")
    if not parser.lang.strip():
        problems.append(f'{name}: <html> needs a lang attribute, e.g. <html lang="en">')

    for ref in parser.refs:
        if ref.startswith("#") or ref.lower().startswith(SKIP_SCHEMES) or ref.startswith("//"):
            continue
        if ref.startswith("/"):
            problems.append(
                f"{name}: link '{ref}' starts with '/'. Use a relative path "
                "(e.g. 'style.css'), or the link will break under /repo-name/."
            )
            continue
        target_path = unquote(urlparse(ref).path)
        if not target_path:
            continue
        target = (page.parent / target_path).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            problems.append(f"{name}: '{ref}' points to a file that does not exist")

    for match in sorted(set(PLACEHOLDER.findall(text))):
        problems.append(f"{name}: unreplaced placeholder {match} (was it added to build.py?)")

    return problems


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python3 scripts/check_site.py <folder>")

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        sys.exit(f"error: folder '{sys.argv[1]}' not found. Did the build step run?")
    if not (root / "index.html").exists():
        sys.exit("error: index.html is missing; the site has no home page.")

    pages = sorted(root.rglob("*.html"))
    problems: list[str] = []
    for page in pages:
        problems.extend(check_page(page, root))

    if problems:
        print(f"FAILED: {len(problems)} problem(s) found in {len(pages)} page(s):\n")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)

    print(f"OK: checked {len(pages)} page(s), no problems found.")


if __name__ == "__main__":
    main()
