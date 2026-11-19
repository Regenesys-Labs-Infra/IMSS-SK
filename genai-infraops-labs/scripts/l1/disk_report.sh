#!/usr/bin/env bash
set -euo pipefail

if (( $# != 0 )); then
  printf 'Usage: %s\n' "${0##*/}" >&2
  exit 2
fi

if ! command -v du >/dev/null 2>&1 || ! command -v sort >/dev/null 2>&1; then
  printf 'Error: du and sort are required.\n' >&2
  exit 127
fi

printf 'Top 10 directories directly under /var (largest first):\n'
printf '%-12s %s\n' "SIZE" "DIRECTORY"

du_status=0
if du_output=$(LC_ALL=C du -x -h --max-depth=1 -- /var 2>&1 | awk '
  /^du: / {
    print > "/dev/stderr"
    had_errors = 1
    next
  }
  { print }
  END {
    if (had_errors) {
      exit 1
    }
  }
'); then
  :
else
  du_status=$?
fi

if (( du_status != 0 )); then
  printf 'Warning: some /var paths could not be read; report may be incomplete.\n' >&2
fi

printf '%s\n' "$du_output" \
  | LC_ALL=C sort -hr \
  | awk 'NF >= 2 && $2 != "/var" && count < 10 { print; count++ }'

if (( du_status != 0 )); then
  exit 1
fi
