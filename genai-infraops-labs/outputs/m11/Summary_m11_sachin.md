# Module 11 Summary - Sachin

- **Module:** Guardrails, Governance & Secure AI Operations
- **Use case:** UC-02 - PII and secrets sanitisation gate
- **Date:** 2026-11-25

## Objective

Reduce the risk of exposing personal information, credentials, or prompt-injection
content when using AI for service-desk work. The workflow sanitizes ticket text,
flags suspicious instructions, and requires human review before AI use.

## Work completed

### Sanitizer and tests

Extended `tools/sanitise.py` with named patterns for:

- Indian mobile numbers, including optional `+91` and common spaces or hyphens.
- `HM-######` employee IDs.
- AWS access-key IDs and AWS secret keys.
- Bearer and JWT tokens.
- Windows UNC paths.
- Passwords in connection strings.

The sanitizer replaces matches with typed placeholders and records detected
categories in the redaction report. A correction also covers AWS secrets written
as `secret <value>`, without an equals sign or colon.

Added focused regression tests in `tools/test_sanitise.py`.

### Sanitized ticket output

Regenerated:

- `outputs/m11/raw_tickets_pii_sanitised.csv`
- `outputs/m11/redaction_report.json`

The report records detected categories and flags ticket `INC0010247` as
`INJECTION_SUSPECT`. The final run masked the AWS secret and formatted mobile
numbers that had appeared unredacted in the earlier output.

### Safe prompt rewrites

Rewrote all five examples in `labs/m11/unsafe_prompts.md` to address:

1. Credentials in troubleshooting requests.
2. Untrusted instructions embedded in tickets.
3. Broad agent permissions.
4. Customer contact information.
5. Destructive, fleet-wide log deletion.

The alternatives use sanitized placeholders, read-only analysis, dry runs, and
explicit approvals.

### AI usage policy

Completed `labs/m11/ai_usage_policy_template.md` as a role-based Service Desk
policy covering allowed and prohibited data, sanitization, untrusted content,
autonomy tiers, approvals, verification, audit, and incident response. It is a
baseline for team ratification; no specific team members or approvers were
provided.

## Verification

- `.venv/bin/pytest -q tools/test_sanitise.py` - **12 passed**.
- Regenerated the sanitized CSV and confirmed the tested AWS-secret and
  Indian-mobile patterns no longer match its contents.
- The documented known-secret grep check reported **No secrets found**.

Regex-based sanitization is not exhaustive. A reviewer must inspect the output
and sign the redaction checklist before any ticket content is used with AI.

## Deliverables

- `tools/sanitise.py`
- `tools/test_sanitise.py`
- `outputs/m11/raw_tickets_pii_sanitised.csv`
- `outputs/m11/redaction_report.json`
- `labs/m11/unsafe_prompts.md`
- `labs/m11/ai_usage_policy_template.md`
