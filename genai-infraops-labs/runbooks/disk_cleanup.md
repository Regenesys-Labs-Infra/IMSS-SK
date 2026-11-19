# Runbook: Low disk space on /var (L2)
1. `df -h /var` and `du -xh /var --max-depth=2 | sort -h | tail -15` (read-only).
2. Check logrotate status: `cat /var/lib/logrotate/status | grep finapp`.
3. If application logs are large and logrotate is misconfigured, raise a standard change to fix the config.
4. Compress (do not delete) logs older than 7 days: `sudo find /var/log/finapp -name "*.log" -mtime +7 -exec gzip {} \;` - approval needed.
5. Verify: `df -h /var` below 80%.
Escalate to LINUX-L2 lead when: usage grows again within 24 h.
