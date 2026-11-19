#!/usr/bin/env python3
"""UC-11 Human approval gate for agent-proposed remediation plans.

The Resolver agent can only WRITE plans into approvals/pending/. Nothing runs until a named human
approves the plan here AND confirms again at execution time. Every decision is appended to approvals/audit.log.

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
    for state in ("pending", "approved", "rejected", "executed"):
        p = os.path.join(A, state, f"{plan_id}.json")
        if os.path.exists(p):
            return state, p
    sys.exit(f"Plan {plan_id} not found")


def matches(argv, rules):
    for binary, prefix in rules:
        if argv and argv[0] == binary and argv[1:1 + len(prefix)] == prefix:
            return True
    return False


def policy_check(argv):
    problems = []
    if not matches(argv, ALLOWED):
        problems.append(f"command not on allow-list: {' '.join(argv[:3])}")
    if FORBIDDEN_WORDS & {w.lower() for w in argv}:
        problems.append(f"forbidden token: {FORBIDDEN_WORDS & {w.lower() for w in argv}}")
    if argv and argv[0] == "kubectl":
        ns = [argv[i + 1] for i, w in enumerate(argv[:-1]) if w in ("-n", "--namespace")]
        if not ns or not set(ns) <= ALLOWED_NAMESPACES:
            problems.append(f"namespace must be explicit and one of {sorted(ALLOWED_NAMESPACES)}")
    if argv and argv[0] == "systemctl" and (len(argv) < 3 or argv[2] not in ALLOWED_SERVICES):
        problems.append(f"service must be one of {sorted(ALLOWED_SERVICES)}")
    return problems


def cmd_list(_):
    for state in ("pending", "approved", "rejected", "executed"):
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
    probs = policy_check(p["command"]) + [f"rollback: {x}" for x in policy_check(p["rollback"])]
    print("Policy check:", "PASS" if not probs else "FAIL -> " + "; ".join(probs))
    if p.get("rejection"): print("Rejection   :", p["rejection"])


def move(path, plan, state):
    os.makedirs(os.path.join(A, state), exist_ok=True)
    new = os.path.join(A, state, f"{plan['id']}.json")
    json.dump(plan, open(new, "w"), indent=2); os.remove(path)


def cmd_approve(a):
    state, path = find(a.id)
    if state != "pending": sys.exit(f"Only PENDING plans can be approved (is {state})")
    p = json.load(open(path))
    probs = policy_check(p["command"])
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
    r = subprocess.run(argv, capture_output=True, text=True, timeout=120)  # no shell=True, ever
    out = (r.stdout + r.stderr).strip()
    print("     " + out.replace("\n", "\n     ")[:2000])
    return r.returncode, out[:2000]


def cmd_execute(a):
    state, path = find(a.id)
    if state != "approved": sys.exit(f"Plan must be APPROVED before execution (is {state})")
    p = json.load(open(path))
    probs = policy_check(p["command"])
    if probs: sys.exit("Refused at execution - policy check failed: " + "; ".join(probs))
    print("Pre-checks:")
    for c in p["pre_checks"]:
        if not matches(c, READ_ONLY): sys.exit(f"Pre-check is not read-only: {' '.join(c)}")
        run(c, a.dry_run)
    print(f"\nAbout to run (approved by {p['approved_by']}):\n   $ {' '.join(p['command'])}")
    if not a.dry_run and input("Type 'y' to execute: ").strip().lower() != "y":
        audit("EXECUTION_DECLINED", a.id); sys.exit("Not executed.")
    rc, out = run(p["command"], a.dry_run)
    print("\nVerification:")
    results = [{"cmd": v["command"], "expect": v["expect"], "rc": run(v["command"], a.dry_run)[0]}
               for v in p["verification"] if matches(v["command"], READ_ONLY)]
    audit("EXECUTED" if not a.dry_run else "DRY_RUN", a.id, rc=rc, command=p["command"], output=out[:300])
    if not a.dry_run:
        p.update(status="EXECUTED", executed_at=now(), exit_code=rc, verification=results)
        move(path, p, "executed")
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
