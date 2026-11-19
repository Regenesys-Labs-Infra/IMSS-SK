#!/usr/bin/env bash
set -euo pipefail

overall_status=0

print_row() {
  local check=$1
  local value=$2
  local status=$3

  printf '%-32s | %-28s | %-6s\n' "$check" "$value" "$status"

  case "$status" in
    CRIT)
      overall_status=2
      ;;
    WARN)
      if (( overall_status == 0 )); then
        overall_status=1
      fi
      ;;
  esac
}

cpu_value="unavailable"
cpu_status="CRIT"
if load_avg=$(awk '{print $1}' /proc/loadavg) \
  && cores=$(getconf _NPROCESSORS_ONLN) \
  && [[ $cores =~ ^[1-9][0-9]*$ ]]; then
  cpu_result=$(awk -v load_avg="$load_avg" -v cores="$cores" 'BEGIN {
    status = load_avg > 2 * cores ? "CRIT" : load_avg > cores ? "WARN" : "OK"
    printf "%.2f / %d cores\t%s\n", load_avg, cores, status
  }')
  IFS=$'\t' read -r cpu_value cpu_status <<< "$cpu_result"
fi

memory_value="unavailable"
memory_status="CRIT"
if memory_values=$(awk '
  /^MemTotal:/ { total = $2; have_total = 1 }
  /^MemAvailable:/ { available = $2; have_available = 1 }
  END {
    if (have_total && have_available && total > 0 && available >= 0) {
      printf "%d %d\n", total, available
    } else {
      exit 1
    }
  }
' /proc/meminfo); then
  read -r memory_total_kb memory_available_kb <<< "$memory_values"
  memory_result=$(awk -v total="$memory_total_kb" -v available="$memory_available_kb" 'BEGIN {
    used = (total - available) * 100 / total
    status = used > 90 ? "CRIT" : used > 80 ? "WARN" : "OK"
    printf "%.1f%% used\t%s\n", used, status
  }')
  IFS=$'\t' read -r memory_value memory_status <<< "$memory_result"
fi

printf '%-32s | %-28s | %-6s\n' "CHECK" "VALUE" "STATUS"
printf '%s\n' '---------------------------------+------------------------------+-------'
print_row "CPU (1-minute load)" "$cpu_value" "$cpu_status"
print_row "Memory" "$memory_value" "$memory_status"

if disk_output=$(df -P -x tmpfs -x overlay 2>/dev/null); then
  disk_rows=$(awk '
    NR == 1 { next }
    {
      percent_column = 0
      for (i = 1; i <= NF; i++) {
        if ($i ~ /^[0-9]+%$/) {
          percent_column = i
          break
        }
      }
      if (percent_column == 0) {
        next
      }

      used = $percent_column
      sub(/%$/, "", used)
      mount = ""
      for (i = percent_column + 1; i <= NF; i++) {
        mount = mount (i == percent_column + 1 ? "" : " ") $i
      }

      status = used > 90 ? "CRIT" : used > 80 ? "WARN" : "OK"
      printf "%s\t%s%%\t%s\n", mount, used, status
    }
  ' <<< "$disk_output")

  if [[ -n $disk_rows ]]; then
    while IFS=$'\t' read -r mount usage status; do
      print_row "Disk ($mount)" "$usage used" "$status"
    done <<< "$disk_rows"
  else
    print_row "Disk" "no eligible filesystems" "CRIT"
  fi
else
  print_row "Disk" "df unavailable" "CRIT"
fi

for service in nginx docker cron; do
  service_state=""
  if service_state=$(systemctl is-active "$service" 2>/dev/null); then
    if [[ $service_state == "active" ]]; then
      print_row "Service ($service)" "$service_state" "OK"
    else
      print_row "Service ($service)" "$service_state" "CRIT"
    fi
  else
    print_row "Service ($service)" "${service_state:-unavailable}" "CRIT"
  fi
done

case "$overall_status" in
  0)
    printf 'OVERALL: OK\n'
    exit 0
    ;;
  1)
    printf 'OVERALL: WARN\n'
    exit 1
    ;;
  2)
    printf 'OVERALL: CRIT\n'
    exit 2
    ;;
esac
