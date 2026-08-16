#!/usr/bin/env python3
"""Static checks for the Sleepy Magpie site.

Runs without any dependencies or build step:
  1. every local href/src in every .html file resolves to a file that exists
  2. every tool page listed in TOOL_PAGES exists and is linked from index.html
  3. every tool page carries the shared stylesheet, a title, and a link home
  4. no em dashes in the page copy (house style)

Usage: python3 scripts/check-site.py
Exits 0 when everything passes, 1 otherwise.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOOL_PAGES = [
    "tools/ccsm.html",
    "tools/wtm.html",
    "tools/thoughtqueue.html",
    "tools/cirrus.html",
    "tools/book-release-tracker.html",
    "tools/rekibase.html",
]

REF_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')
TAG_RE = re.compile(r"<[^>]+>")

failures = []


def check_local_refs(page: Path) -> None:
    """Resolve every local href/src on a page and record the ones that are missing."""
    html = page.read_text(encoding="utf-8")
    for ref in REF_RE.findall(html):
        if ref.startswith(("http://", "https://", "mailto:", "#", "data:", "//")):
            continue
        target = (page.parent / ref.split("#")[0].split("?")[0]).resolve()
        if not target.exists():
            failures.append(f"{page.relative_to(ROOT)}: broken local ref -> {ref}")


def check_no_em_dash(page: Path) -> None:
    """Flag em dashes in visible copy. Entity forms count too."""
    html = page.read_text(encoding="utf-8")
    if "&mdash;" in html or "&#8212;" in html:
        failures.append(f"{page.relative_to(ROOT)}: em dash entity in markup")
    text = TAG_RE.sub(" ", html)
    if "—" in text:
        snippet = next(
            line.strip() for line in text.splitlines() if "—" in line
        )
        failures.append(f"{page.relative_to(ROOT)}: em dash in copy -> {snippet[:80]}")


def main() -> int:
    pages = sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("tools/*.html"))
    if not pages:
        failures.append("no html pages found")

    for page in pages:
        check_local_refs(page)
        check_no_em_dash(page)

    index = ROOT / "index.html"
    index_html = index.read_text(encoding="utf-8") if index.exists() else ""
    if not index_html:
        failures.append("index.html missing")

    for rel in TOOL_PAGES:
        page = ROOT / rel
        if not page.exists():
            failures.append(f"missing tool page: {rel}")
            continue
        if rel not in index_html:
            failures.append(f"index.html does not link to {rel}")
        html = page.read_text(encoding="utf-8")
        for needle, label in (
            ('href="../styles.css"', "shared stylesheet"),
            ("<title>", "title"),
            ('href="../index.html"', "link back to the home page"),
        ):
            if needle not in html:
                failures.append(f"{rel}: no {label}")

    if failures:
        print(f"FAIL ({len(failures)} problem(s)):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"OK: {len(pages)} pages, {len(TOOL_PAGES)} tool pages, 0 broken local refs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
