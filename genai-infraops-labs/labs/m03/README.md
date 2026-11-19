# Module 3: AI-Assisted Shell, Python & YAML Automation

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 1 | Sessions 1-2 | 0.25 h | 1.75 h | Hands-On Coding Lab |

Participants generate, debug, test and lint automation scripts with Copilot, building a self-service script kit for repetitive Service Desk tasks.

## What you will learn

- Generate Bash health-check scripts and Python log parsers from a precise specification.
- Generate Kubernetes YAML and validate it before use.
- Debug broken scripts with /fix and generate unit tests with /tests.
- Apply idempotency, error handling, logging and confirmation prompts to any script that changes state.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Bash script | A text file of Linux shell commands that runs as one program, used to automate repetitive tasks. |
| Exit code | A number a command returns when it finishes: 0 means success, anything else means an error. Scripts use it to decide what to do next. |
| set -euo pipefail | A safety line at the top of Bash scripts: stop on any error (-e), on undefined variables (-u) and on failures inside pipes (pipefail). |
| Idempotent | Safe to run more than once: the second run causes no extra change or harm. |
| Dry-run | A mode that shows what a script WOULD do without actually doing it. Our scripts use dry-run by default. |
| Linting (ShellCheck, pylint, yamllint) | Automatic checking of code for bugs and bad practice. Findings appear in the VS Code Problems panel. |
| Unit test / pytest | Small automatic checks that prove a function works. pytest runs Python tests. |
| YAML | A human-readable configuration format used by Kubernetes, Ansible and Prometheus. Indentation matters. |
| Allow-list | A fixed list of things that are permitted (for example, which services may be restarted). Everything else is refused. |
| Audit log | A record of who did what and when, kept for accountability and review. |
| MTTR | Mean Time To Resolve: average time from ticket creation to resolution. |

## Real-time Service Desk use case UC-04: L1 self-heal scripts with human confirmation

| | |
|---|---|
| Persona | L2 engineer building tools for L1 |
| Problem statement | Around 30% of desk volume is repetitive: account lockouts, disk-full alerts and hung services. Each needs an L2 login and manual commands, adding 30-60 minutes to MTTR and the risk of a wrong command on the wrong host. |
| What AI does | Copilot generates the scripts from a specification, finds defects with /fix and writes unit tests. |
| Human review checkpoint | L2 reviews every script; live restarts need --execute plus a typed confirmation and are logged. |
| Output asset | Self-service script kit in the repository |
| KPI impact | MTTR for repeat tickets, L2 escalations |

## Hands-on labs

### Lab 3.1: Bash server health check (20 min)

**Objective:** Generate a read-only health-check script for CPU, memory, disk and key services.

**Files:** `labs/m03/health_check.sh`

**Steps**

1. Open labs/m03/health_check.sh. It contains only a specification comment. Place the cursor below it and press Ctrl+I:

   Copilot Chat prompt:

   ```text
   Implement this specification. Read-only. Use set -euo pipefail. Print a table and an overall OK/WARN/CRIT with exit codes 0/1/2.
   ```

2. Run ShellCheck and fix every finding (select the code, Ctrl+I, /fix):

   Terminal:

   ```bash
   shellcheck labs/m03/health_check.sh
   ```

3. Run it:

   Terminal:

   ```bash
   bash labs/m03/health_check.sh; echo "exit code: $?"
   ```


**Expected result:** A table of CPU, memory, disk and service status with an overall status and matching exit code.

**Check before you finish**

- [ ] ShellCheck clean
- [ ] Script changes nothing on the system
- [ ] Exit code matches the overall status

**If something goes wrong**

- 'command not found: shellcheck' - run ./setup/check_env.sh and tell the trainer.

**Deliverable:** Lint-clean health_check.sh.


### Lab 3.2: Python log parser to CSV (25 min)

**Objective:** Parse syslog and nginx access logs into a CSV summary of errors by hour and status code.

**Files:** `labs/m03/log_parser.py`, `data/logs/syslog`, `data/logs/nginx-access.log`

**Steps**

1. In Edit mode, add labs/m03/log_parser.py and ask:

   Copilot Chat prompt:

   ```text
   Implement log_parser.py: argparse with --input and --output; parse nginx access log lines
   (IP, time, method, path, status); write a CSV of count of requests per UTC hour per status code.
   Skip malformed lines and count them. Include type hints and docstrings.
   ```

2. Generate tests: select the code, open Chat and type /tests. Save as labs/m03/test_log_parser.py, then run:

   Terminal:

   ```bash
   python3 labs/m03/log_parser.py --input data/logs/nginx-access.log --output outputs/m03/status_by_hour.csv
   pytest -q labs/m03
   pylint labs/m03/log_parser.py
   ```


**Expected result:** outputs/m03/status_by_hour.csv showing the burst of 503 errors; tests pass.

**Check before you finish**

- [ ] Tests pass
- [ ] Malformed lines handled
- [ ] pylint score above 8

**If something goes wrong**

- If tests fail because of a wrong expectation, fix the test only after checking the real log line.

**Deliverable:** log_parser.py with passing tests.


### Lab 3.3: L1 self-heal script kit with confirmation (60 min)

**Objective:** Build safe scripts for the most repetitive desk tickets (Service Desk use case UC-04).

**Files:** `scripts/l1/`, `scripts/broken/restart_broken.sh`

**Steps**

1. Create scripts/l1/service_restart.sh with inline chat using this specification:

   Copilot Chat prompt:

   ```text
   Write service_restart.sh <service> [--execute].
   - Allow-list: nginx, cron, docker. Reject anything else.
   - Default is dry-run: print pre-checks and the command it WOULD run.
   - With --execute: pre-check (systemctl is-active, last 20 journal lines), ask the user to type the
     service name to confirm, restart with sudo systemctl restart, post-check is-active.
   - Append time, user, service and result to approvals/audit.log. set -euo pipefail.
   ```

2. Lint and test both modes:

   Terminal:

   ```bash
   shellcheck scripts/l1/service_restart.sh
   ./scripts/l1/service_restart.sh sshd          # must be rejected
   ./scripts/l1/service_restart.sh nginx         # dry-run
   ./scripts/l1/service_restart.sh nginx --execute
   tail -3 approvals/audit.log
   ```

3. Generate scripts/l1/lockout_check.sh (show faillock status for a user, read-only) and scripts/l1/disk_report.sh (top 10 directories under /var, read-only).
4. Open scripts/broken/restart_broken.sh. Find at least 3 safety defects yourself, then ask Copilot to list them and fix the file.
5. Generate a Kubernetes Deployment for nginx in labs/m03/deployment.yaml and validate it:

   Terminal:

   ```bash
   kubectl apply --dry-run=client -f labs/m03/deployment.yaml
   ```


**Expected result:** A script kit in scripts/l1/ and an audit entry for one approved restart.

**Check before you finish**

- [ ] Non-allow-listed service rejected
- [ ] Dry-run is the default
- [ ] Typed confirmation required
- [ ] Audit log written
- [ ] 3 defects found in restart_broken.sh

**If something goes wrong**

- The defects to look for: no input validation, unquoted variables, deleting logs, no confirmation, logging to /tmp.

**Deliverable:** scripts/l1/ kit with audit log evidence of one approved restart.


## Save your work

```bash
git add -A
git commit -m "Module 3 labs"
git push
```
