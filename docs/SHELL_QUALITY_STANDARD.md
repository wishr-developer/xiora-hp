# Xiora Shell Quality Standard

Applies to every `*.sh` file authored inside a Xiora-owned repo (Xiora_HP,
XAI parent, brain, services/**, etc.). Vendor-copied scripts under
`node_modules/`, `Pods/`, `.venv/`, `site-packages/`, `hermes-engine*`,
`expo-configure*`, `_archive/`, `backups/` are out of scope.

Source: PDF learning insight 2026-07-19 (Top 5 action items 1 and 4).

## 1. Strict-mode set flags (mandatory)

Every shell script MUST enable strict-mode set flags immediately after the
shebang (and any leading header comment block).

### 1.1 bash scripts

Shebang: `#!/usr/bin/env bash` or `#!/bin/bash`.

Required:

```bash
set -Eeuo pipefail
```

Flag rationale:

- `-e` : exit on first uncaught error (default failure semantics)
- `-E` : ERR trap inherits into functions / subshells (needed for reliable
  error reporting when using traps)
- `-u` : treat unset variables as errors (catches typos before they corrupt
  state)
- `-o pipefail` : make `foo | bar` fail if `foo` fails, not only if `bar`
  fails (essential for catch-and-retry logic)

### 1.2 POSIX sh scripts

Shebang: `#!/bin/sh` or `#!/usr/bin/env sh`.

Required:

```sh
set -eu
```

`-E` and `pipefail` are bash-specific and are omitted so scripts remain
portable to `dash`, `ash`, `busybox sh`.

### 1.3 Preserving intentional soft-failure

`|| true` at the end of a specific command still works with strict-mode
enabled. Prefer it to disabling `-e` globally. Example:

```bash
set -Eeuo pipefail
docker stop old-container 2>/dev/null || true   # ok: soft-fail this one line
```

## 2. `set -o noclobber` (mandatory for bash scripts that write files)

Any bash script that redirects into a file (`>` or `>>`) MUST enable
noclobber so that an accidental `>` on an existing file fails loudly
instead of silently overwriting it.

```bash
set -Eeuo pipefail
set -o noclobber
```

To intentionally overwrite an existing file when noclobber is on, use the
`>|` form:

```bash
echo "$data" >| /path/to/existing/output.json   # explicit overwrite
```

POSIX sh scripts are not required to add `set -o noclobber` because portable
behavior across `dash` / `ash` variants is not guaranteed; add it only when
you know the target interpreter supports it.

## 3. Insertion location

`set` directives are inserted immediately after the shebang line and any
contiguous leading comment block (so the file header banner stays intact).
Existing `set` directives (e.g. `set -euo pipefail`) are upgraded in place to
`set -Eeuo pipefail`; they are never deleted.

## 4. Destructive command safety — `--dry-run` mandatory

Any script that runs a genuinely destructive command MUST accept `--dry-run`
as an argument. When `--dry-run` is passed, the destructive lines print what
they *would* do instead of executing.

### 4.1 What counts as destructive

The following verbs count and require `--dry-run`:

- `rm -rf` (any path)
- `dropdb` / `DROP TABLE` / `DROP DATABASE`
- `docker rm` (container removal)
- `git reset --hard`
- `git push --force` / `git push -f` / `force-push`

The following are explicitly NOT destructive and do NOT require
`--dry-run`:

- `netlify env:set --force`, `vercel env add --force`, `eas project:init --force`
  (idempotent "overwrite existing config" flags)
- Comments that merely mention destructive commands in prose

### 4.2 Reference pattern

Add this block right after the strict-mode `set` calls:

```bash
# --- dry-run guard (Xiora shell quality standard) ---
DRY_RUN=0
for _arg in "$@"; do case "$_arg" in --dry-run) DRY_RUN=1 ;; esac; done
guard() { if [ "$DRY_RUN" = "1" ]; then echo "[dry-run] $*"; else "$@"; fi; }
# --- end dry-run guard ---
```

Then wrap destructive lines with the helper:

```bash
guard rm -rf "$STAGING_DIR"
guard docker rm -f old-container
```

For destructive commands that cannot be wrapped by a single guard (e.g.
`find ... -exec rm -rf {} \;`, SSH-embedded rm, or heredoc SQL with
`DROP TABLE`), branch explicitly:

```bash
if [ "$DRY_RUN" = "1" ]; then
  find "$ROOT" -mtime +30 -print | sed 's/^/[dry-run] rm -rf /'
else
  find "$ROOT" -mtime +30 -exec rm -rf {} \;
fi
```

For scripts whose entire body is a chained remote deploy pipeline, an
early-exit is acceptable:

```bash
if [ "$DRY_RUN" = "1" ]; then
  echo "[dry-run] would deploy $SHA to $REMOTE:$REMOTE_APP"
  exit 0
fi
```

### 4.3 Argument passthrough

Scripts that already accept positional arguments (e.g. `rollback.sh <ts>`)
must strip `--dry-run` from `"$@"` before consuming positional arguments so
the flag does not accidentally become `$1`:

```bash
DRY_RUN=0
_args=()
for _arg in "$@"; do
  case "$_arg" in
    --dry-run) DRY_RUN=1 ;;
    *) _args+=("$_arg") ;;
  esac
done
if [ ${#_args[@]} -gt 0 ]; then set -- "${_args[@]}"; else set --; fi
```

## 5. Enforcement

The verifier `scripts/check-shell-quality.sh` (in this repo) scans a
directory tree for `*.sh` files and reports any violations. Exit code 0
means the tree is clean; non-zero means at least one script violates the
strict-mode or destructive-guard rules.

```bash
# scan a tree
bash scripts/check-shell-quality.sh /path/to/repo

# verbose mode
VERBOSE=1 bash scripts/check-shell-quality.sh /path/to/repo

# also fail on noclobber warnings (default = warn only)
STRICT=1 bash scripts/check-shell-quality.sh /path/to/repo
```

Recommended: add a git pre-commit hook or CI job that calls the verifier
against the repo root and fails the commit / build on non-zero exit.

## 6. Audit findings (baseline 2026-07-19)

Full XAI shell corpus (`/Users/kutsuzawareo/Desktop/XAI`, 192 files
discovered, 180 in-scope after vendor exclusions):

| Metric                                     | Before | After |
| ------------------------------------------ | -----: | ----: |
| Scripts scanned (in-scope)                 |    180 |   180 |
| bash scripts                               |    175 |   175 |
| POSIX sh scripts                           |      5 |     5 |
| Missing `set -Eeuo pipefail` (bash)        |    173 |     0 |
| Missing `set -eu` (POSIX)                  |      5 |     0 |
| bash scripts that write files w/o noclobber |    154 |     0 |
| Destructive commands without `--dry-run`   |     13 |     0* |

\* Six of the original 13 were true positives and were retrofitted with the
`--dry-run` guard. The other seven were false positives (comments,
`netlify env:set --force`, `eas project:init --force`) and are now correctly
excluded by the verifier's refined heuristics.

### 6.1 Destructive scripts retrofitted with `--dry-run`

1. `scripts/xai-restore-test.sh` — wrapped `rm -rf "$TMP"` with `guard`.
2. `scripts/xai-scheduled-backup.sh` — branched retention `find -exec rm -rf`
   on `$DRY_RUN`.
3. `services/platform/ControlCenter/public-edge/scripts/rollback.sh` —
   wrapped SSH `rm -f` / `rm -rf` with `guard`; stripped `--dry-run` from
   positional args.
4. `services/platform/ClaudeHQ/SERVICE/SHOP/lib/build.sh` — wrapped
   `rm -rf "$DIST"` with `guard`.
5. `services/systems/Gourmie/app/infra/deploy_remote.sh` — early-exit in
   `--dry-run` with a full deploy-plan summary; positional-arg passthrough
   preserved.
6. `services/systems/Xiora/Kigen/scripts/asc/bin/build-and-upload-prod.sh` —
   wrapped `rm -rf "$ARCHIVE_PATH" "$EXPORT_PATH"` and `rm -rf "$IPA_VERIFY_DIR"`
   with `guard`.

### 6.2 Known residual issues (not caused by this PR)

- `services/systems/NexaUniversity/deploy/vps-bootstrap.sh` — pre-existing
  syntax error at line 108: escaped `\$(...)` outside any heredoc. Not
  caused by the strict-mode insertion (which is at lines 25-26). Filed as
  follow-up.
- `services/systems/XAIAgentFactory/deploy/docker-entrypoint.sh` — POSIX sh
  entrypoint. Verifier emits WARN because it contains `>/dev/null` which
  the redirect-heuristic misclassifies as a file write. No fix needed; it
  is treated as informational, not FAIL.
