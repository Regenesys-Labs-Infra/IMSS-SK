# Change risk rubric (score each 1-3, total 5-15)
| Factor | 1 (Low) | 2 (Medium) | 3 (High) |
|---|---|---|---|
| Impact if it fails | Single non-prod CI | One prod service degraded | Customer-facing service down |
| Complexity | One step, automated | Several manual steps | Multi-team, schema/data change |
| Change history | Done >5 times, no failures | Done before with issues | First time |
| Backout | Tested, < 15 min | Documented, untested | None or > 1 h |
| Timing | Agreed window, low traffic | Business hours | Month-end / peak |
Total 5-7 Low (Change Manager), 8-11 Medium (Change Manager + peer review), 12-15 High (CAB).
Any internet-exposed rule: InfraSec sign-off mandatory regardless of score.
