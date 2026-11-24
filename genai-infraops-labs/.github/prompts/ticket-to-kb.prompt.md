---
mode: edit
description: UC-03 Turn resolved tickets into a KB article in the team template
---
Using the resolved tickets for category "${input:category}" in #file:data/tickets/tickets_history.csv,
write a KB article to outputs/kb/KB_${input:category}.md with exactly these sections:
Title · Symptoms (user's words) · Applies to · Cause · Resolution steps (L1) · Escalate when · Keywords · Source tickets
Rules: every resolution step must come from at least one resolution_notes entry - cite the ticket numbers.
Steps you cannot trace: mark [VERIFY]. No user names, passwords or personal data.
Audience: a new L1 agent who must follow it in under 2 minutes.
