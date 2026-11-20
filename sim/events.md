# Battle Events

`Battle(party, enemies, rng, events=True)` records what happens as a list of plain dicts in `battle.events`. The front-end draws from these; the Godot port should emit the same shapes. Nothing here is prose except the optional `text` (the old log line, kept for debugging).

Every event has `kind` and `round` (0 before the first round). Units are named by their battle name, which is unique within a fight; **every field naming a unit also gets a fixed id** alongside it (`unit` → `unit_id`, `target` → `target_id`, `targets` → `target_ids`). A Mogel that re-forms changes its name but keeps its id. Cells are `[row, lane]`, with row `"front"` or `"rear"` and lane 0–2.

## Flow

| kind | fields | when |
|---|---|---|
| `start` | `units`: the roster (below) | once, before round 1 |
| `round` | `n` | each numbered round |
| `intent` | `unit`, `side`, `move`, `shown`, `move_kind`, `element`, `target`, `group`, `reason`, `why` | each declared action, before the round resolves |
| `order` | `entries`: `[{unit, move, group}]`, `bonus` | the resolution order, after all intents |
| `bonus` | `units` | a Bonus Round begins |
| `end` | `winner` (`party`, `enemy`, `fled`, `draw`), `rounds` | once |

**Roster entry:** `unit`, `id`, `side`, `pouch` (`item`, `name`, `count`), `family`, `cls`, `rank`, `element`, `cell`, `hp`, `maxhp`, `mp`, `maxmp`, `moves` (`name`, `shown`, `kind`, `element`, `cost`, `cost_type`).

**`shown`** is the name a player sees: the old-language word for heroes, the plain English shout for enemies (`"Volley!"`).

**`reason`** is a stable code, and **`why`** is plain English for the hover: `weak` (the target is weak to it), `finish` (nearly down), `rider` (to leave a status), `reach` (the target stands behind the line), `strike`, `sweep`, `coat`, `bide`, `release`, `scatter`, `mend`, `hex`, `bolster`, `weaken`, `cleanse`, `brace`, `shield`, `rotate`, `dodge`, `step_off`, `fill`, `fall_back`, `advance`, `finish_fallen` (a blow on a Dying hero), `revive`, `flee`.

## Actions and results

| kind | fields |
|---|---|
| `act` | `unit`, `move`, `shown`, `move_kind` (`damage`, `status`), `element`, `targets`, `bonus` |
| `hit` | `src`, `unit`, `element`, `results` (one per hit: `graze`, `hit`, `crit`), `affinity`, `dmg`, `hp`, `maxhp`; `spot` when it's a painted spot landing (paint ignores affinity, so it teaches nothing) |
| `absorb` | `unit`, `src`, `element`, `amount`, `hp` |
| `flurry` | `unit`, `hits` (a Drif chain's length) |
| `shatter` | `unit` (a Frozen target shattered) |
| `covered` | `unit` (the coverer), `instead_of` |
| `heal` | `unit`, `move`, `element`, `targets`: `[{unit, amount, hp}]` |
| `stat` | `unit`, `move`, `stat`, `direction`, `targets` |
| `cleanse` | `unit`, `move`, `targets` |
| `status` | `unit`, `status`, `src` |
| `resist` | `unit` (a status grazed off) |
| `defend` | `unit` |
| `cover` | `unit`, `target` |
| `move` | `unit`, `cell`, and `swapped` + `other_cell`, or `advance` |
| `windup` | `unit`, `move`, `shown`, `target` (a Bid- move winding up) |
| `bide_lost` | `unit`, `move`, `shown` |
| `paint` | `unit`, `move`, `shown`, `element`, `side`, `cell`, `target` (a Mark- spot coated) |
| `skip` | `unit`, `why` (`Frozen`, `Stunned`, `Silenced`, `spent`) |
| `retarget` | `unit`, `move`, `was` (the target it meant), `target` (the one it hit instead), `why` (`down`, `reach`) |
| `fizzle` | `unit`, `move`, `shown` (no one in reach) |
| `silenced` | `unit` (forced onto a free move) |
| `tick` | `unit`, `status` (`Poisoned`, `Bleeding`, `slime`), `dmg`, `hp`, and `element` for slime |

## Falling

| kind | fields |
|---|---|
| `down` | `unit` |
| `reform` | `unit` (new name), `was`, `rank`, `hp`, `maxhp` (a Mogel one size smaller) |
| `crawl` | `unit`, `hp`, `maxhp` (a Draugr not beheaded or burned) |
| `pile` | `unit`, `rounds` (a Bein in a pile of bones) |
| `scatter` | `unit` (who crushed it), `move`, `shown`, `target` (the pile, gone for good) |
| `reassemble` | `unit`, `cell`, `hp`, `maxhp` |

## Heroes falling, and items

| kind | fields |
|---|---|
| `dying` | `unit`, `breaths` (a hero at 0 HP) |
| `breath` | `unit`, `breaths` (left), `src` (who struck, if a finishing blow) |
| `dead` | `unit`, `why` |
| `revive` | `unit` (who revived), `target`, `move`, `was` (`dying`, `dead`), `hp`, `wounded` |
| `stabilised` | `unit`, `hp` (Dying when the fight was won: up at 1 HP, Wounded) |
| `item` | `unit`, `item`, `name`, `target` (then the item's effect follows as its own event) |
| `mp` | `unit`, `amount` |
| `fled` | `unit` (who led the escape, or used a Smoke Pot) |
| `flee_failed` | `unit`, `chance` |

## Playing a fight step by step

`b.begin(control="party")` → `b.phase` (`declare`, `bonus`, `over`), `b.awaiting()` (ids), `b.options(uid)`, `b.submit(uid, key, target)`, `b.commit()`, `b.inspect(uid)`. `begin()` and `commit()` return the events since the last call. `commit()` stops at the start of every round, and at a Bonus Round our heroes earned. `b.fight()` is the same loop with the AI choosing for everyone (`control=None`).

**Order keys:** `m<n>` (a move by its index in the hero's actions, the Halv move included), `cover`, `i:<item>`, `guard`, `move` (target is `[row, lane]`), `flee`. **Targets** are unit ids, or `None` for self and All moves. Party intents are emitted at `commit()`, just before `order`.
