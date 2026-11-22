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
| **Disarmed** (Nov 22) | Feeble 1, Waning 1 | | Disarm (the Spettbein); 1 or 2 stacks. The old game keeps its own Disarmed |

- A bundle stacks 1 to 3 and builds and fades like a counter: one stack per untouched round.
- Effects with a size scale with the stacks (Venom 3: Poison 3 and Bleed 3; fading to 2, both are 2). On/off effects hold while any stack remains.
- Opposite bundles pull stack for stack: Feared 2 hit by Mot 1 is Feared 1; Feared 1 hit by Mot 1 is clean.
- A bundle's effects add to the same real effects already on a unit, capped at 3 (Venom 2 and a separate Poison 1: Poison 3).

## 4. Statuses that aren't counters

- **Reeling:** the unit acts **no earlier than the Late group** (Nov 21 fix: Swift and normal moves drop to Late; Heavy and Last moves stay where they are, so a Bid and Tung release still lands Heavy); stacks are duration. Inflicted by **Vingla** (to totter); also Besk's crash. Its opposite (a forced early group, "Alert") stays unnamed until a move needs it.
- **Axiom 1 (Nov 21): statuses never pull a move earlier.** A unit acts in the latest of its move's group and every limit its statuses impose (Reeling: no earlier than Late). A Reeling hero's Heavy move acts Heavy; a Last release stays Last. A future Alert is the mirror (no later than Swift), and as opposites the two pull against each other like any counter.
- **Axiom 2 (Nov 21): the order you see is the order you get.** A round's order is set when the round starts (the turn tracker); a status gained mid-round shapes the next round's order, as speed already does.
- **Feared** in the new game is pinned with your guard down (above). The old game's "move later" Feared is Reeling's job now.

## 5. Elements: the affinity ladder

| Step | Damage | Bonus Round |
|---|---|---|
| Ineffective | x0.25 | no |
| Resist | x0.5 | no |
| Neutral | x1 | no |
| Weak! | x1.5 | yes |
| Super! | x2 | yes |

- Each element is a counter on the unit, moving along the ladder from the creature's base. **The damage types (Slash, Pierce, Crush) ride the same ladder** (Nov 22, for the boss Beinbryn's Calcify: one step toward resist on Crush, on itself). **Ogn** pushes toward weak (one step; Mer two); **Mot** pushes back. Steps add up across casts within the ladder; casting at the cap only holds it.
- An untouched round slides it one step back toward the base. **Immune and Absorb never move**: they stay a creature's hard identity.
- The board shows where it sits now: "ELD WEK", "VTN RST".
- The play it allows (Joseph's): hero one's Ogneld takes a foe from Ineffective to Resist; enemies act; hero two's Merogneld takes it to Weak!; the Late Tungeld lands on Weak! for x1.5 and a Bonus Round.
- Forced weakness is strong: a boss and elite tool on the enemy side, short and visible.

**Wind-ups** need no new part: **Bid** winds up (round one is the wind-up; round two the hero is locked and it releases; x2.6; lost if broken), and **Tung** moves the release to Heavy (Bidtungeld). Bidskott, Bidkrosh and Bideld are legal now. A fused part for "Bid and Tung" would be a new word with no new meaning; an iconic move gets a byname instead.

## 6. The verbs

| Verb | Alone | With an element (Ogneld, Moteld...) |
|---|---|---|
| **Ogn** (ON *ógn*, terror: "fear makes you vulnerable") | Feared | one step toward weak on that element |
| **Mot** (*mót*, against) | Steadfast | one step toward resist |
| **Dokkn** (*dökkr*, dark) | Cursed | |
| **Eitr** | Poisoned | |
| **Vingla** | Reeling | |

- Variants are reward-card material from one grammar: **Mer** (two steps), **Flok** (a row), **Styng** (a hit of that element first, then the step), **Lonn** (the step plus the element's own rider: Eld gives Burn 1, Reyk gives Blinded; the rest when designed).
- Names: the game reads Ogn as OH-gun, so Ognjord is OH-gun-yord (the j is the Norse y, learned from Jord); OG-n is the source's own reading, kept in its origin note. Mot without an n (Motnjord's "tnj" is hard in English).

## 7. Under discussion (Nov 22): one number per status

Joseph's questions: should the range grow (to -5 to +5), what a stack means, and whether Slowed is a minor Reeling. Claude's draft of the simpler system hiding in today's rules (most of it is already true, just unstated):

1. **Every status is one number** (1 to the cap; opposites share one number, minus to plus).
2. **It counts down one at the start of every round, after doing its round-start job** (Poison ticks; the round's order reads Slowed and Reeling), so a status added this round is felt in full for the rest of it. Adding to it adds (to the cap). No "untouched round" bookkeeping; topping up has to out-pace the count, and costs the topper its turn.
   - Worked example: Nedkraft (Base, adds 2) in round 1: Feeble 2 for the rest of round 1; round 2 starts, Feeble 1; round 3 starts, gone. Cast again in round 2 instead: 1 + 2, Feeble 3. Cast every round and it climbs toward the cap; at the cap, any cast holds it. Halvnedkraft (adds 1) lasts only the rest of the round it lands: the Halv is the weak one.
3. **The tier says how much a move adds:** Halv 1, Base 2, Mer 3, Jatte 4, Ur 5. (This is the case for a cap of 5: one point per tier.)
4. **Each status says what one point does, and is one of two kinds:**
   - **scaling**, the effect times the number: Poisoned (damage a point), Fortified (DEF a point), Frozen (20% a point to lose the turn: Frozen 5 is certain, then 80, 60, 40, 20);
   - **flat**, on while the number lasts, which is then only how long: Keen, Marked, Pinned, Silenced, Slowed, Reeling.
5. **Opposites net on the one number:** Keen 2 meets Blinded 3, Blinded 1.
6. **Named exceptions, few:** fades by use (Song, Stunned), breaks when hit (Frozen), counts when you act (Bleeding).

**Joseph's turn (Nov 22): make every stat flat.** Each side of a stat has one fixed effect (Feeble: ATK down by one fixed share; Mighty: up by one); the number is only how many rounds are left. The tier adds rounds, not size (Halv 1, Base 2, Mer 3); a Drif flurry adds a round a hit (Drifnedkraft landing three hits: Feeble 3); opposites shorten each other on the one number (Aukraft against Feeble). It's the accuracy rule already built ("stacks are duration, not strength", classes.md 7d) spread to every stat, so there's one kind of status, not two. What it gives up: building a stat up for a bigger effect (Setup keeps other tools: Marked crits, Sundered, wind-ups, Weak! and the Bonus Round). The size has to be felt: 10% of a foe's hit (about 1% of a hero) isn't; today's single stage is (Mighty and Fortified x1.33, Feeble and Sundered x0.75). Frozen's 20%-a-point would be the one scaling exception, or Frozen stays flat too.

**Claude's read (Nov 22): one number can't carry both "how much" and "how long".** Coupled (the taper: Feeble 3, 2, 1) gives build-up but every round sheds a level; flat gives clean reading but no build-up. The way out is to let the two kinds of thing be two kinds of thing, as SMT V does with its -kaja and -nda spells:
- **Stats: a level and a timer.** The level runs -3 to +3 on today's curve (up x1.33, x1.67, x2; down x0.75, x0.6, x0.5: true mirrors that never reach zero); Base adds 1, Mer 2, Jatte 3 (no Halv on stats). **One timer per stat, three rounds, refreshed whenever anything moves that stat;** when it runs out, the level returns to 0 at once. Opposites subtract levels. Keen and Marked keep their built effect (on by sign); their level is only how hard they are to cancel. Build-up is back, and holding it is a turn every few rounds.
- **Ailments and bundles: flat, the number is rounds left** (Poisoned, Bleeding, Pinned, Silenced, Slowed, Reeling, Feared, Cursed...). Adding adds rounds, to the cap.
- **A few bespoke ones,** each one line: Frozen, Stunned, Song.
- The board shows a stat as its level with timer pips ("MIG 2 ..."), an ailment as its rounds.

Joseph's linear 20% steps reach x0.2 at Feeble 4: a foe made harmless. Today's curve slows as it goes, which is why it never bottoms out.

Slowed and Reeling under it: both flat. Slowed puts you at the back of your group; Reeling drops you into Late. One reduction for N rounds, not five sizes of reduction: within a group there's only front and back, so there's nothing to scale.

The cap: -3 to +3 is already seven values; -5 to +5 is eleven. Five gains the tier ladder one point each and finer steps (each DEF point near 15% instead of 25%, the same top); the cost is retuning every per-point number and statuses that last up to five rounds, most of a fight.

## 8. Open, for later

- **What Skolja washes off:** bundles, ailments, lowered stages, and also an Ogn push on the affinity ladder? If not, a forced weakness ends only by waiting or by Mot.
- **Bosses and statuses:** a Fornbein that can be Pinned, Feared and Silenced at once may fold. A boss resists one kind, or every status counts down faster on a boss.
- **Bundles with no opposite:** Cursed, Venom and Disarmed answer only to Skolja. Fine, or each wants an answer word, as Mot answers Ogn?

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

# Part 3: The Beinar Roster (v2, Nov 22: the focused session, with Joseph)

The Beinar are the Barrow's dead warband. They kept their old jobs, and a Beinar room should read like a squad with a plan: **each job asks the party one question**, and the room is hard when the questions stack. **Kits differ by rank on purpose:** a Regular and an Elite of one job carry different tools, so a mixed room covers more than either alone; Halv ranks are there to be annoying. Some jobs exist at one rank only, and that's fine.

Family rules stay: the pile (a non-Crush kill stands again in 2 rounds at 50%), weak to Crush and Sol, resist Slash, Pierce, Natt and Aska. Ranks are the yardstick's tiers: Halv is Trash (130 HP), base is Regular (450), Stor is Elite (950), Forn is the Boss (1700). Cost is actions a round (bestiary Part 1).

## The foes' register (agreed)

1. **Foe moves are plain English.** Each lists its twin in the heroes' grammar so the library and the audit can read it.
2. **A move that leaves a status is named for it, as a verb:** Curse leaves Cursed, Sunder leaves Sundered, Silence leaves Silenced, Disarm leaves Disarmed, Fortify leaves Fortified. Players learn the foes' language for free. Exception: **Called Shot** for Marked (a foe move called "Mark" would collide with the heroes' Mark, the spot part).
3. **Tiers show in the name.** Where English has a natural ladder, use it; otherwise **Hi-** for Mer and **Great** for Jatte. Never -er and -est (Graver reads as more serious; Bashest sinks it).

| Ladder | Halv | Base | Mer | Jatte |
|---|---|---|---|---|
| Crush (Krosh) | Bash | Smash | Break | Great Break |
| Pierce (Spett, the spear) | Poke | Thrust | Lunge | Great Lunge |
| Slash (Skar) | Cut | Hew | Carve | Great Carve |
| Pierce flurry (Drifspett) | Spear Flurry | Spear Gale | Spear Storm | |
| Bolts (the element's spell) | Fire Bolt | Hi-Fire Bolt | Great Fire Bolt | |
| A status | Curse | Hi-Curse (2 stacks) | Great Curse (3) | |

Not Crash (said aloud, one vowel from Krosh, the Vasara's hammer).

## The roster at a glance

| Job | Role | Its question to the party | Ranks |
|---|---|---|---|
| **Beinbryn** (sword and shield) | Front: the guard | Can you reach the casters? | Halv, Regular, Elite, Boss |
| **Beinorv** (bow) | Striker | Can you protect the Rear? | Halv, Regular, Elite |
| **Beinseidr** (staff and orb, five elements) | Pest | Can you clean up, and reach the Rear? | Halv, Regular, Elite, Boss |
| **Beinlur** (bone horn) *new* | The dead skald | What do you kill first? | Regular, Elite |
| **Spettbein** (spear) *new* | Duelist | Can you blunt a crit-fisher? | Halv, Regular, Elite |
| **Tork** (maul) *new* | Brute | Can you hold your formation? | Regular, Elite |
| **Skralla** (small rattling bones) *new* | Swarm | Do you have area damage? | Trash only |
| **Fornbein** (the red shield-king) | Commander | Can you break the order? | Boss |

## The jobs

### Beinbryn: the guard
*Trying to say:* "You'll have to go through me." Cover (a family rule) on every rank: it takes the hits meant for an ally under half HP.

| Rank | Kit |
|---|---|
| Halv | Taunt, Cut |
| Regular | Taunt, Hew, Thrust |
| Elite | Taunt, Carve, Fortify |
| Boss (Fornbeinbryn) | **Calcify**, Fortify, Carve, Poke |

- **Taunt:** one hero's single-target attacks this round must go to the Beinbryn, if they can reach it (Egga). The menu must say so: "Taunted: your attack goes to the Beinbryn."
- **Calcify** (new, boss only): "I am a skeleton trying not to get smashed to bits." One step toward resist on **Crush**, on itself, on the affinity ladder (Part 1, section 5), so the ladder must carry damage types as well as elements. (Its seed was Motkrosh; the foes get a word of their own.)
- **Fortify:** Fortified (Aukskold).

Brain, goal *keep the casters standing*:
1. A hero damaged a Beinseidr, a Beinlur or the boss last round: **Taunt** that hero ("the Beinbryn taunts the Ullar, who shot the Beinseidr").
2. Cover, by the family rule.
3. (Boss) it was struck by Crush last round and isn't calcified: Calcify.
4. In the Front, not Fortified, and didn't Fortify last turn: Fortify.
5. Its best strike on the boss's focus. 6. Fall back.

Counterplay: Crush (until it Calcifies); area moves ignore Taunt; Kasta shoves it out of the Front; Sundered and Marked.

### Beinorv: the striker
*Trying to say:* "Your Rear is mine." Reaches anywhere.

| Rank | Kit |
|---|---|
| Halv | Arrow, Called Shot |
| Regular | Arrow, Called Shot, Pinning Shot |
| Elite | Arrow, Pinning Shot, Killing Shot, **Arrow Rain** |

- **Called Shot:** Marked (Peka).
- **Pinning Shot:** a Styng-type: a bite of damage and **Pinned 2** (Genomskott).
- **Killing Shot:** x1.5 on the Pinned (Fangskott).
- **Arrow Rain:** a wind-up on a row (Flokbidskott): it lands next round, and is lost if the archer is Stunned, Frozen or netted.
- Arrow keeps its name across ranks; by the rule its tiers would read Hi-Arrow and Great Arrow (an arcing shot, which fits).

Brain, goal *kill the weakest*, with **claims** so archers work together: one claims the Mark, one the Pin. **The Pin is topped up, not stacked:** while a hero is Pinned 2, nobody re-Pins; at Pinned 1, the claimant (or, if it's busy, the next archer) tops it back to 2. Then: finish anyone in killing range; Killing Shot on the Pinned; Arrow Rain on the row holding the most hurt heroes.

Counterplay: Evasive on the weakest (Gyllenlykt), Lya, Skolja the Pin; Blinded archers whiff (Reyk); reach the Rear (Skott, spells, Svepa pulls it forward); stun the Arrow Rain.

### Beinseidr: the pest
*Trying to say:* "Everything gets worse while I live." **Keeps its five elements** (Natt, Aska, Eld, Hrim, Blixt; never Sol): the colour swap, its resistances and weaknesses, and its bolt. The bolt carries its element's own rider (Hrim chills, Blixt stuns, Aska curses).

| Element | Bolt | Its extra |
|---|---|---|
| Eld | Fire Bolt | **Corpse Candle** (Scorched: the folklore lights over graves) |
| Hrim | Frost Bolt | the chill rides the bolt |
| Blixt | Lightning Bolt | the stun rides the bolt |
| Natt | Shadow Bolt | |
| Aska | Grave Bolt | the curse rides the bolt |

| Rank | Kit |
|---|---|
| Halv | Bolt, Curse |
| Regular | Bolt, Silence, Curse |
| Elite | Hi-Bolt, Sunder, Hi-Curse |
| Boss (Fornbeinseidr) | Great Bolt, Hi-Sunder, Hi-Curse, Silence |

- **Curse:** Cursed, the bundle (Part 1): **each stack is Hexed 1 and Poisoned 1** (Dokkn in the heroes' grammar). Hi-Curse lands two stacks.
- **Silence:** Silenced, no MP moves (Bannskott). Martials pay HP, so the brain only Silences casters.
- **Sunder:** Sundered (Nedskold); Hi-Sunder, two.

Brain, goal *soften the line*:
1. The party's strongest caster isn't Silenced: **Silence** it.
2. The boss's focus isn't Cursed (or has fewer stacks than this Beinseidr can give): Curse it.
3. (Elite, Boss) the Front's toughest hero isn't Sundered: Sunder it.
4. (Eld) the focus isn't Scorched: Corpse Candle.
5. Its bolt on the most-hurt Cursed hero (Hexed: magic lands harder). 6. Fall back.

Counterplay: **Bannskott** (it pays MP: Silence it back), Skolja, Sol, and reaching the Rear.

### Beinlur: the dead skald (new)
*Trying to say:* "Get up. We're not done." The lur is the Dagskald's own Bronze Age horn: the Beinlur is what a Dagskald becomes in the Barrow. It strikes with a spare bone.

| Rank | Kit |
|---|---|
| Regular | Bash, Dirge, Sharpen Sight |
| Elite | Smash, Dirge, Rise!, Sharpen Sight |

- **Dirge:** a Song verse on an ally: heals at the start of each round (Kvad).
- **Rise!:** a bone pile on its side stands **now**, at up to **75%** (the pile rule alone: 2 rounds, 50%). Rooms without a Beinlur keep the plain rule.
- **Sharpen Sight:** Keen on an ally (its hits crit 1 in 3). Shared with the Spettbein; both check for Keen before casting (a claim), so they don't waste turns on the same ally.

Brain, goal *keep the warband standing*: 1. A pile lies on its side and it didn't Rise last turn: Rise the most useful (Beinseidr, then Beinorv, then Beinbryn). 2. An ally under 60% without a verse: Dirge. 3. The boss's focus is set and the side's best striker isn't Keen (and nobody claimed it): Sharpen Sight. 4. Bash or Smash. 5. Fall back.

Counterplay: the priority kill (low HP, Rear); Crush the piles before it raises them; Bannskott (its songs cost MP); Sol.

### Spettbein: the duelist (new)
*Trying to say:* "I find the gap." A spear: **Range Medium** (reaches the Rear while it stands in the Front). Pierce, and the Vasara is weak to Pierce: the anvil's bane.

| Rank | Kit |
|---|---|
| Halv | Poke, Sharpen Sight |
| Regular | Thrust, Spear Flurry, Sharpen Sight |
| Elite | Lunge, Spear Gale, Disarm, Sharpen Sight |

- **Spear Flurry / Gale / Storm:** Pierce hits that keep coming on a coin flip (Drifspett).
- **Disarm:** Disarmed, rebuilt as a bundle: **each stack is Feeble 1 and Waning 1** (ATK and MAT down: you dropped your weapon), 1 or 2 stacks, fading like a counter. Not a martial Silence: no attacks at all would be the strongest status in the game. (The old game keeps today's Disarmed.)

Brain: 1. Nobody on its side who'd use it is Keen: Sharpen Sight (itself first). 2. The hero who dealt the most damage last round isn't Disarmed: Disarm it. 3. Keen: its flurry on a hero weak to Pierce, else the focus. 4. Its thrust. 5. Fall back.

Counterplay: Blinded pulls Keen back to even (Reyk); Evasive; Fortified; Crush.

### Tork: the brute (new; the held name, "desiccated")
*Trying to say:* "Out of my way." A big dried-out skeleton with a grave-stone maul.

| Rank | Kit |
|---|---|
| Regular | Smash, Shoulder Charge |
| Elite | Break, Shoulder Charge |

- **Shoulder Charge:** pushes a Front hero back a row. **If the cell behind is taken, or the push would empty the Front, the hero bounces:** stays put, and both heroes are slammed (the shoves' crash rule: each takes a share of its own max HP and the other's). Played smart, the Tork hurts the Rear through the Front.

Brain: 1. A hurt Rear hero stands behind a Front hero: Shoulder Charge the Front hero (the bounce hits both). 2. Its maul on the boss's focus. 3. Fall back.

Counterplay: a Pinned hero is a wall (it can't be moved); Steadfast (planned); Lya; kill it first.

### Skralla: the swarm (new; the held name, "rattling")
*Trying to say:* "There are so many of us." Small rattling bones, Trash only, **up to six** to a room: a room that spends a sixth to a quarter of the party's HP on chaff, unless the party has area damage. **A Skralla dies for good** (too small to leave a pile; the room shouldn't drag). Kit: **Poke**. **No brain:** the shared scorer is enough; noise is its job.

### Fornbein: the commander
*Trying to say:* "On my word."

Kit: **Command**, **Cleaver**, **Carve** (Great Carve at boss tier, by the rule), **Rally**.
- **Command:** each round it names a focus (the weakest Front hero); the intent line says so ("the Fornbein points at the Vasara"), and its side values attacking that hero more. Kill it and the order breaks.
- **Cleaver:** a wind-up on a row, Slash (Flokbidskar). A row can't be dodged by stepping aside: the answers are bracing (Guard, Skoldborg, Lya) or breaking it (Stun, Freeze, the net): **Stelblixt finally has a boss to stop.**
- **Rally:** Mighty 2 on its side (Allmeraukraft).
- Desperate (50% and below in the Front): drop the routine, its strike every turn.

Brain: 1. Command. 2. Its side isn't Mighty and it didn't Rally in the last two rounds: Rally. 3. Two or more heroes stand in the focus's row: Cleaver on that row. 4. Carve the focus. 5. Fall back.

## Rooms (a first guess)

| Room | Who | What it asks |
|---|---|---|
| Trash | 4 to 6 Skralla, or 2 Skralla and 2 Halvbeinorv | area damage; protect the weakest |
| Regular | Beinbryn, Beinseidr, Beinorv | the triangle: shield, pest, striker |
| Elite | Storbeinbryn, Tork, Beinlur, Storbeinorv | hold formation; kill the horn first |
| Boss | Fornbein, Beinlur, Beinbryn, Beinseidr (and their piles) | break the order before the Cleaver lands |

## What foes still can't do after this roster

Knot (the Skurmar's identity: fine) and Bound beyond the Drattr's net (rare by design). Feeble now comes from Disarm.

## What the build needs

1. **The status rules** (Part 1): counter names (Waxing, Waning, Warded, Hexed), the bundles (Cursed: Hexed and Poisoned a stack; Disarmed: Feeble and Waning a stack), and **the affinity ladder over damage types too** (for Calcify).
2. **The brains** (Part 2), with claims and the fallback counts.
3. **Foe versions of hero mechanics:** Taunt aimed at the party's orders (the menu says so), Dirge (the song kind on foes), Shoulder Charge (a shove on heroes, with the bounce), Silence on heroes, the row wind-ups (Arrow Rain, Cleaver; to check: whether a foe Bid on a row resolves today).
4. **Rise!:** a new action, standing a pile now at up to 75%.
5. **The foes' register in data:** moves named by the ladders above, each with its heroes'-grammar twin recorded (so the library's Foes' moves chapter can show it).
6. **Art:** Joseph's four starters cover the Beinbryn, Beinseidr and two Beinorv; the Beinseidr's five element ramps exist. New bodies (Beinlur, Spettbein, Tork, Skralla) need sprites; stand-ins can be the sword-and-shield frames, tinted.
7. Then the Draugr the same way, and mixed rooms to playtest.

## Decided (Nov 22, Joseph)

The foes' register (above); Bash, Smash, Break; Poke, Thrust, Lunge; Calcify; Disarmed as Feeble and Waning a stack; the Beinseidr keeps five elements, bolts named plainly; Rise! (up to 75%; plain pile rules elsewhere); Pinning Shot as a Styng-type at Pinned 2, topped up by claim; Arrow Rain and Cleaver as row wind-ups; the names Beinlur, Tork, Skralla, Spettbein.

Also decided: the Slash ladder **Cut, Hew, Carve**; the pilot is **the built four plus the Beinlur**, then Tork, Spettbein and Skralla once the brains prove out.
