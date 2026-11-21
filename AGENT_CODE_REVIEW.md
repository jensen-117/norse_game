# Agent Code Review — Wave 4a bug-fix checkpoint

Review date: 20 November 2026  
Repository: [jensen-117/norse_game](https://github.com/jensen-117/norse_game)  
Reviewed main: [05909829250a968db0f4b2fdbed22799f06d8a70](https://github.com/jensen-117/norse_game/commit/05909829250a968db0f4b2fdbed22799f06d8a70)  
Compared with: [Wave 4 entry, 8e034de](https://github.com/jensen-117/norse_game/commit/8e034dec62b76c9fdf20001e79fd20ae861edfd4)

**Use this as the current checkpoint and handoff.** It incorporates the banked findings and preserves the previous review and resolutions below. Current statuses here supersede older summaries. Repository review was read-only: no repository files, commits or baselines were changed.

## Recommendation and current status

**Pause feature integration for a bug-fix checkpoint here.** Wave 4a adds useful, playable mechanics, but a normal combination of its new recovery move with existing enemy AI can crash a fight. Three further integration defects are independently reproduced. Resolve these alongside the banked action-lifecycle and protection findings before building more interactions on them.

Do not make a global balance adjustment from the current AI usage counts. The AI cannot consider some legal refreshes at all (C17), and defensive wind-up evaluation remains incomplete (C13). Finish the correctness checkpoint, settle the explicit rule decisions below, then rerun the same measurement configuration.

| ID | Priority | Current status | Finding |
|---|---|---|---|
| C16 | **P1** | **Closed (CPHASH)** | Djupanda can crash a Bonus Round when a Net Drattr values interrupting it |
| C05 | P2 | **Closed (CPHASH)** | An action-time fall can escape wind-up cancellation |
| C12 | P2 | **Closed (CPHASH)** | Egga is bypassed by finishing blows |
| C13 | P2 | **Closed (CPHASH)** | Planning hides queued wind-up threats |
| C17 | P2 | **Closed (CPHASH)** | AI filters out refreshes and useful compound status moves before scoring them |
| C18 | P2 | **Closed (CPHASH)** | Skrida can move into a Dying ally's occupied cell |
| C19 | P2 | **Closed (CPHASH)** | Styng's added hit bypasses Cover |
| C15 | P2 | **Closed (CPHASH)** | A legacy class silently switches the Lab's enemy balance profile |
| A03 | P3 | **Closed (CPHASH)** | Keyboard test resets focus before exercising Enter |

**Checkpoint resolved (Nov 20, after the fixes; coding agent).** Every technical finding in the table is Closed, each with a Resolution block in its own section (cause, change, failing-before evidence, tests, verification). C14's prevention work is done (provenance and a drift check). The rule calls and D09/D10 were settled by Joseph on Nov 20; the decisions are recorded in the rules (classes.md, pillars.md), the data, the move descriptions and the tests together:

| Question | Decision (Joseph, Nov 20) |
|---|---|
| Pin's movement lock | **The cell** ("pull to the Front and Pin to lock them there"): no Move, Swap, Advance or Skrida, lanes included, and no one swaps with a Pinned unit. `rooted="cell"` in the status row. Cover moves no one, for heroes or enemies, so a Pinned unit still Covers. Kasta will treat it as a wall |
| Re-applying Scorched (D10) | **The new Sveda's own blow**, and **Scorched ticks off the caster's power, not a share of max HP**: one Eld hit at the applying tier's power (his MAT against the target's MDF and affinity, taken when it lands) x `SCORCH_POWER` 0.6, at 100/50/20%. A Blast flare restarts the fade and keeps the blow. Percentages of max HP move to Eitr (stacking poison 2/4/6%; next, a feature) |
| Free Halv forms | **Halv is opt-in per verb: attacks only** (`halv=True` on the nine damage verbs). Halvsveda, Halvlak, Halvvakna, Halvskolja, Halvegga, Halvknyta and the rest no longer compile. Free attacks are fine; free heals, taunts, knots break things |
| Bidhevn (D09) | **Double an equally primed Hevn**: Hevn's own x2 for Bid (`manner_power`, compiler data); other Bid moves keep x2.6 |
| Skrida | **Aimed at a cell, like Move**: empty, he steps there; an ally's, they trade places; Move's rules; Nimble either way. No hidden destination or automatic swap |
| Cover and Styng (C19) | **Cover takes a single-target move that deals damage, whole** (Styngegga strikes and dares the protector; Styngnaglskott hits and Pins it) |
| Hevn's count | Attacks that hurt her, reset at each action opportunity (acted, lost to a stun, a Bonus Round's) |
| Weakness on status moves | Every status move; the extra stack goes to the main status (a Pin gains a round, a Scorch nothing); Helvad keeps its rule |
| The Lab (C15) | The new game only; legacy stays in the regression scripts |

**Measurement after the fixes (D10, D08):** the 60-per-shape sweep, regenerated with provenance, moved by at most two points of win rate anywhere (starting trio leg 1 boss 4: 65% to 63%; everything else within a fall per fight). The usage count says why: in 60 default-budget rooms the AI Brennumar casts Sveda 7 times at leg 2 and Lonnsveda 9 times at leg 3, against about 200 Elds or Merelds; there are 8 Scorch ticks in all. C17 lets it consider a refresh; it still declines, because **at `SCORCH_POWER` 0.6 a Base Sveda is a worse move than Eld**: it lands half the time (the tier's status line chance), and when it lands it burns about 1.02 of the caster's hits over three rounds, versus Eld's 1.0 now. It pays only on an Eld-weak target (sure, plus the Bonus Round) or with the forge's free refresh. This is a knob, not a defect: a value near 1.2 would make a landed Sveda about two hits (about one expected), which reads as the intended "fire you feed". Left for Joseph; the Scorch economy (stronger-then-cheaper refresh, Blast maintenance against single-body bosses) is still worth the scripted comparison D10 proposes before freezing it.

**C14 update:** The stale-result defect is resolved at this snapshot: the refreshed report reproduces exactly with its documented **60 fights per shape**, or **1,800 room fights** total. Source provenance and an automatic drift check remain recommended prevention work. Do not carry forward the previous mismatched 30-fight rows as current results.

C01–C04, C06–C11, A01 and A02 retain their previous Closed status. D01–D08 remain design/measurement work with the updates below. D09 and D10 record this pass's two explicit balance decisions; they are not disguised code defects.

## Independent verification and limits

- **239 unittest cases ran and passed.** The seven Lab modules have identical Git blobs to their sim counterparts, providing the equivalent of the additional filesystem parity test and supporting the reported **240**. The standalone autofill/replay test also passed.
- The **37 Wave 4a tests** pass. They include complete-turn cases, formula checks and direct AI-choice checks; they are not all end-to-end turn tests.
- The **4,535 legacy moves/kits**, **288 fixed-party fights**, and **480 wider regression fights** match the previous checkpoint.
- **49 saved page records replay natively:** 48 Auto fights and the new Naglskott/Sveda menu scenario. Winner, round, log length and full log digest match; engine hash is `9948739d5e`.
- The committed sweep reproduces at `sweep.report(60)`, including all three party/leg combinations.
- All nine starting-trio kit snapshots return no excluded moves: Vasara, Ullar and Brennumar, legs 1–3.
- Targeted probes verify the new failures and the rule arithmetic described below. The new native tests and sources are commit-pinned.
- Main was rechecked at the end of the investigation and still pointed to the reviewed commit.

**Limits:** No fresh browser session or clean-clone runtime build was performed in this pass. Native replay does not independently verify fresh rendering, startup, focus, or animations. The reported per-move frequencies in “60 fights” were not independently reproduced against a separately specified usage-sampling configuration; the saved sweep itself was reproduced. Legacy invariance remains valuable compatibility evidence, but it does not exercise every new-game interaction.

## C16 — Djupanda crashes the Net Drattr's interruption valuation

**Priority:** P1. Fix before further integration or treating Auto sweeps as robust.

**Cause:** `bind_value()` assumes every stored wind-up is a damage move. Djupanda has kind `windfall`, a self target and no damage element. When the enemy considers throwing its net at that actor, `expected_damage()` indexes `ELEMENT[None]`.

Sources: [engine.py:1202–1209](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1202-L1209), [expected damage:638–642](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L638-L642), [Bonus Round planning:1745–1750](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1745-L1750).

**Reproduce:** Run this from the sim directory against the reviewed commit. It uses the actual starting-trio leg-3 kits and an unmodified Net Drattr kit:

```python
import random
from engine import Battle, build_hero, spawn_family

v = build_hero("Vasara", 3)
u = build_hero("Ullar", 3)
br = build_hero("Brennumar", 3)
br.mp = 0
e = spawn_family("Drattr", "Drattr", 50, job="Net")
b = Battle([v, u, br], [e], random.Random(20), events=True)
b.begin("party")
b.submit(v.uid, "guard")
b.submit(u.uid, "guard")
key = "m" + str(next(i for i, a in enumerate(br.actions)
                     if a["name"] == "Djupanda"))
b.submit(br.uid, key)
b.commit()  # KeyError: None
```

**Observed:** The Drattr naturally chooses Spett and hits Pierce-weak Vasara for 52 displayed damage. Brennumar winds up Djupanda. The Drattr earns its Bonus Round, considers its still-available net, and the commit crashes:

`commit → plan_phase → declare → bind_value → expected_damage → KeyError: None`

No replacement enemy move or hand-built release is needed.

**Why it matters:** A valid new kit move combined with existing enemy behavior stops the fight instead of resolving the turn. The current test for a stunned Djupanda does not cover an enemy deciding how to interrupt it.

**Suggested fix and rationale:** Introduce a typed pending-effect valuation: damage wind-ups expose damage threat; recovery wind-ups expose recovery value; future heal, song or other effects use their own utility. The interruption scorer can value preventing any of them without pretending all effects deal damage. A minimal type guard prevents the exception, but returning zero for all non-damage wind-ups should be an explicit temporary approximation, not the final AI contract. Coordinate the representation with C13's stored/queued pending-action query.

**Close when:** The seed-20 complete-turn fixture finishes without an exception; a Net Drattr can sensibly value stopping Djupanda; ordinary damage-wind-up interruption remains covered; normal and Bonus Round planning handle non-damage charges. Add the test before the fix and show it fails on this commit.

**Resolution (Nov 20, CPHASH): Closed.**
- **Cause:** `bind_value()` read a stored wind-up as damage; Djupanda is a windfall with no target or damage element.
- **Change:** one query for a unit's pending action, `Battle.pending(u)`, across the whole lifecycle (stored `u.bide`, or the queued release, whose charge token now carries its target: `(token, action, target)`), and a typed value, `pending_value(f, ref)`: an attack is worth its expected damage on its target; a windfall the MP it brings, valued as the AI values Meditate (in the asker's ref: an explicit approximation, commented); any other kind a plain action's worth. `bind_value` reads it.
- **Failing before:** the review's seed-20 fixture raised `KeyError: None` at 0590982; the Net's value of stopping Djupanda equalled its value of a calm caster.
- **Tests:** `C16_NonDamageWindUps`: the seed-20 complete turn finishes; the Net values stopping Djupanda above a calm caster; a damage wind-up still adds exactly `NET_BIDE` x its expected damage. Normal and Bonus Round planning both go through `declare`, so both use the typed value.
- Verification at the end of the checkpoint: 272 unittest cases, including `sim/test_checkpoint4a.py` (a class per finding; its 24 finding tests run against 0590982 first: 13 failures and 5 errors there, the errors new API); the standalone autofill test; the 4,535 legacy moves and the 288 fixed-party fights byte-identical; regress.py's 480 fights identical but one, explained under C18; fresh browser sessions: `s_smoke`, `s_c02`, `s_wave3`, `s_wave4a` and the new `s_focus` pass; the 48 Auto fights re-recorded at this engine (all new-game: C15) and the menu record replay natively.

## C17 — The AI skips legal refreshes and useful secondary effects

**Priority:** P2. Fix before balance decisions based on rare Scorch or status-move use.

**Cause:** `declare()` skips a status action as soon as `capped(target, main_status)` is true. For every non-counter status, `capped()` means only “already present.” Consequently, the new remaining-burn calculation in `status_value()` cannot be reached for a target already carrying Scorched. The same gate excludes extending Pin and excludes compound moves whose main counter is capped but whose added hit or rider is still useful.

Sources: [early filter, engine.py:1366–1372](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1366-L1372), [capped:653–657](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L653-L657), [remaining-burn valuation:1453–1474](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1453-L1474).

**Reproduce:**

1. Build a Brennumar with only Sveda plus the automatic Halveld. Use a neutral, high-HP dummy, as in the existing test helpers.
2. Apply Scorched, then set its fade step to 2.
3. Compare `b.status_value(br, sveda, enemy, 100)` with repeated `b.declare(br)` results.
4. Separately, give Ullar Lonnpeka, cap the target at Marked 3, and leave DEF neutral.

**Observed:** With a 1,000,000-HP dummy, Sveda's computed value is **48,000**, yet all 30 seeded declaration samples choose Halveld. Lonnpeka has positive secondary-effect value but all 30 samples choose Halvskott; the Sundered opportunity never reaches the candidate list.

**Why it matters:** “The AI uses this move sometimes” is insufficient evidence that it understands the move's loop. The Scorch refresh behavior is playable by a person but categorically excluded from Auto decisions, obscuring its sustained pressure.

**Suggested fix and rationale:** Evaluate whether the *whole move* has useful marginal effects: main application, extension/reset, secondary rider, added damage and tempo reward. Keep a capped-counter optimization only when all relevant components are exhausted. Represent status reapplication policies in one place shared with execution so the AI models the chosen heat/duration policy rather than duplicating a different one.

**Close when:** Controlled tests make the AI refresh a nearly faded burn, extend a shorter Pin when worthwhile, and consider Lonnpeka's uncapped Sundered rider or Styng damage despite a capped main effect. Also verify it avoids truly redundant applications. Re-measure usage and sweeps after the change.

**Resolution (Nov 20, CPHASH): Closed.**
- **Cause:** `declare()` skipped a status move whenever its main status was "capped" (for a non-counter: merely present), before any value was computed.
- **Change:** in the new game the AI scores the whole move and skips it only when the whole is worth nothing: `status_value()` = the chance the main status lands x what it adds now (`status_gain()`), + the second status (counted only if the main one lands), + a payoff on the side (scaled by the share it adds), + Styng's hit (which strikes either way), x1.5 for a weakness's Bonus Round. `status_gain()` asks the engine's own policy (`status_instance()`, `reapplied()`, also used by `apply_status()`): a counter, what its stacks change; a burn, what it adds over what's still burning; a refresh, the rounds it adds; a refused status, nothing. Old fights keep the old filter and value, byte for byte.
- **Failing before:** the fading-burn Sveda (value 48,000 on a 1,000,000-HP dummy) never chosen; Lonnpeka on Marked 3 never reached the candidate list.
- **Tests:** `C17_WholeMoveValue`: a nearly faded burn is refreshed, and a fresh one of the same blow is redundant; a shorter Pin is extended and a longer one isn't; Lonnpeka on the fully Marked still Sunders (and is picked, at that target), and is redundant at Marked 3 and Sundered 3; Styng counts despite a capped main status.
- **Measurement:** the sweep was rerun only after this and the rule changes (C14 below).

## C18 — Skrida treats a Dying ally's cell as empty

**Priority:** P2.

**Cause:** `glide_cell()` builds occupancy from living allies only. Ordinary Move explicitly treats a Dying hero as occupying a cell and refuses that destination. Self-targeted Skrida can therefore put two party members in one cell.

Sources: [glide destination, engine.py:1146–1167](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1146-L1167), [ordinary Move's occupancy rule:1864–1873](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1864-L1873).

**Reproduce:** Using the existing `test_wave4a` helpers, make Ullar with Skrida, Vasara and Dagskald against a quiet dummy. Begin a party-controlled fight. Place Ullar at front/0, Vasara at front/1 and Dagskald at rear/0. Set Dagskald's HP to zero and call `b.downed(d)`. Order Skrida on Ullar himself and Guard for other awaiting heroes.

**Observed:** Ullar moves to rear/0; the Dying Dagskald remains at rear/0. Vasara keeps the Front occupied, so the Front rule does not prevent this case.

**Why it matters:** It breaks board occupancy and creates ambiguous targets, rendering and later revival behavior. Future forced movement would inherit another inconsistent definition of “empty.”

**Suggested fix and rationale:** Share cell occupancy and movement legality between Move, Skrida and forthcoming displacement. Distinguish vacant, living occupant, fallen occupant, pinned occupant and any special terrain rule. A Dying hero should not disappear from occupancy merely because they cannot act. Recheck the destination at resolution as well as in the UI.

**Close when:** Self Skrida selects a genuinely legal alternative cell or stays put; it never overlaps a Dying ally. Test ordinary movement, explicit swaps, a full rear row, a fall between ordering and resolution, and revival after the attempted glide.

**Resolution (Nov 20, CPHASH): Closed.**
- **Cause:** `glide_cell()` counted living allies only; Move, the menu and the AI each had their own idea of an occupied cell.
- **Change:** one occupancy rule: `holder(u, cell)` (a living ally, or a Dying hero who still lies there), and `step_to(u, cell)` -> (ok, the ally there, why not): the fallen's cell is taken; no one leaves a Pinned unit's cell or enters it; never empty the Front. Move's resolution, the menu's cells (`move_cells`, `cell_options`), the AI's step-up, fall-back and step-off, Advance, and Skrida all read it, and Skrida is checked again when it lands. Skrida now aims at a cell, like Move (Joseph, Nov 20), so there's no automatic destination to get wrong.
- **Failing before:** the review's fixture put the Ullar on the Dying Dagskald's cell (rear 0) at 0590982.
- **Tests:** `C18_TheFallenHoldTheirCell`: Skrida isn't offered the fallen's cell and can't be ordered there; a hero falling into the destination after the order holds the glide (three heroes, three cells), and revival keeps them apart; ordinary Move and the AI's step-up respect it.
- **The one changed regression fight:** regress.py fight 415 of 480 (Wildwood/Barrow mix, level 30): in round 8 a Hafrunar stepping off Mogel slime used to step onto rear 0, where a Dying Dagskald lay; now it takes rear 2. Same winner and length class (an enemy win before and after); every other fight byte-identical.

## C19 — Styng's added damage bypasses Cover

**Priority:** P2.

**Cause:** Ordinary damage redirects through Cover before calling `land()`. `styng_hit()` calls `land()` directly. Extracting shared damage arithmetic did not also share the interception step. The status branch only handles the separate `thrown` marker used by nets.

Sources: [normal interception, engine.py:1046–1062](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1046-L1062), [Styng direct call:1125–1132](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1125-L1132), [status branch:1014–1023](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1014-L1023), [Cover rule, combat_spec.md:116–122](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/combat_spec.md#L116-L122).

**Reproduce:** Use Ullar against two quiet enemy dummies. Give the second enemy a Cover action aimed at the first and queue it normally in the turn's protection group. Order an attack against the first enemy. Compare Skott with Styngnaglskott, keeping the rest of the fixture the same.

**Observed:** Skott emits `covered` and damages the protector (198 in the fixture). Styngnaglskott instead damages the protected target (69 while it is guarding), with no interception event. The rule says single-target hits strike the coverer; no exception for Styng is defined.

**Why it matters:** The attack component of a compound move silently bypasses a core defense. Lya, future rider attacks and enemy protection will become harder to reason about if each path has separate interception behavior.

**Suggested fix and rationale:** Route damage effects through a shared targeting/interception step before the hit calculation. Preserve the protected ally's position for reach, as normal Cover does. Explicitly decide the status component's delivery policy: intercepting the added strike need not silently move a taunt or an independently targeted status to the coverer. Do not simply redirect the entire compound move without that decision.

**Close when:** A single-target Styng hit respects Cover; shape/All effects retain their exceptions; rear coverers use the original target's reach position; events identify the actual damage recipient. Test Styngnaglskott and Styngegga, including the documented policy for their non-damage components.

**Resolution (Nov 20, CPHASH): Closed.**
- **Cause:** the damage branch intercepted through Cover before `land()`; `styng_hit()` called `land()` directly; the status branch only caught `thrown` nets.
- **Change:** one interception step, `intercept(u, a, tgts)`, before any hit: a protector takes a single-target move that deals damage (a strike, a spell, a status move or taunt with Styng) or is thrown, **the whole move** (Joseph, Nov 20: Styngegga is a small attack plus Egga on one target, not two effects that can split). Rows, columns and All aren't caught; a move without damage isn't either. The protector is reached where the ally stood (the reach spot is passed to Styng's hit).
- **Failing before:** Styngnaglskott damaged the protected Drattr with no `covered` event.
- **Tests:** `C19_CoverCatchesStyng`: Styngnaglskott hits and Pins the protector, not the ally; Styngegga strikes and taunts the protector; a plain Naglskott isn't caught; a Rear protector is struck where the ally stood.

## Banked findings — status after Wave 4a

The complete earlier reproduction notes remain in the preserved report below.

- **C05 remains open.** The Bleeding/crawling-Draugr probe still fires its interrupted charge for about 72.62 HP with zero loss events. The token is still consumed before action-time ticks at [engine.py:871–877](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L871-L877). Retain the token through interruptible hooks, revalidate, then consume it at execution.
- **C12 remains open.** Targeted Egga still lets a taunted Drattr finish Dying Dagskald before target redirection runs; the fixture ends with Dagskald dead. See [929–941](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L929-L941) and [806–818](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L806-L818).
- **C13 remains open.** The pending Bidskott threat still changes from **50.325278934070276 to 0** during planning while its release token remains valid. See [1533–1536](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1533-L1536) and [1628–1635](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1628-L1635). Fix this alongside C16 using typed pending-effect information.
- **C15 remains open.** The same all-sheet versus mixed-party test still switches Forndraugr from x1.75 HP / x2.25 damage / one action to x1 HP / x1 damage / three actions, while sheet heroes retain x1.2 damage. See [428–440](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L428-L440). Make the encounter profile explicit; preserve a deliberate legacy mode.
- **A03 remains open.** The original keyboard scenario still explicitly focuses the body. The new Wave 4a menu test also does so before clicking targets. Those tests exercise menu actions, not the original click-Fight-then-Enter focus regression. Keep the application fix, and add a dedicated natural-focus test.

### C14 resolution update

**Resolved at commit 0590982, independently verified.** The report was regenerated with 60 trials per room shape. At that sample size, `sweep.report(60)[0]` matches the committed report after line-ending normalization. This is 1,800 room fights across 10 shapes and 3 party/leg configurations.

The original problem—making a decision from a stale saved report—is absent at this snapshot. The preventive recommendation remains: include a source/configuration fingerprint and a check-only drift test. Keep the historical mismatch as evidence of why that guard is useful.

## Review of the five implementation calls

These are recommendations for design decisions, not permission to silently rewrite the specification. Record whichever policies are accepted in the rules, compiler/execution data, move descriptions and tests together.

| Call | Assessment and recommendation |
|---|---|
| **1. Pin locks the whole spot** | The implementation consistently intends a cell lock, but the locked written rule says **cannot change rows**. This is a real expansion: it also removes lateral escape from hazards and same-row swaps. My default recommendation is to honor the narrower row lock unless stronger anchoring is explicitly desired. Represent movement restrictions as policy, e.g. row lock versus cell lock, so later roots and displacement do not depend on scattered status-name checks. |
| **2. Re-Pin keeps the longer duration; Sveda keeps the hotter heat** | Keeping the longer *remaining* Pin duration is sensible and prevents a weaker reapplication from shortening it. Hotter-heat retention has a larger economic consequence: a cheaper application can sustain a stronger burn. I recommend that Sveda resets fade using the applying tier's heat, while Blast refresh preserves existing heat; retaining the maximum instead should be a deliberate combo rule and measured as such (D10). |
| **3. Hevn counts attacks, resets even on a lost action** | Counting damaging attack actions rather than animation impacts is a reasonable balance rule: two-hit Blast and flurries do not get arbitrary extra weight. Describe it as “attacks that damaged her since her last action opportunity,” not “every hit.” Resetting at a lost action opportunity is consistent with “since her last turn,” but makes stun/Bonus Round timing important. Keep one explicit policy for successful, skipped, interrupted and bonus actions; do not let incidental resolver returns define it. |
| **4. Weakness applies to every status move; extra stack only on the main status** | This agrees with the broader status-move rule in refactor_plan.md, while classes.md gives Reyk as an example. I recommend keeping the general rule and the single extra main-status increment. Document how non-stack effects translate it: a base Pin on a Pierce-weak foe lasts **3 rounds**, but Scorched currently receives **no extra heat** from the extra-stack parameter. Helvad remains an explicit exception. |
| **5. A sole Front Skrida holds position but gains Nimble** | Keeping the Front occupied and retaining Nimble is reasonable. The implementation is more nuanced than the summary: with a living ally directly behind in the same lane, self-targeted Skrida **swaps them**, even when Ullar is the sole Front hero. I reproduced rear/0 Ullar and front/0 Dagskald afterward. Describe the invariant as “never empties the Front,” and decide whether self-targeted automatic swaps are intended. Fix C18 regardless. |

Sources: [written Pin, classes.md:68–70](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/classes.md#L68-L70); [reapplication, engine.py:683–689](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L683-L689); [attack counting, engine.py:1095](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1095); [action reset:1682–1683](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1682-L1683); [weak status effects:1019–1044](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1019-L1044); [glide selection:1146–1176](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L1146-L1176).

## D09 — Define precisely what Bidhevn doubles

**Status:** Open balance/rule decision; the arithmetic is verified.

At the same tier, target, attributes and hit-count state:

| Damaging attacks received | Hevn / uncharged base Hevn | Current Bidhevn / uncharged base Hevn |
|---:|---:|---:|
| 0 | 1.0 | 2.6 |
| 1 | 1.25 | 3.25 |
| 4 or more | 2.0 | 5.2 |

The current Bidhevn is therefore **2.6 times an equally primed Hevn**, not 5.2 times that primed move. The 5.2 figure uses a Hevn with no retaliation bonus as the denominator. That distinction matters when choosing the fix.

Sources: [compiler's manner multiplier, words.py:217–229](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/words.py#L217-L229); [Hevn payoff, engine.py:627–635](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L627-L635); [“releases double,” classes.md:94–96](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/classes.md#L94-L96).

**Recommendation:** If “double” means double the Hevn she would release with the same accumulated retaliation, give this verb's Patient variant an explicit x2 multiplier. That yields **up to x4** an uncharged base Hevn, or exactly x2 a fully primed ordinary Hevn. If the desired total ceiling is x2 uncharged Hevn, that is a different rule; neither a simple x2 manner nor the current +100% payoff produces that ceiling.

Store a permitted per-verb manner scaling policy in the compiler/data rather than changing Bid globally or special-casing the printed name inside damage execution. Keep the accumulation window independent of the multiplier. Retain the current x2.6 behavior for other Bid moves unless a separate design change is intended.

**Validate before settling:** Compare immediate Hevn, Guard-then-Hevn and Bidhevn at controlled incoming attack counts, speeds and interruption rates. Test the exact damage ratio against an equivalently primed Hevn, plus the agreed reset policy for Bonus Rounds and skipped actions. A test asserting the present grammar multiplier only freezes today's behavior; it does not settle what “double” should mean.

## D10 — Measure Scorch's sustained economy, not only one base application

**Status:** Open balance decision. No blanket boss immunity or automatic nerf is recommended from these numbers alone.

A successfully applied, uninterrupted burn over all three ticks removes approximately these shares of the target's initial max HP, before integer rounding:

| Applying tier | Total over 100/50/20 fade |
|---|---:|
| Halv | 6.8% |
| Base | **13.6%** |
| Mer | 19.04% |
| Jatte | 25.84% |
| Ur | 34.0% |

The user's base figure is correct: `0.08 × (1 + 0.5 + 0.2) = 0.136`. Against a target requiring 18.4 average attack actions by the Layer 1 metric, that is approximately 2.5 such actions of damage. It is **conditional on landing and all ticks occurring**, spread over time; it is not automatically 2.5 actions of immediate expected value. Normal landing chance, the opportunity cost, interrupted/killed bodies and cleansing matter. Against an Eld-weak target the guaranteed application plus a Bonus Round materially improves the deal.

**A more important reapplication consequence:** The compiler accepts a free Halvsveda. In a controlled legal custom kit, Mersveda costs 12 MP at the default sheet and establishes heat 1.4; a subsequent Halvsveda costs 0 MP yet retains heat 1.4 and resets the fade. The next full tick remains **11.2% max HP**. This is compiler-supported and reachable through the new custom-kit API, but that two-Sveda setup is not in a shipped kit snapshot or the current Lab kit selector. Do not describe it as a normal current-kit exploit.

Sources: [Scorched data, data.py:399–442](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/data.py#L399-L442); [stronger heat retained, engine.py:683–689](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/engine.py#L683-L689); [free Halv pricing, words.py:245–251](https://github.com/jensen-117/norse_game/blob/05909829250a968db0f4b2fdbed22799f06d8a70/sim/words.py#L245-L251).

**Recommendation:** First fix C17 so Auto can consider the mechanics it is supposed to measure. Then compare a scripted player-like policy with the AI on representative single-body bosses and reforming/crawling families: one application, repeated Sveda, stronger-then-cheaper refresh, and Blast maintenance. Track action cost, landing probability, MP/HP economy, ticks realized and fight length.

My preferred initial rule is applying-tier heat on Sveda refresh, with existing heat preserved by Blast. That preserves the intended Brennumar/Skurmar partnership while preventing a weaker recast from inheriting stronger heat for free. If max-heat retention is chosen intentionally, test and price that loop explicitly.

Percentage damage can be a useful identity for fighting durable foes. If it overwhelms the intended choices after those tests, adjust shared data—tick share, scaling or a documented cap based on caster power—rather than adding arbitrary boss-name immunities. Do not choose a new global coefficient from rare-AI-use counts.

## Updated holistic assessment

The nine playable starting-trio snapshots are a meaningful milestone. Pin feeding Banskott, Sunder feeding Pierce, Scorch feeding wind, and protection feeding Hevn form understandable party interactions. The free basic attack and explicit recharge choices support readable resource decisions. Keeping new effects in data and sharing damage calculations are sound directions.

The new defects show where the common boundaries still need work: an effect is more than damage, an attack has targeting and interception before arithmetic, and a board cell can be occupied by someone who cannot act. Fix those concepts once before Kasta/Svepa, Song and Knots create more combinations.

**D08 update:** The old caveat that the starting trio's leg-3 kits omit Lonnegga, Banskott and Lonnsveda is now obsolete: all three classes' leg-1–3 snapshots compile without exclusions. Dagskald and Skurmar still await their remaining signatures. The definitions of Layer 1, win-conditioned room costs and AI-policy results remain as previously reviewed.

The refreshed report shows **35% net HP spent** for the starting trio's smallest fodder room, still above the intended 10–25%; the 4-slot elite costs **55%** among wins versus a 40–50% target. Some survival and leg-3 results improve substantially, but “the sweep is easier than the targets” is not uniformly true across all metrics. Avoid equating a higher win rate with reaching the intended resource pace.

Keep D01/D02/D03's connected-route validation: full bars at the start of isolated fights do not establish healer-free route endurance or whether free recovery encourages stalling. Add representative human or scripted tactical play after the correctness fixes; compare like sample sizes and record the active rules profile.

## Coding-agent handoff

Work through this checkpoint before integrating more Wave 4 effects:

1. Add a failing complete-turn regression for C16, then fix non-damage wind-up valuation. Coordinate pending-effect state with C13.
2. Finish C05 and C12's interruption/forced-target boundaries; preserve existing resolution history.
3. Fix C17, C18 and C19 with shared effect-value, occupancy and interception rules. Make each reproduction fail on the reviewed code before changing it.
4. Resolve C15's explicit Lab profile and A03's natural-focus test.
5. Record the accepted decisions for Pin movement, reapplication heat, Hevn counting/reset, status weakness and Skrida fallback. D09/D10 contain recommendations; distinguish an approved rule from a coding default.
6. Rerun tests and browser checks, capture current page records, replay them, and regenerate the sweep only after behavior is settled.

Keep all finding IDs. Append a Resolution block to each fixed item with cause, change, rationale, commit, failing-before evidence and verification. C14's current mismatch is already resolved; add provenance/drift protection rather than reopening it on old numbers.

Verification should include the 240-count suite/parity basis, the separate autofill test, legacy move/fight comparisons, new-game interaction tests, a fresh browser session including keyboard focus and actual status actions, native replays, and a reproducible 60-per-shape report. Explain changed new-game results; do not overwrite them as if they were pure refactors. Unchanged legacy fights alone cannot close new-game defects.

---

## Preserved earlier review and resolution history

The following Wave 4 entry checkpoint and earlier repository report are retained as history. They contain reproduction details for banked findings. This document's top status table and Wave 4a updates take precedence, especially C14's resolution and the starting trio's now-complete kits.

# Agent Code Review — Wave 4 entry checkpoint

Review date: 20 November 2026  
Repository: [jensen-117/norse_game](https://github.com/jensen-117/norse_game)  
Reviewed main: [8e034dec62b76c9fdf20001e79fd20ae861edfd4](https://github.com/jensen-117/norse_game/commit/8e034dec62b76c9fdf20001e79fd20ae861edfd4)  
Previous review: [Wave 3, abaadf7](https://github.com/jensen-117/norse_game/commit/abaadf76ee4aae9c9d525a9b326d42df8bb5e999)

This is a read-only review and handoff. No repository files or commits were changed. The current findings below take precedence over the historical report preserved at the end. In particular, its “all 13 technical findings closed” statement describes the earlier checkpoint; C05 is reopened here. The banked Wave 3 findings C12, C13, A03 and D08 are now incorporated into this document.

## Current recommendation

Take a focused correctness and measurement checkpoint before relying on the next sweep to freeze balance. Fix C05 and C12 together around action resolution, and C13 around visibility of pending actions. Correct the Lab's balance selection (C15), strengthen its keyboard regression test (A03), then regenerate the sweep with provenance (C14).

Independent Wave 4 implementation can continue, but its new effects should enter playable kits only with complete-turn tests and AI evaluation. Do not interpret unchanged legacy fights as proof that new class behavior works: those legacy parties deliberately bypass the new tuning.

There is no P0/P1 finding in this pass. The six open technical entries are:

| ID | Priority | Current status | Finding |
|---|---|---|---|
| C05 | P2 | Reopened; earlier fixes retained | A release consumes its cancellation token before Bleeding can interrupt it |
| C12 | P2 | Open; reverified after targeted Egga | A finishing blow bypasses taunt redirection |
| C13 | P2 | Open; reverified | Planning hides a queued wind-up from threat evaluation |
| C14 | P2 | New | The committed sweep report does not reproduce at the reviewed commit |
| C15 | P2 | New integration finding | Choosing a legacy class silently changes the enemy ruleset in the Lab |
| A03 | P3 | Open; source rechecked | The browser test removes the focus condition that caused the Enter restart bug |

C01–C04, C06–C11, A01 and A02 retain their prior Closed status; their regression tests pass. This is not a claim that every old resolution was independently re-audited in full. D01–D07 remain design validation work. D08 is partially addressed and updated below.

## Scope and verification

The repository is populated: the pinned tree contains 4,479 tracked blobs/files. Main was rechecked after the investigation and still pointed to the pinned commit.

This pass covered all five commits after the Wave 3 review: initial tuning, the room sweep, class bodies and one action per enemy, rounded approved settings, and targeted Egga / Medvind / Avliva definitions. It reviews Wave 4's entry point, not signatures that have not yet been implemented.

Independent results at the pinned commit:

- **202 unittest cases pass**, plus the standalone autofill/replay test passes. All seven modules loaded by the Lab have identical Git blob hashes to their sim counterparts, including byte-for-byte comparisons of the three changed modules. This supports the reported **204 total checks** when the parity check is counted as one.
- **4,535 legacy moves/kits are identical** to the Wave 3 snapshot.
- **288 fixed-party fights and 480 wider regression fights are identical** to the Wave 3 snapshot.
- **48 committed page Auto records replay natively** with matching winner, rounds, full log digest and line count; engine hash `57674c777c`.
- The **900 room fights** in `sweep.report(30)` were rerun without writing the report. Layer 1 reproduces; some Layer 2 rows differ from the committed report.
- Additional probes reproduce C05, C12 and C13, and the C15 profile switch.
- Medvind applies Quick to one ally, that ally's row with Flok, and the party with All. Flokegga taunts the selected enemy row and leaves the other row alone.
- Banskott and Avliva are correctly refused by Battle while their conditional mechanics remain unresolved. Their newly approved multipliers are not claimed to be implemented.

**Limits:** This pass ran fetched, commit-pinned Python sources through an in-memory import harness. It did not run a fresh browser interaction session, a clean-clone runtime build, or a human-played dive. Native replay of saved browser records does not establish fresh browser rendering, focus, startup or playback correctness. A03 is a test-coverage finding from source inspection, not a claim that the current Enter fix is broken.

## C05 — A release consumes its cancellation token before an action-time fall

**Priority/status:** P2, reopened. This is an additional boundary of the existing C05 lifecycle issue; do not assign a new ID or erase either previous resolution.

**Context and cause:** The token introduced by commit 762ac97 correctly handles a fall after planning but before `resolve()` starts. However, `resolve()` checks and immediately clears `u.charge`, then calls `tick_statuses(u, "action")`. If Bleeding makes a Draugr fall and crawl, or a Mogel re-form, the unit is alive again when that hook returns. `interrupt()` sees neither a stored wind-up nor a token. The old release then continues.

Sources: [release entry, engine.py:825–835](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L825-L835), [action ticks:796–806](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L796-L806), [interruption:675–682](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L675-L682), [fall/crawl/re-form:500–543](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L500-L543).

**Reproduce** from the sim directory:

```python
import random
from engine import *
from grammar import compile_word

v, d = build_hero("Vasara"), build_hero("Dagskald")
e = spawn_family("Draugr", "Draugr", 50)
b = Battle([v, d], [e], random.Random(1), events=True)
a = compile_word("Skott", manner="Bid")
e.actions = [a]
e.bide = (a, d)
e.hp = 1
e.status["Bleeding"] = {"rounds": 3}
b.begin("party")
for uid in b.awaiting():
    b.submit(uid, "guard")
before = d.hp
b.commit()
print(before - d.hp, e.stats["bides_lost"])
print([x.get("text") for x in b.events if x.get("text")])
```

**Observed:** Bleeding deals 77; the Draugr falls and crawls; its old Patient Shot still hits for about 72.62 HP (73 displayed). No `bide_lost` event occurs. Replacing the enemy with `spawn_mogel("Stor", "Jord", 50)` also reproduces it: the new Litel body fires the old charge for about 207.48 HP, with zero losses recorded. These are controlled, valid-action lifecycle fixtures, not claims that those exact charges occur in the shipped room kits. The defect also reproduces at the preceding Wave 3 snapshot, so the new tuning did not introduce it.

**Why it matters:** The agreed “falling ends the wind-up at that moment” rule is still dependent on exactly where the fall happens. Wave 4's additional periodic effects and reactions make this boundary more important.

**Suggested fix and rationale:** Retain the release token through all pre-action hooks that can interrupt or replace the actor. Revalidate it after those hooks, then consume it only when execution is committed. Treat this as an action lifecycle rule shared by all families, rather than special-casing Bleeding, Draugr or Mogel. Ensure an interrupted/skipped release cannot leave a stale token behind.

An in-memory diagnostic change retaining and rechecking the token across the damage tick changed the Draugr result to **zero damage and exactly one loss event**. This validates the proposed direction; it is not an applied or fully verified production patch.

**Close when:** Add failing-before/fixed-after full-turn tests for the crawling Draugr and re-forming Mogel during an action tick; retain the existing post-planning fall/revive tests and uninterrupted-hit assertion. Check one loss event, no old release, and no stale charge after skipping or interruption.

**Resolution (Nov 20, CPHASH): Closed (second follow-up).**
- **Cause:** `resolve()` checked and cleared the release's charge token before the action-time ticks; a Bleeding fall that crawled or re-formed came back alive with nothing left to interrupt.
- **Change:** the token is kept through the action-time hooks: checked on entry (`holds()`), checked again after `tick_statuses(u, "action")`, and consumed only when the release is committed. A fall inside the tick calls `interrupt()`, which clears it, so the release is lost with one loss event. A re-formed Mogel's fresh body carries no charge. No family-specific code.
- **Failing before:** the crawling Draugr's old Patient Shot hit the Dagskald for ~73 with no loss event; the re-forming Mogel's for ~207.
- **Tests:** `C05_ActionTimeFallsEndTheCharge`: the crawling Draugr and the re-forming Mogel fire nothing, record exactly one loss, and leave no stale charge or wind-up; an uninterrupted release still fires and clears its token. The earlier C05 tests (`test_checkpoint.py`) still pass.

## C12 — Egga still does not redirect a finishing blow

**Priority/status:** P2, open; banked from Wave 3 and reproduced against the new targeted Egga.

**Cause:** The branch for attacking a Dying unit executes before `targets_for()`, where taunt redirection lives. A taunted enemy therefore obeys Egga against standing allies but ignores it when finishing a fallen ally.

Sources: [finishing blow before target resolution, engine.py:883–895](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L883-L895), [taunt redirection:764–776](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L764-L776).

**Reproduce:** Build Vasara and Dagskald. Give a level-15 Spear Drattr only `dict(strike("Pierce", power=1), cost=0, reach="any")`. Construct an events-enabled Battle with seed 1. Set Dagskald to 0 HP, call `b.downed(d)`, then set `d.breaths = 2`. Begin with party control, order Vasara's `m2` (Egga) on that enemy's UID, then commit.

**Observed:** The enemy naturally declares against Dagskald. Egga resolves first on that enemy, but there is no drawn event. The finishing blow removes one breath and the end-of-round tick removes the second: Dagskald dies. Vasara was alive and reachable.

**Why it matters:** This is exactly when a player would expect protection to matter. The written rule covers the taunted enemy's single-target attacks; it does not exempt finishing blows.

**Suggested fix and rationale:** Determine the effective forced target before branching into fallen-target or ordinary-hit execution. Share the reach and single-target checks instead of adding a second ad hoc Egga check to the finishing branch. Preserve row/all/spot exceptions and the rule that an unreachable taunter cannot redirect the attack.

**Close when:** A full ordered turn verifies a reachable taunter takes the attack and the fallen ally loses only its ordinary end-of-round breath. Also cover an unreachable or fallen taunter, unaffected area attacks, and targeted Egga not affecting an untaunted second foe.

**Resolution (Nov 20, CPHASH): Closed.**
- **Cause:** the finishing-blow branch ran before `targets_for()`, where Egga's redirect lived.
- **Change:** one helper, `drawn_to(u, a, chosen)`, settles a taunted unit's forced target, and `resolve()` calls it before branching into the finishing blow, the bone pile or ordinary targeting; `targets_for()` uses the same helper. Its conditions are the old ones: a single-target move at the other side (not rows, All or spots), a taunter who is up and in reach.
- **Failing before:** the taunted Drattr finished the Dying Dagskald (dead at the end of the round), no `drawn` event.
- **Tests:** `C12_TauntCatchesFinishingBlows`: the reachable taunter takes the blow and the fallen loses only the end-of-round breath; an unreachable taunter (a short blade, Vasara behind a standing Ullar) doesn't redirect and the fallen in the Front is still finished; an untaunted second foe still finishes.

## C13 — Planning makes a still-pending wind-up disappear from AI threat evaluation

**Priority/status:** P2, open; banked from Wave 3 and reverified.

**Cause:** `plan_phase()` moves each stored `bide` into a queued release and sets `u.bide = None` before ordinary actors declare. `bide_threat()` only reads `u.bide`. The queued token holds the action but not its target, so the shared threat query has lost the information it needs.

Sources: [threat query, engine.py:1319–1322](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L1319-L1322), [planning:1412–1437](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L1412-L1437), [Egga valuation:1241–1249](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L1241-L1249), [defensive board options:1324–1337](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L1324-L1337).

**Reproduce:** Build Vasara and Dagskald plus a level-15 Spear Drattr. Construct a Battle with seed 1. Give the enemy a Bid Skott via `compile_word("Skott", manner="Bid")`, set `e.actions = [a]`, `e.bide = (a, d)`, and `e.actions_per_round = 1`. Compare `b.bide_threat(d)` before and after `b.plan_phase([v, d, e], False)`.

**Observed:** Threat drops from **50.325278934070276 to 0**, even though the release is queued and its token is still held. In the fixture Vasara declares Krosh and Dagskald declares Sol. The defect is the missing threat input; Egga need not always be the optimal choice.

**Why it matters:** Defend, Cover, rotation and the new taunt valuation cannot reliably react to visible wind-ups at their decision point. This weakens both actual Auto behavior and the evidence used for balance.

**Suggested fix and rationale:** Expose active pending actions through one query that survives the stored-to-queued transition and includes actor, target and validity. Publish that state before asking actors to declare. Count a wind-up once, remove it on interruption, and account for its eventual target/reach policy. This can share the lifecycle representation used to fix C05 rather than maintaining a second AI-only copy of charge state.

**Close when:** Threat remains present through planning, disappears immediately on cancellation, is not double counted, and the relevant defensive options receive it. Include a complete-turn fixture demonstrating a sensible defensive response under controlled scores.

**Resolution (Nov 20, CPHASH): Closed, with C16.**
- **Cause:** planning moved each wind-up into a queued release and cleared `u.bide`; `bide_threat()` read only `u.bide`, and the queued token didn't keep the target.
- **Change:** `bide_threat()` reads `pending()`, which sees a stored wind-up or a still-valid queued release (target included). An interruption clears both (`interrupt()`), so the threat goes with it; a wind-up is in one place at a time, so it counts once.
- **Failing before:** threat 50.325 before planning, 0 after, at 0590982.
- **Tests:** `C13_PendingThreatSurvivesPlanning`: the same threat before and after planning; not doubled; 0 after an interruption; and a complete planning step where the healthy Vasara, declaring with the release queued, covers the Dagskald it's aimed at (a level-50 shot, ~286 expected, three times her Krosh; at level 15 her Krosh rightly outscores covering a 50).
- **Fingerprints:** legacy fights unchanged (288 and 480); the one regress.py change is C18's.

## C14 — The committed sweep report is stale after the latest behavior change

**Priority/status:** P2, new; fix before deciding the next balance change.

Sources: [committed result rows, sweep_report.md:50–59](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sweep_report.md#L50-L59), [report generation, sim/sweep.py:109–151](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/sweep.py#L109-L151).

**Reproduce:** From the sim directory, call `sweep.report(30)[0]` and compare it with `../sweep_report.md`. Calling the function instead of the script's main block avoids overwriting the report. Normalize line endings only.

**Observed, starting trio, kit leg 1:**

| Measurement | Committed report | Reproduced at reviewed main |
|---|---:|---:|
| Fodder, 3 slots: HP spent on wins | 41% | 42% |
| Fodder, 5 slots: wins | 80% | 87% |
| Elite, 4 slots: wins | 47% | 57% |
| Elite, 4 slots: HP spent on wins | 59% | 63% |
| Boss, 6 slots: wins | 17% | 13% |

Layer 1 and the starting trio's leg-3 rows reproduce; multiple leg-1 rows do not. The latest targeted-Egga change affects the behavior measured by these rows. The report carries settings but no source fingerprint that exposes this mismatch.

**Why it matters:** The sweep is explicitly being used to choose the next step. A stale result can send that decision in the wrong direction even when tests and legacy fingerprints remain green.

**Suggested fix and rationale:** Regenerate after the correctness fixes, and include reproducible provenance: source hash or commit, sample count, seed policy, party/leg, encounter configuration, kit exclusions and active tuning profile. Add a check-only report comparison that fails on drift without rewriting the expected result. A source hash avoids the circularity of embedding a commit that will itself change when a generated report is committed.

**Close when:** The saved report reproduces with its documented configuration; intentional changes are explained, not merely overwritten; and a rules change can no longer leave the headline report silently stale.

**Prevention (Nov 20, CPHASH):** the report's header now carries a source hash (SHA-256 over data, words, engine, grammar, composer and sweep, line endings normalised) and its whole configuration (rules profile, n, seed policy, places, shapes, parties and legs), and lists any kit moves left out. `python3 sim/sweep.py --check` says whether the saved report is from the current sources; `--check --rerun` regenerates it at its own n and compares, writing nothing. Regenerated after every behaviour change of this checkpoint; see D10.

## C15 — The Lab silently switches enemy balance when one legacy class is selected

**Priority/status:** P2, new integration finding. The engine branch is deliberate and tested; the problem is exposing mixed profiles as ordinary party choices without making the ruleset explicit.

**Cause:** Battle enables the new enemy settings only if every party member has `kit_leg`. The Lab still offers all old classes and its “Roll classes” path can select them. A new sheet hero retains its new body and x1.2 damage in a mixed party, while enemies revert to old HP, old damage and multiple actions.

Sources: [profile inference, engine.py:415–427](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L415-L427), [hero tuning:354–360](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L354-L360), [Lab class menu:24–26](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/lab.py#L24-L26), [random class selection and mixed construction:43–68](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/lab.py#L43-L68), [page class choices, index.html:213](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/fight_lab/index.html#L213).

**Reproduce:** In the Lab, use Vasara/Ullar/Brennumar at level 50, then replace only Brennumar with Hafrunar. Use the same enemy rank/level. An equivalent direct probe builds the first two heroes with `build_hero`, the third with `build_hero("Brennumar")` or `birth("Hafrunar", 50, Random(1))`, and places a fresh level-50 Forndraugr in each Battle.

**Observed:**

| Enemy setting | All sheet heroes | One Hafrunar replaces Brennumar |
|---|---:|---:|
| HP multiplier | 1.75 | 1.0 |
| Damage multiplier | 2.25 | 1.0 |
| Actions per round | 1 | 3 |
| Vasara/Ullar damage multiplier | 1.2 | 1.2 |

**Why it matters:** A party comparison also changes the opposition's rules. A tester can mistake this for class balance, and a random party can enter the hybrid configuration without choosing a different game mode.

**Suggested fix and rationale:** Make the rules/tuning profile explicit at the encounter boundary, and preserve the legacy profile for legacy regression fixtures and records. In the Lab's new-game mode, offer supported sheet classes and roll from that set; expose legacy experiments as a visibly separate mode. If mixed profiles are intentionally useful, label and record them as such. Do not spread class-name exceptions through enemy spawning or silently strip the new heroes' stats.

**Close when:** The Lab cannot silently change profile through a normal class edit or random roll; records identify the profile; legacy records still replay; and profile-selection tests cover both deliberate modes.

**Resolution (Nov 20, CPHASH): Closed.**
- **Change:** the rules profile is explicit at the fight's boundary: `Battle(..., profile=)` and `rules_profile()`. "new" (the new game's settings and rules) needs a party of sheet heroes; "legacy" is the old rules. Unnamed, it follows the party, and a mixed party is refused until a profile is named, so no class edit can switch the opposition's rules silently. The Lab plays the new game only (Joseph, Nov 20): its class menu and its random rolls offer the five sheet classes, `make_party` refuses an old class, `start` names `profile="new"`, and each record stores its profile. `replay.py` replays an old record under the profile it ran with (inferred as before when the record predates the field).
- **Failing before:** the review's mixed party switched Forndraugr to x1 HP, x1 damage, three actions.
- **Tests:** `C15_TheRulesAreNamed`: the review case (all sheets: new; mixed: refused, refused as "new", allowed as an explicit "legacy"); the regression fixtures (old recruits) need no change; the Lab's menu, rolls, refusal and record profile. `test_tuning` updated to name the profile for its mixed case.
- **Records:** the 48 Auto records were re-recorded (all new-game now; before, they mixed classes, i.e. ran the hybrid). `checks/page_fuzz.jsonl` predates the class sheets and no longer replays (its kit indices point at old loadouts); it isn't a current fixture.

## A03 — The browser test masks the Enter-restart regression

**Priority/status:** P3, open; banked from Wave 3.

Source: [sim/checks/s_wave3.py:20–27](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/checks/s_wave3.py#L20-L27). The current application fix remains present at [fight_lab/index.html:330](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/fight_lab/index.html#L330).

**Issue:** Immediately after clicking Fight, the test forcibly focuses the body. That removes the focused-button state which caused Enter to restart a fight. The updated test also clicks a canvas target before pressing Enter, further distancing it from that original sequence.

**Reproduce/verify the gap:** In a disposable test context, remove the application's blur fix and run the current Wave 3 test. Its explicit focus reset prevents it from exercising the original trigger. This mutation check was not run in a fresh browser in this pass; the masking operations are directly present in the source.

**Why it matters:** The Meditate and Egga scenario can remain green while the actual keyboard restart bug returns.

**Suggested fix and rationale:** Add a focused regression that clicks Fight and uses keyboard commands/Enter without any test-induced focus transfer or intervening canvas click. Record the fight seed/session identity and assert it remains the same while the round advances. Keep the targeted-Egga scenario for its own purpose. Exercise the user action, not an implementation detail such as whether blur() was called.

**Close when:** Removing the application fix makes the new regression fail, restoring it makes it pass, and the ordinary keyboard and mouse combat scenarios still pass.

**Resolution (Nov 20, CPHASH): Closed.**
- **Change:** `sim/checks/s_focus.py`: a real mouse click on Fight (the button takes focus), then Enter to fight the round, with no focus change, canvas click or other help; the fight must keep its id and seed while its round advances. The Egga/Meditate scenario keeps its own purpose.
- **Mutation check:** with the page's `blur()` removed (a disposable copy), it fails: "the fight restarted" (a new fight id) and "the round didn't advance"; restored, it passes.

## Design review and D08 update

### D08 — Match each balance claim to what its measurement actually measures

**Status:** Partially addressed. The new class bodies, separate enemy actions setting and real room fights materially improve the old Layer-1-only sweep. The earlier concern about old multi-action enemies being implicit in new-game room fights is superseded: those enemies now act once. Do not carry that obsolete criticism forward.

The remaining distinction matters:

- **Layer 1** divides initial HP by expected damage per attack action. It is not a simulation of killing the whole enemy through crawl/re-form/reassembly, nor a count of individual impacts in a multihit attack. Label it “expected attack actions against initial HP” or clearly define the shorthand. See [sweep.py:38–53](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/sweep.py#L38-L53) and [expected_damage, engine.py:604–608](https://github.com/jensen-117/norse_game/blob/8e034dec62b76c9fdf20001e79fd20ae861edfd4/sim/engine.py#L604-L608).
- The roster weights available variants rather than equal families: 20 of 54 entries are Ande element/rank variants. Keep overall medians, but add family/tier distributions so the solver cannot conceal a difficult family behind many similar entries.
- **Layer 2** correctly includes real combat, but HP/MP and rounds are measured only among wins. They are net end-of-fight deficits, not gross damage or expenditure. Healing, Meditate and martial HP costs affect those numbers. Keep the existing win-rate and falls columns beside them.
- Kits remain intentionally partial. In leg 3, Vasara loses Lonnegga until its rider exists, and Dagskald loses Lonnlak until its cleanse exists. Emit excluded names/reasons in the report. The current leg-3 starting-trio comparison is not evidence for the completed kit's protection loop.
- “AI floor” is a hypothesis, not a measured bound on human performance. The AI has incomplete defensive behavior (C13), while damage evaluation can read true affinities unavailable to a fresh player's knowledge. Call these “current AI-policy results” until paired human/scripted-policy runs establish a useful comparison.

**Recommendation:** Preserve the approved 1.2 / 2.25 / 1.65 / 1.75 settings while fixing correctness and report freshness. Extend the measurements before another global retune. This keeps the solver useful without treating its four median targets as proof of encounter pacing.

### D01, D02 and D03 — What the current rooms imply for the next playable leg

At the reviewed commit, the starting trio's smallest fodder shape wins 97% of 30 trials but loses about **42% net HP on wins**, versus a 10–25% target, with **0.60 falls per fight**. Its 4-slot elite wins 57%; its 4-slot boss wins 57%. These are warnings about the current AI-played room model, not a proven human difficulty verdict.

The five class identities read more clearly with the new bodies: Vasara absorbs pressure, Ullar trades resilience for speed and damage, Brennumar is fragile, Dagskald has magical resilience, and Skurmar is fast. The grammar still supports recognizable growth and party interactions. The danger is judging those interactions before the signatures and defensive behavior actually participate.

For the next decision:

1. Fix the confirmed behavior and reporting defects, then rerun the same seed set so differences remain attributable.
2. Play a short connected route with the starting trio and a healer variant, tracking survival, falls, HP/MP after each room, recovery opportunities, and retreat decisions. Fresh full bars in every isolated room do not test route endurance.
3. Compare room budget, rank mix and enemy count before adjusting global damage again. Enemy action economy is now a visible lever; the large 3-to-6-slot deterioration should inform room authoring.
4. Add representative scripted choices or human play logs for taunt/protection, resource recovery and target priority. Include the time and reward for stalling, preserving D03's original concern.
5. Revisit the full leg-3 comparisons when Wave 4 unblocks the defining moves.

D04–D07 remain the earlier design/UI validation milestones; this pass does not establish return banking, mutation comprehension, decision/playback pacing, or accessible keyboard targeting.

## Handoff and acceptance

Work through C05, C12, C13, C15, A03 and C14 using these IDs. Keep existing resolutions and append follow-up Resolution blocks with cause, change, rationale, commit and verification. The targeted-Egga rule and approved tuning settings are the reviewed design baseline; change them only as an explicit design decision.

For each reproduced defect, first add a meaningful test that fails on this reviewed commit. Prefer shared action lifecycle, target-selection and encounter-profile rules over family-specific exceptions. Regenerate the sweep only after the behavior fixes; explain both unchanged and changed results.

Before closing the checkpoint:

- Run the complete test suite, standalone autofill test and Lab parity check.
- Compare the 4,535 legacy outputs and the 288/480 fight sets; explain any intentional differences.
- Add or update new-game fixtures that actually exercise the affected behavior; unchanged legacy fixtures cannot close these findings.
- Run fresh browser smoke and focus/session tests, then capture and replay current Auto records.
- Reproduce the saved sweep with recorded configuration and source provenance.
- Update the top summary accurately: distinguish fixed, deferred and design-validation items. Do not mark an item closed solely because the existing tests passed.

---

## Historical review and resolutions — preserved record

The following is the repository's existing AGENT_CODE_REVIEW.md as fetched at the reviewed commit. Its original baseline, recommendations and checkpoint summary are historical. The Wave 4 entry checkpoint above is the current status, including the new C05 reopening and banked/new findings. Earlier resolution text is retained so the coding agent can append evidence rather than lose history.

# Agent Code Review — norse_game

Review date: 20 November 2026  
Repository: [jensen-117/norse_game](https://github.com/jensen-117/norse_game)  
Current review baseline: [Wave 2b — 8a7afee433626c3fe532d618f2c95f73a219e035](https://github.com/jensen-117/norse_game/commit/8a7afee433626c3fe532d618f2c95f73a219e035)  
Scope: consolidated technical audit and game-design review through Wave 2b. Repository review was read-only; this report is a separate deliverable. **Fixes applied Nov 20 (see Checkpoint summary and each entry's Resolution).**

## Recommendation

Take a focused bug-fix checkpoint before the next wave wires the new grammar into playable class kits. Address C01 and C08 first, then C09–C11 so the new compiler has dependable legality, targeting, and effect rules. Resolve the compiler contract in A01 alongside that work. Fix C02 before more browser playtesting and C03 before handing the Lab to another developer. C04–C07 should be completed before broader balance conclusions or authored routes depend on those systems.

This is not a recommendation to complete every planned feature before continuing. Song, Knots, displacement, and other explicitly deferred signatures remain later-wave work. Independent content and design work can continue while the affected foundations are corrected. A documented rejection of a currently unsupported combination is an acceptable temporary boundary; accepting it and silently doing something else is not.

The project has a coherent identity: the party is the build, words describe its growing capabilities, and the tapestry records the consequences of routing. The engineering strengths are deterministic simulation, substantial regression coverage, native replay, and data-driven mechanics. The main weakness is that successful behavior preservation also preserves old bugs, while new combinations can compile without having a complete execution contract.

## Checkpoint summary (Nov 20, 2026, after the fixes)

**Resolved: all 13 technical findings are Closed** (C05 was reopened by the re-review and closed again with a follow-up), each with its cause, fix, rationale, commit and verification in its own entry below (IDs kept): C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, A01, A02. The design questions (D01–D07) are validation milestones, not defects, and stay open for the playable-leg milestone; D05's recommendation (a plain-language label beside every spoken name, before/after mutation comparison) is agreed.

**Design decisions taken (Joseph, Nov 20), applied in the fixes:** falling to Dying ends a wind-up (C05); carving adds Mer, finding Jatte, only gear Ur (C08); per-verb target parts from classes.md, no group revive or party-wide self buff yet (C09); manners scale heals, no crits or flurries on heals (C11); Swift + Heavy refused, Patient + one speed manner legal (A02); a nulled or absorbed hit doesn't shatter (C04); knowledge follows a transform without copying across jobs (C06).

**Verification performed at the end of the checkpoint:** 182 tests (31 in `sim/test_checkpoint.py` after the C05 follow-up, 29 before it, one class per finding; plus `test_lab_parity.py`); the legacy golden of 4,535 moves and kits identical throughout; the fixed-party fingerprint identical except one explained change (below); `regress.py` (480 fights) identical for every latent fix; the page's 48 Auto fights run with no page errors and replay natively after every engine change; `checks/s_c02.py` (restart during playback) and `checks/s_smoke.py` pass; a clean clone prepared only by `tools/prepare_lab.py` boots and plays.

**The one baseline change, explained (C01):** 29 of 288 fixed-party fights differ, all party wins with the same rounds, only in breath, dead and stabilised events: 11 heroes who used to die after victory now stabilise. New baseline `sim/checks/fp_c01.sha1`. No other fix changed any fight in either regression set (C04–C07 are latent there, so their tests carry the proof).

**Remaining:** D01–D07 (design validation, at the playable-leg milestone); the deferred work listed below (Wave 3 class integration, Wave 4 signatures, Wave 6 presentation, Holm and Hasin, the dive economy).

**Can the next wave proceed? Yes**, with two conditions the fixes now enforce:
1. **A Battle refuses any move that isn't resolvable yet** (`words.unresolved`). Several kit moves are compiled but not playable until their mechanics land: Egga (taunt) and Kvad, Knyta, Skrida, Kasta, Svepa, Hevn, Djupanda, Banskott, Lonnlak, Lonnsveda, plus statuses with no row yet (Pinned, Scorched). Wave 3 must implement Egga and Meditate (its own scope) and run the level sweep's first layer with executable moves only; each Wave 4 mechanic removes its kind or field from the unresolved lists together with a full-turn test.
2. **Every intentional rule change explains its fingerprint change** in its commit and here, as C01 did.

## Scope, evidence, and status

The repository is populated. The original review verified four commits and 4,457 tracked files at the initial snapshot; those are historical counts, not current totals. The earlier GitHub `size=0` metadata was not reliable evidence of an empty repository.

Reviewed checkpoints:

| Checkpoint | Commit | Assessment |
|---|---|---|
| Initial review / Wave 1a | [cc7410d](https://github.com/jensen-117/norse_game/commit/cc7410d678c65dfa0d12cb531160f572a5c6c954) | Core simulation, encounter generation, knowledge/replay, browser source, tests, and design documents reviewed. Seven technical findings identified. |
| Wave 2a | [11111ad](https://github.com/jensen-117/norse_game/commit/11111ad68613f77afd71b2c288411a1fa66062a8) | Compared with immediate parent Wave 1b, `90fb5d1b7953e718f0675a73c0cc3294fb0889c1`. Behavior preservation passed; compiler coverage had exceptions. |
| Wave 2b | [8a7afee](https://github.com/jensen-117/norse_game/commit/8a7afee433626c3fe532d618f2c95f73a219e035) | Legacy compatibility passed; four new grammar findings identified. Earlier runtime findings rechecked for this rollup. |

All source links below are pinned to Wave 2b unless expressly marked historical. Later commits are outside this report. Open means no fix has been verified, not that no developer may be working on it.

Evidence levels are distinguished throughout: executed reproduction, source/packaging inspection, architectural concern, or design hypothesis. Python checks ran against repository sources loaded in memory. Browser playback was exercised in a JavaScript harness; committed browser recordings were replayed natively. This was not a fresh visual browser playtest, accessibility audit with assistive technology, or completed expedition playtest.

### Priority and action index

P1 means high-impact correctness or a prerequisite for the relevant next milestone. P2 means a confirmed defect or material concern to address in the next appropriate pass. A design P1 is a high-priority validation question, not a claim of a proven bug.

| ID | Priority | Finding | Status / evidence |
|---|---|---|---|
| C01 | P1 | Victory can kill a hero before stabilization | Closed (be4118b) |
| C02 | P1 | Old playback callbacks can commit a new fight | Closed (a4f7c23) |
| C03 | P1 | Fresh checkout lacks reproducible Lab runtime setup | Closed (fe9e76e) |
| C04 | P2 | Flurries bypass Shatter | Closed (a0bb56f) |
| C05 | P2 | Death can preserve a wind-up through revival | Closed (762ac97; reopened once) |
| C06 | P2 | Transformation leaves knowledge under the old identity | Closed (a0bb56f) |
| C07 | P2 | Encounter generation mishandles family constraints | Closed (a0bb56f) |
| C08 | P1 | Ur promotion reverses the cost ladder | Closed (64da699) |
| C09 | P2 | Accepted All variants do not have consistent executable targeting | Closed (64da699) |
| C10 | P2 | Duplicate manners bypass exact capstone recipes | Closed (64da699) |
| C11 | P2 | Heavy healing pays penalties without its power benefit | Closed (64da699) |
| A01 | P2 | Compiler coverage and completeness contract remain unclear | Closed (64da699) |
| A02 | P2 | Modifier validation and speed-conflict policy need definition | Closed (64da699) |

## Confirmed technical findings

### C01 — Winning can kill a hero before victory stabilizes them

**Priority / context:** P1. Present before Wave 2a; reproduced again at 2b. This affects battle outcome and persistent party condition.

**Bug and cause:** `commit()` calls `end_round()` before `next_round()` checks whether combat has ended. `end_round()` removes breaths. Victory stabilization occurs later in `finish()`, after a hero with one remaining breath has already become Dead.

**Reproduce:** Create a level-30 Ullar and Vasara using seeds 1 and 2. Give a level-30 Spear Drattr 1 HP and a Defend action. Give Vasara a Crush strike with power 10,000. Construct the battle with seed 3, down Ullar before `begin('party')`, and set its breaths to 1. Submit Vasara's attack on `e0` and commit. The observed outcome is `winner == 'party'`, Ullar `state == 'dead'`, and no stabilization event. The reproduction uses the public begin/submit/commit sequence after arranging the fixture.

**Why it matters:** A player wins the rescue window but still loses the hero. It contradicts the explicit victory/flee stabilization behavior and can distort run attrition and death statistics.

**Suggested fix and rationale:** Make terminal outcome settlement an explicit phase shared by normal and bonus-round completion. Once a terminal outcome is established, stabilize eligible survivors before any timer that applies only to ongoing combat. Keep the order of effects documented rather than adding an exception for a particular hero or final attack. Decide separately how simultaneous end-of-round damage and defeat should work; do not accidentally change that rule through a blanket early return.

**Close when:** Last-breath victory stabilizes correctly; an ongoing fight still loses breaths; flee and bonus-round victory obey the same policy; already Dead heroes are not revived by stabilization; finishing twice cannot emit duplicate rewards or terminal events.

**Source:** [engine.py:1411–1452](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L1411-L1452).

**Resolution (Nov 20, commit [be4118b](https://github.com/jensen-117/norse_game/commit/be4118b)): Closed.**
- **Cause:** confirmed as described: `commit()` ran `end_round()` (which takes breaths) before `next_round()` noticed the fight was over and `finish()` stabilised the Dying.
- **Fix:** `commit()` settles the outcome as soon as a phase leaves the party victorious or fled (`party_settles()`), before any end-of-round timer; `finish()` is idempotent (a second call does nothing). Defeat and draw keep the old order, so the rule for a wiped party is deliberately unchanged (the review's caution about simultaneous defeat).
- **Verification:** `test_checkpoint.py` `C01_VictorySettlesFirst`: last-breath victory stabilises (Wounded, one `stabilised`, one `end`, a second commit adds nothing); an ongoing fight still loses a breath; a fled fight obeys the same rule; the Dead stay dead. 154 tests; page check (48 Auto fights) clean and replayed natively.
- **Fingerprint change, explained:** 29 of 288 fights differ, all party wins with the same rounds, differing only in `breath`/`dead`/`stabilised` events; 11 heroes who used to die after victory now stabilise. New baseline `sim/checks/fp_c01.sha1`.
- **Limits:** the Bonus Round path shares the same settle point (covered by the code path, not a separate fixture).

### C02 — Playback from an old fight can advance a new fight

**Priority / context:** P1 before further browser playtesting. Reproduced in a JavaScript harness at 2b.

**Bug and cause:** Automatic playback schedules an untracked callback that later calls the current global Lab battle. Starting another fight replaces that battle but does not invalidate pending callbacks or asynchronous playback. `onState()` also re-enables start controls before a scheduled continuation runs. Autopilot has another delayed commit path.

**Reproduce:** Queue an Auto continuation for fight A with a fake timer. Switch Auto off and present a new declaration state for fight B before firing that timer. Fire A's callback. In the harness, one old timer remained; it called `commit` once against B and changed B to the returned terminal state. No user command for B caused that commit.

**Why it matters:** UI animation can change the wrong battle, overwrite presentation state, or advance play without the player's decision. This also makes browser recordings less trustworthy during rapid restarts.

**Suggested fix and rationale:** Give each fight/playback session a generation token. Capture it in callbacks and check it after every awaited animation before touching state or issuing commands. Track and cancel timers on restart; use the same invalidation for Auto, autopilot, and manual playback. Share a single session/playback state with outer controls. Cancellation alone is insufficient for callbacks already running, while disabling a button alone does not protect programmatic restarts.

**Close when:** Starting B during any wait in A prevents all subsequent A commands and state writes; normal playback and speed-zero playback still complete; repeated restarts leave no live continuation from a retired session.

**Sources:** [screen.js:775–798](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L775-L798), [827–849](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L827-L849), [930–935](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L930-L935), [index.html:310–326](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/index.html#L310-L326).

**Resolution (Nov 20, commit [a4f7c23](https://github.com/jensen-117/norse_game/commit/a4f7c23)): Closed.**
- **Cause:** confirmed in a real browser: Auto playback's continuation was a bare `setTimeout` that called the current global battle; starting fight B didn't retire fight A's pending continuation, which then committed against B (B refused for missing orders, and A's playback crashed: three page errors).
- **Fix:** playback sessions in `screen.js`: `later()` schedules continuations that drop themselves if a newer fight has started; `play()` checks `live()` after every await; a retired session's `sleep()` never resumes, so no stale animation writes into the new fight; `begin()` retires the old session and clears its timers; a refused commit is reported instead of crashing. Auto, autopilot and manual playback use the same rule. (Outer controls still re-arm at `onState`: starting a new fight then is allowed, and now safe.)
- **Verification:** `sim/checks/s_c02.py` (Playwright): four restarts during A's pending continuation leave B at round 1 awaiting orders with no commits and no page errors; a whole Auto fight at fast speed plays to the end; the 48 instant-speed Auto fights still run and replay natively.
- **Limits:** tested with real timers in Chromium, not with every animation path individually; the generation check covers them by construction.

### C03 — A fresh checkout cannot launch the Fight Lab as supplied

**Priority / context:** P1 for reproducible handoff. Confirmed by source and committed-tree inspection, not a fresh browser boot.

**Bug and cause:** The page requires `py/pyodide.js` and `py/stdlib.json`. The runtime directory is ignored and absent from the committed tree. The custom packaging is described, but no committed bootstrap procedure reconstructs all required artifacts. This does not establish that the separately published Lab is broken.

**Reproduce:** Obtain the pinned tree without untracked local assets and serve `fight_lab/` over HTTP. Inspect the script reference and `boot()` fetches: the required runtime paths are absent. Startup cannot reach rule loading using those files alone.

**Why it matters:** Another developer or agent cannot reproduce the claimed page checks from the repository. Local assets can silently become part of the build contract.

**Suggested fix and rationale:** Add a version-pinned preparation command, a manifest of runtime inputs, and a short launch guide. Generate the custom standard-library package deterministically, and verify downloaded inputs with checksums. Keeping generated runtime files ignored is reasonable if setup can recreate them. Use the same preparation path for local development and publication to avoid two packaging implementations.

**Close when:** A clean checkout can prepare and serve the Lab using only documented commands; an automated smoke check reaches the ready state and executes a fight; no pre-existing runtime directory is needed.

**Sources:** [.gitignore:9–10](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/.gitignore#L9-L10), [index.html:118](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/index.html#L118), [167–189](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/index.html#L167-L189).

**Resolution (Nov 20, commits [fe9e76e](https://github.com/jensen-117/norse_game/commit/fe9e76e), [e2d9507](https://github.com/jensen-117/norse_game/commit/e2d9507)): Closed.**
- **Cause:** confirmed: `fight_lab/py/` was ignored and nothing in the repository could rebuild it; `stdlib.json` was a hand-curated subset with no recorded rule.
- **Finding while fixing:** the four runtime files are byte-identical to the npm release of Pyodide 0.26.4; `stdlib.json` is 296 of the 516 files in its `python_stdlib.zip`, in zip order, as compact JSON, and can be rebuilt byte for byte.
- **Fix:** `fight_lab/runtime_manifest.json` pins the version, the npm tarball and its published sha512 integrity, the 296 stdlib file names, and the SHA-256 of every output. `tools/prepare_lab.py` (plain Python, no npm) fetches the tarball, refuses it unless the integrity matches, extracts the runtime, rebuilds `stdlib.json` from the manifest, and verifies every checksum; `--check` verifies without fetching. `fight_lab/README.md` is the launch guide (and states that publishing uses the same files). `sim/checks/s_smoke.py` serves a folder itself, boots to Ready and plays one Auto fight. `py/` stays ignored, as the review allows, because setup recreates it.
- **Verification:** a clean clone (no `py/`, empty download cache) prepared only with the documented command matched every checksum, booted to Ready and played an Auto fight to the end. Also added `sim/test_lab_parity.py`: every module the page loads matches `sim/` (review step 3).
- **Limits:** needs network access to registry.npmjs.org on first run; Playwright and Chromium for the smoke check. The stdlib list is now explicit data: a new import in the sim must be added to it (README says how).

### C04 — Flurries bypass Shatter

**Priority / context:** P2. Existing combat inconsistency, reproduced at 2b.

**Bug and cause:** Ordinary attacks consume a shatterable status and multiply damage. The separate `flurry → hit_once` path does neither.

**Reproduce:** Create a level-30 Ullar and Spear Drattr, raise the target's HP to 10,000, and apply Frozen. Resolve one Drif Skott flurry hit. Frozen remains. Under the ordinary attack path, Frozen is removed and a `shatter` event is emitted. The 2b recheck applied Frozen using `apply_status` rather than constructing obsolete status fields.

**Why it matters:** The tactical choice to preserve a freeze or cash it in depends on attack implementation rather than the stated rule. More attack variants will compound this divergence.

**Suggested fix and rationale:** Extract a shared per-hit effect step for status consumption and relevant damage modifiers. Ordinary attacks, split hits, and flurries should call it while retaining their distinct sequencing and rider rules. Specify which hit consumes Frozen and how null/absorb interacts with it. A small shared function is sufficient; a generalized event framework is not necessary to solve this.

**Close when:** Ordinary, split-hit, and flurry attacks follow the same specified Shatter policy, consume the status the intended number of times, and emit the corresponding event. Include null/absorb and multi-target cases.

**Sources:** [engine.py:898–926](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L898-L926), [950–962](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L950-L962), [988–1008](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L988-L1008).

**Resolution (Nov 20, commit [a0bb56f](https://github.com/jensen-117/norse_game/commit/a0bb56f)): Closed.**
- **Cause:** confirmed: Shatter lived inline in the plain hit loop; the flurry path (`hit_once`) had no Shatter step.
- **Fix:** `Battle.shatter()` is one per-hit step called by plain hits, multi-hits and flurries: the first hit that actually deals damage, not nulled and not absorbed, ends Frozen for its multiplier, once. Sequencing and riders stay path-specific.
- **Decision applied:** a nulled or absorbed hit doesn't shatter (it used to on the plain path) (Joseph, Nov 20).
- **Verification:** `C04_OneShatterRule`: a three-hit flurry shatters once; a three-hit plain move shatters once; null and absorb don't shatter on either path. The fingerprint (288) and regress.py (480) are identical: none of their fights flurries into, or nulls onto, a frozen target.

### C05 — Death does not immediately cancel a wind-up

**Priority / context:** P2. Existing lifecycle defect, reproduced at 2b. Whether entering Dying should also interrupt a wind-up is a separate design decision.

**Bug and cause:** `die()` leaves `bide` intact. Planning discards a wind-up only if its owner is still not alive at that later moment. Revival before planning therefore restores eligibility for an action begun before death.

**Reproduce:** Put a Bid Skott and its target in an Ullar's `bide` field. Call `die(hero, 'probe')`, then `stand_up(hero, .2, True)`, then `plan_phase([hero, enemy], False)`. A `_release` action is queued for the revived hero.

**Why it matters:** Death interruption depends on event ordering, permitting an old charged attack to survive a supposedly terminal transition.

**Suggested fix and rationale:** Centralize interruption of pending actions at state transitions. Death should call that operation and emit the appropriate loss event. Make Dying, stun, transformation, and other interrupt causes explicit policies as they are needed. This avoids duplicating cleanup across future revive moves or relying on the next planning pass to notice a past death.

**Close when:** Death followed by immediate revival cannot release the old charge; interruption is recorded once; a hero that survives uninterrupted still releases normally. Document and test the chosen Dying policy.

**Sources:** [engine.py:616–618](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L616-L618), [1304–1310](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L1304-L1310).

**Resolution (Nov 20, commit [a0bb56f](https://github.com/jensen-117/norse_game/commit/a0bb56f)): Closed.**
- **Cause:** confirmed: `die()` left the wind-up in place; only the next planning pass dropped it, and only if its owner was still down.
- **Fix:** `Battle.interrupt()` ends a pending wind-up at the state change, with one `bide_lost` event (why: fell or dead). `die()` calls it, and so does `downed()` for every fall: a hero to Dying, a Draugr crawling, a Bein pile, a Mogel re-forming. Planning no longer has anything to catch.
- **Decision applied:** falling to Dying interrupts a wind-up immediately (Joseph, Nov 20).
- **Verification:** `C05_FallingEndsAWindUp`: death then revival can't release (one `bide_lost`); falling to Dying ends it; an unbroken wind-up still releases. Fingerprints identical (no wind-up owner falls mid-charge in those fights).
- **Limits:** Stun, Frozen and the net still break a wind-up at release time, as before; transformation doesn't (no transforming unit winds up today).

**Reopened (Nov 20, re-review at a280256): Closed again (commit [762ac97](https://github.com/jensen-117/norse_game/commit/762ac97)).**
- **What the first fix missed:** planning moves a charge from `u.bide` into the round's queue and clears `u.bide`; `interrupt()` checked only `u.bide`, so a unit that fell after planning still released. The re-review's fixture: a charged Draugr fell, crawled on, and fired its old Bidskott for 53 damage with no `bide_lost` (60 in this checkout's fixture).
- **Fix:** an action-generation token, as the re-review recommended. Planning gives each queued release a fresh token held on the unit (`u.charge`); `interrupt()` clears both the stored wind-up and the queued token, with one `bide_lost`; a release fires only while it holds the unit's current token. A Mogel re-forming replaces the unit's state, so its token changes too. No entry is removed from the resolver's local queue.
- **Verification:** `C05_FallingEndsAWindUp` adds `test_a_fall_after_planning_cancels_the_queued_release` (the Draugr fixture: no damage, one `bide_lost`) and `test_a_hero_falling_after_planning_loses_the_release`; `test_an_unbroken_wind_up_still_releases` now also checks the hit lands with no `bide_lost`. `test_drattr`'s net test builds its release as planning does. Golden, fingerprint and regress.py identical (no fight in those sets falls between planning and release); page check clean.

### C06 — Transforming enemies learn under the wrong identity

**Priority / context:** P2. Reproduced at 2b.

**Bug and cause:** Drattr transforms from Net to Spear, but `Memory.observe()` does not update its UID-to-identity mapping on `transform`. Later observations remain filed under the Net key while Inspect requests Spear knowledge.

**Reproduce:** Start a battle against a Net Drattr and pass the start events to `Memory.observe()`. Transform it to Spear, hit it with Skott, and observe the resulting events. Inspect the transformed enemy through `Memory.mask()`. Pierce still appears as `?`, despite the hit having recorded its affinity under the old identity.

**Why it matters:** Players can discover information that the interface then hides. The stale mapping also affects which identity receives subsequent kill credit.

**Suggested fix and rationale:** Treat identity changes as explicit events consumed by knowledge, presentation, and replay. Include the new knowledge identity in the event, or derive it through one shared identity function. If some knowledge should transfer across jobs, define that sharing per property rather than merging all jobs unconditionally; future transformations may genuinely change affinities.

**Close when:** Post-transformation hits reveal the current identity's affinity, kills use the intended identity, pre-transformation knowledge remains intact, and save/reload preserves the results. Recheck existing reform/crawl behavior.

**Sources:** [engine.py:973–981](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L973-L981), [knowledge.py:25–65](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/knowledge.py#L25-L65).

**Resolution (Nov 20, commit [a0bb56f](https://github.com/jensen-117/norse_game/commit/a0bb56f)): Closed.**
- **Cause:** confirmed: `Memory.observe()` mapped each unit to its identity at the start and never read `transform`.
- **Fix:** `transform` events (which carry the new job) update the unit's identity in `Memory`: what's learned afterwards files under the new job, what was learned before stays under the old one, nothing is copied across, and kill credit goes to the job it fell as.
- **Decision applied:** no knowledge sharing across jobs for now; sharing can come per property later (Joseph, Nov 20).
- **Verification:** `C06_KnowledgeFollowsTheJob`: after Net becomes Spear, a Slash hit shows on the Spear's sheet; the Net keeps its Pierce entry and gains nothing; save and reload keep the record; the kill counts for the Spear. Reform and crawl handling are unchanged (they already updated or kept identity).

### C07 — Encounter generation does not reliably enforce family constraints

**Priority / context:** P2; fix before authored routes rely on these constraints. Reproduced at 2b.

**Bug and cause:** Feasibility considers costs and unit count but not all remaining family requirements after a candidate is selected. If a required family is absent, the minimum-family filter falls back to the unrestricted pool, allowing an invalid result.

**Reproduce:** Use two entries: A costs 1, B costs 2; both have weight 1 and `ranged=False`. With budget 2 and `family_max={'A': 1}`, seeds 1 and 2 raise `CompositionError` even though B alone satisfies the constraints. With only B available and `family_min={'A': 1}`, seed 1 returns B instead of rejecting the impossible requirement.

**Why it matters:** Feasible authored encounters can fail depending on randomness, and impossible encounters can silently violate their design constraints.

**Suggested fix and rationale:** Include remaining family minima/maxima in the feasibility state, or use bounded backtracking over complete candidate choices. Reject unavailable requirements explicitly. Validate every completed pack against the full rule set. Given small encounter sizes, favor a simple correct solver with memoization if needed over a greedy special case for each new restriction.

**Close when:** Every returned pack satisfies all declared rules; feasible small pools do not fail due to an unlucky first choice; impossible requirements raise a useful error. Compare generated small cases with exhaustive enumeration, including cost caps, family caps, minima, unit limits, and ranged requirements.

**Source:** [composer.py:112–181](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/composer.py#L112-L181).

**Resolution (Nov 20, commit [a0bb56f](https://github.com/jensen-117/norse_game/commit/a0bb56f)): Closed.**
- **Cause:** confirmed: the feasibility check counted costs and units but not family rules, and a missing minimum fell back to the open pool.
- **Fix:** `_feas()` (memoized) decides whether a pack can still be finished under the cost caps, the unit limit and the family maxima and minima; `compose()` offers only cost faces and units that keep it finishable, refuses impossible minimums up front, and never falls back to the open pool. Without family rules it takes exactly the old path, so existing packs roll identically.
- **Verification:** `C07_PacksKeepTheirRules`: the review's two cases (B alone under family_max A=1; an impossible family_min raises); and 300 generated small problems (127 legal, 173 impossible, with costs, caps, bans, unit limits and family rules) compared with exhaustive enumeration over 3 seeds each: every returned pack is legal and every refusal is truly impossible. The old composer fails both tests. Fingerprints identical.
- **Limits:** the ranged rule still re-rolls (tries) rather than solving; it isn't a family rule and wasn't in the finding.

### C08 — Advancing to Ur can make a stronger spell cheaper

**Priority / context:** P1 before the new grammar feeds playable kits or mutation rewards. New in the reviewed 2b path; not a legacy-kit regression.

**Bug and cause:** Tier promotion can reach Ur, including indirectly from a verb whose native tier is Mer. `TIER_WEIGHT` omits Ur, and pricing silently defaults its weight to zero.

**Reproduce:** Call `compile_verb('Storm')`, then with `tier='Mer'`, then `tier='Jatte'`:

| Input | Effective tier | Power | MP share |
|---|---|---:|---:|
| Storm | Mer | 28 | 0.16 |
| Mer + Storm | Jatte | 38 | 0.256 |
| Jatte + Storm | Ur | 50 | 0.10 |

Orkan similarly moves from 0.256 to 0.4096 to 0.16. Passing `tier='Ur'` also produces the underpriced result.

**Why it matters:** A stronger upgrade can be cheaper than the original move, undermining progression, reward value, and balance. The public compiler also allows the ordinary upgrade path to cross a tier described as gear-only.

**Suggested fix and rationale:** Represent tier power, rank, price weight, and availability explicitly. Validate the effective destination tier against the move's acquisition context; ordinary carving must not gain gear-only access by promotion arithmetic. When Ur is authorized, use an explicit pricing policy, not a missing-key fallback. Retain separate policies for carved moves, gear grants, fixed items, and authored enemy costs where those intentionally differ.

**Close when:** Ordinary upgrades cannot directly or indirectly acquire restricted tiers; authorized Ur has deliberate pricing; increasing an otherwise equivalent tier cannot reduce its price unless an explicit, tested design exception says so. Cover every native verb tier, not just Base-root spells.

**Sources:** [words.py:172–206](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L172-L206), [data.py:619](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/data.py#L619).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Cause:** confirmed: tier promotion was arithmetic on the ladder with no limit, and `TIER_WEIGHT` had no Ur, so its price fell back to zero.
- **Fix:** `normalize()` checks the tier part against the move's source (`SOURCE_TIER`: carving adds Mer, finding Jatte, gear Ur), and refuses any result of Ur unless the source is gear, so promotion can't reach a gear-only tier. Ur has an explicit price weight (3). A rung still climbs from the verb's own (Merorkan: Orkan is Mer, so Jatte), as classes.md requires.
- **Decision applied:** carving reaches Mer, finding Jatte, only gear Ur (Joseph, Nov 20).
- **Verification:** `C08_TierAccessAndPrice`: Storm + Jatte is refused unless from gear; a Jatte part can't be carved; for **every verb, tier and source**, an accepted part never exceeds its source and Ur appears only from gear; for every verb, a higher tier never costs less.
- **Limits:** acquisition context is a parameter the caller passes (`source`); the reward and carving code that will pass it arrives with the dive.

### C09 — Accepted All variants can affect only the caster or do nothing

**Priority / context:** P2; resolve before exposing these combinations to players. Full-turn reproductions at 2b.

**Bug and cause:** The compiler sets `all=True` but retains the verb's original target category. Self targeting overrides All, while revive still depends on an individually chosen target. There is no validation that the requested target modification is supported by the verb and resolver.

**Reproduce:** Put `compile_verb('Aukseid', target='All')` on a hero, price it, and submit it in a three-hero battle. MAT stages become `[1, 0, 0]`. Separately compile `Vakna` with `target='All'`, put an ally into Dying, and submit the action with the All aim supplied by the interface. The ally stays Dying, no revive event occurs, and the action produces no revival. In that probe no MP was spent, but the turn was consumed.

**Why it matters:** Names, accepted recipes, costs, and actual targeting disagree. A move that compiles successfully can waste an action or charge for a nonexistent upgrade.

**Suggested fix and rationale:** Define target eligibility and target scope separately—for example, eligible allies versus a single, row, or all selection. Use the resulting target specification consistently in menus, legal-target queries, AI, and resolution. Declare allowed target modifications per verb or capability. If group revival or expanding self buffs is not yet designed, reject it explicitly rather than adding ad hoc exceptions inside the resolver.

**Close when:** Every allowed target modifier executes on the declared set; unsupported modifiers fail compilation with a clear reason; already-All moves cannot purchase a redundant All upgrade without an explicit effect. Include no-eligible-target and dead-versus-dying cases.

**Sources:** [words.py:180–185](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L180-L185), [engine.py:695–703](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L695-L703), [1473–1482](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L1473-L1482).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Cause:** confirmed: All set `all=True` without checking that the verb or the resolver supports it; self targeting returned before scope was read.
- **Fix:** each verb lists the target parts it may take (`VERBS[...]["targets"]`, from classes.md); anything else is refused at compile, including All on a move that already reaches everyone. Eligibility (self, ally, enemy, fallen) and scope (one, row, all) are separate: a self move's row and All scopes resolve in `targets_for`. Aukskold's own target is now herself, as classes.md says (it was one ally).
- **Decision applied:** per-verb targets from classes.md; a group revive and a self buff turned party-wide stay out until designed (Joseph, Nov 20).
- **Verification:** `C09_TargetsDoWhatTheySay`: All on Aukseid, Vakna, Byr, Kvad, Knyta, Egga and Lya is refused; Aukskold reaches herself, her row, or everyone in real turns; an All Lak heals every ally in a real turn.
- **Limits:** which target parts each verb accepts is provisional data until the mutation session.

### C10 — Duplicate manners bypass exact capstone recipes

**Priority / context:** P2. Executed compiler reproduction at 2b.

**Bug and cause:** Capstone lookup converts parts to a `frozenset`, which removes duplicates, while the part count and price still include them.

**Reproduce:** `compile_verb('Skott', tier='Mer', manners=('Drif', 'Drif'), lonn=True)` is accepted as Tusensplitter. It has four carved parts and an HP share of 0.140625. The ordinary three-part recipe costs 0.09375. The duplicate Drif does not provide a second flurry benefit.

**Why it matters:** The cap is not checking the same recipe that pricing and effect merging consume. Invalid recipes receive valid capstone identities and misleading prices.

**Suggested fix and rationale:** Normalize and validate the parts once, then pass that representation to cap checking, naming, effect assembly, and pricing. If manners are nonrepeatable, reject duplicates. If repetition is allowed for future mechanics, use a multiset or ordered representation as appropriate. Do not silently deduplicate only during capstone matching.

**Close when:** Exact named recipes compile; duplicate and surplus parts fail unless explicitly supported; equivalent allowed orderings produce the intended result; names, cost counts, and effect counts all agree.

**Source:** [words.py:155–170](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L155-L170).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Cause:** confirmed: capstone lookup used a set (which drops repeats) while the count and price used the list.
- **Fix:** `normalize()` refuses repeated manners; the cap, capstone and byname lookup, effects and price all read one canonical part list (`verb_parts`).
- **Verification:** `C10_RecipesAreExact`: a double Drif is refused; the exact Tusensplitter recipe compiles; a surplus part is OverCap.

### C11 — Heavy healing receives the penalty without the power benefit

**Priority / context:** P2. Full-turn comparison at 2b. The precise healing multiplier is a design choice; accepting a paid, penalized modifier with no defined benefit is the problem.

**Bug and cause:** `merge_manners()` calculates a power multiplier, but the heal branch assigns only `TIER_POWER[eff]`. Damage and Styng use the multiplier. Bidlak has the same omission in its compiled healing power.

**Reproduce:** Compare `compile_verb('Lak')` and `compile_verb('Lak', manners=('Tung',))` in otherwise identical seeded battles, with a sufficiently wounded ally and a caster whose maximum MP is 100. Both heal 58.964919 HP in the review fixture. Lak costs 6 MP; Tunglak costs 10 and executes in group -2, Heavy. Both compiled powers are 20.

**Why it matters:** Players can spend an upgrade and more MP for a strictly worse version of the same heal. It also breaks the expectation that manner composition has a consistent meaning.

**Suggested fix and rationale:** Define modifier applicability in terms of effect capabilities, such as scalable damage or scalable healing. Apply a documented healing benefit where intended, or reject the manner on heals. Do not blindly multiply every numeric field—revive fractions, status stacks, and movement distance may need different policies. One explicit applicability rule can support future effect kinds without silently doing nothing.

**Close when:** Accepted Heavy/Patient healing has the designed payoff in actual turns, with correct cost and timing; rejected combinations fail before being offered as rewards. Include combinations with multiple manners and distinguish output-power checks from end-to-end healing checks.

**Source:** [words.py:175–188](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L175-L188).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Cause:** confirmed: the heal branch took the tier's power and ignored the manners' multiplier.
- **Fix:** damage, answers and heals all scale with manners (`SCALES`); each manner states what it needs (`MANNER_NEEDS`): Heavy and Patient need a scalable effect, Reckless and Flurry need hits, so they're refused on heals and status moves.
- **Decision applied:** manners scale healing like damage (it enables the Heavy "prayer" heal); crits and flurries don't apply to heals (Joseph, Nov 20).
- **Verification:** `C11_ManneredHeals`: in real turns, Tunglak heals exactly 1.2x Lak, costs more, and acts Heavy (-2); Jarf and Drif on Lak are refused.
- **Limits:** a Patient heal's release is covered by the shared wind-up path, not by its own end-to-end fixture.

## Architecture and contract findings

### A01 — Compiler consolidation still has exceptions and an incomplete public contract

**Priority / evidence:** P2. Identified during 2a and rechecked at 2b. This is a coverage and maintenance concern, not evidence that the extraction changed existing gameplay.

**Observed behavior:** Non-revive items, including Firecracker, still construct moves with `act()` directly. Enemy Net Throw also bypasses `compile_move`; attempting to compile Bound through that API raises `KeyError`. Enemy splitting, flurry attachment, and authored overrides are applied afterward in `family_move()`. Wave 2b adds `compile_verb()`, which also assembles through `act()` rather than through `compile_move()`.

**Reproduce:** Instrument `engine.compile_move` while calling `damage_spell('Eld', 'Base')`, `item_move('firecracker')`, and `family_move(('status', 'Bound', 'Base', dict(name='Net Throw', once=True, sure=True, thrown=True)))`. The observed call counts are 1, 0, and 0. A direct `compile_move('revive', 'Vakna', 'Base')` lacks `hp`, `reaches`, and `wound`; the legacy `vakna()` wrapper supplies them.

**Why it matters:** A future rule added to one compiler path may not reach items, enemies, or class verbs. A caller cannot tell whether the returned dictionary is an executable move or a partial intermediate representation. Wrapper-versus-compiler equality tests cannot detect a mistake shared by both.

**Suggested fix and rationale:** Establish one documented executable move contract and a shared final validation/lowering boundary. Multiple input adapters are reasonable: old builders, class grammar, items, and authored enemy moves have different inputs and pricing needs. They need not all be forced through the player grammar API. A complete move should contain every required runtime field; alternatively, label partial specifications distinctly and require explicit finalization before use. Keep origin-specific prices and overrides explicit, especially fixed item effects and enemies that never pay HP.

This allows extensibility without requiring one enormous compiler function. Simple typed records, small validators, and explicit adapters are enough; a plugin framework or a large class hierarchy would be premature.

**Close when:** Every executable move path reaches the shared contract check, or a documented intentional exception has equivalent checks. Direct public APIs either produce complete executable moves or clearly return specifications requiring finalization. Representative items, enemies, revives, legacy grammar, and class verbs all have independent expected-behavior checks.

**Sources:** [engine.py:17–30](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L17-L30), [1704–1755](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/engine.py#L1704-L1755), [words.py:122–132](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L122-L132), [160–210](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L160-L210).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Fix:** the move contract lives in `words.py`: `check_move()` (the fields every move and each kind needs) and `unresolved()` (a kind or effect the engine can't yet carry out: Wave 4 kinds, Wave 4 fields, statuses with no row). `finalize()` applies both and is the last step of `compile_move`, `item_move` and `family_move`; class verbs are checked in `compile_verb` and carry their `unresolved` list. `compile_move("revive", ...)` is complete on its own. **Battle refuses any move that breaks the contract or isn't resolvable yet**, so a compiled but unfinished move can't enter a playable kit.
- **Adapters kept on purpose:** items keep fixed powers, enemies never pay HP, class verbs price as shares; each is a separate input adapter meeting the same contract (the review's recommendation).
- **Verification:** `A01_OneContract`: every item, Net Throw, a bare compiled revive and every kit move meet the contract; Kvad (a Wave 4 kind) compiles but a Battle with it is refused. The legacy golden (4,535 moves) is identical.
- **Limits:** Wave 4 must remove each kind and field from the unresolved lists as it implements them, with a full-turn test for each.

### A02 — Modifier validation and speed-conflict semantics need a clear policy

**Priority / evidence:** P2. Accepted-input probes at 2b. Some behavior is demonstrably permissive; whether order-dependent speed is intended remains a design question.

**Reproduce and observe:**

- `compile_verb('Eld', target='Bogus')` succeeds as Boguseld, charges a 0.10 MP share, and remains a single-target attack.
- Adding All to Byr, which already targets all allies, increases its share from 0.0625 to 0.10 without expanding its target set.
- `manners=('Snar', 'Tung')` yields group -2, while `('Tung', 'Snar')` yields group 1. Both use the combined power multipliers and the same price; the last speed group wins.

**Why it matters:** Unknown parts and redundant upgrades can enter the content pipeline. Order-sensitive combination behavior can be deliberate, but it must be a rule designers and players can predict rather than an incidental dictionary overwrite.

**Suggested fix and rationale:** Declare valid part values, applicability, repetition, and conflict rules in the grammar data or a small validation layer. Keep legitimate ordered combinations such as Patient + Heavy. For competing speed manners, explicitly choose rejection, precedence, or an ordered transformation rule and expose that meaning in descriptions. Validate authoring data and player mutation choices through the same policy.

**Close when:** Unknown targets fail clearly; redundant modifiers are rejected or have an explicit benefit; speed conflicts have documented expected results and permutation tests. This work should share the normalization used for C09–C11 rather than introduce a second set of legality rules.

**Source:** [words.py:141–206](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L141-L206).

**Resolution (Nov 20, commit [64da699](https://github.com/jensen-117/norse_game/commit/64da699)): Closed.**
- **Fix:** `normalize()` refuses unknown targets, tiers and manners; refuses Swift with Heavy in either order; refuses redundant parts (Swift on a First move, Patient on an already Patient move, All on a move that reaches everyone). Patient with one speed manner stays legal and is order-free: it releases in that manner's group.
- **Decision applied:** Swift + Heavy refused as contradictory; Patient + one speed manner legal (Joseph, Nov 20).
- **Verification:** `A02_ModifierPolicy`: unknown parts, Swift + Heavy both orders, and redundant parts are refused; Bid + Tung and Tung + Bid give the same release group and price.

## Game-design findings and validation questions

These are decisions and experiments, not all confirmed defects. They should be resolved at the milestone where the relevant systems can be played. Preserve the central party-synergy identity while testing whether it remains enjoyable across a run.

### D01 — Prove one connected leg before expanding content

**Priority / context:** P1 validation milestone after essential class functionality. Independent fights cannot establish persistent attrition, reward usefulness, or the Rest-versus-Carve tradeoff.

**How to evaluate:** Build one seven-column leg using the actual starting trio, a small mutation pool, optional elite, camp, and boss. Carry party resources and permitted state between rooms. Run identical route/reward seeds with multiple policies and observe human play.

**Risk:** A combat system that works in isolation may produce an expedition dominated by compulsory recovery, irrelevant rewards, or a single safe route.

**Recommendation and rationale:** Instrument completion, HP/MP trajectory, deaths, chosen rewards, unused rewards, Rest/Carve decisions, and elite participation. Tune a small complete loop before multiplying encounters and reward content. Keep route and reward data replaceable so the experiment does not hard-code one ideal party.

**Completion evidence:** A playable leg demonstrates meaningful routing and mutation choices at the intended difficulty, with failed runs explainable by decisions and encounter pressure rather than hidden resource traps.

**Source:** [dive_spec.md:18–27](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/dive_spec.md#L18-L27).

### D02 — Protect healer-free viability

**Priority / context:** P1 balance question. The starting trio lacks Dagskald; martial skills consume the same HP that funds expedition survival.

**How to evaluate:** Compare the starting trio and healer substitutions across identical route and reward seeds. Measure not only wins but skill use, camps required, Carve opportunities, and remaining resources.

**Risk:** A healer may become an economic necessity instead of an interesting alternative, or martial characters may be discouraged from using their defining techniques.

**Recommendation and rationale:** Tune recovery opportunities and resource costs around explicit party-level targets. Preserve class differences; avoid hidden emergency subsidies tied to a particular party composition. Diagnose where the resource gap arises before changing global HP costs or healing strength.

**Completion evidence:** Competently played healer-free parties can finish the intended leg and sometimes choose Carve, while the healer changes risk and tactics without becoming compulsory.

**Sources:** [pillars.md:35–44](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/pillars.md#L35-L44), [69–82](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/pillars.md#L69-L82).

### D03 — Free recovery may reward stalling

**Priority / context:** P1 economy decision before final cost tuning. Free Halvlak healing is reproduced; a dominant expedition-wide stall strategy has not been established.

**Observed behavior:** A newly compiled Halvlak costs zero and restored 29.4824595 HP in the review fixture with the caster already at zero MP. This follows the stated free-Halv rule and is not a compiler defect. Planned Meditate, growing Song healing, and persistent Knots add further recovery considerations.

**How to evaluate:** Compare prompt victory with deliberately leaving a weak enemy alive while healing, recovering MP, or accumulating persistent resources. Measure net resources per extra turn, time added, and subsequent-room advantage. Include healer-free and healer parties.

**Risk:** Optimal play may require boring cleanup turns, undermining attrition, camps, and the pace target. A faster strategy should not be routinely punished for declining repetitive recovery.

**Recommendation and rationale:** Explicitly decide which effects are free under Halv and what bounds profitable recovery. Possible policies include finite recovery budgets, mounting encounter pressure, or carefully scoped restrictions. Choose after measuring, and express the policy consistently across recovery effects rather than patching each named spell. Do not remove free Halv attacks merely to solve a healing-specific problem.

**Completion evidence:** The intended recovery strategy is stated and tested; deliberate stalling does not dominate ordinary play unless that tradeoff is intentional and enjoyable. Check that any anti-stall rule does not make healer-free runs untenable.

**Sources:** [words.py:202–206](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L202-L206), [classes.md:120–125](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/classes.md#L120-L125), [157–160](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/classes.md#L157-L160).

### D04 — Define what voluntary return banks

**Priority / context:** P1 design clarification before implementing the extraction loop.

**Issue:** The dive promises returning home with loot, while the pillars reset run moves, gear, Omens, and the pouch. The concrete persistent payoff of an early return remains unclear in the reviewed specifications.

**How to evaluate:** Write down the retained rewards, unlocks, losses, and tapestry outcome for defeat, early return, and final victory. Apply those rules to one example run at each leg boundary.

**Risk:** Without a distinct banked benefit, continuing or returning may be an obvious choice rather than a meaningful gamble.

**Recommendation and rationale:** Define a small run-settlement contract before building screens or rewards around it. Keep reward retention policy separate from battle termination so future modes can share combat without sharing progression rules. This can be a concise data table; it does not require restoring the deferred city economy.

**Completion evidence:** A player can explain what is protected by returning and what is risked by continuing; all three outcomes produce consistent saves and visible summaries.

**Sources:** [dive_spec.md:20–27](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/dive_spec.md#L20-L27), [pillars.md:34–39](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/pillars.md#L34-L39).

### D05 — Make compound words readable when choosing moves and mutations

**Priority / evidence:** P2 UX concern from source inspection; unfamiliar-player comprehension has not been measured. The current menu clips long names and the detail card displays only a small portion of the description at once.

**How to evaluate:** Give unfamiliar players a basic move and two legal mutations. Ask them to predict target scope, timing, cost, and effect before acting, then compare their expectation with the outcome. Include Merstyngnaglskott and Patient + Heavy combinations.

**Recommendation and rationale:** Retain the spoken name, add a concise plain-language effect label, and show a clear before/after mutation comparison. Generate those descriptions from the validated move specification so UI text cannot drift from mechanics. Teach one modifier at a time rather than requiring grammar memorization at the first decision.

**Naming assessment:** Svedeld, Eitreyk, and Lonnsol read consistently within the established system. Merstyngnaglskott is long but consistent; retain it with a readable description. Do not create a capstone only to shorten a word, because capstones should communicate a special recipe or identity. Rider prefixes belonging to the verb is a sound representation: a shared status does not require one universal spoken prefix.

**Completion evidence:** Players can predict a move's behavior without decoding every morpheme, and long names remain inspectable without obscuring essential costs or targets.

**Sources:** [screen.js:648–674](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L648-L674), [words.py:177–200](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/words.py#L177-L200).

### D06 — Measure decision time and playback time separately

**Priority / context:** P2 pacing question. The proposed dive is about 15 fights in 45–60 minutes, with three heroes, bonus actions, inspection, and playback.

**How to evaluate:** Record active decision time, animation time, inspection frequency, repeated commands, and total session duration. Observe normal-speed human play rather than inferring duration from Auto fight round counts.

**Risk:** Even two- or three-round fights can create a slow run if each requires many repetitive interactions or lengthy presentation.

**Recommendation and rationale:** Preserve time for meaningful decisions and notable events; make familiar commands quick to repeat and ordinary playback easy to accelerate. Use event categories and player-controlled speed rather than hard-coding special animation delays for named moves. Ensure fast-forward uses the same command safety rules as normal playback (C02).

**Completion evidence:** The playable-leg measurements project to the intended session length without rushing important choices or making the battle unreadable.

**Sources:** [dive_spec.md:62](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/dive_spec.md#L62), [screen.js:42–58](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L42-L58).

### D07 — Complete keyboard targeting and accessible combat output

**Priority / evidence:** P2 before outside testing. Source inspection shows canvas hit regions and a keyboard handler that does not provide a complete target-selection path. This is an implementation gap, not a measured assistive-technology compatibility result.

**How to evaluate:** Attempt a complete fight without a pointer: choose a hero, inspect a move, select a target or board cell, cancel, confirm, and recover from an invalid choice. Separately check whether a nonvisual interface exposes current state and available actions.

**Recommendation and rationale:** Use a shared command/selection model for pointer and keyboard input, with visible focus and complete target navigation. Expose semantic controls or an accessible text representation alongside the canvas. Avoid maintaining an independent keyboard combat implementation that can diverge from the pointer rules.

**Completion evidence:** A player can complete the same legal actions by keyboard, focus is predictable, and essential state changes are available in text. Verify with real users and assistive technology when that interface exists.

**Sources:** [index.html:111–113](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/index.html#L111-L113), [screen.js:786–799](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/fight_lab/screen.js#L786-L799).

## Verified strengths and limits of the evidence

| Check | Independently observed result |
|---|---|
| Initial test suite | 124 unittest cases plus the standalone autofill/replay check passed. |
| Wave 2a test suite | 137 unittest cases plus the standalone check passed: 138 total. |
| Wave 2b test suite | 148 unittest cases plus the standalone check passed: 149 total. |
| Legacy move/kit preservation | All 4,535 cases matched across the 2a refactor; all matched again between 2a and 2b. |
| Expanded legacy grammar comparison at 2a | 12,600 successful outputs matched the parent, plus 840 matching rejections. This was not exhaustive coverage of the new 2b grammar. |
| Fixed-party fights | 288 fights; 2a and 2b matched the Wave 1b fingerprint. |
| Wider regression fights | 480 fights; 2a and 2b matched the Wave 1b result hash. |
| Browser recordings | All 48 committed Auto records replayed natively at each reviewed compiler checkpoint, matching results, rounds, log lengths/checksums, and engine identity. No fresh visual browser run was performed by the reviewer. |
| Lab source parity | Seven Python module copies matched at 2a; the three changed copies at 2b matched their simulation counterparts, with the other four unchanged. |
| Patient + Heavy meteor | A complete two-round Bidtungeld probe paid 16 MP from a 100-MP bar once, dealt no immediate damage, then released in Heavy with no second payment and dealt about 52.5761 damage in the fixture. |
| New spellings | Svedeld, Eitreyk, Lonnsol, and Merstyngnaglskott compiled exactly as reported. |

Recorded fingerprint identifiers:

| Baseline | 288-fight fingerprint | 480-fight result hash |
|---|---|---|
| Initial Wave 1a review | `19b3946cc2cd69e2354cb2f42da59aba7b33c778` | `02d06c81eaca35a91d329872a21ecafcf56d9bae` |
| Wave 1b / 2a / 2b | `8c8e46cc40ad8e45f9bd9e1d1e69e4dfa74746f9` | `15cbdefc62e0ec6f2d9462de5008c7109431fbcd` |

The baseline changed with Wave 1b's deliberate rule changes, not with the 2a extraction or 2b additions. The 2b replay engine identifier was `743e962015`.

These checks establish repeatability and preservation, not universal correctness. Existing fight suites largely exercise old kits. A spelling test establishes agreement with authored names, not that the named effect executes. Keep the fingerprints, but complement them with independent expectations for timing, targets, resources, and state transitions.

## Deferred work that is not being counted as a current defect

The reviewed plan explicitly schedules class integration and several effect handlers after 2b. Do not inflate the bug count by treating all unfinished planned mechanics as regressions.

- Wave 3 owns fixed class sheets, kit integration, related pricing integration, and the old-kit Kross → Krosh transition.
- Wave 4 owns unfinished signatures and effects such as Song, Knots, displacement, and several designated riders. In particular, successful compilation of their data is not yet evidence of playable end-to-end behavior.
- Wave 6 includes displaying keywords on move cards and additional status/event presentation. Having keyword metadata on compiled moves is not the same as showing it in the current page.
- Holm and Hasin remain deferred to the mutation session.
- The complete dive economy and tapestry loop have not yet been validated through a playable expedition.

The useful boundary is: authored specifications may exist before implementation, but only executable, validated combinations should be offered as playable actions. Future work should not accidentally activate partial specifications merely because compilation succeeds.

**Sources:** [refactor_plan.md:83–117](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/refactor_plan.md#L83-L117), [data.py:559–566](https://github.com/jensen-117/norse_game/blob/8a7afee433626c3fe532d618f2c95f73a219e035/sim/data.py#L559-L566).

## Suggested implementation and verification sequence

1. **Fix outcome and compiler foundations.** C01 and C08 first, then C09–C11. Normalize parts once, validate their applicability and acquisition context, produce a complete move specification, and price it using an explicit policy. Resolve A01/A02 at the same boundary. Prefer small shared functions and data declarations over named-move exceptions.
2. **Repair existing interaction paths.** C04–C06 cover hit effects, interruption, and identity transitions. Use the common transitions rather than patching each consumer independently. Fix C07 before route generation relies on family rules.
3. **Make the Lab reproducible and safe to restart.** C02/C03, plus automated equality checks or a generated-copy step for shared simulation modules. Run a fresh browser smoke test from the documented clean setup.
4. **Resume the planned class/signature waves.** For each newly playable mechanic, add a representative full-turn test and interaction checks against existing targeting, timing, resource, and death rules. Do not require legacy hashes to remain identical when an intentional rule change is approved; review and document the expected baseline change.
5. **Validate one connected leg.** Use D01–D04 to assess economy and progression, and D05–D07 to assess comprehension, pace, and input access. Expand content after those measurements support the design.

### Checkpoint exit criteria

- Every prioritized finding is either fixed with targeted evidence, or explicitly deferred with its affected functionality kept out of the playable path.
- The new grammar rejects unknown, unsupported, duplicate, and unauthorized combinations according to a documented policy.
- Every accepted playable move has complete execution fields; its declared targets, cost, timing, and effects agree with actual execution.
- Outcome and lifecycle probes pass, including last-breath victory and death/revival during a wind-up.
- The existing test suite and replay checks pass after changes, with intentional fingerprint changes explained rather than overwritten without review.
- A clean Lab startup and a restart-during-playback test succeed before handing the page to additional testers.

### Test choices that provide useful independent evidence

Use hand-authored expectations for the reported failures. Add invariant checks across generated legal parts where they catch families of errors: legal tier destinations, monotonic costs under equivalent upgrades, exact capstone membership, valid target sets, and completeness of runtime fields. For encounters, compare small generated problems with an exhaustive reference solver. For playback, use controlled timers and generation changes. These tests verify rules and observable outcomes instead of mirroring the implementation.

Avoid a large snapshot of every incidental dictionary field as the only oracle. Keep the legacy golden comparison for refactor safety, while allowing intentional rule changes to have clear, independent tests.

## Reproduction fixture for the new grammar findings

The following fixture was executed against the pinned source during review. It uses deterministic setup and the battle's begin/submit/commit interface. It temporarily replaces the first hero's actions so a new compiled move can be exercised before new class kits are wired. It does not claim that the current shipped old kit exposes these moves.

Run the Python body from a checkout's `sim` directory or with that directory on `PYTHONPATH`. To keep a reproduction read-only, use `python -B` and do not save changed fixtures over repository files.

```python
import random
from engine import Battle, act, birth, price_bars, spawn_family
from words import compile_verb

def arena(verb, **parts):
    party = [birth(cls, 10, random.Random(i)) for i, cls in enumerate(
        ('Brennumar', 'Dagskald', 'Skurmar'))]
    move = compile_verb(verb, **parts)
    party[0].actions = [move]
    party[0].maxmp = party[0].mp = 100
    price_bars(party[0])
    enemy = spawn_family('Drattr', 'Drattr', 10, job='Spear')
    enemy.maxhp = enemy.hp = 100000
    enemy.aff = {}
    enemy.actions = [act('defend', 'Defend', target='self')]
    enemy.actions_per_round = 1
    battle = Battle(party, [enemy], random.Random(10), events=True)
    return battle, party, enemy, move

def commit(battle, key='m0', target=None):
    for uid in battle.awaiting():
        battle.submit(uid, key if uid == 'p0' else 'guard',
                      target if uid == 'p0' else None)
    battle.commit()

# C08: inspect effective tier, power, and cost share.
for tier in (None, 'Mer', 'Jatte', 'Ur'):
    move = compile_verb('Storm', tier=tier)
    print('Storm', tier, move['tier'], move['power'], move['share'])

# C09: All on a self buff.
b, p, e, move = arena('Aukseid', target='All')
b.begin('party')
commit(b)
print('Allaukseid MAT stages:', [u.stages['MAT'] for u in p])

# C09: All revival receives no individual target.
b, p, e, move = arena('Vakna', target='All')
p[1].hp = 0
b.downed(p[1])
b.begin('party')
commit(b)
print('Allvakna:', p[1].state, p[0].mp,
      [x['kind'] for x in b.events if x['kind'] == 'revive'])

# C10: duplicate manner still matches the named recipe.
move = compile_verb('Skott', tier='Mer', manners=('Drif', 'Drif'), lonn=True)
print('Duplicate recipe:', move['name'], move['share'])

# C11: same heal, different price and timing.
for manners in ((), ('Tung',)):
    b, p, e, move = arena('Lak', manners=manners)
    p[1].hp -= 100
    before = p[1].hp
    b.begin('party')
    commit(b, target='p1')
    print(move['name'], p[1].hp - before, 100 - p[0].mp, move.get('group'))

# D03: demonstrated free recovery, not proof of a dominant run strategy.
b, p, e, move = arena('Lak', tier='Halv')
p[0].mp = 0
p[1].hp -= 50
before = p[1].hp
b.begin('party')
commit(b, target='p1')
print('Halvlak:', move['cost'], p[1].hp - before, p[0].mp)
```

Expected observations at the reviewed, unfixed snapshot: C08's Storm shares are 0.16, 0.256, 0.10, 0.10; C09 reports `[1, 0, 0]` and `dying, 100, []`; C10 reports Tusensplitter with 0.140625; C11 heals about 58.964919 in both cases but costs 6 versus 10; D03 heals about 29.4824595 at zero MP. Floating-point displays may contain insignificant trailing digits.

## Keeping this review current

Retain the IDs when fixing or revisiting findings. Record the fixing commit, the relevant behavioral test, and the verification result before changing an item to Closed. If a design decision changes the expected behavior, record that decision and update the associated test rather than silently treating the old finding as invalid. Keep confirmed defects, architectural follow-ups, and playtest questions separate in later rollups.


