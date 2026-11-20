"""Step 7 check: fights recorded by the Fight Lab page (Pyodide, wasm32) replayed natively, compared line by line.

    python3 check_page.py checks/page_auto.jsonl [checks/page_fuzz.jsonl ...]

A record holds the seeds, party, pack and every order; the log holds every line the page wrote (intents included).
Same engine + same orders must give the same log, the same winner and the same number of rounds."""
import json, sys
import lab, replay

def log_lines(events):
    out = []
    for e in events:
        if e["kind"] == "round": out.append(f"-- Round {e['n']}")
        elif e["kind"] == "intent":
            out.append(f"   [{e['side'][0]}] {e['unit']} intends {e['shown']}" + (f" -> {e['target']}" if e.get("target") else "")
                       + (f" ({e['why']})" if e.get("why") else ""))
        elif e.get("text"): out.append(e["text"])
    return out

def check(rec):
    b = replay.replay(rec)
    mine, page = log_lines(b.events), rec["log"]
    if page and page[0].startswith("... (earlier lines cut)"): page = page[1:]; mine = mine[-len(page):]
    problems = []
    if rec.get("engine") != lab.ENGINE: problems.append(f"engine {rec.get('engine')} != {lab.ENGINE}")
    if (b.winner, b.round) != (rec["winner"], rec["rounds"]): problems.append(f"result {b.winner}/{b.round} vs page {rec['winner']}/{rec['rounds']}")
    if mine != page:
        i = next((k for k, (x, y) in enumerate(zip(mine, page)) if x != y), min(len(mine), len(page)))
        problems.append(f"log differs at line {i}: native {mine[i:i+1]} | page {page[i:i+1]} ({len(mine)} vs {len(page)} lines)")
    return problems

if __name__ == "__main__":
    total = bad = 0; wins = {}
    for path in sys.argv[1:]:
        for line in open(path):
            rec = json.loads(line); total += 1
            wins[rec["winner"]] = wins.get(rec["winner"], 0) + 1
            p = check(rec)
            if p: bad += 1; print(rec.get("hab"), rec["lab_seed"], rec["bseed"], *p, sep=" | ")
    print(f"{total} fights, {bad} mismatched; winners {wins}")
