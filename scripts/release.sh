#!/usr/bin/env bash
# Release the site to the Cloudflare Worker.
#
# Runs the site checks, refuses to ship uncommitted changes (so what's live always matches a
# commit), then deploys the static assets with Wrangler.
#
# Usage: scripts/release.sh [--dry-run] [--allow-dirty]
set -euo pipefail

cd "$(dirname "$0")/.."

dry_run=false
allow_dirty=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    --allow-dirty) allow_dirty=true ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

echo "==> Running site checks"
python3 scripts/check-site.py

if ! $allow_dirty && [ -n "$(git status --porcelain)" ]; then
  echo "error: working tree has uncommitted changes. Commit them or pass --allow-dirty." >&2
  exit 1
fi

commit="$(git rev-parse --short HEAD)"

if $dry_run; then
  echo "==> Dry run (nothing will be uploaded)"
  npx --yes wrangler deploy --dry-run
else
  echo "==> Deploying $commit to Cloudflare"
  npx --yes wrangler deploy --message "release $commit"
fi
