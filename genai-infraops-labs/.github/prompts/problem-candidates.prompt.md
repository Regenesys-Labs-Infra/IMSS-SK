---
mode: ask
description: UC-06 Propose problem records from ticket clusters
---
Using #file:outputs/m07/clusters.csv:
1. Name each cluster in <= 6 words.
2. Compute monthly effort hours = (cluster tickets / 3 months) x mean handle_time_min / 60. Show the arithmetic.
3. Rank and propose the top-5 Problem candidates with: problem statement, suspected root cause (HYPOTHESIS),
   evidence ticket numbers (>= 3), workaround in use, KB gap (yes/no against data/kb/).
Output Markdown suitable for outputs/m07/problem_report.md.
