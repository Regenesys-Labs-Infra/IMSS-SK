#!/usr/bin/env python3
"""UC-02 Sanitisation gate: mask sensitive values in ticket text BEFORE it is used with any AI tool.

Usage:
  python tools/sanitise.py data/tickets/raw_tickets_pii.csv [--column description] [--out outputs/m11/] [--report]

PATTERNS covers common PII and credential formats; review the report because no regex set catches
every sensitive value. Lab task: extend PATTERNS with Copilot inline chat and add tests.
"""
import argparse, csv, json, os, re, sys

PATTERNS = {
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "IPV4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "INDIAN_MOBILE": r"(?<!\w)(?:\+91[\s-]?)?[6-9](?:[\s-]?\d){9}(?!\w)",
    "EMPLOYEE_ID": r"\bHM-\d{6}\b",
    "AWS_ACCESS_KEY": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "AWS_SECRET": (
        r"(?i)\b(?:aws[_ -]?)?secret(?:[_ -]?(?:access[_ -]?)?key)?\s*"
        r"(?:[:=]\s*|\s+)(?:'[^']{40}'|\"[^\"]{40}\"|\{[^}]{40}\}|[A-Za-z0-9/+=]{40})"
    ),
    "BEARER_TOKEN": (
        r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*|"
        r"\beyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
    ),
    "UNC_PATH": r"\\\\[^\\/\s]+\\[^\\/\r\n,;\"']+(?:\\[^\r\n,;\"']*)?",
    "CONNECTION_STRING_PASSWORD": (
        r"(?i)\b(?:password|pwd)\s*=\s*(?:'[^']*'|\"[^\"]*\"|\{[^}]*\}|[^;\s]+)"
    ),
    "PASSWORD_PHRASE": r"(?i)(?:password|pwd|passwd)\s*(?:is|:|=)\s*\S+",
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
