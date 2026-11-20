# Fight Lab Spec v3

The build-to for the first playable thing: a browser page where you roll a party, stock pouches, roll an enemy pack, and fight it. It is a dev tool and the first slice of the real fight screen. It sits beside **combat_spec.md** (the rules) and **sim/events.md** (what a fight reports).

**Status key.** **Locked** means agreed (Nov 8). **Proposed** means a default to build against until play says otherwise.

---

## Part 1: The Engine, Step by Step (Built, Nov 8)

Today `Battle.fight()` plays a whole fight on its own. The page needs it one decision at a time. The rules don't change; the round loop is split into steps the page can call.

```
b = Battle(party, enemies, rng, events=True)
b.begin()                  -> events (start, round 1)
loop:
    b.phase                -> "declare" | "bonus" | "over"
    b.awaiting()           -> the heroes who need an order now (ids)
    b.options(uid)         -> every move that hero can use now, each with its legal targets
    b.submit(uid, key, target)    (any number of times, until committed; last one wins)
    b.commit()             -> events for everything that resolved, up to the next round's orders
    b.inspect(uid)         -> a unit's card (Part 3); free, changes nothing
    b.preview_order()      -> the turn-order bar; never rolls the fight's dice
```

- **`begin()`** emits `start` and the first `round`, then plans the enemies: their intents are in the events before you choose anything.
- **`awaiting()`** lists the heroes who choose this step. It leaves out the Dying and the Dead, a hero locked by a Bid wind-up (their slot reads the move's name and an ellipsis), and a hero the engine moves for them (Advance).
- **`options(uid)`** is what the menu draws from: each move with its cost, whether it's affordable, its speed group, and its legal targets (by id) on the board as it stands. Illegal targets are left out, so the board can grey them.
- **`submit()`** records an order; **`commit()`** checks every awaited hero has one, resolves the round (or the Bonus Round), and stops at the start of the next round (or at a Bonus Round your heroes earned, or the end). If nobody is awaited (all locked, Frozen or Dying), the page just commits again, so playback goes round by round.
- **Keys and the regression check** are in sim/events.md. Rebuilding `fight()` on these steps changed nothing: 320 fixed-seed fights play out event for event as before. (It also turned up a real bug: Bonus Round entrants came out of a set, so their order depended on memory addresses. Fixed in both versions before comparing.)
- **Flee** now rolls its chance (Part 12 of combat_spec); a Smoke Pot always works. Events `flee_failed`, `retarget` and `fizzle` are new.
- **Reach is checked again when a move resolves.** If the target has moved out of reach, the engine picks another legal one (same row first) and **reports it** with a `retarget` event: "Vasara can't reach the Mogel; she strikes the Bein instead." Today it switches silently; that's fine for the AI and reads as a bug to a player.
- **Bonus Rounds need their own decision.** If a hero earns one, `commit()` stops with `phase == "bonus"` and `awaiting()` lists only the entrants. Enemy entrants declare automatically.
- **`fight()` stays** for the sim, as a loop over the same steps with the AI choosing for the party. One code path, so the sim and the page can't drift apart.
- **The page never runs rules.** It reads `options()`, `inspect()` and events, and sends `submit()` and `commit()`.

---

## Part 2: The Command Menu (Locked)

**Layout (Locked, Nov 8):** the text box keeps its size (three rows at Joseph's font). Moves on the left as a 2×3 block (the Halv move first, then the slotted moves, each with its cost); utilities on the right as a 2×3 block. Fight lives in the utilities' sixth slot, greyed until every hero has an order.

```
 Halvskar        Blotskar   8  │  Pouch   Flee 55%
 Skar        8   Cover         │  Guard   Inspect
 Merskar    16                 │  Move    Fight
```

**Clicking a move turns the left half into its card** (Locked): "< name · reach tag · cost" on the first row, the plain line under it (two rows; ▼ scrolls the rare longer one), and the board lights the legal targets. Click a target to give the order, "<" or Esc or right-click to go back, or click any utility to change your mind. A move with nothing to aim (self, all) shows its card and a second click uses it. The utilities stay live throughout. The Pouch also opens in the left half.

| Command | What it does |
|---|---|
| **The Halv move, by name** | Free, always on top. Click, then a target. |
| **The four slotted moves** | Each shows its cost; ones you can't afford are greyed. Click, then a target. |
| **Pouch ▸** | Opens the hero's items just right of the word, with counts. Click one, then a target. **Back** (the arrow, Esc or right-click) closes it. |
| **Guard** | Defend. One click; no target. |
| **Move** | Click a spot on your side. If an ally stands there, the row reads "Swap with Vasara". |
| **Flee** | Shows the chance of getting away. One click; success ends the fight for everyone, failure wastes the hero's turn. |
| **Inspect** | Click any unit to read its card (Part 3). Free: it doesn't use the hero's order, and you're back at the same hero's menu after. |

**Loadout.** A hero has **four move slots**, filled from a pool: the class kit plus a move from each piece of equipped gear. Unequipping gear empties its move's slot; nothing fills it for you, so checking moves before a dive is part of the ritual. In the full game you change slots at the Inn; in the lab, on the party card.

**Giving orders.**
- **Heroes choose in any order.** After you give one an order, the next hero without one comes up, so the quick path is three clicks in a row. Click any portrait to jump to that hero or change their order.
- **Under each portrait, the order by name:** "Skarkross → Mogel", "Guard", "Life Draught → Vasara", "Move → Rear 2".
- **Fight** stays greyed until everyone awaited has an order. It reads **Fight (Flee)** when someone is fleeing. Enter presses it.
- **Nothing resolves until Fight.** Moves and swaps happen on the mover's turn (the +1 group), in the order the turn-order bar shows. A hero who moves spends the round moving.
- **Targets light up:** legal ones highlight, illegal ones grey; a row or All move lights the whole row or side.
- **Hover a move** to read its card: its word, its plain reading, power, cost, speed group, reach.
- ~~Repeat~~ (dropped Nov 9: Fight with missing orders fills them, Part 5). **Number keys** pick commands; **Tab** steps between heroes (built).

---

## Part 3: What You Know (Proposed)

combat_spec Part 2 already rules that **affinities are hidden until discovered**, per enemy kind, and remembered in the Company's bestiary. The fight screen shows it like this:

- **On the board, always:** each enemy's name, an HP bar (no number), its intent and the hover "why", status icons.
- **The enemy HP bar (Locked):** Res64 green, turning yellow and then red as it shrinks *(proposed: yellow at half, red at a quarter)*; the emptied part shows a dark red-purple backing; a 1px black border.
- **When a hit lands,** the floater says what it found: **Weak!**, **Resist**, **Null**, **Absorb**. That result goes into the bestiary for that kind and element. A plain hit records "normal" quietly.
- **Inspect (Locked)** is free and shows **what the Company remembers**: name and rank, status and stat stages, its intent with the why, and whatever the bestiary knows. Unknown facts show as **?**. Your own heroes show their full card.
- **Remembering is earned by fighting** *(proposed thresholds, all knobs)*:

| Fact | Learned by |
|---|---|
| An affinity | Hitting the kind with that element or damage type once |
| HP (current / max as numbers) | Felling 20 of the kind |
| MP | Felling 40 of the kind |

- **Facts are kept at the level they vary:** affinities per family, rank and element (an Eld Mogel and a Vatn Mogel differ); HP and MP per family and rank (element doesn't change them), so kills count across elements.
- **Inspecting a kind for the first time** adds it to the bestiary, with whatever is known.
- **Kennit** (later): a skill or item that costs a turn and fills in every **?** for that kind. ("Do you ken it?")

**In the lab:** a dev toggle, **Know everything**, fills every card. The lab's bestiary is kept in the browser, with a Reset.

---

## Part 4: Reading the Board (Locked)

- **Each enemy's intent** sits over its head: an icon and a short phrase ("Engulf → Vasara"). **Hovering it** shows the why, in prose ("The Mogel lunges at Vasara: she's nearly down").
- **The turn-order tracker (Locked, Nov 8):** Joseph's 128×16 frame (3 px border, a 122×10 window). **10×10 face chips:** an 8×8 head crop of the unit's sprite (hand-drawn 8×8 icons later), the frame in side colour (blue party, red enemy), **gold on whoever acts next**, and **A/B in the corner** for twins (3×5 on an ink backing). Nine fit, so most rounds don't scroll. **Before Fight** you drag it or use the arrow keys; **on Fight** it snaps to the start and each chip slides off the left as its unit finishes. **Hover a chip:** a small plate with the name (more on request), and the unit lights up on the board; hovering a unit lights its chip. The order is exact: each unit's tie coin is flipped when the round is planned.
- **Tiny UI font (Locked):** 3×5, capitals and digits (PICO-8-like), with a 1 px shadow. Joseph's main font stays for the text box and menu.
- **Under each hero:** HP and MP; **breath pips** on the Dying; status icons; the order they've been given.
- **Skipped heroes say why:** a Bid-locked hero's slot reads the move's name and "…"; a Dying hero shows their breath pips.
- **The text box** narrates as events play.

---

## Part 5: Playback (Locked; built Nov 9)

- **Every creature is static (Nov 9):** one sprite per creature, plus a second for a state where one exists (a Bein's bone pile, a downed hero, a crawling Draugr). Life comes from code motions, not frames, so 32rogues-based sprites drop in with no new code. Joseph's existing animated frames are no longer played; frame 0 is the sprite.
- **The motion kit** (screen.js `MOTION`, one table, ms at normal speed, whole pixels): lunge (martial attackers step at the target and back), hop (casts, items, wind-ups, getting up), flash (white silhouette on a hit), shake (damped), squash (whole rows only: bracing, landing in a pile), idle bob (1 px, out of step per unit), look (a rare, short glance the other way), dissolve (death: an ordered-dither fade), step (Move/Swap hops cell to cell), hit-stop, the tracker slide, and the beats between events.
- Events play one at a time: the actor moves, the hit effect plays (Joseph's hit_slash / hit_crush2 / hit_pierce2 for martial; the element sheet's burst for magic; its sparkle for heals, buffs and hexes), contact freezes the clock (**hit-stop**: 70 ms, 150 on a weakness or crit), the target flashes and shakes, the number rises with a WEAK/CRIT/RESIST tag after it, the line goes in the text box. A sweep's later hits come quicker.
- **Speed:** normal, fast (about 3x), instant. **Space** skips the rest of the round.
- Effects atlas: fight_lab/assets/fx.png + fx.json, built by art_work/tools/build_fx.py (martial cadences from hits_martial.py CADENCE).

**Fight with orders missing (Nov 9):** Fight is always live. If any hero has no order: *"Two heroes do not have orders. They will Halv-strike foes at random."* with OK / Back (Enter = OK, Esc = Back). On OK every unordered hero Halv-strikes: in party slot order, each picks a random living foe it can reach that nobody has picked yet; when none is left the chain starts over (bone piles only when no living foe is in reach). No hidden information is used. The picks go through submit (lab.autofill), so the record replays them. The filled orders blink on their blue badges for half a second, then the round plays. A hero with no usable Halv-strike Guards instead, and the message names them. Replaces the proposed Repeat.

---

## Part 6: The Screen (Locked)

The battle mock's screen: two 3×2 boards on the dungeon floor, walls behind, the text box with its studs and rune plaque at the bottom, our font. A small fixed resolution, scaled up by whole numbers. The menu's line count is measured against the text box at our font before it's locked.

**The text box fill (Locked, Nov 8):** Joseph's watercolour at full display resolution, not quantized: the grey painting, tinted along the area's stone ramp as a smooth gradient, one random crop (flipped either way) per fight. Frame, studs and text stay on the pixel grid above it. Boxes that open now and then (Inspect, menus later) take a fresh crop each time. The five coloured versions are on hand for areas that want a painted colour.

**The frames (Locked, Nov 8): Joseph's cord** (art_res64/ui/cord_frame.aseprite), a twisted cord with gripping beasts, cut into pieces the page stretches (period 4 on every side). **The battle text box:** rearing beasts on the top corners, the cord knotting round the bottom ones (no room below), a strand of cord as the divider between moves and utilities. **Floating boxes** (Inspect now, menus and dialogue later): beasts above, the spare heads diving from the bottom corners, a fresh watercolour crop inside each time. Kept at this scale on purpose: a 3 px cord and 10 px heads match 32 px heroes. (Open: a 1 px ink outline either side of the cord if it ever gets lost over a busy background.)

**The board, roomier (Nov 8):** cells 44 px wide (one floor slab) instead of 34, one slab between the armies, the floor lifted 14 px into the wall so the lanes are 24/26/31 px deep. Heads no longer reach into the lane behind.

**Intents at the feet (Nov 8; frame and icons updated Nov 9):** now Joseph's **13×13** frame (art_res64/ui/intent_frame_13.aseprite) with the 9×9 icon at (2,2). Nov 9 picks: melee Pierce = the stab icon (spear retired), club dropped, Guard = rune shield, Cover = banded shield, Move/Swap = boot with speed lines, Flee = boot with dust cloud, wind-ups (Bid-) = the three aura frames looping at 160 ms (the spiral is the still version, for plates), "?" = an intent you can't read, chest and potion both kept (potion restores, chest is anything else). Was: Joseph's 12×12 frame (art_res64/ui/intent_frame_12.aseprite) beside each unit's feet, on the side facing the foe, holding Joseph's 9×9 icon (intent_icons_9.aseprite): rust frame when the move is aimed at a hero, stone when it isn't, blue for a hero's own order. Shape always means the same kind of action; only magic's sparkle takes the element's colour. Icons: sword/sweep (Slash), hammer/club swing (Crush), spear (Pierce up close), arrow/volley (Pierce at range), wand (magic, 12 tints), green cross (heal), heater shield (Guard), round shield (Cover), green up arrow (buff), red down arrow (hex), potion/chest (items). Open: 8 (pick?), 10/11 (smash), 14/15/16, 18 (?), and moves/wind-ups (still small glyphs).

**Where things sit (built):** party names, HP and MP top left in 3×5; the tracker top centre; the round top right; a hover plate across the wall under the tracker (who, what they intend, why); Inspect as a sheet over the room; heroes' orders in 3×5 above their heads; enemies' intents as 7×7 glyphs above theirs (red when aimed at a hero).

**Art (Locked):** the wizard for every class, in school colours; Ande and Mogel in every element; the Draugr ladder; the Beinar on their idle frames, shaking when hit and dropping when they fall; intent and status icons as glyphs in our font until drawn.

---

## Part 7: The Lab Panel (Locked)

A dev panel players never see, beside the fight:

- **Party:** three slots; pick a class and level for each, or roll them. Cards show stats, the move pool and the four slots.
- **Pouches:** stock each hero from the full item list, free.
- **Enemies:** roll a pack (habitat, budget, ranged rule, level) or pick units by hand.
- **Fight**, or **Auto** (the AI plays your side, and you watch).
- **Dev:** the seed, playback speed, rule toggles, Know everything, the bestiary Reset, the raw event log.
- **Later:** gear, the runes, and departing into a dungeon, once the assembler exists.

---

## Part 8: How It Ships (Built, Nov 8)

- **One published page** (an artifact), shareable by link. The engine runs in the page through Pyodide 0.26.4, shipped beside the page: published pages may only fetch their own files. The host doesn't serve archives, so Python's standard library ships as `stdlib.json` (only the ~300 modules the rules and Pyodide use) and the page packs it into the zip Pyodide boots from. The sim's Python files and the art ship beside the page too.
- The page is plain JavaScript and a canvas. Python does the rules; JavaScript draws and takes clicks.
- The lab remembers your last party, pouches and bestiary in the browser.

---

## Later

- **Elemental weapons** (gear that changes or adds an element). Gear isn't in the lab yet.
- **Kennit.**
