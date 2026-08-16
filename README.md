# sleepymagpie.com

The static site for Sleepy Magpie, LLC. A home page listing the tools, plus a detail page for each one.

No framework, no dependencies, no build step. Plain HTML, one shared stylesheet, a self-hosted webfont, and some PNGs.

## Layout

```
index.html            home page, with a static card per tool
styles.css            shared theme for every page
tools/                one page per tool
  ccsm.html
  wtm.html
  thoughtqueue.html
  cirrus.html
  book-release-tracker.html
  rekibase.html
assets/<tool>/        screenshots and icons for that tool's page
scripts/check-site.py the test suite
```

## Setup

Nothing to install. Clone the repo and you have the whole site.

## Running locally

```sh
python3 -m http.server
```

Then open <http://localhost:8000>. Opening `index.html` directly from the filesystem works too, the paths are all relative.

## Building

There is no build step. What is in the repo is what gets served.

## Tests

```sh
python3 scripts/check-site.py
```

It checks that every local `href`/`src` resolves to a file that exists, that every tool page exists and is linked from the home page, that each tool page carries the shared stylesheet and a link back home, and that no em dashes crept into the copy. Exits non-zero on any failure, so it works fine as a CI or pre-commit step.

## Adding a tool

1. Copy an existing page in `tools/` and keep the same sections and class names, so it inherits the theme.
2. Drop any screenshots into `assets/<tool>/`, downscaled to about 1400px wide.
3. Add a card to the Projects list in `index.html`.
4. Add the new page's path to `TOOL_PAGES` in `scripts/check-site.py`.
5. Run the tests.

Page copy should come from that tool's own README so the site and the repo do not drift apart.
