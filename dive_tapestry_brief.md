# Brief: a code-drawn mock of the dive tapestry

You're making a mock of the map screen for a turn-based pixel-art dungeon game with a Norse setting. The map is a **woven tapestry** that fills in as the party walks a dungeon, in the spirit of Slay the Spire's map but read left to right like a woven saga. Draw it **entirely with code** (Python + Pillow, or JS canvas), as clean pixel art.

## 1. Research first (look, don't copy)

Look up real pieces and study how they're built before drawing anything:
- **The Överhogdal tapestries** (Härjedalen, Sweden, Viking Age; held at Jamtli, Östersund): linen ground, figures in red, blue-black and brown wool; stylised horses, riders, ships, buildings, trees, all in a flat, blocky, left-to-right procession.
- **The Bayeux Tapestry:** the central narrative band between two narrow borders full of small beasts, knots and running motifs; how the borders frame without competing.
- **The Oseberg tapestry fragments:** processions, wagons, figures in a narrow band.
- **Norse interlace and ornament:** Borre ring-chain, Jelling ribbon animals, Mammen, Ringerike and Urnes styles; simple interlace knots (two-strand plait, triquetra, endless knot); filigree borders and corner pieces. Note how interlace reads at small sizes: over-under breaks every crossing, consistent strand width.
- **Gotland picture stones** (Lärbro, Tängelgårda), only for mood: the game's Rune Gate screen is a carved stone; the tapestry is what it opens onto.

Make everything original: take the vocabulary (procession, flat figures, border rhythm, interlace logic), not any specific design.

## 2. Hard rules

- **Palette:** Resurrect 64, exactly these 64 colours, nothing else:
  `2e222f 3e3546 625565 966c6c ab947a 694f62 7f708a 9babb2 c7dcd0 ffffff 6e2727 b33831 ea4f36 f57d4a ae2334 e83b3b fb6b1d f79617 f9c22b 7a3045 9e4539 cd683d e6904e fbb954 4c3e24 676633 a2a947 d5e04b fbff86 165a4c 239063 1ebc73 91db69 cddf6c 313638 374e4a 547e64 92a984 b2ba90 0b5e65 0b8a8f 0eaf9b 30e1b9 8ff8e2 323353 484a77 4d65b4 4d9be6 8fd3ff 45293f 6b3e75 905ea9 a884f3 eaaded 753c54 a24b6f cf657f ed8099 831c5d c32454 f04f78 f68181 fca790 fdcbb0`
- **Pixel art:** no anti-aliasing, no blur, no gradients, no alpha blending, 1 px lines, whole-number scaling only (nearest neighbour). Dithering is fine.
- **Colours by role:**
  - Cream linen field (fdcbb0, with ab947a / fca790 / 966c6c for weave texture and wear).
  - Borders and edges in blues (323353, 484a77, 4d65b4), wine reds and purples (7a3045, 753c54, 831c5d, 6b3e75, 45293f).
  - Stitched glyphs in the same reds, blues and purples, like wool on linen.
- **Screen:** the game is **320×180**. The tapestry occupies the top **~130 px**; the bottom ~50 px is the game's text box (draw a plain dark placeholder box there: 2e222f with a 1 px 625565 edge).

## 3. Layout

- **Borders:** about **16 px top and bottom**, decorated with interlace, knots and small running motifs (Bayeux-like beasts are welcome). Corner or end pieces where a band starts and ends.
- **The middle strip:** about **90 px tall**, mostly bare cream. This is where the choices are stitched.
- **Three bands, one per leg of the dive,** joined end to end along one long tapestry. Each band has an **accent colour** in its border (try: band 1 wine red, band 2 deep blue, band 3 purple) on the same cream field. A divider ornament where one band meets the next.
- **A leg, left to right:** an entry fight glyph, then **three columns of 2 to 4 glyphs**, then an **elite** glyph. After band 3's elite, a **boss** glyph. Columns are about **44 px apart**.
- **Threads:** each glyph joins one or two glyphs in the next column by a thread (1 px, stitched look: dashes or a two-tone running stitch).
- **Glyphs:** main room glyphs **13×13**, in a flat Överhogdal style. Make placeholder glyphs for: fight (a figure with a sword), elite (a horned figure), boss (a crowned figure), rest (a hall or hearth), treasure (a hoard or chest), merchant (a ship), event (scattered lots or rune slips), and a party marker (a small band of figures or a ship's prow) that sits on the current glyph.
- **Spoils glyphs:** about **7×7**, up to four or five tucked under a main glyph: a skull, a fish fin, a slime drop, a wisp, an antler, coins, a gem, and a fallen figure.

## 4. Show these states (all in one long tapestry)

The party is mid-dive, in band 2:
1. **Woven past** (band 1 and the start of band 2): each column shows only the glyph that was chosen, in full colour, with its thread pulled tight and coloured; the unchosen glyphs are gone or very faint; its **spoils glyphs** are stitched beneath (a fight shows the skulls of what was slain; a treasure shows coins; somewhere, one fallen figure).
2. **The current glyph,** with the party marker on it.
3. **Two columns ahead:** faint, **half-stitched outlines** of their glyphs (single colour, dotted or partial), threads drawn but not filled.
4. **Beyond sight:** **bare warp threads** only: plain vertical strings on the cream, nothing stitched.

## 5. Deliverables

1. **The whole tapestry** as one strip, about **16 columns, ~700×130 px** at 1×, plus a 4× copy.
2. **Three 320×180 screens** at 1× and 4×: the camera panned to the current spot (the past running off the left), with the text box placeholder. One shows a glyph hovered (outline it, and put a line of placeholder text in the box).
3. **The code,** parameterised so we can change sizes, column spacing, colours and the glyph set, and feed it a list of columns (glyph types, chosen index, spoils, sight).
4. **A short note** on what you took from the references and what you'd change.
