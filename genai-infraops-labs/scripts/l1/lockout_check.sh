#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <username>\n' "${0##*/}" >&2
}

if (( $# != 1 )); then
  usage
  exit 2
fi

username=$1
if [[ -z $username || $username == -* ]]; then
  printf 'Error: provide a username that does not start with "-".\n' >&2
  exit 2
fi

if ! command -v faillock >/dev/null 2>&1; then
  printf 'Error: faillock is not installed or is not in PATH.\n' >&2
  exit 127
fi

printf ' faillock status for %s:\n' "$username"
faillock --user "$username"
