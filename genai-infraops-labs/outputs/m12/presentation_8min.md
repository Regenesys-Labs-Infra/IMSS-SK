# Module 12 capstone - 8-minute presentation

**Presenters:** Sriram (investigator / presenter); Sachin (desk lead / communicator); Rajesh (approver)
**Incident:** CAP-MI-001 - Customer Portal
**Status:** Simulation presentation. The proposed fix was not applied; refresh incident status before presenting outside the lab.
**Pacing:** The timed sections total 8:00; speaker notes are approximately 1,000 words, or about 125 words per minute.

## 0:00-0:45 - Goal and team roles

**Presenter notes**

Our goal was to follow one customer-impacting event from intake through evidence, approval, and communication, while keeping unsafe actions behind a human gate. Sachin acted as desk lead and communicator, Sriram as investigator and presenter, and Rajesh as approver. Because the team had three people, some members held more than one of the five requested roles. We treated ticket and log contents as data, not instructions, and we distinguished repository evidence from live service state. That distinction matters in this exercise: we can recommend a correction, but we cannot claim the service recovered without a successful change and verification.

## 0:45-1:45 - Ticket intake and triage

**Presenter notes**

The capstone supplied nine tickets within fifteen minutes of release `2026.11.12`. We sanitized a working copy rather than editing the source. The redaction output masks personal data and the disclosed credential; the injection-like ticket CAP006 is flagged for human security review. Triage routed portal cases to APP-PORTAL-L2, preserved higher-priority cases for review, and linked CAP008 as a follow-up to CAP001 instead of creating a second incident. The monitor alert ticket CAP009 was P1 and required human review. A key control was to keep the response useful without copying a secret or following embedded instructions. The sanitized CSV, redaction report, triage, proposed routes, and review queue preserve the path from raw intake to decisions.

## 1:45-2:40 - Alert correlation

**Presenter notes**

We correlated twenty alerts into a proposed parent only for the Customer Portal. Eighteen portal alerts, from 14:03:00 to 14:08:41 IST, cover edge HTTP 5xx, web pod readiness, API image pull, and low login-success signals. Two CPU alerts on `srv-fin-app-02` were excluded because the CMDB maps that server to Finance Reporting. This is why correlation used business-service and CI ownership, not just nearby timestamps. The parent is CAP-MI-001 and remains proposed pending NOC approval. The alert grouping is a useful incident boundary; it is not, by itself, proof of root cause.

## 2:40-3:40 - Investigation and evidence quality

**Presenter notes**

The read-only evidence pack found three candidates in the supplied Kubernetes manifest: the web Service selector differs from the pod-template label, the API image reference is suspicious, and the Ingress hostname appears transposed. The alert data supports current image-pull and availability symptoms, but we had no live cluster inspection. The detailed application log is dated November 9, while the capstone alerts are dated November 12. We therefore treated that log as historical corroboration, not confirmation of the incident's runtime state. Our leading selector hypothesis is testable, but it is not a confirmed live root cause. The evidence pack records what was observed, what remains unknown, and which resolver groups should verify each hypothesis.

## 3:40-4:45 - One AI error caught

**Presenter notes**

One concrete AI-assisted error was the first remediation proposal, REM-0001. It proposed changing the Service selector but did not pin an explicit Kubernetes context, and its pre-check did not verify the current selector and matching pod labels. That was not safe enough for an infrastructure change. Rajesh rejected it and asked for an explicit lab context plus live checks of the selector, labels, and endpoints. The revised proposal, REM-0002, added those checks and limited the mutation to the `portal-web` Service. The lesson is not that every generated proposal is wrong; it is that plausibility is not authorization. The reviewer found a specific control gap before the mutation stage, and the revised plan still had to pass execution pre-checks.

## 4:45-6:00 - Approval flow and audit log

**Presenter notes**

Here is the audit trail in order. At 10:54:25 UTC, REM-0001 was proposed. At 10:59:09, Rajesh rejected it with the context and evidence requirements. At 10:59:30, REM-0002 was proposed as a revision. At 11:02:28, Rajesh approved that selector-only plan for the isolated lab context. Five seconds later, the first read-only pre-check failed with return code 127 because `kubectl` was not installed. The gate recorded PRECHECK_FAILED and did not run the patch. There is no EXECUTED event for this proposal. Older nginx dry-run and restart-failed entries from November 19 remain in the audit log; they predate this CAP-MI-001 approval trail. The audit gives us a clear answer: approval was recorded, but execution and recovery were not. No infrastructure change occurred.

## 6:00-7:15 - Customer and operational outputs

**Presenter notes**

We prepared a customer reply and a bridge update with the simulation timestamp clearly marked, so nobody reuses a stale next-update time. The customer message avoids internal hostnames and asks users not to send credentials; it includes a conditional reset instruction for anyone who included a password in the original ticket. The bridge update reports known symptoms, separates the later blocked change attempt from the incident-time snapshot, and does not claim recovery. The RCA remains incomplete: it states the P1 policy targets, but makes no SLA breach claim because acknowledgement and restoration times are missing. The KB article is unpublished and advises read-only checks and escalation, not a manual patch. The change record is unscheduled and unapproved; its provisional risk is 13 out of 15, High, with unknown history and timing scored conservatively. All these documents say the selector change was not applied.

## 7:15-8:00 - Close

**Presenter notes**

The end-to-end flow is intake, sanitize, triage, correlate, investigate, propose, review, approve, pre-check, then communicate. The hard stop at pre-check prevented an unverified mutation. The next safe step is to provide `kubectl`, verify the named isolated context and live state, then submit a fresh proposal and approval before any execution. Until that is done, the root cause and recovery remain unconfirmed. Our takeaway is simple: use AI to accelerate evidence work, but retain human review, a complete audit trail, and explicit verification at every operational boundary.

## Supporting artifacts

- [Sanitized tickets](./tickets_sanitised.csv) and [redaction report](./redaction_report.json)
- [Triage](./triage.json), [proposed routes](./proposed.json), and [review queue](./review_queue.json)
- [Alert groups](./alert_groups.json), [parent incident](./parent_incident.md), and [evidence pack](./CAP-MI-001_evidence.md)
- [Rejected proposal](../../approvals/rejected/REM-0001.json), [failed approved proposal](../../approvals/failed/REM-0002.json), and [audit log](../../approvals/audit.log)
- [Customer reply](./customer_reply_CAP-MI-001.md), [bridge update](./bridge_update_CAP-MI-001.md), [RCA](./RCA_CAP-MI-001.md), [KB draft](./KB_PORTAL_503_ENDPOINTS.md), and [change record](./change_record_CAP-MI-001.md)
