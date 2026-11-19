# Module 1: Gen AI for Infrastructure Operations

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 1 | Session 1 | 0.5 h | 0.5 h | Concept + Guided Lab |

Participants understand how large language models behave in operations work and set up their GitHub Copilot workbench in VS Code inside the lab VM.

## What you will learn

- Explain tokens, context window, hallucination and non-determinism in operational terms.
- Use Copilot Chat in Ask, Edit and Agent modes and choose a model in the model picker.
- Write structured prompts (role, context, constraints, output format) for infrastructure scenarios.
- Apply the team's safe-AI rules: what may and may not be shared with Copilot.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Large Language Model (LLM) | The AI engine behind Copilot. It has read huge amounts of text and code and predicts the most likely next words. It does not 'know' your servers - it only knows what you show it. |
| Prompt | The instruction you type to the AI. A good prompt says who the AI should act as, what information to use, what to produce and in what format. |
| Token | A small piece of text (about 3/4 of a word). Models read and write in tokens, and every model has a limit on how many it can handle at once. |
| Context window | How much text the model can 'see' in one go: your prompt, attached files and its own answer. Anything outside the window is invisible to it. |
| Hallucination | When the AI states something that sounds correct but is invented - a command flag, a hostname, a KB number. This is why every lab has a verification step. |
| GitHub Copilot | The AI assistant built into VS Code. It suggests code as you type (inline suggestions) and answers questions in the Copilot Chat panel. |
| Ask / Edit / Agent mode | Three Copilot Chat modes. Ask = answers questions, changes nothing. Edit = proposes changes to the files you choose; you accept or reject. Agent = plans multi-step work, edits files and runs commands, asking your approval for each tool or command. |
| Model picker | The drop-down in Copilot Chat that selects which AI model answers. Different models can give different answers to the same prompt. |
| #file, @workspace, @terminal | Ways to give Copilot context. #file attaches a file, @workspace lets it search the repository, @terminal lets it read your terminal output. |
| Synthetic data | Realistic but invented tickets, logs and users created for training. We never use real customer data, passwords or production systems in labs. |
| CMDB / CI | Configuration Management Database: the list of IT assets. Each asset (server, app, printer) is a Configuration Item (CI) with an owner group. |
| MTTA / FCR | Mean Time To Acknowledge: how long before someone starts working a ticket. First Contact Resolution: % of tickets solved at the first contact without escalation. |

## Real-time Service Desk use case UC-01: Smart ticket intake and first response

| | |
|---|---|
| Persona | L1 Service Desk agent |
| Problem statement | Tickets such as "Portal very slow, disk full error, pls fix urgent!!" arrive with no CI, error text or business impact. L1 spends 2-3 email cycles collecting basics, MTTA rises and tickets are often routed to the wrong group. |
| What AI does | Copilot summarises the ticket in 3 lines, lists missing facts as up to 4 questions, drafts a first response (max 120 words) and proposes a read-only first-response checklist. |
| Human review checkpoint | L1 agent checks the summary, removes questions the CMDB already answers, edits and sends the reply. |
| Output asset | Reusable prompt file .github/prompts/ticket-first-response.prompt.md |
| KPI impact | MTTA, First Contact Resolution |

## Hands-on labs

### Lab 1.1: Workbench set-up and repository clone (10 min)

**Objective:** Confirm VM access, VS Code, Copilot sign-in and the course repository.

**Files:** `setup/check_env.sh`, `README.md`

**Steps**

1. Log in to your lab VM (browser or SSH) and open VS Code. Sign in to GitHub (Accounts icon, bottom-left) and confirm the Copilot icon in the status bar is active (not crossed out).
2. Open a terminal in VS Code (Terminal > New Terminal) and clone the course repository. Your trainer shares the URL.

   Terminal:

   ```bash
   cd /opt/genai-infra-labs
   git clone <course-repository-url> genai-infraops-labs
   cd genai-infraops-labs
   git checkout -b participant/<your-name>
   code -r .
   ```

3. When VS Code asks whether you trust the authors of this folder, choose Yes (workspace trust).
4. Check your tools:

   Terminal:

   ```bash
   ./setup/check_env.sh
   ```

5. Open Copilot Chat (Ctrl+Alt+I), choose Ask mode and run:

   Copilot Chat prompt:

   ```text
   @workspace Explain the structure of this repository in a table: folder, purpose, which module uses it.
   ```

6. Write your check result to labs/m01/README-result.md, then commit and push:

   Terminal:

   ```bash
   git add labs/m01/README-result.md
   git commit -m "M1 Lab 1.1 environment check"
   git push -u origin participant/<your-name>
   ```


**Expected result:** check_env.sh prints PASS for each tool; your branch appears on GitHub.

**Check before you finish**

- [ ] Copilot icon active
- [ ] Repository cloned and branch pushed
- [ ] All environment checks PASS (or failures reported to the trainer)

**If something goes wrong**

- Copilot icon crossed out: sign out and back in to GitHub, then reload the window (Ctrl+Shift+P > Developer: Reload Window).
- git push asks for a password: use GitHub sign-in in VS Code or a personal access token supplied by your administrator.

**Deliverable:** Branch pushed with labs/m01/README.md listing your environment check result.


### Lab 1.2: Disk-full troubleshooting checklist with two models (20 min)

**Objective:** Generate and compare a troubleshooting checklist for a production disk-full scenario.

**Files:** `labs/m01/scenario_disk_full.md`

**Steps**

1. Open labs/m01/scenario_disk_full.md. It contains a ticket, a df -h output and a service status.
2. Naive prompt first (Ask mode). Note how generic and risky the answer is:

   Copilot Chat prompt:

   ```text
   #file:labs/m01/scenario_disk_full.md fix this
   ```

3. Now the structured prompt:

   Copilot Chat prompt:

   ```text
   Role: You are a senior Linux L2 engineer following ITIL.
   Context: #file:labs/m01/scenario_disk_full.md
   Task: Produce a troubleshooting checklist for this disk-full incident.
   Constraints: read-only checks first; never delete files without listing them and asking for approval;
   mark any assumption as ASSUMPTION; do not invent hostnames or paths not in the file.
   Output: numbered checklist with columns Step | Command | Why | Expected result.
   ```

4. Change the model in the model picker and run the same structured prompt again.
5. Compare the two answers. Look for: invented command flags, paths not in the scenario, any delete command (rm -rf) offered without approval.
6. Save the safer checklist with your notes to labs/m01/checklist.md and commit.

**Expected result:** A checklist that starts with read-only checks (df, du, journalctl, logrotate status) and marks clean-up as approval-required.

**Check before you finish**

- [ ] At least one AI error identified and explained
- [ ] No destructive command without approval
- [ ] Assumptions labelled

**If something goes wrong**

- If an answer is cut off, ask: 'continue from step N'.
- Keep both answers - the comparison is the learning.

**Deliverable:** Validated checklist with at least one AI error identified and corrected.


## Save your work

```bash
git add -A
git commit -m "Module 1 labs"
git push
```
