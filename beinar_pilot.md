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

## 7. Settled (Nov 22, Joseph): stats and ailments are different things

> **Superseded in part (Nov 24):** see `Battle_Refactor_Current.md` (D1: accuracy; D2: stats persist for the fight and combine into five counters, so the staircase and the split names go; D3: held stats; D4: bundles are shorthand, so Feared is Late and Sundered 1, Steadfast a held DEF).


This replaces the counter and bundle timing in sections 2 and 3 (their names, tug-of-war and bundle lists stand). The new game only; old fights keep the old rules.

**One rule for time:** at the end of each round (after any Bonus Round), **every stat, ailment and bundle that nobody moved this round drops by one.** "Moved" is any change: adding, an opposite pulling it back, topping it up. A status is never counted down in the round it lands.

**Stats: a level.**
- Each stat runs **-3 to +3** on the curve **x0.5, x0.6, x0.75, x1, x1.33, x1.67, x2** (true mirrors: one step up and one down land back on x1; it never reaches zero).
- **Base moves a stat 1 level, Mer 2, Jatte 3.** A Halv carries no stat move of its own; a Halv with a rider adds 1, like Base (a Halv's weakness is its damage, not its rider).
- Opposites pull on the same level (Mighty 2 hit by Feeble 1: Mighty 1). The staircase: left alone, it steps back one a round. Build-up is team play: a buffer keeping the Vasara at Mighty 2 holds it for one cast a round; a self-buff pays off about once. Mighty 3 and Feeble 3 (double, half) are earned, not free.
- Keen and Marked keep their built effect (on by sign, classes.md 7d); their level is how hard they are to cancel.
- Worked (Joseph's): R1 the buffer's Aukraft on the Vasara, she hits x1.33. R2 again: Mighty 2, x1.67, no step down. R3 the buffer turns to the Huskarl: she hits x1.67, then steps to Mighty 1. R4 x1.33, then 0.

- **A printed size wins, otherwise the tier decides** (Nov 22): a move's own stat moves by its tier; a rider's printed size lands as printed (Gyllenlykt: Evasive 3, whatever its tier). A bigger version (a Mergyllenlykt) is where the cap would stretch to 5.
- **Built (step 1, Nov 22):** the curve, the staircase and the tier sizes were already the engine's; the printed-size rule is new (new game only). `test_status_rules.py` pins Joseph's worked example.

**Ailments: flat, the number is rounds.**
- Poisoned, Bleeding, Pinned, Silenced, Slowed, Reeling...: the same flat effect whatever the number; **the number is how many full rounds after this one it lasts.** Deepening an ailment extends its life, never its strength.
- Worked (Joseph's): Poison 1 in R1: it ticks at the start of R2, and R2's end takes it to 0. Another Poison in R2 makes it 2, with no drop that round; then it ticks, drops, ticks, drops, and is cured.
- Poisoned ticks at the start of each round; Bleeding bites when its bearer acts; Slowed and Reeling are read when the round's order is set.
- Base adds 1 round, Mer 2, Jatte 3; a Drif flurry adds one a hit.

- **Built (step 2, Nov 22):** Poisoned, Bleeding, Pinned and Silenced are rounds in the new game (`data.STACKED_AILMENTS`): each landing adds, to 3; a round nobody added to it, it drops one, never the round it lands. A status move rolls as a hit does (a whiff 1 in 3 when behind; a graze shrugs it off); a clean hit lands it for certain, a weakness adds a stack to the main status only; with Styng the status rides the Styng hit's roll; damage riders land on every clean hit. Helvad keeps its gamble. Old fights identical; `test_status_rules.py`. The gauntlet barely moved (within the noise of 60 runs), since today's foes rarely lean on ailments: the trim waits for the Beinar, who will. Still to do: the move cards still say "may" (they change with the card pass).

- **Built (step 3, Nov 22):** Late is one rule in the new game (`data.LATE_STATUSES`): Reeling (new), Chilled and Feared drop a unit's moves to Late; Heavy and Last stay; protection moves (Guard, Cover, Taunt) are spared, as Fear always spared them; two sources are still just Late. Reeling and Chilled are rounds like the other ailments. Pinned and Chilled no longer touch SPD. A second chill freezes and **Frozen replaces Chilled** (no freeze-lock after the thaw). **Bosses** (by tier, the new game) shrug off Bound, Stunned, Frozen and Death; on a boss a second chill just holds the Chilled. Old fights identical.

**Bundles** (Feared, Steadfast, Cursed, Venom, Disarmed) step down like a stat. **Their stat parts are as big as their number** (Cursed 2 is Hexed 2); **their ailment parts are on while they last** (Cursed 2 is also Poisoned while it holds).

- **Built (step 4, Nov 22):** `data.BUNDLES` in the new game: Feared (DEF -1 a stack, and Late), Steadfast (DEF +1 a stack; never made Late, never shoved; a wall for bumps; it can still be Chilled and frozen: the cold isn't the stagger), Cursed (MDF -1 a stack, Hexed, and Poisoned), Venom (Poisoned and Bleeding), Disarmed (ATK and MAT -1 a stack, Feeble and Waning). Each counts like an ailment (adds, holds the round it's added to, drops one a round left alone); stat parts are as big as the number; ailment parts are on while it lasts, and two sources of one ailment keep a single one on (one Poison tick, not two). Feared and Steadfast pull stack for stack. MAT and MDF counters are named in the new game (Waxing, Waning, Warded, Hexed). The old game keeps its Cursed (two rolled stats) and its names. Old fights identical; the gauntlet within noise.

- **Built (step 5, Nov 22):** no automatic element riders in the new game; a foe's child-element attack becomes its Styng form (`data.CHILD_TWIST`: Reyk Blinded, Hrim Chilled, Gro Poisoned, Aska Cursed; a hit at 0.7 of the spell and the twist, certain on a clean hit; named by the grammar, Allhrim becomes Allstynghrim). Today's generated kits use the Styng form for every child attack; hand-made kits (the enemy pass) choose plain twist or Styng form move by move. Blixt's stun is Stelblixt's. Disarmed goes to 3 like the rest (Joseph: the cap of 2 dated from when Disarm was bespoke). Old fights identical.
- **The gauntlet after steps 2 to 5 (60 runs a party and leg, against this morning):** Regulars won 5 to 11 points less, Elites 2 to 9. The cause is plain in the counts (30 runs of the Dagskald trio at legs 1 and 3, statuses landing on heroes): Frozen 9 to 197, turns lost 20 to 174, Chilled 23 to 273, Poisoned 30 to 269, Bleeding 45 to 128. Certain twists on every clean hit (and All-forms chilling the whole party) make two chills, and so a freeze, nearly free. The trim is the freeze.
- **The freeze, trimmed (Nov 22, Joseph): the third chill freezes** (`data.CHAIN_AT`: a chill freezes only a target already Chilled 2; Chilled 1, Chilled 2, then Frozen, which begins its taper). Rerun: Frozen on heroes 197 to 136, turns lost 174 to 120 (this morning: 9 and 20); win rates mostly back. What's left is the All-form chill waves: with an All-form's twist switched off, Frozen falls to 49; with area chills allowed to chill but not to freeze, Frozen is 86 and the win rates match this morning's.
- **A wave chills, an ice punch freezes (Nov 22, Joseph):** a row or All chill only stacks Chilled; only a single-target chill tips Chilled 2 into Frozen. Built; Frozen on heroes 84 and turns lost 84 in the same 60 runs, win rates as this morning. A dedicated full-power ice attack (an "Ice Lance" for bosses, with a hero twin to be coined) is welcome inside the Hrim family.
- **The fire ladder, for the Brennumar's kit pass (Nov 22, Joseph; recorded, not built):**
  - **Sveda** is damage-free and lands **Singed** 1 (an ailment: rounds, to 3). **Singed** ticks a weak fire burn at each round's start, about **half an Eld**, from the singer's power and the target's Eld affinity (not a share of HP). Flat: Singed 2 ticks like Singed 1.
  - **A single-target Sveda, or a single-target Blast (the Skurmar's wind), on Singed 2 makes it Scorched**, which replaces the Singed. **Scorched** burns **2.0 Elds, then 1.0, then 0.6** (the taper), in Eld damage with weaknesses counted, **from the singer's stats** (the Brennumar's fire; the wind only fans it). No Singed lands while Scorched; Blast never extends Scorched, so the burn always ends.
  - **Shapes follow the frost rule:** Mer Sveda lands Singed 2 at once (the next single Sveda converts); Floksveda and Allsveda singe a row or the field but never convert: a wave singes, a focused flame scorches. **Styngsveda** hits and singes.
  - **Lamsveda** (Lonnsveda): Singed and Feeble 1, "the burn lames the arm" (the game's one hero source of Feeble stays).
  - **Svedeld is cut:** Eld is a pure parent, with no rider. **Balsveda** (Old Norse *bál*, a pyre: straight to Scorched) is pocketed; at 3.6 Elds for one cast it would need the Mer rung or more.
  - **The numbers:** three Svedas on one target pay about 4.6 Elds (0.5 and 0.5 from Singed, then 3.6) against 3 for three Elds, the bulk while the Brennumar is free; with the Skurmar converting, a round sooner. Singed counts down like any ailment, so the build has to be steady (a cast missed and it burns out), and holding Singed without converting pays slowly, never for free. The Eld Beinseidr's Corpse Candle lands Singed too: the Barrow teaches the ladder from both sides.

**One cap: 3** (stats -3 to +3, bundles 1 to 3, ailments up to 3 rounds). The escape hatch, if a fight needs breathing room: -5 to +5.

**Bespoke, one line each:** Frozen (loses turns; any damaging hit breaks it and shatters), Stunned (clears the first time it costs an action), Song (heals at each round's start until it runs out).

**Slowed and Reeling:** both flat. Slowed: the back of your group. Reeling: into the Late group. One reduction for N rounds.

**Considered and set aside:** one number carrying both size and time (the taper: Feeble 3, 2, 1), every stat flat (no build-up), a level with a refreshing timer (SMT V's way: two numbers on a tag), linear 20% steps (x0.2 at Feeble 4 makes a foe harmless).

## 7b. The watertightness pass (Nov 22, Joseph): settled

- **Ailments land in stacks, one round a stack; most moves give 1.** A move lists its stacks (Death Bite: Poison 1); each landing adds them (Drif hits, one each); the cap is 3; Mer and Jatte (2 and 3) exist but are rare. The per-tick size is the tuning knob (Poison: a share of max HP at each round's start). The card reads **"Death Bite | 0 HP | ~80 | Poison 1"** (name, cost, clean damage, effect); hovering Poison says what one round does and that the number is rounds left. Two Draugr biting one hero hold it at Poison 3: fair, and answered by Skolja or by killing one.
- **No foe spams a move:** a brain rule ("not the same move twice in a row") for moves like Death Bite, rather than a new cooldown mechanic. An HP cost stays an option.
- **"Refuse" reapply goes:** today Poisoned, Bleeding, Silenced, Stunned, Feared, Cursed and Disarmed bounce off a second landing; in the new game adding adds.
- **Bespoke:** Scorched (the fading burn the wind stokes), Frozen, Stunned, Song.
- **Late is one primitive, worn by several:** Reeling is Late alone; **Chilled** is Late and a second chill freezes; **Feared** is Late and DEF down a level a stack (it no longer pins). **Pinned is rooted only** (its hidden SPD -1 goes), so it stays the archers' setup for Fangskott. Late from two sources is still just Late.
- **Slowed and Quick are the SPD stat** (a level on the staircase): earlier or later within your group. Not ailments.
- **Frenzy** (the Stordrattr's, was a second Allaukraft): Mighty 1 and Sundered 1 on its side. One name, one meaning.
- **Aska loses its automatic Curse rider** (and, below, every element loses its automatic rider). Aska (Natt's child: ash and decay) curses through its own moves; Natt and Aska are also the home for Ogn moves and for drains (the Seidar's vampiric sustain).
- **Steadfast** (Feared's opposite, confirmed): DEF up a level a stack, and can't be made Late or shoved.
- **Printed effects land for certain on a clean hit** (Nov 22, Joseph). Whiffs and grazes already drop riders, so the accuracy roll is the only gamble; the card says what lands ("Poison 1"), never a hidden chance. Today's status-line chances (Bannskott's ~30%, Blotskott's) go in the new game; status moves get weaker hosts (less damage or a dearer cost) to pay for it. The old game keeps its chances.
- **Parents hit, children twist** (Nov 22, Joseph). The damage schools: **Eld, Vatn, Jord, Sol, Natt, Blast.** Their children lean on statuses and tricks, with no damage of their own until Styng adds the hit: **Reyk** (blinds), **Hrim** (chills; a second chill freezes; Mer adds Chilled 2, never an instant freeze), **Gro** (poisons: thorns and rot), **Aska** (curses; the home of Ogn and drains). **Blixt** stays the damage spike (Stel's stun its designated extra); **Lak** is the healing school. **The automatic element riders go** (Reyk blinds, Hrim chills, Blixt stuns, Gro poisons, Aska curses on any spell, by chance): a twist is the move itself, printed on its card. The foes speak the same rule, so the Ande and Mogel spell kits are rebuilt for the new game.
- **Skolja washes ailments** (Nov 22, Joseph): every harmful ailment to 0, Bleeding and Pinned included, the harmful bespoke ones too (Scorched, Frozen, Stunned, Bound), and harmful bundles whole (Cursed, Venom, Disarmed, Feared: a bundle clears as one). **Not stats.** Lowered stats have their own answers: the staircase fades them, and every Auk move pulls its opposite back. **In a pinch, Lonnskolja does both:** its designated rider also lifts every lowered stat to 0 (one step dearer). Nothing washes the affinity ladder: an Ogn push slides back on its own, or Mot pushes it back.
- **Built (step 6, Nov 22):** in the new game Skolja washes every status but the helpful ones (`data.HELPFUL_STATUSES`: Song, Steadfast) and leaves stats; **Lonnskolja** (Skolja's designated rider, 12 MP) also lifts every lowered stat to 0, raised ones untouched. The AI weighs a wash by what it would actually clear. Old fights identical. **The status rules' six steps are built.**
- **Bundles with no opposite stay that way** for now (Cursed, Venom, Disarmed): strong, and fit for seasoned heroes and tough bosses; Skolja is their answer.
- **Bosses are immune to what takes a turn away:** Bound, Stunned, Frozen (already), and Death.
- **The one-sided pairs** (Keen; Waning, Hexed, Warded for heroes; Slowed for heroes; Quick in no kit) are lexicon and kit work, spread to the heroes who'd want them as the roster fills.
- **Supports:** twelve classes want three or four supports as main roles to field different teams; the roles chart has three (Dagskald, Nalarbani, Lundar) and two more as second roles (Seidar, Hafrunar).

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

## 7. Team plans (Nov 23, agreed with Joseph; not built)

**Why:** the Nov 23 calibration fights. 54 of 58 foe attacks went at the Vasara and the Dagskald ended every fight at 100%: the packs were all Front melee, and the only glue between brains was "the boss's focus." A **plan** is the layer above the units' own rules: the pack's shared focus and stance.

**The priority target** (Joseph's rule; every plan that hunts uses it): 1. anyone reachable at 60% HP or below, the lowest first; 2. otherwise anyone with a heal; 3. otherwise the lowest HP. Coin flip on ties; the Dying are skipped (finishing blows have their own rule).

**Who picks:** at the start of round 1 the pack's **head** (the boss; otherwise its most expensive unit) picks a plan from the legal ones, weighted by family. The plan goes on the intent line. Each unit's rules read **the plan's focus** and **its stance** (hold or press) where Part 3 says "the boss's focus."

| Plan | The pack | The Front | Legal when the pack has | Until |
|---|---|---|---|---|
| **Hunt** | presses the priority target | **holds**: Cover, Fortify; strikes only what's in front | reach | the target falls: re-pick; the target is above 60% after 3 rounds (the party is protecting it): re-plan |
| **Break** | everyone on the Front hero | presses: Sunder, Frighten, then the heavies | anything (the fallback) | that hero falls: Hunt |
| **Inflict** | keeps its debuffers covered and stacks debuffs | holds | two or more debuff moves | the focus carries 2+ debuffs, or 3 rounds: Hunt or Break |
| **Stabilize** | 1-2 rounds of reset: Fortify, Calcify, Rally, a heal, a raise, a boss's once-a-fight ultimate (Joseph's Hrim boss whose move skips Chilled straight to Frozen) | holds | a heal, raise or cleanse, or two or more defensive buffs | back to the plan before |
| **Desperate** | the family's last stand (below) | | a trigger: the pack has lost half its cost, or the head fell | the end |

- **Stabilize triggers** when the head or a key caster is under 40% while the heroes are healthier than the pack.
- **Desperate by family:** the Bein **break** (setups stop; each unit's strongest strike on the most-hurt hero). The Draugr **dig in** (Part 4: the grudge).
- **Re-planning** is checked at round end, at most one switch every 2 rounds (no flip-flopping), and **every switch is announced** ("The Beinbryn lock shields." "The dead turn on the singer."). That line is the player's tell and the "they realised halfway in" moment.
- **Variety** comes from family weights (the Bein lean toward Inflict and Hunt, the Draugr toward Break), from what the room's makeup makes legal, and from a small weighted roll; not from noise. A family that always opens the same way is fine: players learn it and play around it. Every family opening the same way is not.
- **Guard against over-correcting:** Hunt can't win every pick (the healer would fall every fight instead of never). Its weight is tuned against Joseph's damage picture (section 5).

## 8. The mirror: composition (Nov 23, agreed; not built)

Most hero squads carry Rear reach, so most packs do too. A pack of N units **reserves one reach slot for every three units, rounded up** (1 for 2-3 units, 2 for 4-6), filled first and seated by role. **Reach** is a damage move that hits our Rear from where the unit stands (the catalog's `ranged` tag: a spell, a bow, a throw, the Spettbein's spear from the Front).

- **Regular, Elite and Boss rooms:** always, except a named **brute room** about 1 in 8, so it never becomes a law the player can count on.
- **Trash rooms:** half the time (a Halvbeinorv); the Skralla swarm is a deliberate exception.
- **Within the budget:** a reach unit takes a melee unit's place; the room's cost doesn't change.
- **The adds dial** (calibration: +0/+1/+2 units on top) stays separate. Added units fill reach slots first. Its default is picked **after the brains**, from Joseph's fights and the gauntlet: brains and adds both make rooms harder, and tuning both at once is guessing.
- **Built (Nov 23):** `composer.mirror` (one reach slot per three units, rounded up; a brute room 1 in 8, a room of Trash only 1 in 2), swapping the cheapest unit that can't reach our Rear for one that can, of the same cost and tier: the room keeps its price and shape. On in the Lab's calibration rooms (calibration room numbers reshuffled; old records still replay, each keeps its pack), the Lab's freeform rolls (the new default of its Ranged menu), the sweep and the gauntlet; off for the old checks (fingerprints, regress and the move golden identical). `sim/test_mirror.py`.
- **What it did, alone (150 rooms a kind, the Dagskald, Skurmar and Vasara at leg 2, the AI on both sides):** almost nothing to where the damage goes. Elite rooms left the Vasara at 43% / 40% (plain / mirrored), the Skurmar 69% / 71%, the Dagskald 89% / 90%; Boss rooms 36% / 33%, 60% / 61%, 77% / 79%. The gauntlet got a little harder (Regulars cleared 200 / 191 of 240; runs reaching the end of the Boss 17 / 14). **The packs can now reach the Rear but the shared scorer still prefers the Vasara: the brains (section 7) are what move the fire.** The mirror is the precondition, not the fix.
- **Reach by family today** (catalog entries that reach / total): Ande 60/60, Mogel 60/60, Bein 18/22, Drattr 4/10, Draugr 1/5, Djur 0/4. **Ande and Mogel are the glue families:** near-unrestricted reach, so they pair with the Drattr, the Draugr and the Djur. The Draugr stay thin on purpose (Part 4). The Djur want a spitter (Joseph: elemental Wyrms that spit their element). The Drattr want a reed blowgun (Joseph: a bow that works underwater).

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

*Revised Nov 23 (Joseph): no Taunt on foes, and Cover takes one hit.* "This guy wants to get his DEF up, attack with Slash, and Cover when needed."

| Rank | Kit |
|---|---|
| Halv | Cover, Cut |
| Regular | Cover, Hew, Fortify |
| Elite | Cover, Carve, Fortify, **Calcify** |
| Boss (Fornbeinbryn) | **Bulwark**, Calcify, Great Carve, Fortify |

- **Cover** (Lya): a move, not a passive. Name an ally; the **first** single-target move aimed at it this round is taken by the Beinbryn, and then the stance ends. One interception, so two Beinbryn can't lock the board. **This is the shared rule, heroes and foes** (Lya, below).
- **Bulwark** (Lonnlya): Fortified 1 and Cover in one move.
- **Calcify** (Elite and Boss; on the Seidr only at Boss): "I am a skeleton trying not to get smashed to bits." One step toward resist on **Crush**, on itself, on the affinity ladder (Part 1, section 5), so the ladder must carry damage types as well as elements (not built; the Elite and Boss can ship without it and gain it after). Big, so few carry it.
- **Fortify:** Fortified (Aukskold).
- Taunt (Egga) stays the heroes'. A foe Taunt would also have needed the party's orders and the menu rebuilt around it.

Brain, goal *keep the casters standing*:
1. The plan holds, and a Beinseidr or the head is the party's likely target (it was struck last round, or it's under 50%): **Cover** it (Bulwark if it has it and isn't Fortified).
2. (Elite, Boss) it was struck by Crush last round and isn't calcified: Calcify.
3. In the Front, not Fortified, and didn't Fortify last turn: Fortify.
4. Its best strike on the plan's focus. 5. Fall back.

Counterplay: Crush (until it Calcifies); spend one hit on the Beinbryn to break the Cover, then strike the caster; area moves aren't caught; Kasta shoves it out of the Front; Sundered and Marked.

**The intercession ladder (Nov 23, Joseph; not built).** Lya is **intercession** (I protect someone you might fire at); Egga is **Taunt** (I draw your fire). Both are the heroes'; **foes get intercession only**, nothing Taunt-adjacent that steers the party's attacks.

| Hero word | Foe name | Interceptions this round | Also |
|---|---|---|---|
| Lya (8 HP) | Cover | 1 | |
| Merlya (16 HP) | Hi-Cover | 2 | |
| Jatte (foe bosses) | Great Cover | 3 | |
| Lonnlya | Bulwark | 1 | Fortified 1 on the coverer first |
| Merlonnlya | Hi-Bulwark | 2 | Fortified 1 |

The number is interceptions; the stance ends when they're spent or the round ends. **One coverer per ally:** a newer Lya replaces the older. A whole move is one interception (a flurry, a Styng hit, the net). Rows, columns and All aren't caught. Lya keeps its 8 HP price (Joseph: it's used strategically). Lonnlya needs Lya's designated rider in the data (Fortified 1); Merlya already compiles.

**The shared Cover rule (Nov 23, Joseph; not built):** in the new game, **Lya** takes one interception and ends; the old game keeps today's round-long Lya, byte-identical. **Lonnlya** (Fortified 1, then Cover; classes.md already planned it) is the "Merdamma" Joseph reached for: Lonn is the grammar's slot for a verb's own rider, and Mer would mean a bigger number, which Cover doesn't have. A one-hit Lya is worth less than today's, so its 8 HP price is re-checked when it's built. (Joseph floated **Damma**, "to dam", for the move; Lya already holds it. Damma stays free for a row-wide block, a Flok cover, if one is ever wanted.)

### Beinorv: the striker
*Trying to say:* "Your Rear is mine." Reaches anywhere.

*Revised Nov 23 (Joseph):* the archer hits the Rear naturally; its brain tells it where to aim.

| Rank | Kit |
|---|---|
| Halv | Arrow, Called Shot |
| Regular | Arrow, Pinning Shot, Killing Shot, its **quiver arrow** |
| Elite | Rapid Arrows, Pinning Shot, Killing Shot, Volley, Sharpen Sight |
| Held back | Arrow Rain |

- **The quiver:** each Beinorv rolls **Barbed Arrow** (Bleeding) **or Poison Arrow** (Poisoned) when it's placed, as a Beinseidr rolls its element. One ailment per archer keeps kits lean; two archers with different quivers are the dovetail.
- **Rapid Arrows** (Drif): the heroes' flurry rule with foe numbers. Two hits always land, each coin flip won adds one more, up to five, each worth a third of an Arrow: about **0.96 of an Arrow** on average (hero Drif: 0.94), five hits 1 time in 8. Each hit rolls its own whiff, as Drif does today. (Five separate rolls at a third each was weighed: it averages 1.5 Arrows, and fixing that shrinks every hit to chip damage.)
- **Volley** (the row) at Elite and Boss only. **Arrow Rain** (the row wind-up) is held back.
- **Sharpen Sight** (Keen) moves here from the deferred Beinlur.
- **Called Shot:** Marked (Peka). The Halv archer's job: fodder that sets up the others.
- **Pinning Shot:** a Styng-type: a bite of damage and **Pinned 2** (Genomskott).
- **Killing Shot:** x1.5 on the Pinned (Fangskott).
- **Arrow Rain:** a wind-up on a row (Flokbidskott): it lands next round, and is lost if the archer is Stunned, Frozen or netted.
- Arrow keeps its name across ranks; by the rule its tiers would read Hi-Arrow and Great Arrow (an arcing shot, which fits).

Brain, goal *the plan's focus* (under Hunt, the priority target: the hurt, then the healers, then the weakest), with **claims** so archers work together. Its quiver arrow goes on a focus that doesn't already carry that ailment. one claims the Mark, one the Pin. **The Pin is topped up, not stacked:** while a hero is Pinned 2, nobody re-Pins; at Pinned 1, the claimant (or, if it's busy, the next archer) tops it back to 2. Then: finish anyone in killing range; Killing Shot on the Pinned; Arrow Rain on the row holding the most hurt heroes.

Counterplay: Evasive on the weakest (Gyllenlykt), Lya, Skolja the Pin; Blinded archers whiff (Reyk); reach the Rear (Skott, spells, Svepa pulls it forward); stun the Arrow Rain.

### Beinseidr: the pest
*Trying to say:* "Everything gets worse while I live." **Keeps its five elements** (Natt, Aska, Eld, Hrim, Blixt; never Sol): the colour swap, its resistances and weaknesses, and its bolt. The bolt carries its element's own rider (Hrim chills, Blixt stuns); the Grave Bolt is plain Aska damage (Nov 23).

| Element | Bolt | Its extra |
|---|---|---|
| Eld | Fire Bolt | (carries Singed once the fire ladder lands) |
| Hrim | Frost Bolt | the chill rides the bolt |
| Blixt | Lightning Bolt | the stun rides the bolt |
| Natt | Shadow Bolt | |
| Aska | Grave Bolt | none: a full-size bolt of Aska damage, no curse (a hand-made move, not a Styng form) |

| Rank | Kit |
|---|---|
| Halv | Bolt, Curse |
| Regular | Bolt, Silence, Curse |
| Elite | Hi-Bolt, Sunder, Hi-Curse |
| Boss (Fornbeinseidr) | Great Bolt, Hi-Sunder, Hi-Curse, Silence, Calcify |

*Revised Nov 23 (Joseph):* **Corpse Candle is cut**: the bolt by element is enough, and the Fire Bolt takes Singed when the Brennumar fire ladder is built. The bolt's size follows the rank (a Halv bolt for the Halv Seidr, Base for the Regular, Mer for the Elite: about one hero Eld's worth at Regular). The Frost Bolt takes its Styng form by the rule (0.7 and the certain chill). **The Grave Bolt doesn't** (Joseph, Nov 23): the Curse and Aska were broken apart for a reason, so it's a plain bolt of Aska damage at a bolt's full size; the Aska Seidr curses with its Curse. Generated foes' Aska attacks keep their Styng forms (Styngaska on the Askande is correct). **No heals on the Seidr:** when foe healing comes, it comes as **one job** (the Beinlur, or a lich-like Seidr variant), not spread across every Seidr, which would make the pest the only kill in every room.

- **Curse:** Cursed, the bundle (Part 1): **each stack is Hexed 1 and Poisoned 1** (Dokkn in the heroes' grammar). Hi-Curse lands two stacks.
- **Silence:** Silenced, no MP moves (Bannskott). Martials pay HP, so the brain only Silences casters.
- **Sunder:** Sundered (Nedskold); Hi-Sunder, two.

Brain, goal *soften the line*:
1. The party's strongest caster isn't Silenced: **Silence** it.
2. The boss's focus isn't Cursed (or has fewer stacks than this Beinseidr can give): Curse it.
3. (Elite, Boss) the Front's toughest hero isn't Sundered: Sunder it.
4. (Eld) the focus isn't Scorched: Corpse Candle (Singed; a single-target candle on Singed 2 scorches).
5. Its bolt on the most-hurt Cursed hero (Hexed: magic lands harder). 6. Fall back.

Counterplay: **Bannskott** (it pays MP: Silence it back), Skolja, Sol, and reaching the Rear.

### Beinlur: the dead skald (new; **held back**, Nov 23)
*Held back (Joseph):* healing is the strongest thing a foe can do, so the Beinlur waits until the pilot's brains have been tested. Its Sharpen Sight went to the Elite Beinorv. **Revised (Nov 23, Joseph):** it's the foes' Dagskald, a necromancer that keeps the Bein topped up and defended; it uses the Beinseidr's staff-and-orb body until Joseph draws its own. **The Draugr are excluded from Rise!** (they have the crawl).

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

Brain: 1. **Command:** as the head, it picks the plan (Part 2, section 7) and says its focus out loud. 2. Its side isn't Mighty and it didn't Rally in the last two rounds: Rally. 3. Two or more heroes stand in the focus's row: Cleaver on that row. 4. Carve the focus. 5. Fall back.

## Rooms (a first guess)

| Room | Who | What it asks |
|---|---|---|
| Trash | 4 to 6 Skralla, or 2 Skralla and 2 Halvbeinorv | area damage; protect the weakest |
| Regular | Beinbryn, Beinseidr, Beinorv | the triangle: shield, pest, striker |
| Elite (pilot) | Storbeinbryn, Storbeinseidr, two Beinorv (two quivers) | break the Cover; reach the Rear |
| Boss (pilot) | Fornbein, Beinbryn, Beinseidr, Beinorv (and their piles) | break the order before the Cleaver lands |
| Elite (later) | Storbeinbryn, Tork, Beinlur, Storbeinorv | hold formation; kill the horn first |

## What foes still can't do after this roster

Knot (the Skurmar's identity: fine) and Bound beyond the Drattr's net (rare by design). Feeble now comes from Disarm.

## What the build needs

*Revised Nov 23 for the pilot (the built four: Beinbryn, Beinorv, Beinseidr, Fornbein).*

**Status (Nov 23, late):** step 3 (the mirror) is built; the rest waits on the `battle_system_adr.md` review. **Nov 24:** the review is recorded in `Battle_Refactor_Current.md`; Waves A-C there come first, then this list resumes. Resume at the intercession ladder (step 4's Cover), then the kits, then the brains (refactor_plan.md, "Where we paused"). **Nov 24:** Cover built (Battle_Refactor_Current.md D10); next, the kits ("Decided (Nov 24)" below).

1. **The status rules** (Part 1): **built** (Nov 22). Still to come: the affinity ladder over damage types (for Calcify; the Elite and Boss can ship without it).
2. **The brains** (Part 2, sections 1-3): the units' rules, with claims and the fallback counts; **the team plans** (section 7), with the priority target, legality, re-planning and the announced switch.
3. **The mirror** (section 8) in the composer and the calibration rooms.
4. **Foe versions of hero mechanics:** Cover by the shared one-hit rule (Lya in the new game; Bulwark as Lonnlya), Silence on heroes, the quivers, Rapid Arrows (Drif with foe numbers), the row moves (Volley; Cleaver as a wind-up; to check whether a foe Bid on a row resolves today). Later, with their jobs: Dirge, Shoulder Charge, Rise!.
5. **The foes' register in data:** moves named by the ladders above, each with its heroes'-grammar twin recorded (so the library's Foes' moves chapter can show it), and the units' English names in place of the generated ones ("Halvstyngaska").
6. **Art:** Joseph's four starters cover the Beinbryn, Beinseidr and two Beinorv; the Beinseidr's five element ramps exist. New bodies (Beinlur, Spettbein, Tork, Skralla) need sprites; stand-ins can be the sword-and-shield frames, tinted.
7. Then the Draugr (Part 4), and mixed rooms to playtest.

## Decided (Nov 22, Joseph)

The foes' register (above); Bash, Smash, Break; Poke, Thrust, Lunge; Calcify; Disarmed as Feeble and Waning a stack; the Beinseidr keeps five elements, bolts named plainly; Rise! (up to 75%; plain pile rules elsewhere); Pinning Shot as a Styng-type at Pinned 2, topped up by claim; Arrow Rain and Cleaver as row wind-ups; the names Beinlur, Tork, Skralla, Spettbein.

Also decided: the Slash ladder **Cut, Hew, Carve**; the pilot is **the built four plus the Beinlur**, then Tork, Spettbein and Skralla once the brains prove out.

## Decided (Nov 23, Joseph)

- **Team plans:** Hunt (Siege and Pick Off merged, on Joseph's priority target), Break, Inflict, Stabilize, Desperate; picked by the head, weighted by family, announced on a switch (Part 2, section 7).
- **The mirror:** reach slots in every pack, within the budget (Part 2, section 8). The adds dial's default waits for the brains.
- **Cover is one interception, heroes and foes alike** (new game); no foe Taunt. Lonnlya (Bulwark) is Fortified 1 and Cover.
- **Kits:** the Beinbryn as revised; the Beinorv quiver (Barbed or Poison), Rapid Arrows, Volley for Elite and Boss, Arrow Rain held back, Sharpen Sight on the Elite archer; the Beinseidr loses Corpse Candle; Calcify on Elite and Boss Beinbryn and the Boss Seidr.
- **The pilot is the built four** (Beinbryn, Beinorv, Beinseidr, Fornbein). The Beinlur is held back; foe healing comes later as one job.
- **The Draugr stay thin on reach** (Part 4); Ande and Mogel are the glue families.

# Part 4: The Draugr (Nov 23, a first pass; agreed in outline)

The saga dead. They hit hard and act after you (SPD 0.6). The Bein are a drilled squad you **out-think**; the Draugr are a grudge you **manage**. Two ideas run the family:

- **The drag:** every Draugr status makes a hero **Late** (Grab: Reeling; Frighten: Feared; the Frost Bolt: Chilled), so a slow family's hits land before your heal.
- **The grudge:** a Draugr's focus is whoever hurt it most. The player's own choices pick the target.

They don't protect each other (no Cover): a Gandraugr in a pure Draugr room is exposed, and that's the counterplay. **Reach stays thin on purpose** (Joseph): the Gandraugr is their only reach, and the mirror fills a big room's second reach slot from guests (Bein, Ande, Mogel). Family rules stay: the crawl (killed by anything but Slash or Eld, it crawls on once at 35%), weak to Slash, Eld and Sol, resist Crush, Natt and Aska. Built moves are in `data.FAMILIES`; *new* marks a move the pass adds. Moves take the foes' register: the status moves are **Frighten** (Feared) and **Curse** (Cursed).

| Unit | Tier | Seat | Its plan | Kit |
|---|---|---|---|---|
| **Halvdraugr** | Trash | Front | "Clutch at your ankles." | Claw, Rake (all); *new* **Grab** (Reeling 1: Late) |
| **Draugr** | Regular | Front | "You hurt me. You." | Grave Axe (Slash), Barrow Fist (Crush), Sweep (all: punishes a clumped line), Frighten (DEF down and Late: sets up the axe) |
| **Stordraugr** | Elite | Front | "Bleed, then bite." | Hi-Grave Axe, Hi-Barrow Fist, Sweep, Blot (Bleeding; by the register **Bleed**, Joseph's call); *new* **Death Bite** (about 80 and Poisoned 1: the finisher) |
| **Gandraugr** | Regular, Magical | Rear (reach) | "Slow the singer." | Shadow Bolt (Natt), Frost Bolt (Hrim, its Styng form: Chilled; three single-target casts freeze), Frighten, Curse |
| **Forndraugr** | Boss | Front | "Mine. All of it." | Great Break (Barrow Fist, Jatte), Hi-Sweep, Hi-Frighten, Great Curse; *new* **Grudge** (its Command: names the hero who hurt it most, out loud); *new* **Unyielding** (Desperate: Steadfast 3 on itself, never Late, never shoved) |

**Dovetails:** the Gandraugr Frightens the Dagskald (Late: the heal lands after the hits): their kind of Hunt, which slows the healer rather than killing him. Grab, then Frighten, then Death Bite: a Late, DEF-down hero takes the bite before it can answer. Three Frost Bolts freeze the fastest hero, which evens the tempo. Sweep punishes clumps. **Mixed Barrow rooms** pay both families off: the head picks the plan; a Beinbryn Covers the Gandraugr; Beinorv Pins hold heroes in place for slow heavies; the Draugr give the Bein the muscle they lack.

**Desperate (the grudge):** each Draugr strikes whoever hurt *it* most; the Forndraugr goes Unyielding. The Bein break; the dead dig in.

# Part 5: Parked (Nov 23)

- **Reach as culture:** the families tell us who needs to exist. A people with bows in every band isn't a cheat when bows are who they are. Seeds: the Djur's spitting Wyrms (each spits its element), the Drattr's reed blowgun (a bow that works underwater).
- **The woodfolk** (Joseph's working name: the **Leshi**; Eldleshi, Vatnleshi, Blastleshi by element). Not dirty goblin cave-raiders: an ancient, shamanistic nature people, half-hidden in their element, a step above the beasts and a step below people. Trickster-elder shamans and warriors twist trails, mimic voices and cause accidents. A Leshi skirmish should feel like the biome itself is messing with your footing, sightlines, sanity and tempo (Dokkn palls, Svindl staggering, Peka and Siktlykt marks). Reach is part of their culture (crude bows, slingsticks, thrown stones). Job seeds: **Stallu** (the Sámi ogre: their big one), **Knol**, **Klo**, **Blotvattr** (the redcap). Naming notes: *Leshi* is Slavic (the leshy), where the game's roots are Norse, Germanic and Uralic: a deliberate step outside, or a reason to look for a northern cousin. *Vattr* (ON *vættr*) is the honest Norse root, but sits beside **Vatn** and shares the **-ttr** ending with the **Drattr**. *Gufi* reads as "Goofy." None of these collide with the parser today. Its own naming session, when a room needs them.

## Decided (Nov 23, later)

The Grave Bolt is plain Aska damage, full size, no curse; the Aska Seidr keeps Curse. The intercession ladder (Lya, Merlya, Lonnlya, Merlonnlya; Cover, Hi-Cover, Great Cover, Bulwark, Hi-Bulwark), one coverer per ally. Foes get intercession, never Taunt. The Beinlur is the foes' necromancer-healer on the Seidr's body, held back; no Rise! for the Draugr. **The mirror counts reach wherever a unit stands** (a Mogel or a Spettbein reaches from the Front) and seats units by their role; it's a composer rule, on for the new game's rooms, so old checks keep their packs.

## Decided (Nov 24, Joseph: the pilot after Waves A-D)

The rules moved under this doc (Battle_Refactor_Current.md D1-D14); where these lines and the older ones disagree, these win.

- **Stale above:** a Curse is Sundered and Poisoned (no Hexed); Disarm is a D3 hold (no Waning); nothing whiffs (D1: a Blinded archer grazes; each Rapid Arrows hit rolls the crit and graze ladder); a status's stacks ride one clock (D13).
- **Stats stick, ailments decay** (the Nov 22 split, unchanged): a Curse's Sundered stays until pushed back, its Poison burns out.
- **Pinned is a window:** it lands for its printed rounds (1, 2 or 3) and can't be reapplied while it's on; the archer needs a clean target, or waits. No topping up (the Beinorv rule above is replaced). Pinning Shot is 2; 3 is a Mer or hero form. Silenced already works this way.
- **The quiver: claim and feed.** Each archer keeps its own ailment fed on the focus (the fuse wants 3), so two quivers put both fuses on one hero.
- **Targeting:** the Bein **out-think** you: their Hunt goes for the hero holding the formation together (the healer, the coverer). The Draugr chase whoever hurt them (the grudge). Settled with fights in the brains step.
- **Command isn't a move:** it's the head's role, free and spoken. The Fornbein as head re-plans every round (a headless pack every two), says its focus out loud, and its death breaks the order (Desperate).
- **Rally is a window** (D14): Mighty 2 on its side for 3 rounds, no Rally while one is up, then what it gave is taken back; a hero's Nedkraft eats into it first.
- **Ogn stays on the Fornbein** at Base size: D11's want already means it only Frightens a hero with no Sundered.
- **The Fornbein's kit:** Command (as head), Cleaver, Carve, Rally, Ogn.
- **Order:** 1. Cover (built Nov 24: D10), 2. the kits as data with no brains, measured on the shared scorer, with D14's two fields (Rally first), 3. team plans, then the units' rules.

## Step 2, built (Nov 24): the kits as data, no brains

**What's in.** `data.PILOT_KITS` by rank (Halv, Regular and Stor Beinbryn, Beinorv and Beinseidr; the Fornbein), swapped in where the new game sets its foes up (`Battle.new_game_enemy`, `engine.pilot_kit`); the old game keeps the generated rows. Each row is a family move whose options name its hero twin (`twin`: Pinning Shot is Genomskott, Killing Shot Fangskott, Called Shot Peka, Silence Bann, Sunder Nedskold, Fortify Aukskold, Rally Allmeraukraft, Cleaver Flokbidskar, Cover Lya), with the foe's tier power and no cost; the library lists each foe move's twins. New family-move options: `stacks` (a printed size), `styng` (a bite of that element first), `pays_on`/`pays`, `bide` (a wind-up, x2.6), `window`, `ai_rest`, `target`; a `cover` row (Cover, Hi-Cover, Great Cover). The quiver (`QUIVER`: Barbed or Poison Arrow) is a coin flip from the fight's rng when the archer is set up (the Poison Arrow has no twin: the grammar has no poisoned arrow). Bolts by element (`BOLT_NAME`, Hi- for Mer); the Frost Bolt keeps its name through its Styng twist; the Grave Bolt is plain Aska. The Beinbryn is a guardian because it carries Cover; the Fornbein isn't. Not yet: Calcify, Command (step 3), the Forn Beinbryn and Beinseidr. The Lightning Bolt carries no Stun (the doc's "the stun rides the bolt" needs Lonnblixt's rider on a foe bolt: a call for later). `test_pilot.py`.

**Two scorer fixes on the way:** foes raise their own side only to their want (D11 both ways: Fortify once, then strike); and a stat move that targets self is scored on self (the AI had been "Fortifying the Beinorv" while every cast landed on the Beinbryn; heroes' Aukskold had the same bug in the new game).

**Measured** (the Dagskald, Skurmar and Vasara at leg 2; 150 fights a room):

| Bein-only room (yardstick size) | Generated kits | Pilot kits |
|---|---|---|
| Regular (Beinbryn, Beinseidr, Beinorv) | 4.1 rounds; Vasara 29%, Skurmar 72%, Dagskald 98% | 4.6; 21%, 80%, 100% |
| Elite (a Stor and two Halv) | 3.6; 53%, 70%, 90% | 3.5; 45%, 87%, 100% |
| Boss (Fornbein and a Halv) | 3.4; 63%, 93%, 99% | 3.4; 62%, 94%, 100% |

The gauntlet (mixed Barrow, Wildwood and Rapids rooms): Regulars 195 / 197 of 240, **Elite 50 of 195 / 73 of 197, Boss 26 of 50 / 47 of 73**; the calibration rooms barely moved (Elite: Vasara 27% / 29%, Dagskald 92% / 95%).

**What it shows:**
- **The pilot kits are easier on the shared scorer**, as expected without brains: setups (Pinning Shot 152 times in 75 Regular fights, Silence 102, Fortify) replace raw damage, and nothing follows them up on purpose. Killing Shot is cast often, Pinned or not.
- **The fire still goes to the Vasara;** the Dagskald ends every pure Bein fight at 100%. Targeting is the brains' job (out-think: the formation's keystone).
- **Cover:** 4 Covers in 75 Regular fights. Rule 1 of the Beinbryn's brain.
- **Rally:** 8 casts in 75 Boss fights; the scorer prefers the Cleaver (151 wind-ups). In a bigger room (more strikers to lift) it's worth more; the Fornbein's brain decides it.
- **The Beinbryn and the Vasara trade:** her Brakrosh Sunders it, it Fortifies back (64 lifts of 146 Fortifies): the anvil against the shield, as meant.
- **Room size:** the room table above (Elite: two Stor and two Regulars; Boss: the Fornbein and three Regulars) is far heavier than the yardstick (an Elite and two Trash; a Boss and one Trash): even the generated kits lose there (1% and 34%). Pure Bein rooms at the yardstick's size are easy (the Bein are weak Oskorei). Room sizes are the adds dial's question, after the brains (Part 2 section 8).

**Next: step 3,** the team plans (the head picks, Command spoken, the priority target as out-think), then the units' rules with claims, and the fallback counts.
