# Enemy Brains and the Status Rules (Nov 21: the Beinar pilot, agreed with Joseph)

Two parts. **Part 1** is the status rules for the whole new game: what every move in Part 2, and every hero move, is written in. **Part 2** is how foes think: brains written as data, piloted on the Beinar. Old fights keep the old rules.

---

# Part 1: The Status Rules

## 1. Primitives and bundles

- **A primitive** has one rule: Poisoned ticks, Pinned roots you, a counter moves a stat. Joseph's "felt effects".
- **A bundle** is a named status that holds a list of primitives per stack. One timer, one tag on the board, one cleanse. Joseph's "parent effects". Clearing a bundle clears everything it did, so it holds its effects rather than spawning separate statuses.
- **A move can apply a bundle** (Dokkn, Ogn, Mot) **or primitives directly** as riders (a knife that Bleeds on every hit). Both are legitimate.
- Keep bundles few and memorable: each is a new word to learn, and each needs a one-line hover.

## 2. Counters: the seven stats

| Stat | Up | Down |
|---|---|---|
| ATK | Mighty | Feeble |
| DEF | Fortified | Sundered |
| MAT | Waxing | Waning |
| MDF | Warded | Hexed |
| ACC | Keen | Blinded |
| EVA | Evasive (was Nimble) | Marked |
| SPD | Quick | Slowed |

- Each runs -3 to +3; the name shows its side and size (Keen 3 is ACC +3).
- Opposites pull on the same number: Keen 3 hit by Blind 1 is Keen 2; Blind 3 on Keen 3 is 0, and neither shows.
- An untouched round moves it one step back toward 0.
- ACC and EVA decide the roll (classes.md 7d, built): ahead, a crit 1 in 3 and no graze; behind, a whiff 1 in 3 that lands nothing.

## 3. Bundles

| Bundle | Per stack | On/off while any stack remains | Applied by |
|---|---|---|---|
| **Feared** | DEF -1 | Pinned (can't move or be moved) | Ogn |
| **Steadfast** | DEF +1 | Can't be Pinned or shoved | Mot |
| **Cursed** | Hexed 1, Poisoned 1 | | Dokkn (was Nid) |
| **Venom** | Poisoned 1, Bleeding 1 | | a weapon trait, or a move |

- A bundle stacks 1 to 3 and builds and fades like a counter: one stack per untouched round.
- Effects with a size scale with the stacks (Venom 3: Poison 3 and Bleed 3; fading to 2, both are 2). On/off effects hold while any stack remains.
- Opposite bundles pull stack for stack: Feared 2 hit by Mot 1 is Feared 1; Feared 1 hit by Mot 1 is clean.
- A bundle's effects add to the same real effects already on a unit, capped at 3 (Venom 2 and a separate Poison 1: Poison 3).

## 4. Statuses that aren't counters

- **Reeling:** the unit acts in the Late group, whatever its speed; stacks are duration. Inflicted by **Vingla** (to totter); also Besk's crash. Its opposite (a forced early group, "Alert") stays unnamed until a move needs it.
- **Feared** in the new game is pinned with your guard down (above). The old game's "move later" Feared is Reeling's job now.

## 5. Elements: the affinity ladder

| Step | Damage | Bonus Round |
|---|---|---|
| Ineffective | x0.25 | no |
| Resist | x0.5 | no |
| Neutral | x1 | no |
| Weak! | x1.5 | yes |
| Super! | x2 | yes |

- Each element is a counter on the unit, moving along the ladder from the creature's base. **Ogn** pushes toward weak (one step; Mer two); **Mot** pushes back. Steps add up across casts within the ladder; casting at the cap only holds it.
- An untouched round slides it one step back toward the base. **Immune and Absorb never move**: they stay a creature's hard identity.
- The board shows where it sits now: "ELD WEK", "VTN RST".
- The play it allows (Joseph's): hero one's Ogneld takes a foe from Ineffective to Resist; enemies act; hero two's Merogneld takes it to Weak!; the Late Tungeld lands on Weak! for x1.5 and a Bonus Round.
- Forced weakness is strong: a boss and elite tool on the enemy side, short and visible.

## 6. The verbs

| Verb | Alone | With an element (Ogneld, Moteld...) |
|---|---|---|
| **Ogn** (ON *ógn*, terror: "fear makes you vulnerable") | Feared | one step toward weak on that element |
| **Mot** (*mót*, against) | Steadfast | one step toward resist |
| **Dokkn** (*dökkr*, dark) | Cursed | |
| **Eitr** | Poisoned | |
| **Vingla** | Reeling | |

- Variants are reward-card material from one grammar: **Mer** (two steps), **Flok** (a row), **Styng** (a hit of that element first, then the step), **Lonn** (the step plus the element's own rider: Eld gives Burn 1, Reyk gives Blinded; the rest when designed).
- Names: Ognjord is OG-nyord (the j is the Norse y, learned from Jord). Mot without an n (Motnjord's "tnj" is hard in English).

---

# Part 2: Brains

## 1. The idea

Today every foe runs one shared scorer that values each move and picks the best. A **brain** sits on top: a short list of rules written as data. It picks when one of its rules fits; when none does, it **falls back** to the scorer, so a brain never freezes and the sweep keeps working. **Every fallback is counted** (per family, per rule) in the gauntlet report: a brain that keeps falling back is missing a move or a rule.

Brains are readable on purpose. The page already shows each foe's intent with a reason; a brain's reason says what it's doing ("Marking the weakest: Skurmar", "guarding the hexers until your line breaks", "desperate"). Predictable foes with visible plans are what make a tactics game fair: the player learns the archers hunt the weakest, so Evasive goes on the weakest, or the Vasara steps in front.

## 2. The vocabulary

**A goal** is a job, a target, and an UNTIL that ends it (then the next goal). Goals are what change across a fight (phases: soften, then punish) and what a boss hands out.

**Under each goal, rules in order**, the first that fits is taken: *condition, target, action.*

- **Conditions:** has a status; missing a status; a status about to run out; stacks at least N; HP below a share; in the Front or Rear; a hero within killing range of a move; **used last turn; used N turns in a row**; someone's claim; the boss's order. Combine with AND, OR, NOT.
- **Targets:** the weakest (the lowest current HP among heroes it can reach; coin flip on ties; the Dying ignored, since finishing blows have their own rule); the Marked; the Pinned; the boss's focus; a named ally (the hexer it guards); self.
- **Actions:** a move; Move to the Rear; Guard; Cover an ally.
- **Claims:** a unit can claim a job ("Mark the weakest"); the next sees it and takes another ("Bleed the Marked"), so a team spreads its work.
- **Planning order:** a unit whose rules read another's plan plans after it (the Draugr after the hexers they guard); otherwise the faster plans first, so the setup is claimed by whoever acts first and lands before the payoff.

**Modes** sit above the goals:
- **Normal:** run the goals.
- **Retreat:** in the Front at 70% HP or below with a healer on its side: Move to the Rear, if that's legal (the Front can't be emptied, a Pinned unit can't move, the Rear needs a free cell); otherwise stay in Normal. In the Rear, Guard and wait for the heal. **Just healed last turn: back to the routine** (no guard-looping); if nothing in it is legal, Move.
- **Desperate:** in the Front at 50% or below: drop the routine, take the strongest attack each turn on the boss's focus or the weakest; no setups. The tell that the player is winning.
- The Beinar have no healer (a future repairer, an Ande that mends the dead, would bring Retreat into play), so they live in Normal and Desperate.

## 3. The Beinar pilot

The Barrow is where Joseph plays, and the Beinar ranks already wear hats. Kits marked *new* are moves the pilot adds.

### The Beinorv (archer): Striker

Kit (Stor: the full rotation; lower ranks a subset): Arrow; Barbed Arrow (Bleeding: exists); *a Mark* (Marked: the dead Ullar's Peka); *a Pin* (Pinned); *a Pin payoff* (more damage on the Pinned).

Goal: kill the weakest. Rules, in order:
1. A hero is within killing range of Arrow: finish them.
2. The weakest isn't Marked and no ally has claimed it: claim and Mark the weakest. (The fastest archer plans first, so it takes the Mark.)
3. The weakest is Marked (or an ally claimed the Mark) and its Bleeding is under 3: Barbed Arrow the weakest.
4. The weakest is Marked and Bleeding 3 (or an ally claimed the Bleed): Pin the weakest.
5. The weakest is Marked, Bleeding and Pinned: the Pin payoff on the weakest (several archers may all cash in).
6. Otherwise: fall back.

### The Beinbryn (shield): Guard

Kit: Old Sword, Shield Bash, Aukskold (exists).

Goal: keep the casters standing. Rules:
1. A Beinseidr or the boss is the boss's focus target or below 50%: Cover it.
2. Its own DEF isn't up and a hero's attack is coming its way: Aukskold.
3. Otherwise: Shield Bash the boss's focus.

### The Beinseidr (bone-mage): Pest

Kit: its element's spell; Dokkn (Cursed: was Nid); Allaukstav at Stor (exists).

Goal: soften the line. Rules:
1. The boss's focus isn't Cursed: Dokkn it.
2. Every Front hero is Cursed, or it cast Dokkn its last two turns: its element's spell on the most-hurt Cursed hero (Hexed: magic lands harder).
3. Otherwise: fall back.

### The Fornbein: Boss

Kit: Old Sword, Shield Bash, Allaukskold, Ogn (exists; in the new game Ogn is Feared: pinned, guard down); *a signature wind-up* (a Bid strike, 30-40% of a mid hero: proposal "Grave Cleave").

Goal: break the line. Rules:
1. **Command:** each round, name a focus (the weakest Front hero); the intent line shows it ("the Fornbein points at the Vasara"); its side values attacking that hero more. Kill the boss and the order breaks.
2. The focus isn't Feared: Ogn the focus (it can't step back, and its guard drops).
3. The focus is Feared: wind up Grave Cleave on it.
4. Allaukskold only when no ally's DEF is up (the fix for the six-buff Fornbein Joseph fought).
5. Otherwise: Old Sword the focus.

## 4. The second example: the hexer troupe

A magic boss in the Rear, two medium Draugr in front, two Askande hexers flanking the boss.

| Unit | Goal 1 | Goal 2 |
|---|---|---|
| Draugr (x2) | Guard: Cover the hexer that's casting Nedskold, UNTIL a hexer has cast its Mark | Attack the weakest, or a weakness it can hit |
| Askande hexers | Nedskold the weakest Front hero; UNTIL every Front hero has Sundered 2+, or it cast Nedskold its last two turns: then Mark (Nedvig) a Front hero not yet Marked (the hexers spread their Marks) | Marked is on the Front, or it Marked last turn: attack until no Front hero is Sundered; then start over |
| The boss | Nedvig the Front twice (Marked) | Flokaska on the softened row; the finisher: Ognaska on one hero (weak to Aska), then everyone piles in |

Names: Nedskold is DEF down, Nedvig EVA down, Aukvig EVA up (*vig*, agile). An enemy-only super-move is fine (Urnedskold: Ur-tier, Marked and Sundered 2): enemies don't need to fit the hero pool.

## 5. Measuring it

- **Joseph's damage picture**, per room, from full HP (the gauntlet's fresh-room mode):

| Room | After the fight |
|---|---|
| Trash | nobody hurt worse than ~90% |
| Regulars | least hurt ~90%, most hurt ~60% |
| Elite | the tank near 25%, the others 60-90% |
| Boss | a second hero near 25%, or someone falls |

- The gauntlet runs (Fodder, Regulars, Elite, Boss, nothing restored), and the fallback counts per brain.
- Joseph's play in the Barrow.

## 6. Open, for the build

- Names for the new Beinar moves (the Mark, the Pin, the Pin payoff, the wind-up), English like their other moves, or Norse like the heroes'.
- The wind-up's exact size and tell.
- A Spettbein (stiletto Beinar: Aukhitt for Keen, Drifspett, Halvspett) as a second Striker.
- Build order (refactor_plan Wave 7): Phase B (the Halv as a pick, Merknyta Late, Evasive), then this pilot (status rules first, then brains), then Phase C (the Circle).
