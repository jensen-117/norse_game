/* The workbench's judge (grammar library L3): is a carve legal, and if not, why, in the compiler's own words.
   It reads only lexicon.json's `bench` table and hero words, which sim/lexicon.py writes from the compiler, and
   test_gloss.py runs it against words.compile_verb on every carve, so the page and the compiler can't disagree.
   A carve: { verb, tier: "Halv"|"Base"|"Mer", target: null|"Flok"|"All", manners: [...], styng: bool,
              rider: null | "Lonn" | a rider word }. */
(function (root) {
  function key(verb, tier, target, manners, styng, riderWord) {
    return [verb, tier || "Base", target || "", manners.join("+"), styng ? "S" : "", riderWord || ""].join("|");
  }
  function judge(lex, c) {
    const B = lex.bench, out = { reasons: [], word: null, parts: [] };
    if (!c.verb) { out.reasons.push("Pick a verb: every word needs a root."); return out; }
    const refuse = B.refuse[c.verb] || {}, own = B.own_rider[c.verb];
    const manners = B.manner_order.filter(m => (c.manners || []).includes(m));
    const parts = [...(c.tier && c.tier !== "Base" ? [c.tier] : []), ...(c.target ? [c.target] : []), ...manners,
                   ...(c.styng ? ["Styng"] : []), ...(c.rider ? [c.rider] : [])];
    out.parts = parts;
    for (const p of parts) if (refuse[p]) out.reasons.push(refuse[p]);
    if (manners.filter(m => B.speed_manners.includes(m)).length > 1) out.reasons.push(`${c.verb}: Swift and Heavy contradict each other`);
    const riderWord = !c.rider ? "" : c.rider === "Lonn" ? own : c.rider;
    if (!out.reasons.length && parts.length > B.cap) {
      const canon = parts.map(p => p === c.rider ? (riderWord === own ? "Lonn" : riderWord) : p).sort();
      const cap = Object.entries(B.capstones).find(([, s]) => s.verb === c.verb && s.parts.join() === canon.join());
      if (!cap) out.reasons.push(`Too many parts: a move carries ${B.cap}, unless together they make a capstone.`);
    }
    if (out.reasons.length) return out;
    const k = key(c.verb, c.tier, c.target, manners, c.styng, riderWord);
    out.word = (lex._byKey ||= Object.fromEntries(lex.hero_words.map(h => [h.key, h])))[k] || null;
    if (!out.word) out.reasons.push("The compiler refuses this carve, for a reason the bench doesn't know yet.");
    return out;
  }
  // ---------------------------------------------------------------- L4: take a word apart (lexicon.parses, in JS)
  function atomTable(lex) {
    return lex._atoms ||= Object.keys(lex.words).filter(k => !/[ !']/.test(k)).map(k => [k.toLowerCase(), k]);
  }
  function parses(lex, word, table) {
    table = table || atomTable(lex); const V = lex.bench.vowels, w = word.toLowerCase(), n = w.length;
    const best = { [n]: [[]] };
    for (let i = n - 1; i >= 0; i--) {
      const cands = [];
      for (const [sp, k] of table) {
        const ends = [];
        if (w.startsWith(sp, i)) ends.push(i + sp.length);
        if (i > 0 && sp[0] === w[i - 1] && sp.length > 1 && w.startsWith(sp.slice(1), i)) ends.push(i + sp.length - 1);
        if (V.includes(sp.at(-1)) && sp.length > 1 && w.startsWith(sp.slice(0, -1), i)) { const j = i + sp.length - 1; if (j < n && V.includes(w[j])) ends.push(j); }
        for (const j of ends) for (const rest of best[j] || []) cands.push([k, ...rest]);
      }
      if (!cands.length) { best[i] = []; continue; }
      const m = Math.min(...cands.map(c => c.length)), seen = new Set();
      best[i] = cands.filter(c => c.length === m && !seen.has(c.join()) && seen.add(c.join()));
    }
    return best[0];
  }
  function broken(lex, parse) {   // lexicon.grammatical: the rule a reading breaks, or null
    const W = lex.words, own = lex.bench.rider_owners;
    for (let i = 0; i < parse.length - 1; i++) {
      const a = parse[i], kind = W[a].kind, nxt = parse[i + 1];
      if (["verb", "weapon", "name"].includes(kind)) return `${a} is a move's root: nothing follows it`;
      if (kind === "family" && W[nxt].kind !== "rank") return `${a} is a family: only its job follows it`;
      if (kind === "rider" && own[a] && !own[a].includes(nxt)) return `${a} belongs to ${own[a].join("/")}`;
    }
    for (let i = 0; i < parse.length; i++)
      if (W[parse[i]].kind === "stat" && (i === 0 || !["Auk", "Ned"].includes(parse[i - 1]))) return `${parse[i]} needs Auk or Ned before it`;
    return null;
  }
  // a reading's atoms -> a hero carve, or why it isn't one
  function carveOf(lex, atoms) {
    const W = lex.words, B = lex.bench, c = { verb: null, tier: "Base", target: null, manners: [], styng: false, rider: null };
    const why = [], add = p => {
      if (["Halv", "Mer"].includes(p)) c.tier = p;
      else if (["Flok", "All"].includes(p)) c.target = p;
      else if (B.manner_order.includes(p)) c.manners.push(p);
      else if (p === "Styng") c.styng = true;
      else if (p === "Lonn") c.rider = "Lonn";
      else c.rider = p;
    };
    atoms.forEach((a, i) => {
      const k = W[a].kind, last = i === atoms.length - 1;
      if (B.name_parts[a] && last) { c.verb = B.name_parts[a].verb; B.name_parts[a].parts.forEach(add); }
      else if (lex.verbs[a] && last) c.verb = a;
      else if (["Halv", "Mer", "Flok", "All", "Styng", "Lonn"].includes(a) || B.manner_order.includes(a)) add(a);
      else if (B.rider_words.includes(a) && !last) add(a);
      else if (["Jatte", "Ur"].includes(a)) why.push(`${a} is found or worn, not carved: the foes' grammar and gear`);
      else if (a === "Mark") why.push("Mark (a spot on the ground) is the foes' grammar");
      else if (["family", "rank"].includes(k)) why.push(`${a} names a creature, not a move`);
      else why.push(`${a} (${k.replace("_", " ")}) has no hero verb to sit on yet: the foes' grammar`);
    });
    if (!c.verb && !why.length) why.push("No verb in it: every move needs a root");
    return { carve: c, why };
  }
  function takeApart(lex, word) {
    const ps = parses(lex, word), out = { word, readings: [] };
    for (const p of ps) {
      const r = { atoms: p, broken: broken(lex, p) };
      if (!r.broken) { const { carve, why } = carveOf(lex, p); r.why = why; if (!why.length) { r.carve = carve; r.judged = judge(lex, carve); } }
      out.readings.push(r);
    }
    const pick = out.readings.find(r => r.judged && r.judged.word) || out.readings.find(r => !r.broken) || out.readings[0];
    out.best = pick || null;
    return out;
  }
  // ---------------------------------------------------------------- L4: coin a word (collisions and near-collisions)
  function dist(a, b) {
    const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
    for (let j = 1; j <= b.length; j++) d[0][j] = j;
    for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++)
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return d[a.length][b.length];
  }
  function allNames(lex) {
    return lex._names ||= [...new Set([...Object.keys(lex.words).filter(k => !/[ !']/.test(k)), ...lex.hero_words.map(h => h.name),
      ...lex.enemy_moves.filter(m => !m.english).map(m => m.name), ...lex.enemy_units.map(u => u.name)])];
  }
  function coin(lex, word) {
    const w = word.trim(), lw = w.toLowerCase(), out = { word: w, exists: null, readsAs: [], near: [], seams: [] };
    if (!w) return out;
    out.exists = allNames(lex).find(n => n.toLowerCase() === lw) || null;
    out.readsAs = parses(lex, w).filter(p => p.length > 1 || p[0].toLowerCase() !== lw);
    const cap = lw.length <= 4 ? 1 : 2;
    out.near = allNames(lex).map(n => [n, dist(lw, n.toLowerCase())]).filter(([n, d]) => d > 0 && d <= cap)
      .sort((a, b) => a[1] - b[1] || a[0].length - b[0].length).slice(0, 16).map(([n, d]) => ({ name: n, dist: d }));
    // the prefixes it would wear: does the compound read cleanly, or into something else?
    const table = atomTable(lex).some(([sp]) => sp === lw) ? atomTable(lex) : [...atomTable(lex), [lw, w]];
    for (const pre of ["Halv", "Mer", "Flok", "All", "Snar", "Styng"]) {
      const v = lex.bench.vowels, a = pre.toLowerCase();
      let joined = a.at(-1) === lw[0] ? a + lw.slice(1) : v.includes(a.at(-1)) && v.includes(lw[0]) ? a.slice(0, -1) + lw : a + lw;
      joined = joined[0].toUpperCase() + joined.slice(1);
      const rs = parses(lex, joined, table);
      out.seams.push({ prefix: pre, name: joined, readings: rs, clean: rs.length === 1 && rs[0].join() === [pre, w].join() });
    }
    return out;
  }

  const api = { judge, key, parses, broken, carveOf, takeApart, coin, dist };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.BenchRules = api;
})(typeof window !== "undefined" ? window : this);
