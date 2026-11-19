# Module 2: GitHub Copilot for Infrastructure Engineers

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 1 | Session 1 | 0.25 h | 1.75 h | Demo + Hands-On Lab |

Participants turn Copilot into a team asset: runbooks from SOPs, explained commands, team instructions and reusable prompt files stored in Git.

## What you will learn

- Convert a standard operating procedure into an automation-ready runbook with pre-checks and rollback.
- Explain Linux, Kubernetes and cloud commands using inline chat and terminal chat (/explain).
- Create .github/copilot-instructions.md and reusable prompt files for the team.
- Build the habit of verifying every AI-generated step before use.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| SOP | Standard Operating Procedure: a written, approved way to do a routine task. |
| Runbook | A step-by-step operational guide with pre-checks, the exact commands, how to verify success and how to roll back. |
| Pre-check / Rollback | Pre-check: what you confirm before changing anything. Rollback: how to return to the previous state if the change fails. |
| Inline chat | Press Ctrl+I (Cmd+I on Mac) in the editor or terminal to ask Copilot about the selected code or command, right where you are working. |
| Slash command | Shortcuts in Copilot Chat: /explain (explain this), /fix (fix the problem), /tests (write tests), /doc (write documentation). |
| copilot-instructions.md | A file in .github/ containing team rules that Copilot automatically follows in every chat in this repository (tone, safety rules, formats). |
| Prompt file | A saved, reusable prompt (.github/prompts/name.prompt.md). Run it by typing /name in Copilot Chat, so the whole team uses the same proven prompt. |
| KB article | Knowledge Base article: a published how-to that lets L1 solve a known issue without escalating. |
| Pull request (PR) | A request on GitHub to merge your branch into a shared branch. Teammates review the changes before they are merged. |
| ITIL 4 | The widely used framework for IT Service Management: Incident, Service Request, Problem, Change and Knowledge Management practices. |

## Real-time Service Desk use case UC-03: Ticket-to-KB knowledge generation

| | |
|---|---|
| Persona | L1/L2 agents, Knowledge Manager |
| Problem statement | VPN failures, password resets, mailbox-full and AD lockouts are solved daily, but resolution notes stay inside closed tickets. The KB is stale, so L1 escalates issues that were already solved. |
| What AI does | Groups resolved tickets, drafts KB articles in the standard template, flags overlap with existing articles and marks any step it cannot trace to a ticket as [VERIFY]. |
| Human review checkpoint | Engineer validates each step against the resolution notes; Knowledge Manager approves and publishes. |
| Output asset | KB article library and ticket-to-kb prompt file |
| KPI impact | KB reuse rate, First Contact Resolution |

## Hands-on labs

### Lab 2.1: SOP to automation-ready runbook (40 min)

**Objective:** Turn a nginx restart SOP into a runbook a new engineer can follow safely.

**Files:** `labs/m02/sop_nginx_restart.md`, `labs/m02/runbook_template.md`, `labs/m02/runbook_with_errors.md`

**Steps**

1. Open labs/m02/sop_nginx_restart.md and labs/m02/runbook_template.md side by side.
2. Switch Copilot Chat to Edit mode, add both files to the working set and ask:

   Copilot Chat prompt:

   ```text
   Convert #file:labs/m02/sop_nginx_restart.md into a runbook using the structure of #file:labs/m02/runbook_template.md.
   Save it as runbooks/nginx_restart.md. Add pre-checks, verification commands with expected output,
   a rollback section and escalation criteria. Number every step.
   ```

3. Review the proposed change and Accept or Discard. Accept only what you have read.
4. In the terminal, run one command from the runbook (for example systemctl status nginx), select the output, press Ctrl+I and type /explain.
5. Open labs/m02/runbook_with_errors.md. Without Copilot first, find the 3 planted errors. Then ask Copilot to review it and compare.

**Expected result:** runbooks/nginx_restart.md with pre-checks, steps, verification, rollback and escalation.

**Check before you finish**

- [ ] Every command exists and is correct for Ubuntu 22.04
- [ ] Rollback present
- [ ] 3 planted errors found

**If something goes wrong**

- Edit mode only changes files you added to the working set.
- If Copilot invents a config path, check it on the VM with ls before accepting.

**Deliverable:** runbooks/nginx_restart.md plus a short list of errors found.


### Lab 2.2: Team instructions and prompt library v1 (30 min)

**Objective:** Create the shared Copilot configuration that every later lab uses.

**Files:** `.github/copilot-instructions.md`, `.github/prompts/`

**Steps**

1. Open .github/copilot-instructions.md (a starter is provided). Read the rules and add one rule of your own for your team.
2. Look at .github/prompts/ticket-first-response.prompt.md - this is the format of a prompt file (front-matter, then the prompt with ${input:...} variables).
3. Create .github/prompts/explain-command.prompt.md with Copilot's help:

   Copilot Chat prompt:

   ```text
   Create a prompt file .github/prompts/explain-command.prompt.md (mode: ask) that takes ${input:command}
   and explains it for an L1 engineer: what it does, each flag, risk level (read-only / changes state), safer alternative.
   ```

4. Do the same for sop-to-runbook and troubleshooting-checklist. Run each one by typing /explain-command, /sop-to-runbook, /troubleshooting-checklist in Copilot Chat.
5. Commit, push, and open a pull request from your branch to team/main on GitHub; ask a neighbour to review.

**Expected result:** Prompt library v1 (5 prompt files) and team instructions in the repository.

**Check before you finish**

- [ ] Each prompt file runs from the / menu
- [ ] Prompts include output format and safety constraints
- [ ] PR opened

**If something goes wrong**

- Prompt files not visible in / menu: confirm the file ends with .prompt.md and is in .github/prompts/.

**Deliverable:** Prompt library v1 merged into the team branch.


### Lab 2.3: Ticket-to-KB article generation (35 min)

**Objective:** Turn resolved tickets into knowledge articles (Service Desk use case UC-03).

**Files:** `data/tickets/tickets_history.csv`, `data/kb/`, `.github/prompts/ticket-to-kb.prompt.md`

**Steps**

1. List the VPN tickets to see the raw material:

   Terminal:

   ```bash
   python3 -c "import pandas as pd; d=pd.read_csv('data/tickets/tickets_history.csv'); print(d[d.category=='VPN'][['number','short_description','resolution_notes']].head(15).to_string())"
   ```

2. Run the prompt file for each category (Edit mode). Type the category when asked:

   Copilot Chat prompt:

   ```text
   /ticket-to-kb   (category: VPN, then Email, then Account lockout)
   ```

3. Compare with the existing article:

   Copilot Chat prompt:

   ```text
   Compare #file:outputs/kb/KB_VPN.md with #file:data/kb/KB0001_vpn_basic.md. List overlaps, contradictions and what to keep.
   ```

4. Swap articles with a neighbour. As Knowledge Manager, find at least one step that is not supported by a source ticket.

**Expected result:** 3 KB articles under outputs/kb/ that cite source ticket numbers.

**Check before you finish**

- [ ] Each step traceable to a ticket
- [ ] Escalation criteria present
- [ ] No user names or secrets

**If something goes wrong**

- If the article cites ticket numbers that are not in the CSV, that is a hallucination - remove them.

**Deliverable:** 3 publish-ready KB articles under outputs/kb/.


## Save your work

```bash
git add -A
git commit -m "Module 2 labs"
git push
```
