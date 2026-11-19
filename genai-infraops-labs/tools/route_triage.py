#!/usr/bin/env python3
"""UC-10 Confidence router: splits AI triage results into an auto-proposed queue and a HUMAN REVIEW queue.

Usage: python tools/route_triage.py outputs/m10/triage.json [--threshold 0.80] [--sample 5]
"""
import argparse, json, os, random

ap = argparse.ArgumentParser()
ap.add_argument("triage")
ap.add_argument("--threshold", type=float, default=0.80)
ap.add_argument("--sample", type=int, default=5, help="spot-check 1 in N proposed items")
a = ap.parse_args()

items = json.load(open(a.triage))
proposed, review = [], []
for t in items:
    reasons = []
    if t["confidence"] < a.threshold: reasons.append(f"confidence {t['confidence']:.2f} < {a.threshold}")
    if t["priority"] in ("P1", "P2"): reasons.append(f"priority {t['priority']}")
    if t["assignment_group"] == "SECOPS" or t["category"] == "Security": reasons.append("security")
    if t.get("needs_human_review"): reasons.append("model flagged review")
    if reasons:
        review.append({**t, "review_reasons": reasons, "status": "AWAITING_LEAD"})
    else:
        proposed.append({**t, "status": "PROPOSED"})

random.seed(7)
for t in proposed:
    if random.randint(1, a.sample) == 1:
        t["spot_check"] = True

out = os.path.dirname(a.triage)
json.dump(proposed, open(os.path.join(out, "proposed.json"), "w"), indent=2)
json.dump(review, open(os.path.join(out, "review_queue.json"), "w"), indent=2)
print(f"Proposed (auto)  : {len(proposed)}  -> {out}/proposed.json  (spot-check flagged: {sum(1 for t in proposed if t.get('spot_check'))})")
print(f"Human review     : {len(review)}  -> {out}/review_queue.json")
for t in review:
    print(f"  {t['number']}  {t['priority']}  {t['assignment_group']:<16} {'; '.join(t['review_reasons'])}")
print("Next: the desk lead records decisions in outputs/m10/lead_decisions.csv (ticket,ai_value,human_value,reason)")
