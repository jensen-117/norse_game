"""Refresh the bestiary's generated parts (stat blocks, results, hunted-by) from the latest sim output."""
import re, subprocess
subprocess.run(["python3", "catalog.py"], capture_output=True, check=True)
B = "../bestiary.md"
b = open(B).read()
out = open("out_families.txt").read()
L30 = out[out.index("=== Level 30"):out.index("=== Level 60")]
fams = ["Ande", "Draugr", "Bein", "Drattr", "Djur", "Oskorei"]
overall = dict(re.findall(r"vs (\w+)\s+party wins\s+(\d+%)", L30))
tiers = re.search(r"by tier: (.*)", L30).group(1).strip()
rows = []
for line in L30.splitlines():
    m = re.match(r"\s+(\w+)\s+((?:\d+%\s+[\d.]+\s*){6})$", line)
    if m: rows.append((m.group(1), re.findall(r"(\d+)%\s+([\d.]+)", m.group(2))))
table = ["| Class | " + " | ".join(fams) + " |", "|---" * 7 + "|"]
for c, vals in rows:
    table.append(f"| {c} | " + " | ".join(f"{w}% ({k})" for w, k in vals) + " |")
results = ("## Part 11: Sim Results\n\nWin rate when each class is in the party, at level 30 (1,500 fights per family), with family "
           "bodies and the speed shift applied. Weak hits per fight in parentheses.\n\n" + "\n".join(table) +
           "\n\nOverall party win rates at level 30: " + ", ".join(f"{f} {overall[f]}" for f in fams) +
           f". Oskorei by tier: {tiers}. Absolute difficulty is a knob; the comparisons are what count.\n")
a = b.index("## Part 11: Sim Results"); z = b.index("---", a)
b = b[:a] + results + "\n" + b[z:]
stats = open("catalog_stats.md").read()
a = b.index("## Part 10: Stat Blocks"); z = b.index("\n---\n", a)
b = b[:a] + "## Part 10: Stat Blocks\n\nGenerated from the sim's data (`sim/catalog.py`), with family bodies applied.\n\n" + stats + "\n" + b[z:]
# hunted-by: top three classes per family
a = b.index("## Part 2: Families at a Glance"); z = b.index("## Part 3", a)
part = b[a:z].split("\n")
for i, l in enumerate(part):
    m = re.match(r"\| \*\*(\w+)\*\* \|", l)
    if m and m.group(1) in fams:
        j = fams.index(m.group(1))
        top = sorted(rows, key=lambda r: -int(r[1][j][0]))[:3]
        cells = l.split(" | "); cells[-1] = ", ".join(f"{c} {v[j][0]}%" for c, v in top) + " |"
        part[i] = " | ".join(cells)
b = b[:a] + "\n".join(part) + b[z:]
open(B, "w").write(b)
print("bestiary refreshed")
