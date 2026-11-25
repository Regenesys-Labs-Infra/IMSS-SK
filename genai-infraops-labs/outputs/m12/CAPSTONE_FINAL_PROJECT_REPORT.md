# Capstone Final Project Report

**Project:** Ticket-to-RCA Operations Assistant
**Incident:** CAP-MI-001 - Customer Portal
**Team branch:** `team/team-sachin`
**Report date:** 2026-11-25
**Delivery status:** Pull request #2 is open. The operational change is not applied; the incident root cause and recovery are not confirmed.

## Executive summary

The team completed the capstone's ticket intake, sanitization, triage, alert correlation, read-only investigation, approval workflow, and communication drafts. Nine tickets were sanitized and routed; twenty alerts were assessed, with eighteen Customer Portal alerts grouped into proposed parent CAP-MI-001 and two Finance Reporting alerts kept separate. The supplied manifest revealed a Service selector mismatch and two additional configuration concerns, but no live cluster inspection was available to confirm runtime cause.

The initial remediation proposal was rejected for inadequate context pinning and pre-checks. A revised selector-only proposal was approved, but its first read-only check failed because `kubectl` was unavailable. The patch did not run. The project therefore demonstrates a complete, auditable handoff up to the execution boundary, not a completed service repair.

## Team and responsibilities

| Member | Assigned roles |
|---|---|
| Sachin | Desk lead, communicator |
| Sriram | Investigator, presenter |
| Rajesh | Approver |

The three-person team shared the five requested roles by assigning multiple roles to some members.

## Project workflow and results

### 1. Ticket sanitization and triage

- Processed the nine capstone tickets using a sanitized working copy; the source CSV was left unchanged.
- Masked personal data and a disclosed credential, and recorded redaction categories in a report.
- Flagged CAP006 as injection-suspect and routed it for security review rather than following its embedded instruction.
- Linked CAP008 as a follow-up to CAP001; CAP009's critical monitoring alert was assigned P1 and kept for human review.
- Produced triage and routing outputs, including the review queue.

### 2. Alert correlation

- Assessed all twenty supplied alerts.
- Grouped eighteen Customer Portal alerts into proposed parent CAP-MI-001, covering 14:03:00-14:08:41 IST on 2026-11-12.
- Excluded CAPALR-018 and CAPALR-019 because their CI, `srv-fin-app-02`, maps to Finance Reporting.
- The parent remains `PROPOSED_PENDING_NOC_APPROVAL`; correlation establishes a useful incident boundary, not root cause.

### 3. Read-only investigation

The evidence pack records three configuration-level findings from the supplied manifest:

1. The `portal-web` Service selector is `app=portal-web-v2`, while the web pod-template label is `app=portal-web`.
2. The `portal-api` image reference is suspicious and capstone alerts report image-pull failures.
3. The Ingress host appears transposed; the canonical hostname and DNS state are unknown.

The detailed portal log is dated Nov 9, while the capstone alerts are dated Nov 12. The log is treated as historical corroboration, not proof of Nov 12 runtime state. No live Kubernetes or ITSM state was queried, so the selector mismatch remains a leading candidate rather than a confirmed incident root cause.

### 4. Approval workflow and audit trail

| Time (UTC, 2026-11-25) | Event | Result |
|---|---|---|
| 10:54:25 | REM-0001 proposed | Initial selector proposal lacked an explicit Kubernetes context and adequate live selector/label checks. |
| 10:59:09 | REM-0001 rejected by Rajesh | Required a pinned lab context and verification of selector, pod labels, and endpoints. |
| 10:59:30 | REM-0002 proposed | Revised selector-only plan added explicit context and pre-checks. |
| 11:02:28 | REM-0002 approved by Rajesh | Approval was for the isolated lab context and narrow Service change. |
| 11:02:33 | `PRECHECK_FAILED` | `kubectl` was unavailable (`rc=127`); the patch command did not run. |

There is no execution or verification success event for REM-0002. The audit log retains older nginx entries from Nov 19 as well as the capstone approval trail.

### AI error caught

The AI-assisted resolver's first proposal, REM-0001, lacked an explicit Kubernetes context and did not check both the live Service selector and matching pod labels before proposing a patch. Rajesh caught the gap and rejected the proposal before execution. The revised proposal added a pinned context and the required pre-checks; it still had to pass the execution gate, which correctly stopped when `kubectl` was missing.

### 5. Approval-gate improvements

Review of the approval tooling found it could rely on the active Kubernetes context and did not stop safely after every failed pre-check. The gate was updated to require explicit context and namespace for Kubernetes commands, stop and invalidate a plan on failed pre-checks, record failed execution or verification distinctly, and decline execution when interactive confirmation is absent. Three focused regression tests passed, covering failed pre-checks, failed verification, and missing explicit context.

### 6. Communication and change documentation

The team prepared a customer reply, bridge update, incomplete RCA, unpublished KB draft, and draft change record. They clearly distinguish facts from hypotheses and do not claim service recovery. The change record is unscheduled and unapproved; its provisional risk score is 13/15 (High), with conservative placeholders for unknown change history and timing. A timed eight-minute presentation script covers the workflow, the rejected proposal, and the audit log.

## Security, governance, and validation

- Ticket and log text was treated as untrusted data; the injection-like ticket was not followed.
- Sensitive ticket content was redacted from the working outputs.
- No infrastructure mutation occurred, and no live service state or recovery was asserted.
- Approval-gate regression tests: **3 passed** (`python3 -m unittest tools.test_approve -v`).
- Triage/remediation schema checks, approval-gate compilation, JSON validator self-test, document length checks, and relative-link checks passed.
- Repository whitespace validation passed with CRLF recognized for the generated CSV (`git -c core.whitespace=cr-at-eol diff --cached --check`).

## Outcome and remaining work

The project completed the privacy-safe intake, triage, correlation, evidence, approval review, audit, and documentation stages. The execution and service-verification objective remains **blocked**, not complete: `kubectl` was missing at the pre-check, so the Service selector was not changed and service recovery was not tested.

Before any future execution:

1. Provide `kubectl` in the controlled environment and verify the named isolated context and namespace.
2. Re-check live Service selector, pod labels, endpoints, API image-pull events, and the canonical Ingress host.
3. Submit a fresh remediation proposal and obtain fresh approval; do not reuse the failed plan.
4. Execute only after checks pass, then verify endpoints, customer-facing behavior, and monitoring.
5. Update the parent incident, RCA, KB article, and change record with verified outcome and timestamps; obtain NOC/CAB approvals where required.

## Deliverables

- [Sanitized tickets](./tickets_sanitised.csv), [redaction report](./redaction_report.json), [triage](./triage.json), [proposed routes](./proposed.json), and [review queue](./review_queue.json)
- [Alert groups](./alert_groups.json), [parent incident](./parent_incident.md), and [investigation evidence pack](./CAP-MI-001_evidence.md)
- [Rejected proposal](../../approvals/rejected/REM-0001.json), [failed approved proposal](../../approvals/failed/REM-0002.json), and [audit log](../../approvals/audit.log)
- [Customer reply](./customer_reply_CAP-MI-001.md), [bridge update](./bridge_update_CAP-MI-001.md), [RCA](./RCA_CAP-MI-001.md), [KB article](./KB_PORTAL_503_ENDPOINTS.md), and [change record](./change_record_CAP-MI-001.md)
- [Eight-minute presentation script](./presentation_8min.md)
- [Approval-gate implementation](../../tools/approve.py), [regression tests](../../tools/test_approve.py), and [Module 9 guidance](../../labs/m09/README.md)
- [Pull request #2](https://github.com/Regenesys-Labs-Infra/IMSS-SK/pull/2)
