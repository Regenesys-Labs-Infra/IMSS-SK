#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <nginx|cron|docker> [--execute]\n' "${0##*/}" >&2
}

if (( $# == 1 )) && [[ $1 == "--help" || $1 == "-h" ]]; then
  usage
  exit 0
fi

if (( $# < 1 || $# > 2 )); then
  usage
  exit 2
fi

service=$1
case "$service" in
  nginx|cron|docker)
    ;;
  *)
    printf 'Error: service is not allow-listed: %s\n' "$service" >&2
    usage
    exit 2
    ;;
esac

execute=false
if (( $# == 2 )); then
  if [[ $2 != "--execute" ]]; then
    printf 'Error: unknown option: %s\n' "$2" >&2
    usage
    exit 2
  fi
  execute=true
fi

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
project_root=$(cd -- "$script_dir/../.." && pwd)

print_prechecks() {
  local service_state=""

  printf 'Service status before action: '
  if service_state=$(systemctl is-active "$service" 2>/dev/null); then
    printf '%s\n' "$service_state"
  else
    printf '%s\n' "${service_state:-unavailable}"
  fi

  printf 'Last 20 journal lines for %s:\n' "$service"
  journalctl --unit "$service" --lines=20 --no-pager
}

write_audit_entry() {
  local result=$1
  local audit_file="$project_root/approvals/audit.log"
  local timestamp
  local username

  timestamp=$(date --iso-8601=seconds)
  username=$(id -un)
  mkdir -p -- "${audit_file%/*}"
  printf '%s\t%s\t%s\t%s\n' "$timestamp" "$username" "$service" "$result" \
    >> "$audit_file"
}

if ! print_prechecks; then
  printf 'Error: pre-checks failed; no restart was attempted.\n' >&2
  write_audit_entry "precheck-failed"
  exit 1
fi

if [[ $execute != true ]]; then
  printf 'DRY RUN: no service changes made.\n'
  printf 'Would run: sudo systemctl restart %s\n' "$service"
  write_audit_entry "dry-run"
  exit 0
fi

if ! read -r -p "Type '$service' to confirm restart: " confirmation; then
  printf 'Error: confirmation input was not received.\n' >&2
  write_audit_entry "confirmation-unavailable"
  exit 1
fi
if [[ $confirmation != "$service" ]]; then
  printf 'Restart cancelled: confirmation did not match.\n' >&2
  write_audit_entry "cancelled"
  exit 1
fi

if sudo systemctl restart "$service"; then
  restart_result="restart-succeeded"
else
  printf 'Error: restart command failed for %s.\n' "$service" >&2
  write_audit_entry "restart-failed"
  exit 1
fi

post_state=""
if post_state=$(systemctl is-active "$service" 2>/dev/null) \
  && [[ $post_state == "active" ]]; then
  printf 'Service status after restart: %s\n' "$post_state"
  write_audit_entry "success"
  exit 0
fi

printf 'Error: %s did not report active after restart (%s).\n' \
  "$service" "${post_state:-unavailable}" >&2
write_audit_entry "$restart_result-postcheck-failed"
exit 1
