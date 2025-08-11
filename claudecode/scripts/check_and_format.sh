#!/usr/bin/env bash
set -euo pipefail

# check_and_format.sh
# 用途：对“本次编辑/改动的文件”执行语法/类型检查，成功后执行格式化；失败则阻断（退出码2）。
# 兼容：macOS/Linux/Windows（通过 powershell 提示音）。

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 1

# -------- args --------
FILES_ARG=""
DRY_RUN=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --files)
      FILES_ARG="$2"; shift 2 ;;
    --dry-run)
      DRY_RUN=true; shift ;;
    *)
      echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# -------- helpers --------
log() { echo "[check] $*" >&2; }
json_ok() { echo "{\"status\":\"ok\",\"files\":[$(printf '"%s",' "$@" | sed 's/,$//')],\"detail\":\"lint+format passed\"}"; }
json_err() { local msg="$1"; shift; echo "{\"status\":\"error\",\"files\":[$(printf '"%s",' "$@" | sed 's/,$//')],\"detail\":\"${msg}\"}"; }

in_project() {
  local p="$1";
  [[ "$p" == /* ]] || p="$PROJECT_DIR/$p"
  [[ "$p" == "$PROJECT_DIR"* ]]
}

play_success() {
  # macOS
  if command -v afplay >/dev/null 2>&1 && [[ -f "/System/Library/Sounds/Glass.aiff" ]]; then afplay "/System/Library/Sounds/Glass.aiff" 2>/dev/null && return 0; fi
  if command -v osascript >/dev/null 2>&1; then osascript -e 'beep 1' 2>/dev/null && return 0; fi
  # Linux
  if command -v paplay >/dev/null 2>&1; then paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null && return 0; fi
  if command -v aplay >/dev/null 2>&1; then printf '\a' && return 0; fi
  if command -v play >/dev/null 2>&1; then play -n synth 0.1 sine 880 2>/dev/null && return 0; fi
  # Windows (Git Bash / Cygwin)
  if command -v powershell >/dev/null 2>&1; then powershell -c "[console]::beep(880,200)" 2>/dev/null && return 0; fi
  printf '\a' || true
}

play_fail() {
  for i in 1 2 3; do
    # macOS
    if command -v afplay >/dev/null 2>&1 && [[ -f "/System/Library/Sounds/Basso.aiff" ]]; then afplay "/System/Library/Sounds/Basso.aiff" 2>/dev/null; elif command -v osascript >/dev/null 2>&1; then osascript -e 'beep 1' 2>/dev/null; \
    # Linux
    elif command -v paplay >/dev/null 2>&1; then paplay /usr/share/sounds/freedesktop/stereo/dialog-warning.oga 2>/dev/null; elif command -v aplay >/dev/null 2>&1; then printf '\a'; elif command -v play >/dev/null 2>&1; then play -n synth 0.1 sine 440 2>/dev/null; \
    # Windows
    elif command -v powershell >/dev/null 2>&1; then powershell -c "[console]::beep(440,200)" 2>/dev/null; else printf '\a'; fi
    sleep 0.05 || true
  done
}

have() { command -v "$1" >/dev/null 2>&1; }

# 检测 ESLint 配置是否存在（v9+ eslint.config.* 或传统 .eslintrc* 或 package.json: eslintConfig）
eslint_config_exists() {
  [[ -f eslint.config.js || -f eslint.config.mjs || -f eslint.config.cjs || -f eslint.config.ts || -f eslint.config.mts || -f eslint.config.cts ]] && return 0
  [[ -f .eslintrc.js || -f .eslintrc.cjs || -f .eslintrc.json || -f .eslintrc.yaml || -f .eslintrc.yml ]] && return 0
  if [[ -f package.json ]] && command -v grep >/dev/null 2>&1; then
    grep -q '"eslintConfig"' package.json && return 0 || true
  fi
  return 1
}

# -------- collect files --------
COLLECTED=()
if [[ -n "$FILES_ARG" ]]; then
  read -r -a COLLECTED <<<"$FILES_ARG"
elif [[ -n "${CLAUDE_EDITED_FILES:-}" ]]; then
  read -r -a COLLECTED <<<"$CLAUDE_EDITED_FILES"
else
  if [[ -d .git ]] && have git; then
    mapfile -t COLLECTED < <(git diff --name-only --diff-filter=ACMR HEAD 2>/dev/null | tr '\n' ' ')
  fi
fi

# de-dup and filter
FILTERED=()
for f in "${COLLECTED[@]}"; do
  [[ -z "$f" ]] && continue
  # normalize to relative path
  if [[ "$f" == /* ]]; then f="${f#"$PROJECT_DIR/"}"; fi
  [[ -f "$f" ]] || continue
  if in_project "$f"; then FILTERED+=("$f"); fi
done

if [[ ${#FILTERED[@]} -eq 0 ]]; then
  log "no files to process; exiting ok"
  json_ok >/dev/null
  play_success
  exit 0
fi

# Group files by type
JS_TS=() JSONS=() MARKS=() YAMLS=() PYS=() GOS=() RSS=() SHS=() OTHERS=()
for f in "${FILTERED[@]}"; do
  case "$f" in
    *.js|*.jsx|*.ts|*.tsx) JS_TS+=("$f") ;;
    *.json) JSONS+=("$f") ;;
    *.md|*.markdown) MARKS+=("$f") ;;
    *.yml|*.yaml) YAMLS+=("$f") ;;
    *.py) PYS+=("$f") ;;
    *.go) GOS+=("$f") ;;
    *.rs) RSS+=("$f") ;;
    *.sh) SHS+=("$f") ;;
    *) OTHERS+=("$f") ;;
  esac
done

FAILED_FILES=()

# ---- language handlers ----
# JS/TS/JSON/MD/YAML with prettier
run_prettier() {
  local mode="$1"; shift; local files=($(printf '%q ' "$@"))
  if [[ ${#files[@]} -eq 0 ]]; then return 0; fi
  if have npx; then local PRETTIER="npx --yes prettier"; elif have prettier; then local PRETTIER="prettier"; else return 0; fi
  if [[ "$mode" == "check" ]]; then
    $PRETTIER --check "${files[@]}" || return 1
  else
    $PRETTIER --write "${files[@]}" || return 1
  fi
}

run_eslint() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  # 无配置则跳过 ESLint（避免 v9 缺省配置报错）
  if ! eslint_config_exists; then return 0; fi
  if have npx; then npx --yes eslint "${files[@]}"; elif have eslint; then eslint "${files[@]}"; else return 0; fi
}

run_tsc() {
  [[ -f tsconfig.json ]] || return 0
  if have npx; then npx --yes tsc --noEmit; elif have tsc; then tsc --noEmit; else return 0; fi
}

handle_js_stack() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  # lint/type-check
  run_eslint "${files[@]}" || return 1
  run_tsc || true
  # format
  if $DRY_RUN; then run_prettier check "${files[@]}" || return 1; else run_prettier write "${files[@]}" || return 1; fi
}

handle_json_md_yaml() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  if $DRY_RUN; then run_prettier check "${files[@]}" || return 1; else run_prettier write "${files[@]}" || return 1; fi
}

# Python: ruff/black/pyright
handle_python() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  local lint_ok=true
  if have ruff; then ruff check "${files[@]}" || lint_ok=false; elif have npx; then :; fi
  if [[ "$lint_ok" == false ]]; then return 1; fi
  if $DRY_RUN; then
    if have black; then black --check "${files[@]}" || return 1; fi
  else
    if have ruff; then ruff check --fix "${files[@]}" || true; fi
    if have black; then black "${files[@]}" || return 1; fi
  fi
}

# Go: go vet + gofmt
handle_go() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  if have go; then
    # 仅在 go.mod 存在时运行 go vet
    if [[ -f go.mod ]]; then
      go vet ./... || return 1
    fi
    if $DRY_RUN; then
      for f in "${files[@]}"; do diff -u "$f" <(gofmt "$f") >/dev/null || return 1; done
    else
      gofmt -w "${files[@]}" || return 1
    fi
  fi
}

# Rust: cargo check + rustfmt
handle_rust() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  # 仅在 Cargo.toml 存在时运行 cargo check
  if [[ -f Cargo.toml ]] && have cargo; then cargo check || return 1; fi
  if have rustfmt; then
    if $DRY_RUN; then rustfmt --check "${files[@]}" || return 1; else rustfmt "${files[@]}" || return 1; fi
  fi
}

# Shell: shellcheck + shfmt
handle_shell() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  if have shellcheck; then shellcheck "${files[@]}" || return 1; fi
  if have shfmt; then
    if $DRY_RUN; then shfmt -d "${files[@]}" || return 1; else shfmt -w "${files[@]}" || return 1; fi
  fi
}

# Others: 默认跳过，避免 Prettier 无法推断解析器导致失败
handle_others() {
  local files=($(printf '%q ' "$@")); [[ ${#files[@]} -eq 0 ]] && return 0
  return 0
}

process_group() {
  local name="$1"; shift
  local files=("$@")
  [[ ${#files[@]} -eq 0 ]] && return 0
  log "processing $name: ${#files[@]} file(s)"
  if "handle_${name}" "${files[@]}"; then
    return 0
  else
    FAILED_FILES+=("${files[@]}")
    return 1
  fi
}

# run per group; any fail will set final rc=2
rc=0
process_group js_stack "${JS_TS[@]+${JS_TS[@]}}" || rc=2
process_group json_md_yaml "${JSONS[@]+${JSONS[@]}}" "${MARKS[@]+${MARKS[@]}}" "${YAMLS[@]+${YAMLS[@]}}" || rc=2
process_group python "${PYS[@]+${PYS[@]}}" || rc=2
process_group go "${GOS[@]+${GOS[@]}}" || rc=2
process_group rust "${RSS[@]+${RSS[@]}}" || rc=2
process_group shell "${SHS[@]+${SHS[@]}}" || rc=2
process_group others "${OTHERS[@]+${OTHERS[@]}}" || rc=2

if [[ $rc -eq 0 ]]; then
  json_ok "${FILTERED[@]}" >/dev/null
  play_success
  exit 0
else
  echo "Some files failed lint/format:" >&2
  printf ' - %s\n' "${FAILED_FILES[@]}" >&2
  json_err "lint/format failed" "${FAILED_FILES[@]}" >/dev/null
  play_fail
  exit 2
fi