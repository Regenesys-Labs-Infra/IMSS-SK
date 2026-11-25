#!/usr/bin/env python3
"""UC-11 Human approval gate for agent-proposed remediation plans.

The Resolver agent can only WRITE plans into approvals/pending/. Nothing runs until a named human
approves the plan here AND confirms again at execution time. Every decision is appended to approvals/audit.log.
Every kubectl command must pin one --context and an allowed namespace. Failed pre-checks abort execution
and invalidate the approval; failed execution or verification is recorded under approvals/failed/.

Usage:
  python tools/approve.py list
  python tools/approve.py show REM-0001
  python tools/approve.py approve REM-0001 --by "<name>" [--note "..."]
  python tools/approve.py reject  REM-0001 --by "<name>" --reason "No pre-check of current selector"
  python tools/approve.py execute REM-0001 [--dry-run]
"""
import argparse, getpass, json, os, subprocess, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "approvals")
AUDIT = os.path.join(A, "audit.log")

# Allow-list: (binary, verb/sub-command prefix). Anything else is refused even if a human approved it.
ALLOWED = [
    ("kubectl", ["patch"]), ("kubectl", ["apply"]), ("kubectl", ["rollout", "restart"]),
    ("kubectl", ["rollout", "undo"]), ("kubectl", ["set", "image"]), ("kubectl", ["scale"]),
    ("systemctl", ["restart"]),
]
ALLOWED_NAMESPACES = {"portal"}
ALLOWED_SERVICES = {"nginx", "cron", "docker"}
READ_ONLY = [("kubectl", ["get"]), ("kubectl", ["describe"]), ("kubectl", ["logs"]),
             ("kubectl", ["rollout", "status"]), ("systemctl", ["is-active"]), ("systemctl", ["status"]),
             ("curl", [])]
FORBIDDEN_WORDS = {"delete", "destroy", "drain", "cordon", "--force", "rm", "-rf", "clusterrole", "rbac"}


def now(): return datetime.now().astimezone().isoformat(timespec="seconds")


def audit(event, plan_id, **kw):
    with open(AUDIT, "a") as f:
        f.write(json.dumps({"time": now(), "event": event, "plan": plan_id, "os_user": getpass.getuser(), **kw}) + "\n")


def find(plan_id):
    for state in ("pending", "approved", "rejected", "executed", "failed"):
        p = os.path.join(A, state, f"{plan_id}.json")
        if os.path.exists(p):
            return state, p
    sys.exit(f"Plan {plan_id} not found")


def matches(argv, rules):
    for binary, prefix in rules:
        if argv and argv[0] == binary and argv[1:1 + len(prefix)] == prefix:
            return True
    return False


def kubectl_scope_problems(argv):
    if not argv or argv[0] != "kubectl":
        return []

    problems = []
    contexts = []
    namespaces = []
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--context" and i + 1 < len(argv):
            contexts.append(argv[i + 1])
            i += 1
        elif arg.startswith("--context="):
            contexts.append(arg.split("=", 1)[1])
        elif arg in ("-n", "--namespace") and i + 1 < len(argv):
            namespaces.append(argv[i + 1])
            i += 1
        elif arg.startswith("--namespace="):
            namespaces.append(arg.split("=", 1)[1])
        elif arg.startswith("-n="):
            namespaces.append(arg.split("=", 1)[1])
        i += 1

    if len(contexts) != 1 or not contexts[0]:
        problems.append("kubectl context must be explicit with exactly one --context")
    if not namespaces or not set(namespaces) <= ALLOWED_NAMESPACES:
        problems.append(f"namespace must be explicit and one of {sorted(ALLOWED_NAMESPACES)}")
    return problems


def policy_check(argv):
    problems = []
    if not matches(argv, ALLOWED):
        problems.append(f"command not on allow-list: {' '.join(argv[:3])}")
    if FORBIDDEN_WORDS & {w.lower() for w in argv}:
        problems.append(f"forbidden token: {FORBIDDEN_WORDS & {w.lower() for w in argv}}")
    problems.extend(kubectl_scope_problems(argv))
    if argv and argv[0] == "systemctl" and (len(argv) < 3 or argv[2] not in ALLOWED_SERVICES):
        problems.append(f"service must be one of {sorted(ALLOWED_SERVICES)}")
    return problems


def plan_policy_check(plan):
    problems = policy_check(plan["command"])
    problems.extend(f"rollback: {problem}" for problem in policy_check(plan["rollback"]))
    for index, command in enumerate(plan["pre_checks"], start=1):
        if not matches(command, READ_ONLY):
            problems.append(f"pre-check {index} is not read-only: {' '.join(command)}")
        problems.extend(
            f"pre-check {index}: {problem}" for problem in kubectl_scope_problems(command)
        )
    for index, verification in enumerate(plan["verification"], start=1):
        command = verification["command"]
        if not matches(command, READ_ONLY):
            problems.append(f"verification {index} is not read-only: {' '.join(command)}")
        problems.extend(
            f"verification {index}: {problem}" for problem in kubectl_scope_problems(command)
        )
    return problems


def cmd_list(_):
    for state in ("pending", "approved", "rejected", "executed", "failed"):
        d = os.path.join(A, state)
        os.makedirs(d, exist_ok=True)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".json"):
                p = json.load(open(os.path.join(d, fn)))
                print(f"{state.upper():<9} {p['id']}  {p['ticket']:<13} risk={p['risk']:<6} {p['summary'][:70]}")


def cmd_show(a):
    state, path = find(a.id)
    p = json.load(open(path))
    print(f"=== {p['id']} [{state.upper()}] ticket {p['ticket']} proposed by {p['proposed_by']} at {p.get('proposed_at')}")
    print(f"Summary     : {p['summary']}\nRoot cause  : {p['root_cause']}\nBlast radius: {p['blast_radius']}\nRisk        : {p['risk']}")
    print("Pre-checks  :"); [print("   $ " + " ".join(c)) for c in p["pre_checks"]]
    print("COMMAND     : $ " + " ".join(p["command"]))
    print("Rollback    : $ " + " ".join(p["rollback"]))
    print("Verification:"); [print(f"   $ {' '.join(v['command'])}   (expect: {v['expect']})") for v in p["verification"]]
    probs = plan_policy_check(p)
    print("Policy check:", "PASS" if not probs else "FAIL -> " + "; ".join(probs))
    if p.get("rejection"): print("Rejection   :", p["rejection"])


def move(path, plan, state):
    os.makedirs(os.path.join(A, state), exist_ok=True)
    new = os.path.join(A, state, f"{plan['id']}.json")
    with open(new, "w") as f:
        json.dump(plan, f, indent=2)
    os.remove(path)


def cmd_approve(a):
    state, path = find(a.id)
    if state != "pending": sys.exit(f"Only PENDING plans can be approved (is {state})")
    p = json.load(open(path))
    probs = plan_policy_check(p)
    if probs: sys.exit("Cannot approve - policy check failed: " + "; ".join(probs))
    p.update(status="APPROVED", approved_by=a.by, approved_at=now(), approval_note=a.note)
    move(path, p, "approved"); audit("APPROVED", a.id, by=a.by, note=a.note)
    print(f"{a.id} APPROVED by {a.by}. Execute with: python tools/approve.py execute {a.id}")


def cmd_reject(a):
    state, path = find(a.id)
    if state != "pending": sys.exit(f"Only PENDING plans can be rejected (is {state})")
    p = json.load(open(path))
    p.update(status="REJECTED", rejection={"by": a.by, "reason": a.reason, "at": now()})
    move(path, p, "rejected"); audit("REJECTED", a.id, by=a.by, reason=a.reason)
    print(f"{a.id} REJECTED. The Resolver agent must read the reason and submit a revision.")


def run(argv, dry):
    print("   $ " + " ".join(argv))
    if dry: return 0, "(dry-run)"
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=120)  # no shell=True, ever
    except subprocess.TimeoutExpired as e:
        out = str(e)
        print(f"     {out}")
        return 124, out[:2000]
    except OSError as e:
        out = str(e)
        print(f"     {out}")
        return 127, out[:2000]
    out = (r.stdout + r.stderr).strip()
    print("     " + out.replace("\n", "\n     ")[:2000])
    return r.returncode, out[:2000]


def cmd_execute(a):
    state, path = find(a.id)
    if state != "approved": sys.exit(f"Plan must be APPROVED before execution (is {state})")
    with open(path) as f:
        p = json.load(f)
    probs = plan_policy_check(p)
    if probs: sys.exit("Refused at execution - policy check failed: " + "; ".join(probs))
    print("Pre-checks:")
    for c in p["pre_checks"]:
        rc, out = run(c, a.dry_run)
        if rc != 0:
            audit("PRECHECK_FAILED", a.id, command=c, rc=rc, output=out[:300])
            p.update(
                status="PRECHECK_FAILED",
                precheck_failure={"command": c, "rc": rc, "output": out[:300]},
                precheck_failed_at=now(),
            )
            move(path, p, "failed")
            sys.exit(f"Pre-check failed (rc={rc}); execution aborted.")
    print(f"\nAbout to run (approved by {p['approved_by']}):\n   $ {' '.join(p['command'])}")
    if not a.dry_run:
        try:
            confirmation = input("Type 'y' to execute: ").strip().lower()
        except EOFError:
            confirmation = ""
        if confirmation != "y":
            audit("EXECUTION_DECLINED", a.id)
            sys.exit("No interactive confirmation received; not executed.")
    rc, out = run(p["command"], a.dry_run)
    print("\nVerification:")
    results = []
    for verification in p["verification"]:
        verify_rc, verify_out = run(verification["command"], a.dry_run)
        results.append({
            "cmd": verification["command"],
            "expect": verification["expect"],
            "rc": verify_rc,
            "output": verify_out[:300],
        })
    succeeded = rc == 0 and all(result["rc"] == 0 for result in results)
    event = "DRY_RUN" if a.dry_run else ("EXECUTED" if succeeded else "EXECUTION_FAILED")
    audit(event, a.id, rc=rc, command=p["command"], output=out[:300], verification=results)
    if not a.dry_run:
        status = "EXECUTED" if succeeded else "EXECUTION_FAILED"
        state = "executed" if succeeded else "failed"
        p.update(status=status, executed_at=now(), exit_code=rc, verification=results)
        move(path, p, state)
    if not succeeded:
        sys.exit(f"Execution or verification failed (command rc={rc}); inspect the audit record.")
    print(f"\nDone (rc={rc}). If verification fails, rollback: $ {' '.join(p['rollback'])} (needs a new approval).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    s.add_parser("list").set_defaults(f=cmd_list)
    x = s.add_parser("show"); x.add_argument("id"); x.set_defaults(f=cmd_show)
    x = s.add_parser("approve"); x.add_argument("id"); x.add_argument("--by", required=True); x.add_argument("--note", default=""); x.set_defaults(f=cmd_approve)
    x = s.add_parser("reject"); x.add_argument("id"); x.add_argument("--by", default=getpass.getuser()); x.add_argument("--reason", required=True); x.set_defaults(f=cmd_reject)
    x = s.add_parser("execute"); x.add_argument("id"); x.add_argument("--dry-run", action="store_true"); x.set_defaults(f=cmd_execute)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
