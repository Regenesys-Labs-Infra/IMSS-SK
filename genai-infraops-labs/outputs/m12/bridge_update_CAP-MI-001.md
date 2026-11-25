# Bridge update - CAP-MI-001

**As at:** 2026-11-12 14:09 IST (capstone simulation; refresh before use)

## Status

Investigating; recovery is not verified.

## Customer impact

Multiple reports describe sign-in errors and slow or unavailable reports. Affected-user count and current state are unknown.

## What we know

- Eighteen critical portal alerts show edge HTTP 5xx, web readiness, API image-pull, and low login-success signals.
- The manifest shows a web Service/pod-label mismatch; the API image and Ingress host remain unverified.
- Nov 9 logs are historical, not proof of Nov 12 runtime state.

## Actions in progress

Evidence pack prepared. Proposed owners: APP-PORTAL-L2 (selector), K8S-PLATFORM-L3 (pods/image), LINUX-L2 (edge/Ingress). Live checks are not done.

## Decisions taken

Group 18 portal alerts as CAP-MI-001; route two Finance alerts separately.

## Next update

14:39 IST in the simulation; refresh before use.

## Post-event operational note (2026-11-25; not part of the 14:09 update)

The approved remediation attempt stopped at its pre-check because `kubectl` was unavailable. No cluster command ran and no change was applied.

## Customer-safe status-page text

We are investigating errors affecting portal sign-in and report access. We have not verified recovery; the next update will be provided by 14:39 IST.
