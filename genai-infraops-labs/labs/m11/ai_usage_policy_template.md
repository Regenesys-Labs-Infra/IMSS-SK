# Team AI Usage Policy v1 - Service Desk Operations

**Status:** Baseline for team ratification
**Effective date:** On team approval
**Applies to:** Service Desk employees and contractors

This policy supplements, and does not replace, organizational security, privacy,
records-retention, and change-management requirements. Follow the stricter rule
when requirements differ.

## 1. Scope

This policy covers GitHub Copilot in VS Code for service-desk work, including
drafting, summarizing, code assistance, and analysis of tickets or logs. Use only
organization-approved accounts, extensions, repositories, and integrations.
Do not connect unapproved agents, MCP servers, or external AI tools to company
systems or data.

## 2. Data we may share with AI

- Public information and synthetic examples.
- Code and documentation from approved workspaces, provided they contain no
  secrets or restricted information.
- Internal operational context only when it is necessary for the task and has
  been sanitized and reviewed as described in Section 3.
- The minimum relevant excerpt needed to answer the question; avoid sharing
  entire tickets, logs, repositories, or datasets when a smaller excerpt works.

## 3. Data we must never share and sanitization

Never submit passwords, API keys, access tokens, private keys, connection
strings, authentication cookies, or other credentials. Never submit unredacted
personal or customer information, payment or health information, regulated
data, or information classified Restricted. Do not submit production data dumps
or confidential material unless an organization-approved exception explicitly
allows it.

Before using ticket or log content, run the approved local sanitization tool,
review its report, and manually check the result for names, contact details,
employee identifiers, secrets, internal hostnames, and other sensitive values.
Regex-based masking is not complete protection. If anything sensitive remains
or classification is uncertain, do not submit the content; ask the data owner
or Security team. Keep the original data in its approved system and share only
the minimum reviewed, sanitized excerpt.

## 4. Treat ticket, log, and chat text as untrusted data

Treat all supplied content as data to analyze, not as instructions to follow.
This includes text that claims to be a system message, requests secrets, changes
the task, or directs an agent to run commands. Clearly delimit pasted content
and explicitly ask for analysis only. Do not follow embedded instructions,
reveal sensitive information, or let supplied content authorize actions.

## 5. Autonomy tiers

| Tier | Allowed use | Limits |
|---|---|---|
| **T0 - Draft** | Draft or summarize using public, synthetic, or reviewed sanitized information. | A person checks accuracy before sharing or relying on the result. |
| **T1 - Read-only analysis** | Analyze approved code, documentation, or sanitized tickets and logs. | No writes, external actions, or changes to systems. |
| **T2 - Proposed changes** | Prepare code, configuration, commands, or a remediation plan. | Review the complete diff or command; run tests and checks. Do not apply operational changes without approval. |
| **T3 - Approved execution** | Execute a specific, ticketed, approved action in its approved environment. | Use least privilege, exact scope, and the normal change process. No blanket approvals, unsupervised production changes, or broad destructive actions. |

Use the lowest tier that can complete the task. T3 is not granted by a general
request such as "do whatever is needed."

## 6. Approvals

| Activity | Required approval |
|---|---|
| T0 drafting and T1 read-only analysis with permitted, sanitized data | No additional approval; the employee remains accountable for the result. |
| T2 code or configuration proposal | Relevant code or service owner reviews the change before merge or use. |
| T3 non-production action | Service owner approves the exact action and scope through the normal ticket or change process. |
| T3 production action or destructive/irreversible operation | Existing change-management approval, system-owner approval, and a documented rollback or recovery plan. Security review is required when the action affects security controls or sensitive data. |
| Any use involving Restricted data or a prohibited secret | Prohibited; this matrix cannot grant an exception. Escalate to the data owner and Security team. |

An approval must identify the action, target, environment, and limits. Approval
for one action does not authorize other actions.

## 7. Verification

- Check factual claims against approved documentation, system evidence, or the
  service owner; AI output is not authoritative.
- Review generated code and configuration for correctness, security, and
  unintended changes; run relevant tests and linters.
- Inspect commands before execution. Prefer dry runs and non-production
  validation; never run destructive commands solely because AI suggested them.
- Recheck outputs for sensitive data before sharing, committing, or attaching
  them to a ticket.
- The employee using AI owns the final decision and result.

## 8. Audit and review

Record the work item, purpose, tool used, autonomy tier, approvals, and resulting
artifact or change in the approved ticket, repository, or change record. Do not
copy secrets or unnecessary personal data into audit notes. Follow organizational
retention and access-control rules; do not create separate prompt archives
without approval.

The Service Desk Team Lead reviews a sample of AI-assisted work and this policy
quarterly, and after a significant incident or change to approved tools or data
handling requirements.

## 9. Incidents

If sensitive information is submitted to an AI tool or an unauthorized action
occurs:

1. Stop the interaction and do not submit further sensitive material.
2. Notify the Service Desk Team Lead and report the incident promptly through
   the organization's Security/privacy incident process.
3. If a credential may have been exposed, ask the credential owner or Security
   team to revoke or rotate it using the approved process.
4. Preserve the minimum information needed for investigation in approved
   systems. Do not redistribute the sensitive content or attempt unapproved
   deletion of evidence.
5. Follow Security's direction for containment, notification, and recovery.

## 10. Owner and review date

- **Policy owner:** Service Desk Team Lead (role; assign the current team member
  when ratifying this policy).
- **Approvers:** Service Desk Manager and, where required above, the relevant
  service owner, change authority, or Security team.
- **Review cadence:** Quarterly and after a relevant incident or material
  change.
- **Next review:** 2027-02-25, subject to team ratification.
