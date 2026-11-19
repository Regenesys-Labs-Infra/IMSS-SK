#!/usr/bin/env python3
"""UC-02 Sanitisation gate: mask sensitive values in ticket text BEFORE it is used with any AI tool.

Usage:
  python tools/sanitise.py data/tickets/raw_tickets_pii.csv [--column description] [--out outputs/m11/] [--report]

The baseline PATTERNS deliberately miss some categories (Indian mobile numbers, employee IDs,
cloud keys, bearer tokens, UNC paths). Lab task: extend PATTERNS with Copilot inline chat and add tests.
"""
import argparse, csv, json, os, re, sys

PATTERNS = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "IPV4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "PASSWORD_PHRASE": r"(?i)(?:password|pwd|passwd)\s*(?:is|:|=)\s*\S+",
    # TODO (lab): INDIAN_MOBILE, EMPLOYEE_ID (HM-######), AWS_ACCESS_KEY, AWS_SECRET, BEARER_TOKEN, UNC_PATH
}

INJECTION_HINTS = [
    r"(?i)ignore (all |any )?previous instructions",
    r"(?i)\b(ai|assistant)\b\s*[:,]",
    r"(?i)note to ai",
    r"(?i)\[system\]",
    r"(?i)mark (it |this )?as (approved|benign)",
]


def sanitise(text, mapping):
    """Replace each sensitive value with a stable typed token; same value -> same token."""
    found = []
    for name, pat in PATTERNS.items():
        def repl(m, name=name):
            val = m.group(0)
            key = (name, val)
            if key not in mapping:
                count = sum(1 for k in mapping if k[0] == name) + 1
                mapping[key] = f"<{name}_{count}>"
            found.append(name)
            return mapping[key]
        text = re.sub(pat, repl, text)
    return text, found


def injection_flags(text):
    return [p for p in INJECTION_HINTS if re.search(p, text)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--column", default="description")
    ap.add_argument("--out", default="outputs/m11/")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    out_csv = os.path.join(a.out, os.path.basename(a.path).replace(".csv", "_sanitised.csv"))
    report = []
    with open(a.path, newline="") as f, open(out_csv, "w", newline="") as g:
        r = csv.DictReader(f)
        w = csv.DictWriter(g, fieldnames=r.fieldnames + ["injection_suspect"])
        w.writeheader()
        for row in r:
            mapping = {}
            clean, found = sanitise(row[a.column], mapping)
            flags = injection_flags(row[a.column])
            row[a.column] = clean
            row["injection_suspect"] = "INJECTION_SUSPECT" if flags else ""
            w.writerow(row)
            report.append({"ticket": row.get("number"), "masked": found, "injection_suspect": bool(flags)})
    rep_path = os.path.join(a.out, "redaction_report.json")
    json.dump(report, open(rep_path, "w"), indent=2)
    print(f"Sanitised file : {out_csv}")
    print(f"Report         : {rep_path}")
    if a.report:
        for x in report:
            print(f"  {x['ticket']}: masked={x['masked'] or '-'} {'<< INJECTION_SUSPECT' if x['injection_suspect'] else ''}")
    print("Human step: review the report and sign the redaction checklist before any AI use.")


if __name__ == "__main__":
    sys.exit(main())
