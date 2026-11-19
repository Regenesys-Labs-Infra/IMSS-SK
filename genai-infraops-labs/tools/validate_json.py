#!/usr/bin/env python3
"""Validate AI-produced JSON against a schema. Fix failures by improving the PROMPT, not by hand-editing.

Usage:
  python tools/validate_json.py schemas/triage.schema.json outputs/m10/triage.json
  python tools/validate_json.py --selftest
"""
import json, os, sys
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def validate(schema_path, data_path):
    schema = json.load(open(schema_path))
    try:
        data = json.load(open(data_path))
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e}")
        return 1
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    for e in errors:
        print(f"FAIL at {'/'.join(map(str, e.path)) or '<root>'}: {e.message}")
    print("VALID" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


def selftest():
    checks = 0
    for rel in ["schemas/triage.schema.json", "schemas/remediation_plan.schema.json",
                "data/tickets/live_queue.json", "data/policy/priority_matrix.json",
                "data/policy/assignment_groups.json", "data/policy/sla_policy.json",
                "data/alerts/alerts_stream.json", "data/incidents/INC-MAJ-0042/worknotes.json"]:
        json.load(open(os.path.join(ROOT, rel)))
        checks += 1
    for s in ["schemas/triage.schema.json", "schemas/remediation_plan.schema.json"]:
        Draft202012Validator.check_schema(json.load(open(os.path.join(ROOT, s))))
        checks += 1
    q = json.load(open(os.path.join(ROOT, "data/tickets/live_queue.json")))
    assert len(q["tickets"]) == 20, "live queue should have 20 tickets"
    print(f"{checks + 1} checks - ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    sys.exit(validate(sys.argv[1], sys.argv[2]))
