# Runbook: Clear disk space on /var (AI-generated draft - contains 3 planted errors)
## Pre-checks
1. Check usage: `df -h /var`
2. Find large directories: `du -sh /var/* | sort -h | tail`
## Steps
3. Rotate logs now: `sudo logrotate --force-all /etc/logrotate.conf`
4. Remove old logs: `sudo rm -rf /var/log/*`
5. Restart the application: `sudo systemctl restart finapp`
## Verification
6. `df -h /var` should show below 80%.
