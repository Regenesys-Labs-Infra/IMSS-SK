# Disk-full troubleshooting checklist

**Scope:** Read-only checks for the synthetic scenario in `scenario_disk_full.md`. No commands were run against `srv-fin-app-02`.

The supplied `df -h` output shows `/var` at 96% with 2.1 GB available, while `/` is at 49%. The `finapp` service is running but reports that writes to `/var/log/finapp/report.log` fail with “No space left on device”.

**ASSUMPTION:** Log rotation may not have freed space as expected; the supplied evidence does not establish whether logrotate is enabled or which files consume most of `/var`.

| Step | Command | Why | Expected result |
|---|---|---|---|
| 1 | `df -h /var` | Confirm current capacity on the affected mount. | `/var` usage and free space; compare with the supplied 96% and 2.1 GB. |
| 2 | `du -xhd1 /var` | Identify which immediate directories use space without crossing filesystems. | Largest directories under `/var`; this does not identify safe deletion candidates by itself. |
| 3 | `find /var/log/finapp -xdev -type f -printf '%s %p\n' \| sort -nr \| head -10` | List the largest files in the known application log directory. | File sizes and paths for review; do not delete or truncate them. |
| 4 | `journalctl -u finapp --since "24 hours ago" --no-pager` | Establish when write failures began and whether other service errors are present. | Relevant `finapp` journal entries, including any repeated disk-space errors. |
| 5 | `systemctl status finapp --no-pager` | Confirm service state and the reported log-write failure. | Current service state and recent messages; the supplied excerpt says active (running). |
| 6 | `systemctl list-timers --all --no-pager \| grep -i logrotate` | Check whether a logrotate timer is listed and when it last ran. | A matching timer if configured; no match is inconclusive and should be investigated. |
| 7 | `df -h /var` and `systemctl status finapp --no-pager` | Recheck after any separately approved maintenance. | Free space and service state should improve; verify logs before closing the incident. |

## Human approval and validation

No cleanup command is included. First review the file listing, identify owners and retention requirements, check backups, and obtain the required human/change approval. Only then should an approved cleanup plan be executed and verified.

## Errors and uncertainties to watch for

- The ticket says “Portal very slow”, but the scenario’s CI is `srv-fin-app-02`, which the CMDB maps to Finance Reporting and `LINUX-L2`. Confirm the affected CI and business impact before routing; do not infer a portal CI from the ticket wording.
- A response that assumes `report.log` is the only space consumer or recommends deleting logs before listing and approval is unsupported and unsafe. The checklist corrects this by inspecting usage first and reserving cleanup for an approved plan.
- The naive prompt and two-model comparison were not run because Copilot Chat and its model picker are not accessible in this session. No model output is represented here as observed.
