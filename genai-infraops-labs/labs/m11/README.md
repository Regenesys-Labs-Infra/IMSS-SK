# Module 11: Guardrails, Governance & Secure AI Operations

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 3 | Session 6 | 0.25 h | 0.75 h | Governance Lab |

Participants consolidate the guardrails used throughout the course into a team AI usage policy and a governance checklist for production use.

## What you will learn

- Classify data and decide what may be shared with Copilot.
- Sanitise tickets and logs before AI use and detect prompt injection.
- Configure Copilot-native controls: content exclusion, tool approval, workspace trust.
- Define production guardrails and an AI governance policy.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| PII | Personally Identifiable Information: names, emails, phone numbers, employee IDs and similar. |
| Secret | A password, API key, token or connection string that grants access. Never paste secrets into AI tools. |
| Redaction / masking | Replacing sensitive values with placeholders such as <EMAIL_1> before data is shared. |
| Regular expression (regex) | A text pattern used to find things like email addresses or phone numbers automatically. |
| Data classification | Labelling data as Public, Internal, Confidential or Restricted to decide how it may be used. |
| Content exclusion | A GitHub Copilot setting that prevents chosen files or folders from being used by Copilot. |
| Workspace trust | A VS Code safety feature: untrusted folders run in restricted mode until you trust them. |
| AI usage policy / governance | The team's agreed rules for using AI safely, and the controls and reviews that make sure they are followed. |

## Real-time Service Desk use case UC-02: PII and secrets sanitisation gate

| | |
|---|---|
| Persona | All desk roles |
| Problem statement | Callers paste passwords, phone numbers, employee IDs and API keys into tickets. Pasting such a ticket into an AI tool creates a data-handling incident. |
| What AI does | Copilot helps extend detection patterns and tests; the script masks values with typed tokens and flags injection text. |
| Human review checkpoint | Reviewer signs the redaction report before the file is used with AI. |
| Output asset | sanitise.py, redaction checklist, team AI usage policy |
| KPI impact | Sensitive data shared with AI tools: zero |

## Hands-on labs

### Lab 11.1: Sanitisation gate and AI usage policy (45 min)

**Objective:** Build the sanitise-before-AI step and finalise the team policy (UC-02).

**Files:** `data/tickets/raw_tickets_pii.csv`, `tools/sanitise.py`

**Steps**

1. Run the baseline sanitiser and note what is missed:

   Terminal:

   ```bash
   python3 tools/sanitise.py data/tickets/raw_tickets_pii.csv --report --out outputs/m11/
   ```

2. Select the PATTERNS dictionary in tools/sanitise.py, press Ctrl+I:

   Copilot Chat prompt:

   ```text
   Add named patterns for Indian mobile numbers (+91 optional), employee IDs HM-######, AWS access keys,
   AWS secret keys, bearer/JWT tokens, Windows UNC paths and connection-string passwords.
   ```

3. Generate tests with /tests (save as tools/test_sanitise.py) and run them; re-run the sanitiser and confirm nothing sensitive remains:

   Terminal:

   ```bash
   pytest -q tools/test_sanitise.py
   python3 tools/sanitise.py data/tickets/raw_tickets_pii.csv --report --out outputs/m11/
   grep -E "Welcome@|AKIA|Summer2026|eyJ" outputs/m11/*.csv || echo "No secrets found"
   ```

4. Rewrite the 5 unsafe prompts in labs/m11/unsafe_prompts.md into safe versions.
5. Complete labs/m11/ai_usage_policy_template.md as a team and commit it.

**Expected result:** No secrets in the sanitised output; INC0010247 flagged INJECTION_SUSPECT; team AI usage policy v1.

**Check before you finish**

- [ ] grep finds nothing
- [ ] Tests pass
- [ ] Policy covers data, prompts, agents, approvals

**Deliverable:** Sanitiser with tests, AI usage policy and governance checklist.


## Save your work

```bash
git add -A
git commit -m "Module 11 labs"
git push
```
