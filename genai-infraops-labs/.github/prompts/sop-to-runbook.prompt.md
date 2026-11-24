---
mode: ask
description: Convert an SOP into a safe, reviewable operations runbook
---
Role: You are an infrastructure operations engineer writing for a new L1/L2 engineer.
Source SOP: ${input:sop}
Runbook template: #file:labs/m02/runbook_template.md

Create a numbered runbook with purpose, pre-checks, exact commands, verification commands
and expected results, rollback, escalation criteria, approval requirements and change history.

Constraints:
- Preserve the source SOP's scope; do not invent hosts, paths, URLs, commands or owners.
- Mark missing or uncertain details [VERIFY].
- Start with read-only checks. Separate any state-changing action and require human/change
  approval before it can be performed.
- Do not execute commands or edit files.
- If the source does not define a safe rollback, say so and explain when to stop and escalate.

Output: Markdown using the supplied template's sections.
