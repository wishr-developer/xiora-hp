#!/usr/bin/env bash
# check-shell-quality.sh
# Enforces the Xiora shell quality standard defined in docs/SHELL_QUALITY_STANDARD.md.
#
# Scans a directory tree for *.sh files and reports:
#   1. bash scripts missing `set -Eeuo pipefail`
#   2. POSIX sh scripts missing `set -eu`
#   3. scripts that write to files (`>` / `>>`) but lack `set -o noclobber`
#   4. destructive scripts (rm -rf, dropdb, docker rm, reset --hard, --force,
#      force-push) that do NOT support a `--dry-run` flag.
#
# Exit codes:
#   0 = all clean
#   1 = one or more issues
#   2 = usage / invocation error
#
# Usage:
#   scripts/check-shell-quality.sh [ROOT]
#   scripts/check-shell-quality.sh --help
#
# Environment:
#   VERBOSE=1  print each scanned file
#   STRICT=1   also fail on noclobber warning (default = warn only)

set -Eeuo pipefail
set -o noclobber

usage() {
  cat <<'USAGE'
Usage: check-shell-quality.sh [ROOT]

Scans ROOT (default: current directory) recursively for *.sh files and reports
scripts that violate the Xiora shell quality standard.

Skips:
  node_modules/, .git/, _archive/, .playwright-mcp/, .pytest_cache/,
  backups/, /Pods/, /.venv/, /site-packages/, hermes-engine, expo-configure

Options:
  -h, --help    Show this message.

Environment:
  VERBOSE=1     Print each scanned file.
  STRICT=1      Treat noclobber warnings as failures.
USAGE
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
esac

ROOT="${1:-.}"
if [[ ! -d "$ROOT" ]]; then
  echo "check-shell-quality: ROOT '$ROOT' is not a directory" >&2
  exit 2
fi

MISSING_STRICT=()
MISSING_NOCLOBBER=()
DESTRUCTIVE_NO_DRYRUN=()
SCANNED=0

# Portable file discovery honoring the skip list.
while IFS= read -r -d '' file; do
  case "$file" in
    */node_modules/*|*/.git/*|*/_archive/*|*/.playwright-mcp/*) continue ;;
    */.pytest_cache/*|*/backups/*|*/Pods/*|*/.venv/*) continue ;;
    */site-packages/*|*hermes-engine*|*expo-configure*) continue ;;
    */Pods-*-frameworks.sh|*/Pods-*-resources.sh) continue ;;
  esac

  SCANNED=$((SCANNED + 1))
  [[ "${VERBOSE:-0}" == "1" ]] && echo "scan: $file"

  # Read first line for shebang and full body for pattern checks.
  first_line=$(head -n 1 "$file" 2>/dev/null || true)
  body=$(cat "$file" 2>/dev/null || true)

  is_bash=0
  is_posix=0
  case "$first_line" in
    "#!/usr/bin/env bash"*|"#!/bin/bash"*|"#!"*bash*) is_bash=1 ;;
    "#!/bin/sh"*|"#!/usr/bin/env sh"*) is_posix=1 ;;
  esac

  # Only enforce on scripts with a recognized shebang.
  if [[ $is_bash -eq 0 && $is_posix -eq 0 ]]; then
    continue
  fi

  # 1) strict-mode check
  if [[ $is_bash -eq 1 ]]; then
    if ! grep -qE '^[[:space:]]*set[[:space:]]+-Eeuo[[:space:]]+pipefail' <<< "$body"; then
      MISSING_STRICT+=("$file")
    fi
  else
    if ! grep -qE '^[[:space:]]*set[[:space:]]+-eu([[:space:]]|$)' <<< "$body"; then
      MISSING_STRICT+=("$file")
    fi
  fi

  # 2) noclobber check (only when the script writes to a file)
  #    Heuristic: look for redirection tokens that are not `>&` or `>>&`.
  if grep -qE '[^&|<>]>[^&|>]|[^&|<>]>>[^&|>]' <<< "$body"; then
    if ! grep -qE '^[[:space:]]*set[[:space:]]+-o[[:space:]]+noclobber' <<< "$body"; then
      MISSING_NOCLOBBER+=("$file")
    fi
  fi

  # 3) destructive command audit
  #    Strip pure-comment lines to avoid false positives from documentation.
  #    Only truly destructive verbs count: rm -rf, dropdb, drop table,
  #    docker rm (container removal), git reset --hard, git push --force /
  #    force-push. Idempotent env-set --force (netlify/vercel/eas init
  #    --force) is excluded because it is not data-destructive.
  code_only=$(grep -vE '^[[:space:]]*#' <<< "$body" || true)
  if grep -qE 'rm[[:space:]]+-[a-zA-Z]*rf|dropdb|drop[[:space:]]+table|docker[[:space:]]+rm[[:space:]]|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+push[[:space:]].*--force|force-push' <<< "$code_only"; then
    if ! grep -qE -- '--dry-run|DRY_RUN|dry_run' <<< "$body"; then
      DESTRUCTIVE_NO_DRYRUN+=("$file")
    fi
  fi
done < <(find "$ROOT" -type f -name '*.sh' -print0 2>/dev/null)

echo
echo "check-shell-quality: scanned $SCANNED shell script(s) under $ROOT"

problems=0

if (( ${#MISSING_STRICT[@]} > 0 )); then
  problems=$((problems + ${#MISSING_STRICT[@]}))
  echo
  echo "FAIL: ${#MISSING_STRICT[@]} script(s) missing strict-mode set flags:"
  printf '  - %s\n' "${MISSING_STRICT[@]}"
fi

if (( ${#MISSING_NOCLOBBER[@]} > 0 )); then
  echo
  echo "WARN: ${#MISSING_NOCLOBBER[@]} script(s) write files without 'set -o noclobber':"
  printf '  - %s\n' "${MISSING_NOCLOBBER[@]}"
  if [[ "${STRICT:-0}" == "1" ]]; then
    problems=$((problems + ${#MISSING_NOCLOBBER[@]}))
  fi
fi

if (( ${#DESTRUCTIVE_NO_DRYRUN[@]} > 0 )); then
  problems=$((problems + ${#DESTRUCTIVE_NO_DRYRUN[@]}))
  echo
  echo "FAIL: ${#DESTRUCTIVE_NO_DRYRUN[@]} destructive script(s) lack --dry-run support:"
  printf '  - %s\n' "${DESTRUCTIVE_NO_DRYRUN[@]}"
fi

if (( problems == 0 )); then
  echo "OK: all scanned scripts satisfy the Xiora shell quality standard."
  exit 0
fi

echo
echo "See docs/SHELL_QUALITY_STANDARD.md for the required fixes."
exit 1
