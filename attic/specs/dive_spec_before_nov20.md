# Dive Spec v1 (Nov 10, 2026)

The bare dive: the smallest real loop. Speak three runes at the Gate, walk three legs, go home with what you carry. Everything inside a fight already exists (the Fight Lab); this is the layer that strings fights together, and the screen that lets you choose your way. Builds on loop_spec Part 8 (the Gate and the dive) and combat_spec Part 16 (rooms and the map).

---

## Part 1: Why a Tapestry (Locked)

- **Fate is woven.** The Norns weave every life at the roots of Yggdrasil; in *Darraðarljóð* the valkyries weave a battle on a loom before it happens. The Rune Gate doesn't send you somewhere: **your three runes set the loom, and the dive is woven as you walk it.**
- **The map is the record.** What you chose and what it cost are stitched in as you go, so at the end the tapestry *is* the story of your dive, shown again on the home screen.
- **Three looks, three jobs:**
  - **The Gate is a picture stone:** carved, scratched grey rock. You carve your three runes into it.
  - **The dive is a tapestry:** cream linen, decorated borders, glyphs stitched along a bare middle strip. Reference: the Överhogdal tapestries, the Bayeux Tapestry, the Oseberg fragments.
  - **Events cast lots:** marked slips scattered on a white cloth, three come up, you choose one (Tacitus, *Germania* 10). This is where a "dealt hand" lives; not the map.

## Part 2: The Shape of a Dive (Locked shape; numbers tune)

- **Three legs,** one per rune; each leg is one woven band in its rune's colours.
- **A leg:** an entry fight, then **three columns of 2 to 4 glyphs** joined by threads, then the **elite**.
- **The boss** comes after the elite. *Open: after every leg's elite, or only the third leg's.*
- **Between legs:** push on, or go home with the loot.
- **Choosing:** hover a glyph and the text box below says what it is; click it. Its thread pulls tight and fills with colour, the other glyphs in that column fade, then a slow zoom to black, and the heroes run in from the left.
- **What carries between rooms:** HP, MP, pouches, Wounded, Dying, Dead. Winning a fight stabilises the Dying at 1 HP, Wounded (combat_spec Part 10).

## Part 3: Sight (Locked)

- **You see two columns ahead.** Past that the tapestry is **bare warp threads**: the future isn't hidden, it isn't woven yet.
- **The two columns ahead** show faint, half-stitched glyph outlines; as you step forward the weave fills in.
- **Played through a leg:** at the entry fight you see columns 1 and 2; at column 1 you see 2 and 3 (now you can steer to a rest before the elite); at column 2 you see column 3 and the elite.
- **The elite and the boss are always known types;** sight only hides the choice rooms.
- **A later hook:** a rune or relic that extends sight by a column (Sol is "sight").

## Part 4: Spoils Woven In (Locked)

When a room is done, the unchosen glyphs in its column fade, and the room's spoils fill the space:

| Room | Spoils glyphs |
|---|---|
| Fight, elite, boss | One per enemy slain, by family (a Beinar skull, a Drattr fin, a Mogel drop, an Ande wisp, a Djur antler, a Draugr...) |
| Treasure | Coins, a gem |
| Any | A fallen figure for a hero who fell |

## Part 5: Rooms in the First Cut (Locked list; contents tune)

| Room | What happens |
|---|---|
| **Fight** | Fodder: Halv and base ranks, from the leg's place (composer habitat) |
| **Elite** | Base and Stor |
| **Boss** | A Drott (3-cost: the Drattr queen, the Forndjur, a Fornbein, ...) backed by Halv or base. Stand-ins first; Joseph draws boss pieces later. If a stand-in feels flat, a Lab-only boss buff (more HP, an extra action) |
| **Rest** | One of: **Rest** (recover HP and MP, raise the Down), **Organize** (pouches from the Haul), **Carve Runes** (+5% to one stat for the dive) |
| **Treasure** | Marks and a find (a draught, a Firecracker, sometimes a Surgeon's Kit), into the Haul |
| **Merchant** | Spend marks on draughts and throwables |
| **Event** | Lots: two or three small ones to start (a shrine that heals or pays, a stranger's deal, a trapped chest) |

**Left out of the first cut:** the Hunt clock (later: woven riders gaining along the bottom border), Midnight and wages, the toll, XP, the city (a placeholder home screen).

**Difficulty:** set by feel once the loop runs. The families are tuned for 25-55% single-fight wins; a ten-fight dive will want about 90% per regular fight and 70% per elite (loop_spec Part 13). Tune pack budgets and levels per room tier.

## Part 6: The Screen (Proposed; pixels tune)

- **320×180,** like the fight. The text box keeps the bottom (as in fights) and describes the hovered glyph.
- **The tapestry** takes the top ~130 px: about 16 px of decorated border at the top and bottom, and a bare **middle strip ~90 px** tall.
- **Colours** (Resurrect 64): a cream linen field; borders and edges in blues (323353, 484a77, 4d65b4), wine reds and purples (7a3045, 753c54, 831c5d, 6b3e75, 45293f). Each leg's band takes its rune's accent.
- **Glyphs:** main glyphs **13×13 or larger** (Joseph draws them); spoils **~7×7**, four or five under a main glyph; up to four main glyphs per column.
- **Columns** about 44 px apart. Your woven past runs off the left; the sight line sits two columns ahead; bare threads fill the right.
- **A whole dive** is about 16 columns, ~700 px wide: the screen pans. The home screen scrolls slowly across the finished tapestry, left to right, like reading it.
- **The party's marker** sits on the current glyph.

## Part 7: The Icons (Locked, Nov 11: Joseph's icon_test_1 and drakkar_icon_1)

Full-colour icons for the choices on the open map; once a room is woven, its record is drawn in tapestry colours (Joseph's iconographic art, so the finished dive is a tapestry of your own weaving; aspirational).

| Use | Icon |
|---|---|
| The party | The longship, white sails. **Idles on the calm drakkar loop** (frames 1, 2, 4, 5, 6, 8, 9 at 200 ms); the lurch frames (3, 7) are cut from the loop, and **play once when the ship sets out** for the chosen room |
| Fight / elite / boss | **The skull ladder:** a skull; a skull and crossed swords; a helmeted skull. The **helmeted skull with an axe** is the dive's final boss (if bosses close every leg) |
| A fallen hero | **The plain cairn** (a 7×7 version among the spoils); the skull cairn could close a wiped party's tapestry |
| Treasure | The chest (open state when looted; the opening wants a bigger lid swing) |
| Merchant | The trader's scales |
| Event | The green mask (mischief); the **blue mask is held** for a second kind of event (a trainer, something special) |
| Rest | The camp, **without its sky** (the moon stays, outlined) |
| Held | The "?" (for intents the party can't read, in fights); the crossed swords; the Snaptun stone (background art, maybe) |

- **Outlines:** a 1 px ink outline (2e222f) **only where white or pale parts meet the linen** (sails, skulls, blades, the moon). Coloured parts keep their own edge.
- **The weave:** sparse weft dashes: one dashed row in four (2 over, 6 under), offset each time. A hint of cloth, not a pattern.

## Part 8: Art List (Joseph; stand-ins from existing icons until then)

- **Room glyphs (13×13+):** fight, elite, boss, rest, treasure, merchant, event; the party marker.
- **Spoils glyphs (~7×7):** one per family, coins, gem, the fallen figure.
- **The tapestry:** field, weave texture, borders, knotwork, threads (code-drawn; see dive_tapestry_brief.md).
- **The Gate's picture stone** (later).

## Open Questions

- The boss after every leg, or only the third?
- How many glyphs per column, and how the threads branch (each glyph joins one or two in the next column?).
- Event list and their lots.
- Merchant stock and prices (loop_spec Part 9 anchors).
