"""Record a finding's resolution in AGENT_CODE_REVIEW.md, keeping its ID.
    python3 tools/review_close.py ID "status cell" resolution.md
Replaces the status cell of the ID's row in the action index, and inserts the resolution block (markdown) after the
finding's Source line(s), i.e. just before the next ### heading."""
import re, sys
fid, status, block = sys.argv[1], sys.argv[2], open(sys.argv[3]).read().strip()
p = "/home/claude/AGENT_CODE_REVIEW.md"; s = open(p).read()
row = re.compile(rf"^(\| {fid} \|[^\n]*\| )([^|\n]*)( \|)$", re.M)
assert len(row.findall(s)) == 1, fid
s = row.sub(lambda m: m.group(1) + status + m.group(3), s)
head = re.search(rf"^### {fid} — .*$", s, re.M); assert head, fid
nxt = re.search(r"^### |^## ", s[head.end():], re.M)
at = head.end() + (nxt.start() if nxt else len(s) - head.end())
if "**Resolution" in s[head.end():at]: raise SystemExit(f"{fid} already has a resolution block")
s = s[:at].rstrip("\n") + "\n\n" + block + "\n\n" + s[at:]
open(p, "w").write(s); print("updated", fid)
