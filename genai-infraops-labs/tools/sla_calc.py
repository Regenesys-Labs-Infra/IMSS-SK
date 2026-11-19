#!/usr/bin/env python3
"""UC-08 SLA impact calculator (deterministic - never let the LLM do this arithmetic).

Usage: python tools/sla_calc.py --incident data/incidents/INC-MAJ-0042/worknotes.json --policy data/policy/sla_policy.json
"""
import argparse, json, os
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("--incident", required=True)
ap.add_argument("--policy", required=True)
ap.add_argument("--out", default="outputs/m08/sla_result.txt")
a = ap.parse_args()

inc = json.load(open(a.incident)); pol = json.load(open(a.policy))
tgt = pol["targets_minutes"][inc["priority"]]
f = datetime.fromisoformat
opened, responded, resolved = f(inc["opened_at"]), f(inc["responded_at"]), f(inc["resolved_at"])
resp = (responded - opened).total_seconds() / 60
reso = (resolved - opened).total_seconds() / 60
lines = [
    f"Incident {inc['number']} ({inc['priority']}, {inc['business_service']})",
    f"Response   : {resp:.0f} min vs target {tgt['respond']} min -> {'MET' if resp <= tgt['respond'] else 'BREACHED by %.0f min' % (resp - tgt['respond'])}",
    f"Resolution : {reso:.0f} min vs target {tgt['resolve']} min -> {'MET' if reso <= tgt['resolve'] else 'BREACHED by %.0f min' % (reso - tgt['resolve'])}",
    f"Outage window (opened to resolved): {opened:%Y-%m-%d %H:%M} to {resolved:%H:%M} IST",
]
os.makedirs(os.path.dirname(a.out), exist_ok=True)
open(a.out, "w").write("\n".join(lines) + "\n")
print("\n".join(lines)); print(f"Saved: {a.out}")
