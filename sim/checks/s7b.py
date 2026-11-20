"""Step 7b: random legal orders, through the page's Python and the page's playback (instant), recorded for replay."""
from playwright.sync_api import sync_playwright
import json, time
OUT = "/home/claude/sim/checks/page_fuzz.jsonl"
FUZZ = r"""
async ([seed, hab, level, budget]) => {
  // a tiny seeded rng so a fuzz run can be repeated
  let x = seed * 2654435761 >>> 0; const R = () => ((x = (x * 1664525 + 1013904223) >>> 0) / 4294967296);
  const pick = a => a[Math.floor(R() * a.length)];
  const items = ["small_life","life","strong_life","small_spirit","spirit","strong_spirit","surgeons_kit","mead","pocket_sand","firecracker","thunderpot","iron_knife","iron_axe","iron_hammer","smoke_pot"];
  const spec = [0,1,2].map(() => ({ cls: "random", level, pouch: [0,1,2].map(() => [pick(items), 1 + Math.floor(R() * 2)]) }));
  Lab.call("set_seed", seed); Lab.call("make_party", JSON.stringify(spec));
  const pk = Lab.call("roll_pack", hab, budget, "any", level, true); if (pk.error) return { skip: pk.error };
  let r = Lab.call("start", "party"); Screen.begin(r, "Neutral");
  const wait = async () => { while (Screen.debug.busy) await new Promise(res => setTimeout(res, 5)); };
  await wait();
  let rounds = 0, kinds = {}, used = {};
  while (Screen.state.phase !== "over" && rounds < 60) {
    for (const id of Screen.state.awaiting) {
      if (R() < 0.15) continue;                                   // leave some for the autopilot
      const o = Lab.call("options", id), ch = [];
      const aimed = m => m.afford && (m.aim === "self" || m.aim === "all" || m.targets.length);
      for (const m of [o.halv, ...o.moves, ...o.items].filter(Boolean)) if (aimed(m)) ch.push(["move", m]);
      ch.push(["guard"]);
      if (o.move && o.move.cells.length) ch.push(["cell"]);
      if (o.flee && o.flee.allowed && R() < 0.08) ch.push(["flee"]);
      const c = pick(ch); let res;
      if (c[0] === "move") { const m = c[1]; const t = (m.aim === "self" || m.aim === "all") ? null : pick(m.targets); res = Lab.call("submit", id, m.key, JSON.stringify(t)); used[m.slot] = (used[m.slot] || 0) + 1; }
      else if (c[0] === "guard") res = Lab.call("submit", id, "guard", "null");
      else if (c[0] === "cell") res = Lab.call("submit", id, "move", JSON.stringify(pick(o.move.cells).cell));
      else res = Lab.call("submit", id, "flee", "null");
      if (!res.ok) return { error: "submit refused: " + res.error + " " + JSON.stringify(c[0]) };
    }
    if (Screen.state.awaiting.length) Lab.call("autofill");
    r = Lab.call("commit"); if (r.error) return { error: "commit: " + r.error };
    for (const e of r.events) kinds[e.kind] = (kinds[e.kind] || 0) + 1;
    Screen._play(r); await wait(); rounds++;
  }
  const rec = Lab.call("record"); rec.hab = hab; return { rec, kinds, used };
}"""
HABS = ["Barrow", "Wildwood", "Rapids", "Biome: Mire", "Biome: Ashfield", "Biome: Eldhall", "Biome: Natthall", "Biome: Solhall"]
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
    errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    p.goto("http://127.0.0.1:8765/index.html")
    p.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=120000)
    p.select_option("#speed", "0")
    out = open(OUT, "w"); t0 = time.time(); kinds = {}; used = {}; n = 0
    for k in range(96):
        res = p.evaluate(FUZZ, [1000 + k, HABS[k % len(HABS)], 24 + (k % 9) * 2, 5 + k % 6])
        if "skip" in res: continue
        if "error" in res: print("ERROR", k, res["error"]); continue
        out.write(json.dumps(res["rec"]) + "\n"); n += 1
        for d, src in ((kinds, res["kinds"]), (used, res["used"])):
            for kk, v in src.items(): d[kk] = d.get(kk, 0) + v
    print(n, "fights", round(time.time() - t0), "s; page errors:", errs[:3])
    print("event kinds:", dict(sorted(kinds.items(), key=lambda x: -x[1])))
    print("order slots:", used)
    b.close()
