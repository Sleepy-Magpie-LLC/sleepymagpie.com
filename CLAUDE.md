# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

The static site for Sleepy Magpie, LLC (sleepymagpie.com): a home page plus one detail page per tool. No framework and no build step.

## Tech Stack

Plain HTML with a single shared stylesheet, a self-hosted webfont (`FacultyGlyphic-Regular.ttf`), and PNG assets. No dependencies or tooling.

## Files

- `index.html`: the home page. The Projects list is a hand-written static list of cards, one per tool, each linking to its page in `tools/`. It is not generated from the GitHub API.
- `styles.css`: the shared theme for every page (colors, type, hero, project cards, tool-page layout). Every page links this, so change it here rather than adding page-level styles.
- `tools/*.html`: one page per tool. Same structure on each: header, hero (title, tagline, tags, links), "What it is", "Features", "Screenshots" where images exist, "Getting started", footer.
- `assets/<tool>/`: screenshots and icons for the tool pages, copied from each tool's own repo and downscaled.
- `scripts/check-site.py`: the only test. Verifies local links resolve, every tool page exists and is linked from the home page, each carries the shared stylesheet, and no em dashes slipped into the copy.
- `FacultyGlyphic-Regular.ttf`, `logo.png`: the display font and the logo.

## Adding a tool

Copy an existing page in `tools/`, keep the same section order and class names, add a card to `index.html`, add the page path to `TOOL_PAGES` in `scripts/check-site.py`, then run the check. Page copy should come from that tool's README, not from imagination.

## Running

Serve the folder statically (`python3 -m http.server`) and open <http://localhost:8000>. Opening `index.html` from the filesystem works too. There is no build step.

Tests: `python3 scripts/check-site.py`.

## Model Selection

- **Claude Sonnet 5** (`claude-sonnet-5`): default. Copy, styling, and markup edits.
- **Claude Opus 4.8** (`claude-opus-4-8`): a larger redesign or a change spanning every page.
- **Claude Haiku 4.5** (`claude-haiku-4-5`): small text or style fixes and quick lookups.
