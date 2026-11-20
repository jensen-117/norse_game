# Agent Code Review — norse_game

Review date: 20 November 2026  
Repository: [jensen-117/norse_game](https://github.com/jensen-117/norse_game)  
Current review baseline: [Wave 2b — 8a7afee433626c3fe532d618f2c95f73a219e035](https://github.com/jensen-117/norse_game/commit/8a7afee433626c3fe532d618f2c95f73a219e035)  
Scope: consolidated technical audit and game-design review through Wave 2b. Repository review was read-only; this report is a separate deliverable. No fixes have been applied.

## Recommendation

Take a focused bug-fix checkpoint before the next wave wires the new grammar into playable class kits. Address C01 and C08 first, then C09–C11 so the new compiler has dependable legality, targeting, and effect rules. Resolve the compiler contract in A01 alongside that work. Fix C02 before more browser playtesting and C03 before handing the Lab to another developer. C04–C07 should be completed before broader balance conclusions or authored routes depend on those systems.

This is not a recommendation to complete every planned feature before continuing. Song, Knots, displacement, and other explicitly deferred signatures remain later-wave work. Independent content and design work can continue while the affected foundations are corrected. A documented rejection of a currently unsupported combination is an acceptable temporary boundary; accepting it and silently doing something else is not.

The project has a coherent identity: the party is the build, words describe its growing capabilities, and the tapestry records the consequences of routing. The engineering strengths are deterministic simulation, substantial regression coverage, native replay, and data-driven mechanics. The main weakness is that successful behavior preservation also preserves old bugs, while new combinations can compile without having a complete execution contract.

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
| C05 | P2 | Death can preserve a wind-up through revival | Closed (a0bb56f) |
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

