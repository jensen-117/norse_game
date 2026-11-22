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
  const api = { judge, key };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.BenchRules = api;
})(typeof window !== "undefined" ? window : this);
