/* The fight screen: 320x180 pixel art, scaled up by whole numbers, with the watercolor text box drawn at full
   resolution underneath (fight_lab_spec Parts 2-6). Python runs the rules; this file draws and takes clicks.
   Needs from the page: window.Lab = { call(fn, ...args) -> parsed JSON, speed() -> ms, onState(r), onEvents(evs) }. */
"use strict";
const Screen = (() => {
  const W = 320, H = 180;
  const C = {
    ink: "#2e222f", white: "#ffffff", dim: "#9babb2", mute: "#7f708a", gold: "#f9c22b", shadow: "#625565",
    blue: "#4d9be6", bshade: "#484a77", red: "#e83b3b", rshade: "#6e2727", frame: "#cd683d",
    hpHi: "#1ebc73", hpMid: "#f9c22b", hpLo: "#e83b3b", hpBack: "#45293f", weak: "#fbff86", heal: "#91db69",
    absorb: "#8fd3ff", plate: "#2e222f", plateEdge: "#7f708a", plateLit: "#c7dcd0", plateDark: "#3e3546",
  };
  // 3x5 capitals and digits (PICO-8-like): rows top to bottom
  const TINY = {
    A: "010101111101101", B: "110101110101110", C: "011100100100011", D: "110101101101110", E: "111100110100111",
    F: "111100110100100", G: "011100101101011", H: "101101111101101", I: "111010010010111", J: "001001001101010",
    K: "101101110101101", L: "100100100100111", M: "101111111101101", N: "110101101101101", O: "010101101101010",
    P: "110101110100100", Q: "010101101110011", R: "110101110101101", S: "011100010001110", T: "111010010010010",
    U: "101101101101011", V: "101101101101010", W: "101101111111101", X: "101101010101101", Y: "101101010010010",
    Z: "111001010100111", "0": "010101101101010", "1": "010110010010111", "2": "110001010100111", "3": "110001010001110",
    "4": "101101111001001", "5": "111100110001110", "6": "011100110101010", "7": "111001010010010", "8": "010101010101010",
    "9": "010101011001110", "/": "001001010100100", "-": "000000111000000", "+": "000010111010000", ".": "000000000000010",
    "%": "101001010100101", "!": "010010010000010", ":": "000010000010000", ">": "100010001010100", "?": "110001010000010",
    " ": "000000000000000", "'": "010010000000000",
  };
  const MARTIAL = new Set(["Slash", "Crush", "Pierce"]);

  let A, atlas, wash, tracker, cord, CORD, badges, icons9, ICON9, bgs = {};   // assets (cord: Joseph's dialog frame, cut in pieces)
  let cv, ctx, Z = 3, P, pc, Q, pq;               // the screen canvas, its scale, the pixel layer, the overlay layer
  let sheetWash = null, sheetRect = null;         // the Inspect sheet's own watercolor: a fresh crop each time it opens
  let area = "Neutral", boxWash = null;           // the text box's watercolor, one crop per fight
  let S = null, units = {}, busy = false;         // Python's state; the drawn units; playing events
  let orders = {}, opts = {}, current = null;     // the player's orders this phase
  let mode = "menu", pending = null, scroll = 0;  // menu | info | pouch | cell | inspect
  let hover = null, hoverChip = null, inspectCard = null;
  let lines = [], floaters = [], trackRows = [], trackOff = 0, acted = 0;
  let mouse = null, t0 = performance.now(), hits = [];

  /* ------------------------------------------------------------ playback: the motion kit (Nov 9)
     Every creature is one static sprite (two for states such as a bone pile); life comes from these code motions.
     Times are ms at normal speed (fast and instant scale them); distances are whole pixels. Tune here. */
  const MOTION = {
    lunge:    { px: 6, out: 110, hold: 70, back: 150 },   // a martial attacker steps at its target and back
    hop:      { px: 4, dur: 240 },                        // casts, items, wind-ups, getting up
    flash:    { dur: 80 },                                // white silhouette on a hit
    shake:    { px: 2, dur: 260 },                        // damped, after the flash
    squash:   { rows: 1, dur: 140 },                      // whole rows only: bracing, landing
    bob:      { px: 1, period: 1700 },                    // idle breathing, out of step per unit
    look:     { idle: false, every: 11000, dur: 420 },    // a glance the other way: off while idle (Joseph, Nov 21:
                                                          // distracting); kept as a motion for reactions later
    dissolve: { dur: 650 },                               // death: a dithered fade
    step:     { dur: 190, px: 3 },                        // Move/Swap: one hop per cell
    hitstop:  { base: 70, weak: 150, crit: 150 },         // the freeze on contact
    slide:    { dur: 180 },                               // the tracker's chips moving up
    beat:     { act: 40, hit: 300, small: 200, round: 360, heal: 300, line: 140 },  // pauses between events
    autoflash:{ dur: 520 },                               // autopilot orders blink before the round plays
    pose:     { dur: 560 },                               // a move's frames (Drattr, bone-mage), spread over this long
    swap:     { beat: 260 },                              // the net Drattr: the pause before she fades to the spear
    bound:    { tick: 110, ticks: 4 },                    // Bound's swirl turns a quarter this often, this many times, then rests
  };
  let vt = 0, lastNow = null, freezeUntil = 0, skipping = false, speedF = 1, trackSlideT = -1e9;
  let fxs = [], FX = {}, fxImg = null, autoUntil = -1, confirmInfo = null;
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  const scratch = document.createElement("canvas"), sc = scratch.getContext("2d");

  /* ------------------------------------------------------------ loading */
  function img(src) { return new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => no(new Error(src)); i.src = src; }); }
  async function load(canvas) {
    cv = canvas; ctx = cv.getContext("2d");
    A = await (await fetch("assets/assets.json")).json();
    [atlas, wash, tracker, cord] = await Promise.all([img("assets/atlas.png"), img("assets/wash_grey.jpg"), img("assets/tracker.png"), img("assets/cord.png")]);
    badges = await img("assets/intents.png"); icons9 = await img("assets/icons9.png");
    ICON9 = await (await fetch("assets/icons9.json")).json();
    CORD = await (await fetch("assets/cord.json")).json();
    fxImg = await img("assets/fx.png"); FX = await (await fetch("assets/fx.json")).json();
    for (const a of ["Neutral", "Vatn", "Eld"]) bgs[a] = await img(`assets/bg_${a}.png`);
    P = document.createElement("canvas"); P.width = W; P.height = H; pc = P.getContext("2d");
    Q = document.createElement("canvas"); Q.width = W; Q.height = H; pq = Q.getContext("2d");
    fit(); window.addEventListener("resize", fit);
    cv.addEventListener("mousemove", e => { mouse = toPx(e); hoverAt(mouse); });
    cv.addEventListener("mouseleave", () => { mouse = null; hover = hoverChip = null; });
    cv.addEventListener("click", e => click(toPx(e)));
    cv.addEventListener("contextmenu", e => { e.preventDefault(); back(); });
    cv.addEventListener("wheel", e => { if (mode === "info") { scroll = Math.max(0, scroll + Math.sign(e.deltaY)); e.preventDefault(); }
                                        else if (S && S.phase !== "over") { trackOff = Math.max(0, trackOff + Math.sign(e.deltaY)); e.preventDefault(); } }, { passive: false });
    requestAnimationFrame(loop);
  }
  function fit() {
    const box = cv.parentElement.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    Z = Math.max(1, Math.floor(Math.min(box.width * dpr / W, 6)));
    cv.width = W * Z; cv.height = H * Z;
    cv.style.width = (W * Z / dpr) + "px"; cv.style.height = (H * Z / dpr) + "px";
    boxWash = null;
  }
  const toPx = e => { const r = cv.getBoundingClientRect(); return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height }; };

  /* ------------------------------------------------------------ the watercolor under the text box */
  function makeWash(seed, rect = A.areas[area].box) {
    const [x0, y0, x1, y1] = rect, w = (x1 - x0 + 1) * Z, h = (y1 - y0 + 1) * Z;
    const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
    let s = seed >>> 0; const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
    const sw = Math.min(wash.width, w), sh = Math.min(wash.height, h);
    const sx = Math.floor(rnd() * (wash.width - sw)), sy = Math.floor(rnd() * (wash.height - sh));
    g.save(); if (rnd() < .5) { g.translate(w, 0); g.scale(-1, 1); } if (rnd() < .5) { g.translate(0, h); g.scale(1, -1); }
    g.drawImage(wash, sx, sy, sw, sh, 0, 0, w, h); g.restore();
    const d = g.getImageData(0, 0, w, h), p = d.data;
    let lo = 255, hi = 0; for (let i = 0; i < p.length; i += 4 * 7) { lo = Math.min(lo, p[i]); hi = Math.max(hi, p[i]); }
    const ramp = A.areas[area].tint.map(h => [1, 3, 5].map(k => parseInt(h.slice(k, k + 2), 16)));
    for (let i = 0; i < p.length; i += 4) {
      const v = Math.min(1, Math.max(0, (p[i] - lo) / Math.max(1, hi - lo)));   // pale paper is light stone, pigment is ink
      const t = v * 2, k = Math.min(1, Math.floor(t)), f = t - k, a = ramp[k], b = ramp[k + 1];
      p[i] = a[0] + (b[0] - a[0]) * f; p[i + 1] = a[1] + (b[1] - a[1]) * f; p[i + 2] = a[2] + (b[2] - a[2]) * f;
    }
    g.putImageData(d, 0, 0); return c;
  }

  /* ------------------------------------------------------------ text */
  function textW(s) { let w = 0; for (const ch of s) w += ((A.font.glyphs[ch] || A.font.glyphs["?"]).w + 1); return Math.max(0, w - 1); }
  function text(x, y, s, col, sh = C.ink) {
    x = Math.round(x); y = Math.round(y);
    for (const pass of sh ? [0, 1] : [1]) {
      let cx = x; pc.fillStyle = pass ? col : sh;
      for (const ch of s) {
        const g = A.font.glyphs[ch] || A.font.glyphs["?"];
        for (const [gx, gy] of g.px) pc.fillRect(cx + gx + (pass ? 0 : 1), y + gy + (pass ? 0 : 1), 1, 1);
        cx += g.w + 1;
      }
    }
    return x + textW(s);
  }
  function tiny(x, y, s, col, sh = C.ink) {
    s = s.toUpperCase();
    for (const pass of sh ? [0, 1] : [1]) {
      let cx = x; pc.fillStyle = pass ? col : sh;
      for (const ch of s) {
        const g = TINY[ch] || TINY["?"];
        for (let i = 0; i < 15; i++) if (g[i] === "1") pc.fillRect(cx + i % 3, y + (i / 3 | 0) + (pass ? 0 : 1), 1, 1);
        cx += 4;
      }
    }
    return x + s.length * 4 - 1;
  }
  const tinyW = s => s.length * 4 - 1;
  function wrap(s, maxw) {
    const out = []; let cur = "";
    for (const w of s.split(" ")) { const t = cur ? cur + " " + w : w; if (textW(t) > maxw && cur) { out.push(cur); cur = w; } else cur = t; }
    if (cur) out.push(cur); return out;
  }

  /* ------------------------------------------------------------ units on the board */
  function spriteKey(u) {
    if (u.side === "party") return look(`hero:${u.cls}`, u.id);   // Joseph's 32R picks: a class has one or more looks
    const el = u.element, r = u.rank, f = u.family, has = k => A.sprites[k] ? k : null;
    if (f === "Mogel") return has(`mogel${r === "Halv" ? 16 : r === "Litel" ? 24 : 32}:${el}`);
    if (f === "Ande" || (!f && el)) return has(`${r === "Halv" ? "halvande" : "ande"}:${el}`) || has(`ande:${el}`) || has(`halvande:${el}`);
    if (f === "Draugr") return has(`draugr:${r}`);
    if (f === "Bein") return has(`bein:${r}`);
    if (f === "Drattr") return has(`drattr:${u.job}`) || look(`drattr:${r}`, u.id);   // the court: one set per job
    return null;
  }
  function look(key, id) {                        // a creature with several looks (key#1, key#2, ...) keeps one, picked by its id
    if (A.sprites[key]) return key;
    const n = Object.keys(A.sprites).filter(k => k.startsWith(key + "#")).length;
    if (!n) return null;
    const h = (id || "").split("").reduce((a, c) => a * 31 + c.charCodeAt(0), 7) >>> 0;
    return `${key}#${1 + h % n}`;
  }
  const REAR_BACK = 6;                            // the Rear stands a little further back in its cell, to give the intents room
  function foot(side, row, lane) {
    const g = A.geo, [ty, th] = g.lanes[lane], fy = ty + th - 5;
    const back = row === 1 ? (side === 0 ? -REAR_BACK : REAR_BACK) : 0;
    return [Math.round(g.GX[`${side}${row}`] + g.K * (g.FRONT - fy)) + (g.pitch - 16) / 2 + 8 + back, fy];
  }
  function cellPoly(side, row, lane) {
    const g = A.geo, [ty, th] = g.lanes[lane], e = y => g.GX[`${side}${row}`] + g.K * (g.FRONT - y);
    const xt = e(ty), xb = e(ty + th - 1);
    return [[xt, ty], [xt + g.pitch - 1, ty], [xb + g.pitch - 1, ty + th - 1], [xb, ty + th - 1]];
  }
  const sideOf = u => u.side === "party" ? 0 : 1, rowOf = c => c[0] === "front" ? 0 : 1;
  function syncUnits(board) {
    const keep = units; units = {};
    for (const b of board) {
      const u = Object.assign({}, keep[b.id] || {}, b);
      u.key = spriteKey(b); u.hp = b.hp !== undefined ? b.hp : (u.hp ?? null); u.frac = b.frac; u.defending = false;
      u.bound = (b.status || []).includes("Bound");
      if (!keep[b.id] || keep[b.id].key !== u.key) { u.anim = "idle"; u.animT = performance.now(); }
      units[b.id] = u;
    }
  }
  function unitBox(u) {
    if (!u.cell) return null;
    let [cx, fy] = foot(sideOf(u), rowOf(u.cell), u.cell[1]);
    if (u.slide) {                                  // Move/Swap: hopping from the old cell to the new one
      const sl = u.slide, p = Math.min(1, (vt - sl.t0) / sl.dur);
      if (p >= 1) u.slide = null;
      else {
        cx = Math.round(sl.from[0] + (cx - sl.from[0]) * p);
        const cells = Math.max(1, sl.cells), q = (p * cells) % 1;
        fy = Math.round(sl.from[1] + (fy - sl.from[1]) * p) - Math.round(Math.sin(Math.PI * q) * MOTION.step.px);
      }
    }
    const m = A.sprites[u.key];
    const w = m ? m.w : 14, h = m ? m.h : 22;
    return { x: cx - (m ? m.foot[0] : 7), y: fy - h, w, h, cx, fy };
  }
  function animFrame(u) {                         // static: one sprite per state (Nov 9). States: standing, downed hero, crawling Draugr
    const m = A.sprites[u.key]; if (!m) return null;
    const a = m.anims;
    if (u.side === "party" && u.state !== "up" && a.downed) return a.downed[0];
    if (u.crawling && u.alive && a.crawl) return a.crawl[0];
    const p = u.pose;                                // a move's frames (sets that opt in: the Drattr court, the bone-mage)
    if (p && vt - p.t0 < p.dur && a[p.name]) { const f = a[p.name]; return f[Math.min(f.length - 1, Math.floor((vt - p.t0) / p.dur * f.length))]; }
    return a.idle[0];
  }
  /* the motions running on a unit, summed: offset, flash, squash rows, flip, dissolve */
  function addFx(u, kind, dur, extra) { if (u) (u.fx = (u.fx || []).filter(f => vt - f.t0 < f.dur)).push(Object.assign({ kind, t0: vt, dur }, extra)); }
  function motion(u) {
    const o = { dx: 0, dy: 0, flash: false, rows: 0, flip: false, dissolve: 0 };
    const facing = u.side === "party" ? 1 : -1;
    for (const f of u.fx || []) {
      const t = vt - f.t0, p = t / f.dur; if (t < 0 || p >= 1) continue;
      if (f.kind === "lunge") {
        const L = MOTION.lunge, a = L.out / f.dur, b = (L.out + L.hold) / f.dur;
        o.dx += facing * Math.round(L.px * (p < a ? p / a : p < b ? 1 : 1 - (p - b) / (1 - b)));
      } else if (f.kind === "hop") o.dy -= Math.round(Math.sin(Math.PI * p) * (f.px || MOTION.hop.px));
      else if (f.kind === "shake") o.dx += Math.round(Math.sin(t / 22) * MOTION.shake.px * (1 - p));
      else if (f.kind === "flash") o.flash = true;
      else if (f.kind === "squash") o.rows += f.rows || MOTION.squash.rows;
      else if (f.kind === "look") o.flip = true;
    }
    if (u.state === "dying") o.dy += 3;            // the fallen lie on the floor (Nov 21)
    if (u.dieT !== undefined) o.dissolve = Math.min(1, (vt - u.dieT) / MOTION.dissolve.dur);
    else if (u.appearT !== undefined && vt - u.appearT < MOTION.dissolve.dur) o.dissolve = 1 - (vt - u.appearT) / MOTION.dissolve.dur;
    else if (u.alive && u.state !== "dying") {     // idle breath, out of step per unit; a rare look the other way
      const ph = ((u.id || "").split("").reduce((a, c) => a * 31 + c.charCodeAt(0), 7) >>> 0) % 1000 / 1000;
      if (((vt / MOTION.bob.period) + ph) % 1 > .55) o.dy -= MOTION.bob.px;
      if (!busy) {
        if (u.nextLook === undefined) u.nextLook = vt + MOTION.look.every * (0.4 + ph);
        if (MOTION.look.idle && vt > u.nextLook) { addFx(u, "look", MOTION.look.dur); u.nextLook = vt + MOTION.look.every * (0.6 + Math.random() * 0.8); }
      }
    }
    return o;
  }
  function drawSprite(u, b, fr) {
    const o = motion(u), w = fr[2], h = fr[3], rows = Math.min(o.rows, h - 1);
    const x = b.x + o.dx, y = b.y + o.dy + rows, hh = h - rows;           // squash: drop whole rows, feet stay put
    if (!o.flash && !o.flip && !o.dissolve) { pc.drawImage(atlas, fr[0], fr[1], w, h, x, y, w, hh); return; }
    scratch.width = w; scratch.height = h; sc.imageSmoothingEnabled = false;
    sc.drawImage(atlas, fr[0], fr[1], w, h, 0, 0, w, h);
    if (o.flash) { sc.globalCompositeOperation = "source-atop"; sc.fillStyle = C.white; sc.fillRect(0, 0, w, h); sc.globalCompositeOperation = "source-over"; }
    if (o.dissolve) {                               // ordered dither: pixels drop out in the Bayer order
      const d = sc.getImageData(0, 0, w, h), cut = o.dissolve * 16;
      for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) if (BAYER[(j & 3) * 4 + (i & 3)] < cut) d.data[(j * w + i) * 4 + 3] = 0;
      sc.putImageData(d, 0, 0);
    }
    pc.save();
    if (o.flip) { pc.translate(2 * b.cx, 0); pc.scale(-1, 1); }
    pc.drawImage(scratch, 0, 0, w, h, o.flip ? 2 * b.cx - x - w : x, y, w, hh);
    pc.restore();
  }
  function drawFx() {                              // hit effects and bursts, on the virtual clock (hit-stop freezes them)
    fxs = fxs.filter(f => vt - f.t0 < f.total);
    for (const f of fxs) {
      const m = FX[f.name]; let t = vt - f.t0, i = 0;
      while (i < m.n - 1 && t >= m.ms[i]) { t -= m.ms[i]; i++; }
      pc.save();
      if (f.flip) { pc.translate(2 * f.x, 0); pc.scale(-1, 1); }
      pc.drawImage(fxImg, m.x + i * m.w, m.y, m.w, m.h, Math.round(f.x - m.w / 2), Math.round(f.y - m.h / 2), m.w, m.h);
      pc.restore();
    }
  }

  /* ------------------------------------------------------------ drawing */
  function loop(now) {
    if (lastNow !== null && now >= freezeUntil) vt += now - lastNow;
    lastNow = now;
    if (A) draw(vt);
    requestAnimationFrame(loop);
  }
  function faceRect(u, b) {                       // where a unit's face is on screen (the atlas's 8x8 portrait spot)
    const m = A.sprites[u.key]; if (!m || !m.face) return null;
    return [b.x + m.face[0] - 1, b.y + m.face[1] - 1, 10, 10];
  }
  function barX(u, b, list) {                     // the bar sits under the feet, slid sideways off any face in front of it
    const x0 = b.cx - 9, y = b.fy + 2, w = 18, h = 4;
    const faces = list.filter(o => o !== u && (o.alive || o.state !== "up")).map(o => faceRect(o, unitBox(o))).filter(Boolean);
    const hits = x => faces.some(([fx, fy, fw, fh]) => x < fx + fw && x + w > fx && y < fy + fh && y + h > fy);
    if (!hits(x0)) return x0;
    for (let d = 1; d <= 18; d++) { if (!hits(x0 + d)) return x0 + d; if (!hits(x0 - d)) return x0 - d; }
    return x0;
  }
  function hpbar(x, y, frac, w = 16) {
    pc.fillStyle = C.ink; pc.fillRect(x, y, w + 2, 4);
    pc.fillStyle = C.hpBack; pc.fillRect(x + 1, y + 1, w, 2);
    if (frac > 0) { pc.fillStyle = frac > .5 ? C.hpHi : frac > .25 ? C.hpMid : C.hpLo; pc.fillRect(x + 1, y + 1, Math.max(1, Math.round(w * frac)), 2); }
  }
  function poly(pts, col) {
    pc.strokeStyle = col; pc.lineWidth = 1; pc.beginPath();
    pts.forEach(([x, y], i) => i ? pc.lineTo(Math.round(x) + .5, y + .5) : pc.moveTo(Math.round(x) + .5, y + .5));
    pc.closePath(); pc.stroke();
  }
  const ICON = {   // 7x7 intent glyphs
    strike: ["......#", ".....#.", "....#..", "#..#...", ".##....", ".##....", "#..#..."],
    pierce: ["....###", ".....##", "....#.#", "...#...", "..#....", "##.....", "##....."],
    crush:  [".####..", ".####..", ".####..", "...#...", "...#...", "...#...", "...#..."],
    spell:  ["...#...", ".#.#.#.", "..###..", "#######", "..###..", ".#.#.#.", "...#..."],
    heal:   ["..###..", "..###..", "#######", "#######", "#######", "..###..", "..###.."],
    hex:    ["...#...", "...#...", "...#...", "#..#..#", ".#.#.#.", "..###..", "...#..."],
    buff:   ["...#...", "..###..", ".#.#.#.", "#..#..#", "...#...", "...#...", "...#..."],
    guard:  ["#######", "#.....#", "#.....#", "#.....#", ".#...#.", "..#.#..", "...#..."],
    move:   ["...#...", "..###..", ".#.#.#.", "...#...", ".#.#.#.", "..###..", "...#..."],
    wind:   ["#######", ".#...#.", "..#.#..", "...#...", "..#.#..", ".#...#.", "#######"],
    item:   ["..###..", ".#...#.", "#######", "#.....#", "#.....#", "#.....#", "#######"],
  };
  function icon(x, y, name, col, edge) {          // a 9x9 ink tag, edged in the side's colour, the glyph in white or gold
    const g = ICON[name] || ICON.strike;
    pc.fillStyle = edge; pc.fillRect(x - 1, y - 1, 9, 9);
    pc.fillStyle = C.ink; pc.fillRect(x, y, 7, 7);
    pc.fillStyle = col; for (let j = 0; j < 7; j++) for (let i = 0; i < 7; i++) if (g[j][i] === "#") pc.fillRect(x + i, y + j, 1, 1);
  }
  function headTop(u, b) {                       // just above the head, not the top of the sprite's box (swords, bows)
    const m = A.sprites[u.key]; return m ? b.y + m.face[1] - 11 : b.y - 10;
  }
  function intentIcon(it) {
    if (!it) return null;
    const k = it.move_kind || it.kind;
    if (it.reason === "release" || it.reason === "bide") return "wind";
    if (it.move === "Guard" || it.move === "Defend" || k === "defend" || k === "cover") return "guard";
    if (k === "move" || ["Swap", "Move", "Step up", "Step off", "Fall back", "Advance"].includes(it.move)) return "move";
    if (k === "heal" || k === "revive" || k === "cleanse" || k === "mp") return "heal";
    if (k === "stat") return it.direction > 0 ? "buff" : "hex";
    if (k === "status") return "hex";
    if (it.item) return "item";
    return it.element === "Pierce" ? "pierce" : it.element === "Crush" ? "crush" : MARTIAL.has(it.element) ? "strike" : "spell";
  }

  function draw(now) {
    pc.clearRect(0, 0, W, H);
    const legal = legalTargets();
    // board highlights: legal targets (white), Move cells (white), the hovered unit's cell (dim)
    if (legal) for (const id of legal) { const u = units[id]; if (u && u.cell) poly(cellPoly(sideOf(u), rowOf(u.cell), u.cell[1]), C.white); }
    if (mode === "cell" && current && opts[current]) for (const c of cellChoices()) poly(cellPoly(0, rowOf(c.cell), c.cell[1]), C.white);
    // units, back to front
    const list = Object.values(units).filter(u => u.cell && (u.alive || u.piled || u.state !== "up" || vt < (u.fadeUntil || 0)));
    list.sort((a, b) => unitBox(a).fy - unitBox(b).fy);
    for (const u of list) {
      const b = unitBox(u), fr = animFrame(u, now);
      pc.fillStyle = C.ink; pc.beginPath(); pc.ellipse(b.cx, b.fy, 6, 2, 0, 0, Math.PI * 2); pc.fill();
      if (!fr) {                                            // no art yet: a labelled stand-in
        const o = motion(u);
        pc.fillStyle = u.side === "party" ? C.bshade : C.rshade; pc.fillRect(b.x + o.dx, b.y + o.dy, b.w, b.h);
        tiny(b.x + 1 + o.dx, b.y + 2 + o.dy, (u.rank || u.family || "?").slice(0, 3), C.white);
      } else if (u.piled) {                                 // the second state: a pile of bones (Joseph's frame 15, Nov 21)
        const pf = (A.sprites[u.key].anims.pile || [])[0], o = motion(u);
        if (pf) pc.drawImage(atlas, pf[0], pf[1], pf[2], pf[3], b.cx - (pf[2] >> 1) + o.dx, b.fy - pf[3] + 1, pf[2], pf[3]);
        else { const third = Math.ceil(fr[3] / 3); pc.drawImage(atlas, fr[0], fr[1] + fr[3] - third, fr[2], third, b.x + o.dx, b.fy - third, fr[2], third); }
      } else drawSprite(u, b, fr);
    }
    for (const u of list) {                                // bars, pips, intents, orders: above every sprite
      const b = unitBox(u);
      const bx = barX(u, b, list);
      if (u.alive) hpbar(bx, b.fy + 2, u.frac);
      if (u.side === "party" && u.state === "dying") { pc.fillStyle = C.hpLo; for (let i = 0; i < u.breaths; i++) pc.fillRect(bx + i * 4, b.fy + 2, 3, 3); }
      if (u.alive && u.knots) { pc.fillStyle = C.white; for (let i = 0; i < u.knots; i++) pc.fillRect(bx + i * 4, b.fy + 5, 3, 2); }   // the Skurmar's knots
      if (u.alive && u.counters && u.counters.length) {   // the stat counters (Nov 21): a short tag each, green up, red down
        const UP = { Mighty: 1, Fortified: 1, Evasive: 1, Keen: 1, Quick: 1 };
        let ty = b.fy + 5 + (u.knots ? 3 : 0) + (u.song ? 3 : 0), tx = bx;
        for (const c of u.counters.slice(0, 3)) { const [nm, n] = c.split(" "), tag = nm.slice(0, 3).toUpperCase() + n;
          tiny(tx, ty, tag, UP[nm] ? C.heal : C.hpLo); tx += tinyW(tag) + 3; }
      }
      if (u.alive && u.held && u.held.length) {           // holds (Nov 24, D3): a short tag and the rounds left, under the counters
        let ty = b.fy + 5 + (u.knots ? 3 : 0) + (u.song ? 3 : 0) + (u.counters && u.counters.length ? 6 : 0), tx = bx;
        for (const h of u.held) { const tag = h.name.slice(0, 3).toUpperCase() + h.rounds;
          tiny(tx, ty, tag, h.harmful ? C.hpLo : C.gold); tx += tinyW(tag) + 3; }
      }
      if (u.alive && u.song) { pc.fillStyle = C.gold; const sy = b.fy + (u.knots ? 8 : 5); for (let i = 0; i < u.song; i++) pc.fillRect(bx + i * 4, sy, 3, 2); }   // the Song's verses (gold)
      const top = headTop(u, b);
      if (u.alive && u.bound) footBadge(u, b, { reason: "bound" });   // netted: shown even mid-playback, where it lands
      else if (u.alive && (!busy || autoUntil > vt)) {   // what they're about to do: Joseph's 13x13 frame at the feet, facing the foe
        let it = null;
        if (u.side === "enemy") it = u.winding ? { reason: "bide" } : u.intent;
        else if (orders[u.id] && !(orders[u.id].auto && autoUntil > vt && Math.floor((autoUntil - vt) / 90) % 2)) it = orderIntent(u.id);
        if (it) footBadge(u, b, it);
      }
      if (false) {
        const atHero = u.intent && u.intent.target_id && units[u.intent.target_id] && units[u.intent.target_id].side === "party";
        const i9 = u.intent && icon9(u.intent);
        if (u.winding) icon(b.cx - 3, top, "wind", C.gold, C.gold);
        else if (i9 !== null && i9 !== undefined) {         // Joseph's 9x9 icons, on an ink tag edged red when aimed at a hero
          pc.fillStyle = atHero ? C.red : C.mute; pc.fillRect(b.cx - 5, top - 2, 13, 13);
          pc.fillStyle = C.ink; pc.fillRect(b.cx - 4, top - 1, 11, 11);
          pc.drawImage(icons9, i9 * 9, 0, 9, 9, b.cx - 3, top, 9, 9);
        }
        else if (u.intent) {
          const g = intentIcon(u.intent), col = g === "buff" ? C.hpHi : g === "hex" ? "#a884f3" : C.white;
          pc.fillStyle = atHero ? C.red : C.mute; pc.fillRect(b.cx - 5, top - 2, 13, 13);
          pc.fillStyle = C.ink; pc.fillRect(b.cx - 4, top - 1, 11, 11);
          const G = ICON[g] || ICON.strike; pc.fillStyle = col;
          for (let j = 0; j < 7; j++) for (let i = 0; i < 7; i++) if (G[j][i] === "#") pc.fillRect(b.cx - 2 + i, top + 1 + j, 1, 1);
        }
      }
      if (u.side === "party" && !busy) {
        if (u.id === current && S.phase !== "over") { pc.fillStyle = C.gold; pc.fillRect(b.cx - 2, top + 1, 5, 1); pc.fillRect(b.cx - 1, top + 2, 3, 1); pc.fillRect(b.cx, top + 3, 1, 1); }
        if (!orders[u.id] && u.winding) tiny(b.cx - (tinyW(u.winding.slice(0, 9)) >> 1), top - 7, u.winding.slice(0, 9), C.dim);
      }
      if (hover && hover.id === u.id) poly(cellPoly(sideOf(u), rowOf(u.cell), u.cell[1]), C.gold);
    }
    drawFx();
    drawFloaters(now);
    drawTracker(now);
    drawStatus();
    drawBox();
    drawCord(...A.areas[area].frame, false);
    pq.clearRect(0, 0, W, H);
    if (inspectCard) { const keep = pc; pc = pq; drawInspect(); pc = keep; }
    else if (hover || hoverChip) drawPlate(hover || hoverChip);
    // compose: the wash under the box window, the pixel art over it
    ctx.imageSmoothingEnabled = false;
    const fr = snapCord(...A.areas[area].frame);
    if (!boxWash) boxWash = makeFill(fightSeed, fr, false);
    ctx.fillStyle = C.ink; ctx.fillRect(0, 0, cv.width, cv.height);
    ctx.drawImage(boxWash, fr[0] * Z, fr[1] * Z);
    ctx.drawImage(bgs[area], 0, 0, W * Z, H * Z);
    ctx.drawImage(P, 0, 0, W * Z, H * Z);
    if (inspectCard) {
      if (!sheetWash) sheetWash = makeFill((Math.random() * 1e9) | 0, sheetRect, true);
      ctx.drawImage(sheetWash, sheetRect[0] * Z, sheetRect[1] * Z);
      ctx.drawImage(Q, 0, 0, W * Z, H * Z);
    } else sheetWash = null;
  }
  /* Joseph's cord frame, every corner as he drew it (assets/cord.json). The twist repeats every 4 px, so a box keeps its
     corners in phase only at some sizes: x1 - x0 = 1 (mod 4), y1 - y0 = 2 (mod 4). snapCord trims a box to the nearest
     smaller size that fits. Floating boxes take the bottom corners with heads attached. */
  function snapCord(x0, y0, x1, y1) {
    x1 -= (((x1 - x0 - 1) % 4) + 4) % 4; y1 -= (((y1 - y0 - 2) % 4) + 4) % 4;
    return [x0, y0, x1, y1];
  }
  /* The fill runs right up to the cord: into every notch of the twist on the inside, and no further. The region is
     traced from the cord itself (a flood fill from the middle, stopped by the cord's pixels). */
  function cordMask(rect, floating) {
    const [x0, y0, x1, y1] = rect, w = x1 - x0 + 1, h = y1 - y0 + 1;
    const t = document.createElement("canvas"); t.width = W; t.height = H;
    const keep = pc; pc = t.getContext("2d"); drawCord(x0, y0, x1, y1, floating); const px = pc.getImageData(x0, y0, w, h).data; pc = keep;
    const m = document.createElement("canvas"); m.width = w; m.height = h; const g = m.getContext("2d"), out = g.createImageData(w, h);
    const seen = new Uint8Array(w * h), stack = [((h >> 1) * w) + (w >> 1)];
    while (stack.length) {
      const i = stack.pop(); if (seen[i] || px[i * 4 + 3]) continue;
      seen[i] = 1; out.data[i * 4 + 3] = 255;
      const x = i % w, y = (i / w) | 0;
      if (x > 0) stack.push(i - 1); if (x < w - 1) stack.push(i + 1); if (y > 0) stack.push(i - w); if (y < h - 1) stack.push(i + w);
    }
    g.putImageData(out, 0, 0); return m;
  }
  function makeFill(seed, rect, floating) {
    const c = makeWash(seed, rect), g = c.getContext("2d");
    g.globalCompositeOperation = "destination-in"; g.imageSmoothingEnabled = false;
    g.drawImage(cordMask(rect, floating), 0, 0, c.width, c.height);
    return c;
  }
  function piece(k, x, y) { const p = CORD[k]; pc.drawImage(cord, p.r[0], p.r[1], p.r[2], p.r[3], x - p.a[0], y - p.a[1], p.r[2], p.r[3]); }
  function run(k, x, y, len, horiz) {
    const p = CORD[k], step = horiz ? p.r[2] : p.r[3];
    for (let i = 0; i < len; i += step) {
      const n = Math.min(step, len - i);
      if (horiz) pc.drawImage(cord, p.r[0], p.r[1], n, p.r[3], x + i, y - p.a[1], n, p.r[3]);
      else pc.drawImage(cord, p.r[0], p.r[1], p.r[2], n, x - p.a[0], y + i, p.r[2], n);
    }
  }
  function drawCord(x0, y0, x1, y1, floating) {
    [x0, y0, x1, y1] = snapCord(x0, y0, x1, y1);
    run("top", x0 + 4, y0, x1 - x0 - 7, true); run("bot", x0 + 4, y1, x1 - x0 - 7, true);
    run("lft", x0, y0 + 3, y1 - y0 - 6, false); run("rgt", x1, y0 + 3, y1 - y0 - 6, false);
    piece(floating ? "blh" : "bl", x0, y1); piece(floating ? "brh" : "br", x1, y1);
    piece("tl", x0, y0); piece("tr", x1, y0);
    return [x0, y0, x1, y1];
  }
  let fightSeed = 1;

  function drawFloaters(now) {
    floaters = floaters.filter(f => vt - f.t < 900);
    for (const f of floaters) {
      if (vt < f.t) continue;                      // a tag waiting its turn (WEAK after the number)
      const k = (vt - f.t) / 900, y = Math.round(f.y - 10 * k);
      tiny(f.x - (tinyW(f.s) >> 1), y, f.s, f.col);
    }
  }
  function drawTracker(now) {
    const x0 = 96, y0 = 1;
    pc.drawImage(tracker, x0, y0);
    pc.save(); pc.beginPath(); pc.rect(x0 + 3, y0 + 3, 123, 10); pc.clip();
    const rows = trackRows.slice(Math.min(trackOff + acted, Math.max(0, trackRows.length - 1)));
    const slide = Math.round(11 * Math.max(0, 1 - (vt - trackSlideT) / MOTION.slide.dur));   // chips slide up as turns pass
    rows.forEach((r, i) => {
      const x = x0 + 3 + i * 11 + slide, u = units[r.id]; if (x > x0 + 126) return;
      const edge = i === 0 && !busy ? C.gold : (r.side === "party" ? C.blue : C.red);
      pc.fillStyle = edge; pc.fillRect(x, y0 + 3, 10, 10);
      pc.fillStyle = r.side === "party" ? C.bshade : C.rshade; pc.fillRect(x + 1, y0 + 4, 8, 8);
      const m = u && A.sprites[u.key];
      if (m) { const fr = m.anims.idle[0]; pc.drawImage(atlas, fr[0] + m.face[0], fr[1] + m.face[1], 8, 8, x + 1, y0 + 4, 8, 8); }
      const suf = / ([A-H])$/.exec(r.name);
      if (suf) { pc.fillStyle = C.ink; pc.fillRect(x + 5, y0 + 6, 5, 7); tiny(x + 6, y0 + 7, suf[1], C.white, null); }
      if (!r.ordered) { pc.fillStyle = "rgba(46,34,47,.55)"; pc.fillRect(x + 1, y0 + 4, 8, 8); tiny(x + 4, y0 + 6, "?", C.white, null); }
      r._box = { x, y: y0 + 3, w: 10, h: 10 };
    });
    pc.restore();
  }
  function drawStatus() {                         // the party, top left: name, HP, MP (3x5)
    let y = 2;
    for (const u of Object.values(units).filter(u => u.side === "party")) {
      const col = u.state === "dead" ? C.hpLo : u.state === "dying" ? C.hpMid : u.id === current ? C.gold : C.white;
      tiny(3, y, u.name.slice(0, 9), col);
      tiny(41, y, `${u.hp}/${u.maxhp}`, u.state === "up" ? C.white : col);
      if (u.maxmp) tiny(77, y, String(u.mp), C.absorb);   // a martial hero has no MP pool (Nov 21)
      y += 6;
    }
    if (S) { const s = S.phase === "over" ? "OVER" : `ROUND ${S.round}${S.phase === "bonus" ? " BONUS" : ""}`; tiny(W - 3 - tinyW(s), 2, s, S.phase === "bonus" ? C.weak : C.white); }
  }
  function plateBox(y, linesArr, title, right) {
    const x0 = 8, x1 = W - 9, h = 8 + 11 * (linesArr.length + 1);
    pc.fillStyle = C.plate; pc.fillRect(x0, y, x1 - x0 + 1, h + 1);
    pc.strokeStyle = C.plateEdge; pc.strokeRect(x0 + 1.5, y + 1.5, x1 - x0 - 2, h - 2);
    pc.fillStyle = C.plateLit; pc.fillRect(x0 + 1, y + 1, x1 - x0 - 1, 1);
    text(x0 + 6, y + 4, title, C.gold); if (right) text(x1 - 6 - textW(right), y + 4, right, C.dim);
    linesArr.forEach((l, i) => text(x0 + 6, y + 15 + i * 11, l, C.white));
  }
  const FRAME = { foe: ["#9e4539", "#6e2727"], calm: ["#7f708a", "#3e3546"], mine: ["#4d9be6", "#484a77"] };
  function footBadge(u, b, it) {
    const atHero = it.target_id && units[it.target_id] && units[it.target_id].side === "party";
    const [outer, inner] = u.side === "party" ? FRAME.mine : atHero ? FRAME.foe : FRAME.calm;
    // just clear of the body, on the side facing the foe (a wide Mogel pushes it further out)
    // Joseph's 13x13 frame: a 1 px edge, a 1 px ring, the 9x9 icon centred
    const x = u.side === "party" ? Math.max(b.cx + 10, b.x + b.w + 1) : Math.min(b.cx - 23, b.x - 14), y = b.fy - 11;
    pc.fillStyle = outer; pc.fillRect(x, y, 13, 13);
    pc.fillStyle = inner; pc.fillRect(x + 1, y + 1, 11, 11);
    pc.fillStyle = C.ink; pc.fillRect(x + 2, y + 2, 9, 9);
    if (it.reason === "bound") {                    // netted: the swirl in the net's greens, a few quarter turns, then still
      const n = Math.min(MOTION.bound.ticks, Math.floor((vt - (u.boundT ?? -1e9)) / MOTION.bound.tick));
      pc.save(); pc.translate(x + 6.5, y + 6.5); pc.rotate(n * Math.PI / 2);
      pc.drawImage(icons9, ICON9.bound * 9, 0, 9, 9, -4.5, -4.5, 9, 9); pc.restore();
      return;
    }
    if (it.reason === "bide" || it.move_kind === "windup") {   // winding up: Joseph's aura, charging
      const f = ICON9["aura" + (1 + Math.floor(vt / 160) % 3)];
      pc.drawImage(icons9, f * 9, 0, 9, 9, x + 2, y + 2, 9, 9);   // the sparks loop on their own; the spiral is the still version
      return;
    }
    const i9 = icon9(it);
    if (i9 !== null && i9 !== undefined) pc.drawImage(icons9, i9 * 9, 0, 9, 9, x + 2, y + 2, 9, 9);
    else {
      const g = intentIcon(it), G = ICON[g] || ICON.strike;
      pc.fillStyle = g === "wind" ? C.gold : C.white;
      for (let j = 0; j < 7; j++) for (let i = 0; i < 7; i++) if (G[j][i] === "#") pc.fillRect(x + 3 + i, y + 3 + j, 1, 1);
    }
  }
  function orderIntent(id) {                       // a hero's order, described like an intent so it gets the same icon
    const o = orders[id], op = opts[id]; if (!o || !op) return null;
    if (o.key === "guard") return { move_kind: "defend" };
    if (o.key === "move") return { move_kind: "move", move: "Move" };
    if (o.key === "flee") return { move_kind: "flee", move: "Flee" };
    const mv = [op.halv, ...op.moves, ...op.items].find(m => m && m.key === o.key); if (!mv) return null;
    return { move_kind: mv.kind, element: mv.element, all: mv.aim === "all", shape: mv.aim === "row" ? "row" : null,
             reach: mv.card && mv.card.reach, item: mv.slot === "item" ? mv.key : null, direction: mv.kind === "stat" ? (mv.targets.some(t => units[t] && units[t].side === "party") ? 1 : -1) : null };
  }
  function icon9(it) {                           // which of Joseph's 9x9 icons says what this enemy is about to do
    const k = it.move_kind, el = it.element, wide = it.all || it.shape === "row";
    if (it.item || it.status === "Bound") return ICON9[k === "heal" || k === "mp" || k === "revive" ? "potion" : "chest"];   // the net is thrown like an item
    if (k === "defend" || it.move === "Defend" || it.move === "Guard") return ICON9.guard;
    if (k === "flee") return ICON9.step;   // boot kicking up dust: bolting
    if (k === "move" || ["Swap", "Move", "Step up", "Step off", "Fall back", "Advance"].includes(it.move)) return ICON9.flee;   // boot with speed lines: moving
    if (k === "cover") return ICON9.cover;
    if (k === "heal" || k === "revive" || k === "cleanse") return ICON9.heal;
    if (k === "stat") return ICON9[it.direction > 0 ? "buff" : "hex"];
    if (k === "status") return ICON9.hex;
    if (k !== "damage") return null;                 // moves, wind-ups, fleeing: the small glyphs
    if (el === "Slash") return ICON9[wide ? "slash_sweep" : "slash"];
    if (el === "Crush") return ICON9[wide ? "crush_sweep" : "crush"];
    if (el === "Pierce") return it.reach === "any" ? ICON9[wide ? "volley" : "arrow"] : ICON9.stab;
    return ICON9["magic:" + el] ?? ICON9.magic;
  }
  const BADGE = { crush: 0, strike: 1, spell: 2, pierce: 3 };
  function badge(it, x, y) {                     // Joseph's 16x16 intent badges; motion lines red when it's coming for a hero
    const ic = intentIcon(it); if (!(ic in BADGE)) return false;
    const atHero = it.target_id && units[it.target_id] && units[it.target_id].side === "party";
    pc.drawImage(badges, (BADGE[ic] + (atHero ? 4 : 0)) * 18, 0, 18, 18, x, y, 18, 18); return true;
  }
  function drawPlate(u) {                        // hover: who this is, and what they're about to do
    if (u.id && units[u.id]) u = units[u.id];
    const it = u.intent, o = orders[u.id], ls = [];
    if (o) ls.push(o.label);
    else if (u.winding) ls.push(`Winding up ${u.winding}.`);
    else if (it && u.side === "enemy" && u.alive) {
      ls.push(`${it.shown}${it.target ? " -> " + it.target : ""}`);
      if (it.why) ls.push(...wrap("Why: " + it.why + ".", W - 30).slice(0, 1));
    }
    if (u.piled) ls.push("A pile of bones. It will stand again unless crushed.");
    if (u.state === "dying") ls.push(`Dying: ${u.breaths} breaths left.`);
    plateBox(19, ls.slice(0, 2), u.name, u.side === "party" ? `${u.hp}/${u.maxhp} HP` : "");
    if (u.side === "enemy" && u.alive && it && !u.winding) badge(it, W - 9 - 22, 21);
  }

  /* ------------------------------------------------------------ the text box */
  const BOX = { rows: [137, 149, 161], wordX: [16, 110], costR: [96, 190], utilX: [210, 256], div: 199 };
  let boxHits = [];
  function boxItem(x, y, w, label, onClick, enabled = true, selected = false, hoverKey = null) {
    boxHits.push({ x: x - 8, y: y - 1, w: w + 10, h: 11, onClick, enabled, hoverKey });
    const hot = mouse && enabled && mouse.x >= x - 8 && mouse.x < x + w + 2 && mouse.y >= y - 1 && mouse.y < y + 10;
    if (selected || hot) text(x - 8, y, ">", C.gold);
    return text(x, y, label, enabled ? (selected ? C.gold : C.white) : C.mute);
  }
  function clip(s, maxW) {                          // a name too long for its slot ends in "." (the move's card says it whole)
    if (textW(s) <= maxW) return s;
    while (s.length > 1 && textW(s + ".") > maxW) s = s.slice(0, -1);
    return s + ".";
  }
  function divider() { run("lft", BOX.div, 138, 34, false); }      // a strand of the cord between moves and utilities
  const NUM = ["No", "One", "Two", "Three", "Four", "Five", "Six"];
  function drawBox() {
    boxHits = [];
    if (mode === "confirm" && confirmInfo && !busy) {          // Fight with orders missing: say so, then OK or Back
      const n = confirmInfo.missing.length;
      text(14, BOX.rows[0], `${NUM[n] || n} hero${n === 1 ? " does" : "es do"} not have orders.`, C.white);
      text(14, BOX.rows[1], confirmInfo.stuck.length ? `${confirmInfo.stuck.join(", ")} can't attack and will Guard.`
                                                   : (n === 1 ? "They will strike a foe at random." : "They will strike foes at random."), C.dim);
      boxItem(BOX.utilX[0], BOX.rows[2], textW("OK"), "OK", autopilot, true, true);
      boxItem(BOX.utilX[1], BOX.rows[2], textW("Back"), "Back", back, true);
      return;
    }
    if (busy || !S || S.phase === "over" || !current || !opts[current]) {   // narration
      const ls = lines.slice(-3);
      ls.forEach((l, i) => text(14, BOX.rows[i], l.s, l.col || C.white));
      return;
    }
    const o = opts[current];
    divider();
    // the right half: the utilities, always live
    const n = o.items.reduce((a, b) => a + b.count, 0);
    const util = [
      ["Pouch", () => { mode = mode === "pouch" ? "menu" : "pouch"; pending = null; }, o.items.length > 0, mode === "pouch"],
      ["Guard", () => order("guard", null, "Guard", "Guard"), true],
      ["Move", () => { mode = "cell"; pending = null; }, o.move.cells.length > 0, mode === "cell"],
      ["Flee", () => order("flee", null, "Flee", "Flee"), o.flee.allowed],
      ["Inspect", () => { mode = "inspect"; pending = null; }, true, mode === "inspect"],
      [Object.values(orders).some(x => x.key === "flee") ? "Fight!" : "Fight", fight, canFight()],
    ];
    util.forEach(([label, fn, en, sel], i) => {
      const x = BOX.utilX[i < 3 ? 0 : 1], y = BOX.rows[i % 3];
      if (label.startsWith("Fight")) { if (en) boxItem(x, y, textW(label), label, fn, true, true); else text(x, y, label, C.mute); }
      else {
        const end = boxItem(x, y, textW(label), label, fn, en, sel);
        if (label === "Flee") text(end + 3, y, o.flee.allowed ? String(Math.round(o.flee.chance * 100)) : "NO", C.dim);   // the chance in %, sized like a cost (no "%": it would run past the frame)
      }
    });
    // the left half: the moves, or one move's card, or the pouch
    if (mode === "info" && pending) return drawInfo(pending);
    if (mode === "pouch") {
      o.items.slice(0, 3).forEach((it, i) => {
        const ok = it.aim === "self" || it.aim === "all" || it.targets.length > 0;
        const nm = clip(it.name, BOX.costR[1] - BOX.wordX[0] - textW("x" + it.count) - 4);
        boxItem(BOX.wordX[0], BOX.rows[i], textW(nm), nm, () => pick(it), ok);
        text(BOX.costR[1] - textW("x" + it.count), BOX.rows[i], "x" + it.count, C.dim);
      });
      return;
    }
    const moves = [o.halv, ...o.moves, o.meditate].filter(Boolean).slice(0, 6);   // Meditate: the magicals' sixth space
    moves.forEach((mv, i) => {
      const col = i < 3 ? 0 : 1, y = BOX.rows[i % 3], x = BOX.wordX[col];
      const ok = mv.afford && (mv.aim === "self" || mv.aim === "all" || mv.targets.length > 0 || (mv.aim === "cell" && (mv.cells || []).length > 0));
      const cost = mv.cost ? String(mv.cost) : "";
      const nm = clip(mv.shown, BOX.costR[col] - x - (cost ? textW(cost) + 4 : 0));
      boxItem(x, y, textW(nm), nm, () => pick(mv), ok, pending && pending.key === mv.key);
      if (cost) text(BOX.costR[col] - textW(cost), y, cost, !ok ? C.mute : mv.drops ? C.hpLo : C.dim);   // red: a last swing
    });
  }
  const RANGE_TAG = { melee: "RANGE SHORT", reach: "RANGE MEDIUM", any: "RANGE LONG" };   // Nov 10: range is the weapon's
  function drawInfo(mv) {
    let plain = (mv.card && mv.card.plain) || "", tag = "";
    plain = plain.replace(/ Range (Short|Medium|Long):[^.]*\./, "").replace(" Thrown: reaches anywhere.", "");   // the tag says it
    if (mv.kind === "damage" && mv.card) tag = RANGE_TAG[mv.card.reach] || "";
    const cost = mv.cost ? `${mv.cost} ${mv.cost_type}` : (mv.slot === "item" ? `x${mv.count}` : "free");
    boxItem(10, BOX.rows[0], textW("<"), "<", back);
    const x = text(BOX.wordX[0] + 2, BOX.rows[0], mv.shown, C.gold);
    if (tag) tiny(x + 4, BOX.rows[0] + 3, tag, C.dim);
    text(BOX.costR[1] - textW(cost), BOX.rows[0], cost, mv.drops ? C.hpLo : C.dim);
    const hint = mv.afford && (mv.aim === "self" || mv.aim === "all");      // inside the box, on its last row (Nov 21)
    const rows = hint || !mv.afford || mv.drops ? 1 : 2;
    const ls = wrap(plain, BOX.costR[1] - BOX.wordX[0]);
    scroll = Math.min(scroll, Math.max(0, ls.length - rows));
    ls.slice(scroll, scroll + rows).forEach((l, i) => text(BOX.wordX[0], BOX.rows[1 + i], l, C.white));
    if (ls.length > scroll + rows) tiny(BOX.costR[1] - 3, BOX.rows[rows] + 4, "V", C.gold, null);
    if (scroll > 0) tiny(BOX.costR[1] - 3, BOX.rows[1] - 1, "^", C.gold, null);
    if (hint) {   // nothing to aim: the title, the body and the hint all use it (Nov 21: Meditate had nothing to click)
      boxHits.push({ x: BOX.wordX[0], y: BOX.rows[0] - 1, w: BOX.costR[1] - BOX.wordX[0], h: BOX.rows[2] + 11 - BOX.rows[0], onClick: () => pick(mv), enabled: true });
    }
    if (!mv.afford) text(BOX.wordX[0], BOX.rows[2], mv.why === "Silenced" ? "Silenced." : `Not enough ${mv.cost_type}.`, C.hpLo);
    else if (mv.drops) tiny(BOX.wordX[0] + (hint ? 92 : 0), BOX.rows[2] + 3, "LAST SWING: YOU WILL FALL", C.hpLo, null);   // the last-HP rule (Nov 21)
    else if (hint) tiny(BOX.wordX[0], BOX.rows[2] + 3, "CLICK AGAIN TO USE", C.gold, null);
  }
  function drawInspect() {                       // the sheet, as the Company remembers it
    const c = inspectCard, x0 = 50, y0 = 26;
    const [, , x1, y1] = drawCord(x0, y0, x0 + 221, y0 + 98, true), w = x1 - x0 + 1, h = y1 - y0 + 1;  // eslint-disable-line
    sheetRect = [x0, y0, x1, y1];
    text(x0 + 6, y0 + 4, c.name, C.gold);
    const sub = [c.rank, c.element, c.side === "party" ? c.cls : null, `L${c.level}`].filter(Boolean).join(" ");
    tiny(x0 + w - 6 - tinyW(sub), y0 + 7, sub, C.dim);
    tiny(x0 + 6, y0 + 18, "HP " + (c.hp === null ? "?" : `${c.hp}/${c.maxhp}`), C.white);
    if (c.maxmp !== 0) tiny(x0 + 70, y0 + 18, "MP " + (c.mp === null ? "?" : `${c.mp}/${c.maxmp}`), C.white);
    if (c.known && !c.known.all && c.side === "enemy") tiny(x0 + 134, y0 + 18, `FELLED ${c.known.kills}`, C.dim);
    let y = y0 + 27;
    if (c.intent) {
      const u = units[c.id];
      if (u && u.intent && c.side === "enemy" && badge(u.intent, x1 - 24, y - 4)) {}
      tiny(x0 + 6, y, "INTENDS " + (c.intent.shown + (c.intent.target ? " > " + c.intent.target : "")).slice(0, 44), C.white); y += 7;
    }
    const st = Object.entries(c.status).map(([k, v]) => `${k} ${v}`).concat(Object.entries(c.stages).map(([k, v]) => `${k} ${v > 0 ? "+" : ""}${v}`))
      .concat(Object.entries(c.held || {}).map(([k, h]) => `${k}: ${h.stat} held, ${h.rounds} round${h.rounds === 1 ? "" : "s"}`));   // holds (D3)
    if (st.length) { tiny(x0 + 6, y, st.join("  ").slice(0, 56), C.hpMid); y += 7; }
    y += 2;
    const affs = Object.entries(c.affinities), cols = 4;
    affs.forEach(([k, v], i) => {
      const x = x0 + 7 + (i % cols) * 53, yy = y + Math.floor(i / cols) * 8;
      const col = v === "?" ? C.dim : v === "weak" ? C.weak : v === "absorb" ? C.absorb : v === "normal" ? C.plateLit : C.white;
      tiny(x, yy, `${k} ${v === "normal" ? "-" : v === "?" ? "?" : v}`.slice(0, 13), col);
    });
    tiny(x0 + w - 7 - tinyW("CLICK TO CLOSE"), y0 + h - 10, "CLICK TO CLOSE", C.dim);
  }

  /* ------------------------------------------------------------ input */
  function unitAt(p) {
    const list = Object.values(units).filter(u => u.cell && (u.alive || u.piled || u.state === "dying"));
    list.sort((a, b) => unitBox(b).fy - unitBox(a).fy);
    for (const u of list) { const b = unitBox(u); if (p.x >= b.x - 2 && p.x < b.x + b.w + 2 && p.y >= b.y - 10 && p.y < b.fy + 6) return u; }
    for (const u of list) { if (inPoly(p, cellPoly(sideOf(u), rowOf(u.cell), u.cell[1]))) return u; }
    return null;
  }
  function cellAt(p) {
    for (const row of [0, 1]) for (let lane = 0; lane < 3; lane++) if (inPoly(p, cellPoly(0, row, lane))) return [row ? "rear" : "front", lane];
    return null;
  }
  function inPoly(p, pts) {
    let inside = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      const [xi, yi] = pts[i], [xj, yj] = pts[j];
      if ((yi > p.y) !== (yj > p.y) && p.x < (xj - xi) * (p.y - yi) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }
  function hoverAt(p) {
    hover = null; hoverChip = null;
    if (p.y < 18) { for (const r of trackRows) if (r._box && p.x >= r._box.x && p.x < r._box.x + 10 && p.y >= r._box.y && p.y < r._box.y + 10) { hoverChip = units[r.id] || null; } return; }
    if (p.y < 132) hover = unitAt(p);
  }
  function click(p) {
    if (!S || !A) return;
    if (inspectCard) { inspectCard = null; return; }
    for (const h of boxHits) if (p.x >= h.x && p.x < h.x + h.w && p.y >= h.y && p.y < h.y + h.h) { if (h.enabled) h.onClick(); return; }
    if (busy || S.phase === "over") { const u = unitAt(p); if (u) inspectCard = Lab.call("inspect", u.id); return; }
    if (mode === "cell") {                            // Move, or a move aimed at a cell (Skrida)
      const c = cellAt(p), mv = c && cellChoices().find(x => x.cell[0] === c[0] && x.cell[1] === c[1]);
      if (mv && pending && pending.aim === "cell")
        return order(pending.key, mv.cell, `${pending.shown} -> ${mv.swap ? mv.swap_name : mv.cell[0] + " " + (mv.cell[1] + 1)}`, pending.shown);
      if (mv) return order("move", mv.cell, mv.swap ? `Swap with ${mv.swap_name}` : `Move to ${mv.cell[0]} ${mv.cell[1] + 1}`, mv.swap ? "Swap" : "Move");
      return;
    }
    const u = unitAt(p); if (!u) return;
    if (mode === "inspect") { inspectCard = Lab.call("inspect", u.id); mode = "menu"; return; }
    if (mode === "info" && pending) {
      if (pending.targets.includes(u.id)) return order(pending.key, u.id, `${pending.shown} -> ${u.name}`, pending.shown);
      if (pending.aim === "self" && u.id === current) return pick(pending);      // a self move: clicking the hero uses it
      return;
    }
    if (u.side === "party" && S.awaiting.includes(u.id)) { current = u.id; mode = "menu"; pending = null; return; }
    inspectCard = Lab.call("inspect", u.id);
  }
  function cellChoices() { return pending && pending.aim === "cell" ? pending.cells : opts[current].move.cells; }
  function legalTargets() { return mode === "info" && pending && pending.aim !== "self" ? pending.targets : null; }   // All: every one lit
  function pick(mv) {
    if ((mv.aim === "self" || mv.aim === "all") && mode === "info" && pending === mv)   // nothing to aim: a second click uses it
      return order(mv.key, null, mv.shown + (mv.aim === "all" ? " -> all" : ""), mv.shown);
    pending = mv; scroll = 0; mode = mv.aim === "cell" ? "cell" : "info";
  }
  function order(key, target, label, short) {
    const r = Lab.call("submit", current, key, JSON.stringify(target));
    if (!r.ok) { say("Can't: " + r.error, C.hpLo); return; }
    orders[current] = { key, target, label, short };
    mode = "menu"; pending = null; inspectCard = null;
    const next = S.awaiting.find(id => !orders[id]); if (next) current = next;
    refreshTrack();
  }
  function back() { inspectCard = null; confirmInfo = null; if (mode !== "menu") { mode = "menu"; pending = null; } }
  function canFight() { return S && S.phase !== "over" && !busy && S.awaiting.length > 0; }
  function ready() { return canFight() && S.awaiting.every(id => orders[id]); }
  function fight() {
    if (!canFight()) return;
    if (!ready()) {                                // orders missing: ask first, autopilot on OK
      const missing = S.awaiting.filter(id => !orders[id]);
      const usable = m => m && m.afford && !m.drops && (m.aim === "self" || m.aim === "all" || m.targets.length);
      const stuck = missing.filter(id => { const o = opts[id]; if (!o) return true;   // no Halv: their simplest attack (lab.autofill)
        return !(o.halv ? usable(o.halv) : o.moves.some(m => m.kind === "damage" && usable(m))); });
      confirmInfo = { missing, stuck: stuck.map(id => units[id] ? units[id].name : id) }; mode = "confirm"; pending = null; inspectCard = null;
      return;
    }
    commitRound();
  }
  /* Playback sessions (AGENT_CODE_REVIEW C02): every fight is a session. Its continuations are scheduled through later()
     and checked with live() after every await, so starting a new fight retires everything the old one left pending:
     no old timer or animation can commit, or write state into, the new fight. */
  let gen = 0; const timers = new Set();
  function later(fn, ms) {
    const g = gen, id = setTimeout(() => { timers.delete(id); if (g === gen) fn(); }, ms); timers.add(id);
  }
  function retire() { gen++; for (const id of timers) clearTimeout(id); timers.clear(); busy = false; autoUntil = -1; }
  function autopilot() {                           // every hero without orders Halv-strikes (lab.autofill: spread, random, recorded)
    const r = Lab.call("autofill"); confirmInfo = null; mode = "menu";
    for (const x of r) orders[x.id] = { key: x.key, target: x.target, label: x.target && units[x.target] ? `${x.shown} -> ${units[x.target].name}` : x.shown, short: x.shown, auto: true };
    refreshTrack();
    const wait = MOTION.autoflash.dur * speedOf();
    if (!wait) return commitRound();
    busy = true; autoUntil = vt + wait;            // the filled orders blink, then the round plays
    later(() => { busy = false; autoUntil = -1; commitRound(); }, wait);
  }
  function commitRound() { const r = Lab.call("commit"); if (r.error) return say(r.error, C.hpLo); play(r); }
  function speedOf() { return Lab.speed() / 220; }
  function key(e) {
    if (!S) return;
    if (e.key === "Escape") return back();
    if (e.key === " " && busy) { skipping = true; freezeUntil = 0; return; }
    if (e.key === "Enter") return mode === "confirm" ? autopilot() : fight();
    if (e.key === "ArrowRight") { trackOff++; return; } if (e.key === "ArrowLeft") { trackOff = Math.max(0, trackOff - 1); return; }
    if (e.key === "ArrowDown" && mode === "info") { scroll++; return; } if (e.key === "ArrowUp" && mode === "info") { scroll = Math.max(0, scroll - 1); return; }
    if (e.key === "Tab" && S.awaiting.length) {
      e.preventDefault(); const i = S.awaiting.indexOf(current);
      current = S.awaiting[(i + (e.shiftKey ? -1 : 1) + S.awaiting.length) % S.awaiting.length]; mode = "menu"; pending = null; return;
    }
    const n = "123456".indexOf(e.key);
    if (n >= 0 && current && opts[current] && mode !== "pouch") { const mv = [opts[current].halv, ...opts[current].moves, opts[current].meditate].filter(Boolean)[n]; if (mv && mv.afford) pick(mv); }
  }

  /* ------------------------------------------------------------ playing a batch of events (Nov 9)
     One event at a time: the actor moves, the effect plays, contact freezes the clock (hit-stop), the target flashes
     and shakes, the number rises, the line goes in the box. Space skips the rest of the round. */
  function say(s, col) { for (const l of wrap(s, W - 30)) lines.push({ s: l, col }); lines = lines.slice(-40); }
  function pose(u, e) {                           // which move frames this act gets: its own name, big, cast, or attack
    const m = A.sprites[u.key]; if (!m || !m.poses) return;
    const a = m.anims, own = (e.shown || "").replace(/["!]/g, ""), magic = e.move_kind !== "damage" || !MARTIAL.has(e.element);
    const big = e.all || e.tier === "Mer" || e.tier === "Jatte";
    const name = a[own] ? own : big && a.big ? "big" : magic && a.cast ? "cast" : a.attack ? "attack" : a.cast ? "cast" : null;
    if (name) u.pose = { name, t0: vt, dur: MOTION.pose.dur * Math.max(1, a[name].length / 2) };
  }
  function floatAt(id, s, col, delay = 0) { const u = units[id]; if (!u) return; const b = unitBox(u); if (b) floaters.push({ x: b.cx, y: Math.max(30, b.y - 2), s, col, t: vt + delay }); }   // tall sprites: stay under the tracker
  function refreshTrack() { try { trackRows = Lab.call("preview"); } catch { trackRows = []; } }
  const sleep = ms => {                          // a retired session's animations never resume (C02)
    const g = gen;
    if (skipping || !speedF || ms <= 0) return g === gen ? Promise.resolve() : new Promise(() => {});
    return new Promise(res => setTimeout(() => { if (g === gen) res(); }, ms * speedF));
  };
  async function hitstop(ms) { if (skipping || !speedF) return; freezeUntil = performance.now() + ms * speedF; await sleep(ms); }
  function centre(u) { const b = unitBox(u); return b ? [b.cx, b.y + Math.round(b.h * .55)] : null; }
  function playFx(name, u) {                     // returns ms to the impact frame
    const m = FX[name], c = u && centre(u); if (!m || !c) return 0;
    fxs.push({ name, x: c[0], y: c[1], t0: vt, total: m.ms.reduce((a, b) => a + b, 0), flip: u.side === "party" });
    return m.ms.slice(0, m.impact).reduce((a, b) => a + b, 0);
  }
  const HIT_FX = { Slash: "hit_slash", Crush: "hit_crush2", Pierce: "hit_pierce2" };
  const fxFor = el => HIT_FX[el] || (FX["burst:" + el] ? "burst:" + el : "burst:Martial");
  const NARRATE = new Set(["held", "unheld", "act", "transform", "hit", "absorb", "heal", "stat", "status", "resist", "defend", "cover", "covered", "move", "windup", "bide_lost",
    "paint", "skip", "silenced", "tick", "down", "reform", "crawl", "pile", "scatter", "reassemble", "dying", "breath", "dead", "revive",
    "stabilised", "item", "mp", "fled", "flee_failed", "retarget", "fizzle", "shatter", "flurry", "cleanse", "immune", "thaw",
    "taunt", "drawn", "flare", "rooted", "weak", "out_of_reach", "song", "song_fades", "knot", "follow", "wall", "spent", "whiff"]);
  const UPS = new Set(["Mighty", "Fortified", "Keen", "Evasive", "Quick"]);   // the counters' up names
  async function play(r) {
    const g = gen, live = () => g === gen;       // this session only: a newer fight retires it
    if (r.error) { busy = false; return say(r.error, C.hpLo); }
    busy = true; mode = "menu"; pending = null; inspectCard = null; confirmInfo = null; acted = 0; trackOff = 0;
    skipping = false; speedF = speedOf();
    const ev = r.events;
    for (let i = 0; i < ev.length; i++) {
      const e = ev[i];
      Lab.onEvent(e);
      if (e.kind === "round") say(`Round ${e.n}`, C.gold);
      else if (e.kind === "bonus") say("Bonus Round!", C.weak);
      else if (e.kind === "end") say({ party: "Victory.", enemy: "The party has fallen.", fled: "The party got away.", draw: "Neither side gives way." }[e.winner], C.white);
      else if (NARRATE.has(e.kind) && e.text) say(e.text, e.kind === "hit" && e.affinity === "weak" ? C.weak : null);
      if (["act", "scatter", "defend", "move", "item", "windup", "skip", "cover"].includes(e.kind)) { acted++; trackSlideT = vt; }
      await step(e, ev[i + 1]);
      if (!live()) return;
    }
    if (!live()) return;
    for (const l of r.learned || []) Lab.onLearn(l);
    skipping = false; freezeUntil = 0;
    S = r; syncUnits(r.board); busy = false; orders = {}; opts = {}; acted = 0; trackOff = 0;
    Lab.onState(r);
    if (S.phase === "over") { current = null; trackRows = []; return; }
    refreshTrack();
    if (Lab.auto() || S.awaiting.length === 0) { later(() => play(Lab.call("commit")), speedF ? 450 * speedF : 0); return; }
    for (const id of S.awaiting) opts[id] = Lab.call("options", id);
    current = S.awaiting[0]; mode = "menu";
  }
  /* what each event looks like, and how long the player waits after it */
  async function step(e, next) {
    const B = MOTION.beat, u = e.unit_id && units[e.unit_id];
    switch (e.kind) {
      case "round": case "bonus": return sleep(B.round);
      case "act": {
        if (!u) return sleep(B.line);
        u.winding = null; pose(u, e);
        if (e.move_kind === "damage" && MARTIAL.has(e.element)) { const L = MOTION.lunge; addFx(u, "lunge", L.out + L.hold + L.back); return sleep(L.out); }
        addFx(u, "hop", MOTION.hop.dur); return sleep(MOTION.hop.dur * .5);
      }
      case "item": if (u) addFx(u, "hop", MOTION.hop.dur); return sleep(MOTION.hop.dur * .5);
      case "hit": {
        if (!u) return sleep(B.line);
        const toImpact = playFx(fxFor(e.element), u);
        await sleep(toImpact);
        const crit = (e.results || []).includes("crit"), weak = e.affinity === "weak";
        u.hp = e.hp; u.frac = e.maxhp ? e.hp / e.maxhp : u.frac;
        addFx(u, "flash", MOTION.flash.dur); addFx(u, "shake", MOTION.shake.dur);
        floatAt(e.unit_id, e.parts ? e.parts.join("+") : String(e.dmg), weak ? C.weak : crit ? C.gold : C.white);   // Twin Slash: N+M
        if (weak) floatAt(e.unit_id, "WEAK", C.weak, 140);
        else if (crit) floatAt(e.unit_id, "CRIT", C.gold, 140);
        if (e.affinity === "resist" || e.affinity === "null") floatAt(e.unit_id, e.affinity.toUpperCase(), C.dim, 140);
        await hitstop(weak ? MOTION.hitstop.weak : crit ? MOTION.hitstop.crit : MOTION.hitstop.base);
        return sleep(next && next.kind === "hit" ? B.hit * .5 : B.hit);      // a sweep's hits come quicker
      }
      case "whiff": if (u) { addFx(u, "hop", MOTION.hop.dur, { px: 2 }); floatAt(e.unit_id, "MISS", C.dim); } return sleep(B.hit);   // the new roll (Nov 21): it lands nothing
      case "absorb": if (u) { u.hp = e.hp; u.frac = Math.min(1, e.hp / ((u.maxhp || e.hp) || 1)); playFx("spark:" + (e.element || "Martial"), u); floatAt(e.unit_id, "+" + e.amount, C.absorb); floatAt(e.unit_id, "ABSORB", C.absorb, 140); } return sleep(B.hit);
      case "heal":
        if (u) pose(u, e);
        (e.target_ids || []).forEach((id, i) => { const t = units[id], x = e.targets[i]; if (t && x) { t.hp = x.hp; t.frac = t.maxhp ? x.hp / t.maxhp : t.frac; playFx("spark:Gro", t); addFx(t, "hop", MOTION.hop.dur, { px: 2 }); floatAt(id, "+" + x.amount, C.heal); } });
        return sleep(B.heal);
      case "stat": case "cleanse":
        if (u) pose(u, e);
        (e.target_ids || []).forEach(id => { const t = units[id]; if (t) playFx(e.direction > 0 || e.kind === "cleanse" ? "spark:Gro" : "spark:Natt", t); });
        return sleep(B.heal);
      case "status":
        if (u && e.status === "Bound") { u.bound = true; u.boundT = vt; addFx(u, "squash", MOTION.squash.dur, { rows: 2 }); return sleep(B.hit); }   // netted
        if (u && UPS.has(e.status)) { playFx("spark:Gro", u); return sleep(B.small); }       // Evasive from a glide
        if (u) { playFx("spark:Natt", u); addFx(u, "shake", MOTION.shake.dur * .6); } return sleep(B.small);
      case "skip": if (u && e.why === "Bound") { u.bound = false; addFx(u, "shake", MOTION.shake.dur); } return sleep(B.line);
      case "transform": {                              // the net is spent: a beat, fade out, the spear, fade in
        if (!u) return sleep(B.line);
        await sleep(MOTION.swap.beat);
        u.dieT = vt; await sleep(MOTION.dissolve.dur);
        u.job = e.job; u.key = spriteKey(u); u.dieT = undefined; u.appearT = vt;
        return sleep(MOTION.dissolve.dur);
      }
      case "song": (e.target_ids || []).forEach((id, i) => { const t = units[id]; if (t) { t.song = (e.stacks || [])[i] || 0; addFx(t, "hop", MOTION.hop.dur, { px: 2 }); } }); return sleep(B.small);
      case "song_fades": if (u && e.status === "Song") u.song = e.stacks; return sleep(B.small);
      case "knot": if (u) { u.knots = e.knots; if (e.knots > (e.was || 0)) addFx(u, "hop", MOTION.hop.dur); } return sleep(B.small);
      case "mp": if (u) { playFx("spark:Vatn", u); floatAt(e.unit_id, "+" + e.amount + " MP", C.absorb); } return sleep(B.small);
      case "tick": if (u) { u.hp = e.hp; u.frac = u.maxhp ? e.hp / u.maxhp : u.frac; addFx(u, "flash", MOTION.flash.dur); floatAt(e.unit_id, String(e.dmg), C.hpMid); } return sleep(B.small);
      case "defend": if (u) { u.defending = true; addFx(u, "squash", MOTION.squash.dur); } return sleep(B.small);
      case "cover": if (u) addFx(u, "hop", MOTION.hop.dur, { px: 2 }); return sleep(B.small);
      case "move": {
        if (!u) return sleep(B.line);
        const from = u.cell ? foot(sideOf(u), rowOf(u.cell), u.cell[1]) : null;
        const n = u.cell ? Math.abs(rowOf(u.cell) - rowOf(e.cell)) + Math.abs(u.cell[1] - e.cell[1]) : 1;
        const dur = MOTION.step.dur * Math.max(1, n) * (speedF ? 1 : 0);
        if (from && dur && !skipping) u.slide = { from, t0: vt, dur: dur, cells: Math.max(1, n) };
        const o = e.swapped_id && units[e.swapped_id];
        if (o) { const of = o.cell ? foot(sideOf(o), rowOf(o.cell), o.cell[1]) : null; if (of && dur && !skipping) o.slide = { from: of, t0: vt, dur, cells: Math.max(1, n) }; o.cell = e.other_cell; }
        u.cell = e.cell;
        return sleep(MOTION.step.dur * Math.max(1, n) + 60);
      }
      case "windup": if (u) { u.winding = e.shown; addFx(u, "hop", MOTION.hop.dur, { px: 2 }); } return sleep(B.small);
      case "down": if (u) { u.alive = false; u.frac = 0; addFx(u, "flash", MOTION.flash.dur); u.dieT = vt + MOTION.flash.dur; u.fadeUntil = vt + MOTION.flash.dur + MOTION.dissolve.dur; } return sleep(MOTION.dissolve.dur * .6);
      case "pile": if (u) { u.alive = false; u.piled = true; u.frac = 0; u.dieT = undefined; addFx(u, "squash", MOTION.squash.dur, { rows: 2 }); } return sleep(B.small);
      case "scatter": { const t = e.target_id && units[e.target_id]; if (t) { t.piled = false; t.dieT = vt; t.fadeUntil = vt + MOTION.dissolve.dur; } return sleep(B.small); }
      case "crawl": if (u) { u.crawling = true; u.alive = true; u.dieT = undefined; u.frac = e.hp / e.maxhp; addFx(u, "squash", MOTION.squash.dur, { rows: 2 }); } return sleep(B.small);
      case "reform": if (u) { u.name = e.unit; u.rank = e.rank; u.key = spriteKey(u); u.frac = e.hp / e.maxhp; u.alive = true; u.dieT = undefined; addFx(u, "flash", MOTION.flash.dur); addFx(u, "hop", MOTION.hop.dur); } return sleep(B.heal);
      case "reassemble": if (u) { u.alive = true; u.piled = false; u.dieT = undefined; u.cell = e.cell; u.frac = e.hp / e.maxhp; addFx(u, "hop", MOTION.hop.dur); addFx(u, "flash", MOTION.flash.dur); } return sleep(B.heal);
      case "dying": if (u) { u.state = "dying"; u.alive = false; u.hp = 0; u.frac = 0; u.breaths = e.breaths; addFx(u, "shake", MOTION.shake.dur); } return sleep(B.hit);
      case "breath": if (u) u.breaths = e.breaths; return sleep(B.line);
      case "dead": if (u) { u.state = "dead"; u.breaths = 0; } return sleep(B.line);
      case "revive": { const t = e.target_id && units[e.target_id]; if (t) { t.state = "up"; t.alive = true; t.hp = e.hp; t.frac = t.maxhp ? e.hp / t.maxhp : .1; playFx("spark:Sol", t); addFx(t, "hop", MOTION.hop.dur); floatAt(e.target_id, "UP", C.heal); } return sleep(B.heal); }
      case "stabilised": if (u) { u.state = "up"; u.alive = true; u.hp = e.hp; } return sleep(B.line);
      case "end": return sleep(B.round);
      default: return NARRATE.has(e.kind) && e.text ? sleep(B.line) : null;
    }
  }

  /* ------------------------------------------------------------ a new fight */
  function begin(r, areaName) {
    retire();                                     // the old fight's continuations can't reach this one
    area = A.areas[areaName] ? areaName : "Neutral";
    fightSeed = (Math.random() * 1e9) | 0; boxWash = null;
    units = {}; lines = []; floaters = []; fxs = []; orders = {}; opts = {}; current = null; mode = "menu"; pending = null; inspectCard = null; confirmInfo = null;
    S = Object.assign({}, r); syncUnits(r.board);
    play(r);
  }
  function inspectId(id) { inspectCard = Lab.call("inspect", id); }
  return { load, begin, key, inspectId, _play: play, get state() { return S; }, get debug() { return { mode, pending: pending && pending.key, busy, current, hits: boxHits.map(h => [h.x, h.y, h.w, h.h, h.enabled]),
    units: Object.values(units).filter(u => u.cell).map(u => { const b = unitBox(u); return { id: u.id, name: u.name, side: u.side, alive: u.alive, hp: u.hp, key: u.key, bound: !!u.bound, pose: u.pose && vt - u.pose.t0 < u.pose.dur ? u.pose.name : null, cx: b.cx, cy: Math.round((b.y + b.fy) / 2) }; }),
    cells: [0, 1].flatMap(r => [0, 1, 2].map(l => ({ cell: [r ? "rear" : "front", l], xy: foot(0, r, l) }))), lines: lines.slice(-3).map(l => l.s) }; } };
})();
