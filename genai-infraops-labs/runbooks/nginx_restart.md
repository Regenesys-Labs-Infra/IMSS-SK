# Runbook: Restart nginx on a web node
| Field | Value |
|---|---|
| Applies to | Ubuntu 22.04 web node running nginx; confirm target host [VERIFY] |
| Owner group | Web or infrastructure operations [VERIFY] |
| Risk | Medium |
| Approval needed | Yes — obtain the required change approval before restarting |

## 1. Purpose

Restore the site when users report that it is down, following SOP-OPS-014. This runbook
does not include cache clearing: the SOP gives no cache path or safe procedure.

## 2. Pre-checks (read-only)

1. Confirm users report that the site is down; the source SOP says not to restart nginx
   for other symptoms.
2. Confirm the affected CI is the intended web node and record the incident and change
   reference [VERIFY].
3. Confirm the required human/change approval is recorded.
4. Check the nginx service state:
   `sudo systemctl status nginx --no-pager`
   Expected: current service state and recent messages are displayed; record them.
5. Test the nginx configuration:
   `sudo nginx -t`
   Expected: configuration syntax is OK and the test is successful. Stop and escalate
   if the test fails.
6. Obtain the site owner's approved health-check URL [VERIFY]; do not guess a URL.

## 3. Steps (numbered, one action each, exact command)

1. Confirm all pre-checks passed and the approval covers this restart.
2. Restart nginx:
   `sudo systemctl restart nginx`
3. Check whether nginx is active:
   `systemctl is-active nginx`
   Expected: `active`.

## 4. Verification (command + expected result)

1. Recheck service status:
   `sudo systemctl status nginx --no-pager`
   Expected: `Active: active (running)` with no new failure reported.
2. Check the site using the health-check URL supplied by the site owner [VERIFY].
   After replacing the placeholder with that approved URL, run:
   `curl --silent --show-error --output /dev/null --write-out 'HTTP %{http_code}\n' --max-time 10 '<approved-health-check-URL>'`
   Expected: the HTTP status meets the success condition defined by the site owner; the
   SOP does not specify a URL or HTTP status. Do not run with the placeholder unchanged.
3. Confirm with the caller or application team that the site is usable.

## 5. Rollback

A service restart does not change configuration and has no direct rollback command. If
nginx does not return to service or the site remains unavailable, do not repeat the
restart or clear cache. Capture read-only diagnostics and escalate. Restoring a
configuration or cache requires a separate, approved procedure and is outside this SOP.

## 6. Escalate when

1. The affected host, approval, or health-check URL cannot be confirmed [VERIFY].
2. `nginx -t` fails or `systemctl is-active nginx` does not return `active`.
3. The site remains unavailable after the approved restart; the SOP says to contact the
   application team. Confirm its current contact and escalation route [VERIFY].

## 7. Change history

- 2026-11-24: Drafted from SOP-OPS-014 for review. No service command was run.
- Cache clearing is intentionally excluded because the source provides no path or safe
  procedure.
