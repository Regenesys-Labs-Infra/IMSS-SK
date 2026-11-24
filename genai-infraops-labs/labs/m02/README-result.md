# Module 2 Lab Results

**Date:** 2026-11-24
**Data:** Synthetic training materials and ticket history
**Execution scope:** Local file and data review only; no infrastructure changes were made.

## Lab 2.1: SOP to runbook

- Drafted [runbooks/nginx_restart.md](../../runbooks/nginx_restart.md) from SOP-OPS-014
  and the supplied template. It includes read-only pre-checks, an approval gate, expected
  verification results, escalation criteria, and a rollback limitation.
- Did not restart nginx or run `/explain`; the local shell is not the lab web node and
  Copilot Chat is not accessible here.
- Reviewed `runbook_with_errors.md` and found the three planted issues:
  1. `logrotate --force-all` is not a supported option in the local `logrotate` help;
     `--force` is listed. Verify the target host's version before use.
  2. `rm -rf /var/log/*` deletes all log files without review or approval and may destroy
     evidence.
  3. The required result of “below 80%” is an invented threshold; no target is provided.
- Additional safety concern: restarting `finapp` is state-changing and is not shown to
  free space. It requires a separate, approved plan.

## Lab 2.2: Team instructions and prompt library

- Added a team rule requiring KB resolution steps to cite ticket IDs and unsupported
  details to be marked `[VERIFY]`.
- Added `explain-command`, `sop-to-runbook`, and `troubleshooting-checklist` prompt files.
  Together with the existing M02 `ticket-first-response` and `ticket-to-kb` prompts, the
  M02 prompt set contains five files.
- The prompts were reviewed as files but were not invoked from Copilot Chat's `/` menu;
  that UI check remains outstanding.

## Lab 2.3: Ticket-to-KB generation

- Ran the prescribed ticket query with the project virtual environment because system
  Python does not have pandas installed.
- Source counts: 33 VPN tickets, 36 Email tickets, and 26 Account lockout tickets.
- Drafted three articles under `outputs/kb/`, citing source ticket IDs and marking
  procedures not present in the notes `[VERIFY]`. No user names or secrets were included.
- Compared the VPN draft with the existing article in
  [KB_VPN_comparison.md](../../outputs/kb/KB_VPN_comparison.md). A neighbour review was
  not available; the comparison is a source-ticket audit, not a peer review.

## Outstanding interactive and GitHub steps

- Copilot Chat prompt execution, the `/explain` interaction, prompt-menu validation, and
  neighbour review require the VS Code UI and another reviewer; they were not performed.
- A pull request was not opened. The authenticated GitHub account previously received
  HTTP 403 for repository write access. This local work is not pushed.
