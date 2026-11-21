"""Encounter v0 -- data tables. Every number here is a draft knob."""

ATTRS = ["STR", "CON", "SPD", "DEX", "WIL", "INT", "WIS"]

# ---------------------------------------------------------------- tiers / costs
TIERS = ["Halv", "Base", "Mer", "Jatte", "Ur"]
TIER_POWER = {"Halv": 10, "Base": 20, "Mer": 28, "Jatte": 38, "Ur": 50}   # compressed
TIER_COST = {"Halv": 0, "Base": 8, "Mer": 16, "Jatte": 32, "Ur": 0}       # Ur lives on gear
TIER_LEARN_LEVEL = {"Halv": 1, "Base": 1, "Mer": 20, "Jatte": 50}
RIDER_CHANCE = {"Halv": 0.0, "Base": 0.20, "Mer": 0.30, "Jatte": 0.40, "Ur": 0.50}
STATUS_LINE_CHANCE = {"Halv": 0.35, "Base": 0.50, "Mer": 0.75, "Jatte": 0.90, "Ur": 0.95}
ALL_COST_MULT, ALL_POWER_MULT = 1.5, 0.75
HALVLAK_COST = 4                      # healing is never free

# ---------------------------------------------------------------- elements
SCHOOL_OF = {"Eld": "Eld", "Reyk": "Eld", "Vatn": "Vatn", "Hrim": "Vatn",
             "Blast": "Blast", "Blixt": "Blast", "Jord": "Jord", "Gro": "Jord",
             "Sol": "Sol", "Lak": "Sol", "Natt": "Natt", "Aska": "Natt"}
CHILD_OF = {"Eld": "Reyk", "Vatn": "Hrim", "Blast": "Blixt", "Jord": "Gro",
            "Sol": "Lak", "Natt": "Aska"}

# power and cost multipliers, variance, hits, rider
ELEMENT = {
    "Eld":   dict(power=1.15, cost=1.25, var=0.10, hits=1, rider=None),
    "Reyk":  dict(power=0.80, cost=1.00, var=0.10, hits=1, rider="AccDown"),
    "Vatn":  dict(power=1.00, cost=0.75, var=0.10, hits=1, rider=None),
    "Hrim":  dict(power=1.00, cost=1.00, var=0.10, hits=1, rider="Chilled"),
    "Blast": dict(power=0.45, cost=0.75, var=0.10, hits=2, rider=None),
    "Blixt": dict(power=1.25, cost=1.25, var=0.40, hits=1, rider="Stunned"),
    "Jord":  dict(power=1.00, cost=0.70, var=0.00, hits=1, rider=None),
    "Gro":   dict(power=0.70, cost=1.00, var=0.10, hits=1, rider="Poisoned"),
    "Sol":   dict(power=1.00, cost=1.00, var=0.10, hits=1, rider=None),
    "Natt":  dict(power=1.00, cost=1.00, var=0.10, hits=1, rider=None),
    "Aska":  dict(power=0.60, cost=1.00, var=0.10, hits=1, rider="Cursed"),
    "Slash": dict(power=1.00, cost=1.00, var=0.10, hits=1, rider=None),
    "Pierce": dict(power=1.00, cost=1.00, var=0.10, hits=1, rider=None),
    "Crush": dict(power=1.00, cost=1.00, var=0.10, hits=1, rider=None),
}
MARTIAL = {"Slash", "Pierce", "Crush"}

# school-wide affinities for caster classes (and creatures of that school)
SCHOOL_AFFINITY = {
    "Eld":   dict(resist=["Eld", "Reyk"], weak=["Vatn", "Blixt"]),
    "Vatn":  dict(resist=["Vatn", "Hrim"], weak=["Jord", "Reyk"]),
    "Blast": dict(resist=["Blast", "Blixt"], weak=["Eld", "Gro"]),
    "Jord":  dict(resist=["Jord", "Gro"], weak=["Blast", "Hrim"]),
    "Sol":   dict(resist=["Sol"], weak=["Natt"]),
    "Natt":  dict(resist=["Natt", "Aska"], weak=["Sol"]),
}

# ---------------------------------------------------------------- zodiac
# name, elemental resist, elemental weak, martial resist, martial weak,
# attribute shaping (PLACEHOLDER pairs until signs are designed)
ZODIAC = [
    ("Arin",   "Eld",   "Vatn",  "Slash",  "Pierce", ("CON", "SPD")),
    ("Kerti",  "Eld",   "Blast", "Crush",  "Slash",  ("INT", "CON")),
    ("Eimyr",  "Eld",   "Jord",  "Pierce", "Crush",  ("STR", "WIS")),
    ("Mierka", "Vatn",  "Eld",   "Pierce", "Slash",  ("WIS", "STR")),
    ("Knarr",  "Vatn",  "Blast", "Slash",  "Crush",  ("SPD", "CON")),
    ("Johka",  "Vatn",  "Jord",  "Crush",  "Pierce", ("WIL", "DEX")),
    ("Bjark",  "Blast", "Eld",   "Slash",  "Crush",  ("DEX", "WIL")),
    ("Varde",  "Blast", "Vatn",  "Crush",  "Pierce", ("CON", "INT")),
    ("Hrafn",  "Blast", "Jord",  "Pierce", "Slash",  ("INT", "STR")),
    ("Otso",   "Jord",  "Eld",   "Crush",  "Slash",  ("STR", "DEX")),
    ("Myyra",  "Jord",  "Vatn",  "Pierce", "Crush",  ("WIS", "SPD")),
    ("Bauta",  "Jord",  "Blast", "Slash",  "Pierce", ("CON", "WIL")),
]

# ---------------------------------------------------------------- classes
# atk / mat: attribute weights. train: level-up point priority.
CLASSES = {
    # casters
    "Brennumar": dict(kind="magical", school="Eld", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Hafrunar":  dict(kind="magical", school="Vatn", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Skurmar":   dict(kind="magical", school="Blast", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Lundar":    dict(kind="magical", school="Jord", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "CON"]),
    "Dagskald":  dict(kind="magical", school="Sol", mat={"WIS": 1.0}, atk={"STR": 1.0},
                      train=["WIS", "CON"]),
    "Seidar":    dict(kind="magical", school="Natt", mat={"INT": 0.5, "WIL": 0.5},
                      atk={"STR": 1.0}, train=["INT", "WIL"]),
    # martials
    "Ullar":     dict(kind="martial", weapon="Bow", dmg="Pierce", weak="Slash", atk={"DEX": 1.0},
                      mat={"INT": 1.0}, train=["DEX", "CON"]),
    "Nalarbani": dict(kind="martial", weapon="Stikk", dmg="Pierce", weak="Crush",
                      atk={"DEX": 0.5, "SPD": 0.5}, mat={"INT": 1.0}, train=["DEX", "SPD"]),
    "Hersir":    dict(kind="martial", weapon="Greatsword", dmg="Slash", weak="Pierce",
                      atk={"STR": 0.5, "DEX": 0.5}, mat={"INT": 1.0}, train=["STR", "DEX"]),
    "Huskarl":   dict(kind="martial", weapon="Axe", dmg="Slash", weak="Crush",
                      atk={"STR": 0.75, "CON": 0.25}, mat={"INT": 1.0}, train=["STR", "CON"]),
    "Berserker": dict(kind="martial", weapon="Club", dmg="Crush", weak="Slash", atk={"STR": 1.0},
                      mat={"INT": 1.0}, train=["STR", "CON"]),
    "Vasara":    dict(kind="martial", weapon="Hammer", dmg="Crush", weak="Pierce",
                      atk={"STR": 0.5, "CON": 0.5}, mat={"INT": 1.0}, train=["STR", "CON"]),
}
CASTERS = [c for c, d in CLASSES.items() if d["kind"] == "magical"]
MARTIALS = [c for c, d in CLASSES.items() if d["kind"] == "martial"]

# ---------------------------------------------------------------- statuses
POISON_TICK = 0.08     # of max HP, start of each numbered round
BLEED_TICK = 0.08      # of max HP, when the bleeding character goes to act
STATUS_DURATION = 3    # numbered rounds
CHILL_DURATION = (2, 4)
FREEZE_DURATION = (1, 3)
STUN_LOSE_CHANCE = 0.5
SHATTER_MULT = 1.5

# ---------------------------------------------------------------- hit model
GRAZE_BASE, CRIT_BASE, STEP = 0.20, 0.05, 0.10
GRAZE_MULT, CRIT_MULT = 0.5, 1.5

# ---------------------------------------------------------------- enemies
# Authored creatures. genes default to average (15.5).
ENEMIES = {
    "Frost Wolf": dict(atk={"STR": 1.0}, mat={"INT": 1.0},
                       aff=dict(resist=["Vatn", "Hrim"], weak=["Jord", "Reyk", "Crush"]),
                       actions=[("strike", "Pierce", "Bite"), ("spell", "Hrim", "Base", False)]),
    "Bog Archer": dict(atk={"DEX": 1.0}, mat={"INT": 1.0},
                       aff=dict(resist=["Jord", "Gro"], weak=["Blast", "Hrim", "Slash"]),
                       actions=[("strike", "Pierce", "Arrow"), ("skill", "Pierce", "Base", True, "Volley")]),
    "Ember Beetle": dict(atk={"STR": 0.5, "CON": 0.5}, mat={"INT": 1.0},
                         aff=dict(absorb=["Eld"], resist=["Reyk", "Slash"], weak=["Vatn", "Blixt", "Crush"]),
                         actions=[("strike", "Crush", "Mandible"), ("spell", "Eld", "Base", False)]),
}
ENEMIES.update({
    "Grave Hound": dict(atk={"STR": 1.0}, mat={"INT": 1.0},
                        aff=dict(resist=["Natt", "Aska", "Pierce"], weak=["Sol", "Slash"]),
                        actions=[("strike", "Slash", "Rend"), ("spell", "Aska", "Base", False)]),
    "Gale Harpy": dict(atk={"DEX": 1.0}, mat={"INT": 1.0},
                       aff=dict(resist=["Blast", "Blixt", "Crush"], weak=["Eld", "Gro", "Pierce"]),
                       actions=[("strike", "Slash", "Talon"), ("spell", "Blast", "Base", True)]),
    "Stone Troll": dict(atk={"STR": 1.0}, mat={"INT": 1.0},
                        aff=dict(resist=["Jord", "Gro", "Slash"], weak=["Blast", "Hrim", "Pierce"]),
                        actions=[("strike", "Crush", "Club"), ("skill", "Crush", "Base", False, "Smash")]),
})
ENEMY_STRIKE_POWER = 16
HP_MULT = 3.0          # scales every max HP; tuned for ~7-round fights at level 30
CRIT_EARNS_BONUS = False

# ---------------------------------------------------------------- birth and growth
PERSONALITY_MULT = 0.20   # boosted attribute grows +20%, reduced one -20%
CLASS_TILT = 0.50         # weapon feeders grow up to +50%; the rest pay for it evenly
FIT_EXPONENT = 9.0        # weighted-random class roll: chance ~ fit ** exponent (about 2 in 3 recruits fit)

# ---------------------------------------------------------------- the Ande spirit family
# rank: name prefix, cost (= slots = actions per round), HP multiplier,
#       main single tier, All tier (None = no All move), utility slots
SPIRIT_RANKS = [
    ("Halv",  dict(prefix="Halv",  cost=1, hp=1.0, main="Halv",  all="Halv", utils=[])),
    ("Litel", dict(prefix="Litel", cost=1, hp=1.2, main="Base",  all="Halv", utils=[])),
    ("Ande",  dict(prefix="",      cost=2, hp=2.0, main="Base",  all="Base", utils=["U1"])),
    ("Stor",  dict(prefix="Stor",  cost=2, hp=2.5, main="Mer",   all="Base", utils=["U1", "U2"])),
    ("Drott", dict(prefix="Drott", cost=3, hp=3.5, main="Jatte", all="Mer",  utils=["U1", "U3"])),
]
# U1 = sibling element (cast at the rank's main tier); U2 = status or debuff (rank tier);
# U3 = the Drott's sovereign move.
SPIRIT_KITS = {
    "Eld":   dict(U1=("dmg", "Reyk"), U2=("status", "Poisoned"), U3=("stat", "MAT", +1, "Mer")),
    "Reyk":  dict(U1=("dmg", "Eld"),  U2=("status", "Blinded"),  U3=("stat", "ACC", -1, "Mer")),
    "Vatn":  dict(U1=("dmg", "Hrim"), U2=("status", "Disarmed"), U3=("stat", "MDF", +1, "Mer")),
    "Hrim":  dict(U1=("dmg", "Vatn"), U2=("stat", "SPD", -1),    U3=("stat", "DEF", +1, "Mer")),
    "Blast": dict(U1=("dmg", "Blixt"), U2=("stat", "ACC", -1),   U3=("stat", "EVA", +1, "Mer")),
    "Blixt": dict(U1=("dmg", "Blast"), U2=("status", "Feared"),  U3=("stat", "SPD", +1, "Mer")),
    "Jord":  dict(U1=("dmg", "Gro"),  U2=("stat", "SPD", -1),    U3=("stat", "DEF", +1, "Mer")),
    "Gro":   dict(U1=("dmg", "Jord"), U2=("status", "Poisoned"), U3=("heal", "Mer")),
    "Sol":   dict(U1=("heal",),       U2=("status", "Blinded"),  U3=("stat", "MDF", +1, "Mer")),
    "Lak":   dict(U1=("dmg", "Sol"),  U2=("stat", "DEF", +1),    U3=("stat", "MDF", +1, "Mer")),
    "Natt":  dict(U1=("dmg", "Aska"), U2=("status", "Feared"),   U3=("status", "Blinded", "Jatte")),
    "Aska":  dict(U1=("dmg", "Natt"), U2=("status", "Cursed"),   U3=("status", "Death", "Jatte")),
}
SPIRIT_TRAIN = 0.25      # extra per level into the spirit's INT, CON, and WIS
SPIRIT_HP_SCALE = 0.5    # each slot is 'half a hero' so a 6-slot pack is a fair fight for 3
SPIRIT_DMG_SCALE = 0.6    # multiplies enemy STR and INT (physical families); 0.5 before the board (the board protects the Rear)
ANDE_MAT_SCALE = 0.65    # Ande spirits are pure casters: a little more bite...
ANDE_MP_MULT = 2.0       # ...and deeper MP pools, since they can't fall back on free strikes
HELVAD_CHANCE = 0.25     # base chance of instant death, before WIL and Aska affinity

# ---------------------------------------------------------------- martial families (the undead)
MAGICAL = dict(type="Magical")   # a rank's options (see rank_rows): its Type
SPLASH_SHARE = 0.27              # the Halvdrattr's row Splash costs this share of its max MP: 3-4 casts at any level
# rank: (name, cost = slots = actions, HP multiplier, moves)
# moves: ("strike", type, name, tier, all?, status?)  -- free for enemies
#        ("spell", element, tier) / ("status", status, tier) / ("stat", stat, dir, tier, all?) -- cost MP
FAMILIES = {
    "Draugr": dict(
        aff=dict(weak=["Slash", "Eld", "Sol"], resist=["Crush", "Natt", "Aska"]),
        ranks=[
            ("Halvdraugr", 1, 1.0, [("strike", "Slash", "Claw", "Halv"), ("strike", "Slash", "Rake", "Halv", True)]),
            ("Draugr", 2, 2.0, [("strike", "Slash", "Grave Axe", "Base"), ("strike", "Crush", "Barrow Fist", "Base"),
                                ("strike", "Slash", "Sweep", "Base", True), ("status", "Feared", "Base")]),
            ("Stordraugr", 2, 2.5, [("strike", "Slash", "Grave Axe", "Mer"), ("strike", "Crush", "Barrow Fist", "Mer"),
                                    ("strike", "Slash", "Sweep", "Base", True),
                                    ("strike", "Slash", "Blot", "Base", False, "Bleeding")]),
            ("Forndraugr", 3, 3.5, [("strike", "Crush", "Barrow Fist", "Jatte"), ("strike", "Slash", "Sweep", "Mer", True),
                                    ("status", "Feared", "Mer"), ("status", "Cursed", "Jatte")]),
            ("Gandraugr", 2, 2.0, [("spell", "Natt", "Mer"), ("spell", "Hrim", "Mer"),
                                   ("status", "Feared", "Base"), ("status", "Cursed", "Base")], MAGICAL),
        ]),
    "Bein": dict(          # the Beinar: weak Oskorei, by job (sword and shield, bow, staff), each rank a size and tint
        aff=dict(weak=["Crush", "Sol"], resist=["Slash", "Pierce", "Natt", "Aska"]),
        ranks=[
            # Beinbryn ("bone mail"): the shield wall. Covers its allies (see BEIN_GUARDIANS).
            ("Halvbeinbryn", 1, 1.0, [("strike", "Slash", "Rusty Blade", "Halv"), ("strike", "Crush", "Shield Bash", "Halv")]),
            ("Beinbryn", 2, 2.0, [("strike", "Slash", "Old Sword", "Base"), ("strike", "Crush", "Shield Bash", "Base"),
                                  ("stat", "DEF", 1, "Base")]),
            ("Storbeinbryn", 2, 2.5, [("strike", "Slash", "Old Sword", "Mer"), ("strike", "Crush", "Shield Bash", "Base"),
                                      ("stat", "DEF", 1, "Base", True)]),
            # Beinorv ("bone arrow"): the archer. Its shots reach anywhere (its bow: Long).
            ("Halvbeinorv", 1, 1.0, [("strike", "Pierce", "Arrow", "Halv")], dict(weapon="Bow")),
            ("Beinorv", 2, 2.0, [("strike", "Pierce", "Arrow", "Base"), ("strike", "Pierce", "Volley", "Halv", True)], dict(weapon="Bow")),
            ("Storbeinorv", 2, 2.5, [("strike", "Pierce", "Arrow", "Mer"), ("strike", "Pierce", "Volley", "Base", True),
                                     ("strike", "Pierce", "Barbed Arrow", "Base", False, "Bleeding")], dict(weapon="Bow")),
            # Beinseidr: the bone-mage. "@" is its element, chosen at spawn (BEINSEIDR_ELEMENTS).
            ("Halvbeinseidr", 1, 1.0, [("spell", "@", "Halv")], MAGICAL),
            ("Beinseidr", 2, 2.0, [("spell", "@", "Base"), ("status", "Cursed", "Base")], MAGICAL),
            ("Storbeinseidr", 2, 2.5, [("spell", "@", "Mer"), ("status", "Cursed", "Base"), ("stat", "MDF", 1, "Base", True)], MAGICAL),
            # the Drott: the red shield-king
            ("Fornbein", 3, 3.5, [("strike", "Slash", "Old Sword", "Jatte"), ("strike", "Crush", "Shield Bash", "Mer"),
                                  ("stat", "DEF", 1, "Base", True), ("status", "Feared", "Base")]),
        ]),
}

# ---------------------------------------------------------------- the Drattr (the catch)
# Hunted water creatures: weak to the spear. ON drattr, "a pull, a haul"; Swedish fors, "rapids".
FAMILIES["Drattr"] = dict(       # Joseph's drattr_1 sheet (Nov 9): a sea court. Jobs by sprite; shown names by rank.
    aff=dict(weak=["Pierce", "Jord", "Reyk"], resist=["Slash", "Vatn", "Hrim"]),
    ranks=[
        # the young (sprites 7, 6)
        ("Halvdrattr", 1, 1.0, [("strike", "Pierce", "Nip", "Halv"),
                                ("spell", "Vatn", "Halv", dict(name="Splash", shape="row", mp_share=SPLASH_SHARE))]),
        ("Drattr", 2, 2.0, [("strike", "Pierce", "Bite", "Base"), ("strike", "Crush", "Tail Slap", "Base")],
         dict(job="Young")),
        # the palace guard (1, 2): the shield brother Covers, the sword brother flurries
        ("Drattr", 2, 2.0, [("strike", "Slash", "Slash", "Base"), ("strike", "Slash", "Rend", "Base", False, "Bleeding")],
         dict(job="Shield", guard=True, weapon="Sword")),
        ("Drattr", 2, 2.0, [("strike", "Slash", "Twin Slash", "Base", dict(hits=2)),
                            ("strike", "Slash", "Rend", "Base", False, "Bleeding"),
                            ("strike", "Slash", "Swift Strikes", "Base", dict(manner="Drif"))],
         dict(job="Swords", weapon="Sword")),
        # the fishers (3, 4): spear, and the net (thrown once, then she fights as the spear)
        ("Drattr", 2, 2.0, [("strike", "Pierce", "Spett", "Base"),
                            ("strike", "Pierce", "Skewer", "Base", dict(shape="column", falloff=[1.0, 0.5])),
                            ("strike", "Slash", "Halvskar", "Halv")],
         dict(job="Spear", weapon="Spear")),
        ("Drattr", 2, 2.0, [("status", "Bound", "Base", dict(name="Net Throw", line="throws a net!", group=1, once=True, sure=True, thrown=True,
                                                               then="Spear")),
                            ("strike", "Pierce", "Spett", "Base"), ("strike", "Slash", "Halvskar", "Halv")],
         dict(job="Net", takes="spear", weapon="Spear")),
        # the big ones (5, 8, 11)
        ("Stordrattr", 2, 2.5, [("stat", "ACC", -1, "Base", True, dict(name="Lure")), ("strike", "Crush", "Slam", "Mer"),
                                ("spell", "Vatn", "Base")],
         dict(job="Angler")),
        ("Stordrattr", 2, 2.5, [("stat", "ATK", 1, "Base", True, dict(name="Feeding Frenzy", also=("DEF", -1))),
                                ("heal", "Base"), ("strike", "Pierce", "Bite", "Base")],
         dict(job="Princeling", type="Magical", role="rear")),
        ("Stordrattr", 2, 2.5, [("spell", "Vatn", "Mer", dict(name="Undertow")), ("spell", "Vatn", "Base"),
                                ("spell", "Hrim", "Base"), ("cleanse", "Base")],
         dict(job="Mystic", type="Magical")),
        # the queen (16)
        ("Forsdrattr", 3, 3.5, [("spell", "Vatn", "Mer", True, dict(name="Riptide")), ("spell", "Vatn", "Jatte"),
                                ("spell", "Hrim", "Mer"), ("strike", "Pierce", "Trident", "Mer")],
         dict(job="Queen", type="Magical", weapon="Spear")),
    ])
# ---------------------------------------------------------------- the Djur (forest beasts)
# Swedish djur, ON dyr ("animal"; same word as English "deer"). Hunted: weak to the spear and arrow.
FAMILIES["Djur"] = dict(
    aff=dict(weak=["Pierce", "Eld"], resist=["Crush", "Gro"]),
    ranks=[
        ("Halvdjur", 1, 1.0, [("strike", "Pierce", "Bite", "Halv"), ("strike", "Pierce", "Pack Snap", "Halv", True)]),
        ("Djur", 2, 2.0, [("strike", "Pierce", "Bite", "Base"), ("strike", "Slash", "Rend", "Base"),
                          ("strike", "Slash", "Pack Rush", "Base", True), ("status", "Feared", "Base")]),
        ("Stordjur", 2, 2.5, [("strike", "Pierce", "Gore", "Mer"), ("strike", "Slash", "Rend", "Mer", False, "Bleeding"),
                              ("strike", "Slash", "Pack Rush", "Base", True)]),
        ("Forndjur", 3, 3.5, [("strike", "Pierce", "Gore", "Jatte"), ("strike", "Slash", "Pack Rush", "Mer", True),
                              ("status", "Feared", "Mer"), ("stat", "ATK", 1, "Base", True)]),
    ])

# ---------------------------------------------------------------- jobs and Types (Nov 9)
# A rank may end in an options dict. "job" is its own key (several jobs can share one shown name, so the
# Drattr guard and the Drattr spearman are both "Drattr"); without one, the job is the rank's name.
# "type" is Martial or Magical (default Martial): the Type points the family's attack lean (see TYPE_LEAN).
# Other options: guard (Covers like a Beinbryn), role ("front"/"rear", overriding the kit's guess).
def rank_rows(family):
    """A family's ranks as dicts: name, cost, hp, moves, job, type, opts."""
    out = []
    for r in FAMILIES[family]["ranks"]:
        opts = r[4] if len(r) > 4 else {}
        out.append(dict(name=r[0], cost=r[1], hp=r[2], moves=r[3], job=opts.get("job", r[0]),
                        type=opts.get("type", "Martial"), opts=opts))
    return out

def rank_row(family, job):
    """One rank by its job key (a rank's plain name works too, for families without jobs)."""
    rows = rank_rows(family)
    return next((r for r in rows if r["job"] == job), None) or next(r for r in rows if r["name"] == job)

# ---------------------------------------------------------------- the Oskorei (the Wild Hunt)
# Fixed formations. Every hunter is Blast school plus the martial weakness of the class it mirrors.
# Hunt Horn: while a horn-bearer lives, every enemy in the formation gets +1 ACC.
# unit: (name, cost, hp, martial weakness, horn?, moves)
OSKOREI_TIERS = {
    1: [("Halvoskorei Axe", 1, 1.0, "Crush", False, [("strike", "Slash", "Axe", "Halv"), ("spell", "Blast", "Halv", True)]),
        ("Halvoskorei Hammer", 1, 1.0, "Pierce", False, [("strike", "Crush", "Hammer", "Halv"), ("spell", "Blast", "Halv", True)]),
        ("Halvoskorei Bow", 1, 1.0, "Slash", False, [("strike", "Pierce", "Arrow", "Halv", dict(weapon="Bow")), ("spell", "Blast", "Halv", True)]),
        "hound", "hound", "hound"],
    2: [("Ryttar", 2, 2.0, "Pierce", False, [("strike", "Crush", "Ride Down", "Base"),
                                              ("strike", "Slash", "Spectral Blade", "Base"), ("strike", "Crush", "Trample", "Base", True),
                                              ("stat", "DEF", 1, "Base")]),
        ("Hornblasar", 2, 2.0, "Slash", True, [("spell", "Blast", "Base"), ("spell", "Blixt", "Base"),
                                                ("spell", "Blast", "Base", True), ("status", "Silenced", "Base")]),
        "hound", "hound"],
    3: [("Storoskorei Greatsword", 2, 2.5, "Pierce", False, [("strike", "Slash", "Greatsword", "Mer"),
                                                              ("strike", "Slash", "Cleave", "Base", True), ("spell", "Blast", "Mer")]),
        ("Storoskorei Stiletto", 2, 2.5, "Crush", False, [("strike", "Pierce", "Stiletto", "Mer", dict(weapon="Stikk")),
                                                           ("strike", "Pierce", "Blot", "Base", False, "Bleeding"), ("spell", "Blast", "Mer")]),
        ("Storoskorei Maul", 2, 2.5, "Slash", False, [("strike", "Crush", "Maul", "Mer"), ("spell", "Blixt", "Mer"),
                                                       ("stat", "DEF", -1, "Base")])],
    4: [("Huntmaster", 3, 3.5, "Pierce", True, [("strike", "Slash", "Hunt's Edge", "Jatte"),
                                                 ("strike", "Pierce", "Rain of Spears", "Mer", True, dict(weapon="Javelin")),
                                                 ("status", "Feared", "Mer"), ("ur", "Blast")]),
        ("Storm-caller", 3, 3.5, "Slash", True, [("ur", "Blixt"), ("spell", "Blast", "Mer", True),
                                                  ("status", "Silenced", "Mer"), ("stat", "SPD", 1, "Mer", True)])],
}
ENEMY_UR_COST = 48        # MP for an Ur spell carried on an enemy's gear
SILENCE_ROOT = "Bann"     # ON/Swedish bann, "ban, prohibition"

HALV_BODY = 2.0          # Halv-rank enemies keep Halv moves but have bodies that hit harder (x STR and INT)

# ---------------------------------------------------------------- family bodies
# Multipliers on combat stats, balanced by VALUE, not by raw sum: a point of HP or ATK/MAT is
# worth 1, DEF or MDF 0.5 (each only stops half the threats), SPD 0.5 (turn order plus the
# speed shift on the Graze roll), WIL 0.25.
# Stats a family never uses stay at 1.0 so they can't be dumped for free power.
FAMILY_BODIES = {
    "Draugr":  dict(HP=1.2, ATK=1.05, MAT=0.9, DEF=1.0, MDF=0.9, SPD=0.6, WIL=1.0),
    "Bein":    dict(HP=0.9, ATK=1.0, MAT=1.0, DEF=1.4, MDF=0.9, SPD=0.8, WIL=1.2),
    "Drattr":  dict(HP=1.1, ATK=0.9, MAT=1.1, DEF=0.8, MDF=1.2, SPD=1.0, WIL=0.9),
    "Djur":    dict(HP=0.7, ATK=1.3, MAT=1.0, DEF=0.9, MDF=0.8, SPD=1.4, WIL=0.8),
    "Ande":    dict(HP=0.9, ATK=1.0, MAT=1.1, DEF=0.8, MDF=1.3, SPD=1.0, WIL=0.9),
    "Oskorei": dict(HP=1.0, ATK=1.0, MAT=1.0, DEF=1.0, MDF=0.9, SPD=1.1, WIL=1.0),
}

# Types (Nov 9): Martial creatures lean to ATK, Magical ones to MAT.
# "swap" points the family's existing lean the Type's way: a Martial Drattr hits with the 1.1 the family
# casts with. Value-neutral, so no family gets stronger. "tilt" moves TYPE_TILT from the stat the creature
# doesn't use to the one it does: free power (Wildwood 39% -> 27% party wins at L10, 150 fights each).
# None turns Types off.
TYPE_LEAN = "swap"
TYPE_TILT = 0.15

# ---------------------------------------------------------------- speed and the Graze roll
SPEED_STEP = 0.25        # every 25% faster than your opponent = +1 net stage on the roll
SPEED_CAP = 2            # capped at +/-2

# ---------------------------------------------------------------- the Mogel (slimes)
# Swedish mogel, "mould". Living mould in every element: the physical half of a spirit pack.
# Slash cuts them (weak), Crush is neutral, Pierce passes through (resist); they absorb their own
# element and share their school's weaknesses. The plain olive Mogel is the Jord one (mould is earth).
# Death drops a Mogel a size instead of killing it: any 32px rank re-forms as a Litelmogel (16px),
# a Litelmogel as a Halvmogel (8px), and only the Halvmogel truly dies. One rank's cost pays for its
# whole chain, so each re-formed body comes back with only a share of its normal HP.
#       rank: prefix, cost (= slots = actions), HP multiplier, art size, Engulf tier, element spell
#             tier, Splatter (All Crush) tier, Withdraw (Defend)?, sovereign Reabsorb (self heal)?
MOGEL_RANKS = [
    ("Halv",  dict(prefix="Halv",  cost=1, hp=1.0, size=8,  crush="Halv",  spell="Halv",  splatter=None,   withdraw=False, reabsorb=False)),
    ("Litel", dict(prefix="Litel", cost=1, hp=1.2, size=16, crush="Base",  spell="Halv",  splatter=None,   withdraw=False, reabsorb=False)),
    ("Mogel", dict(prefix="",      cost=2, hp=2.0, size=32, crush="Base",  spell="Base",  splatter="Halv", withdraw=True,  reabsorb=False)),
    ("Stor",  dict(prefix="Stor",  cost=2, hp=2.5, size=32, crush="Mer",   spell="Mer",   splatter="Base", withdraw=True,  reabsorb=False)),
    ("Drott", dict(prefix="Drott", cost=3, hp=3.5, size=32, crush="Jatte", spell="Jatte", splatter="Mer",  withdraw=False, reabsorb=True)),
]
MOGEL_REFORM = {"Drott": "Litel", "Stor": "Litel", "Mogel": "Litel", "Litel": "Halv", "Halv": None}
MOGEL_REFORM_HP = 0.35    # share of the smaller body's normal HP it re-forms with (tuning knob)
MOGEL_AFF = dict(weak=["Slash"], resist=["Pierce"])   # plus: absorb own element, weak to its school's weaknesses
FAMILY_BODIES["Mogel"] = dict(HP=0.95, ATK=1.0, MAT=1.0, DEF=1.0, MDF=1.0, SPD=0.8, WIL=1.0)

# ---------------------------------------------------------------- speed groups (combat_spec Part 3)
# Actions resolve by group, highest first; SPD only orders units inside a group.
# An action may set "group" itself; otherwise its kind decides. Fear drops any action below the
# protection group to FEAR_GROUP (if not already lower). Protection (+3) is immune to Fear.
USE_SPEED_GROUPS = True
PROTECT_GROUP = 3
FEAR_GROUP = -1
SPEED_GROUP_BY_KIND = {"defend": 3, "cover": 3, "taunt": 3, "move": 1}

# ---------------------------------------------------------------- stat counters and status shapes (pillars Part 5c)
# One counter per stat, -STACK_CAP..+STACK_CAP: its own stacks plus its sources (statuses that also touch the stat),
# capped in total. Up and down cancel. A counter nobody pushed this round moves one step toward zero at its end.
# The named statuses ARE the counters: Blinded 2 is ACC at -2. MAT and MDF have no names yet.
STACK_CAP = 3
STAT_NAMES = {"ATK": ("Feeble", "Mighty"), "DEF": ("Sundered", "Fortified"), "ACC": ("Blinded", "Keen"),
              "EVA": ("Marked", "Nimble"), "SPD": ("Slowed", "Quick"), "MAT": (None, None), "MDF": (None, None)}
COUNTER_OF = {n: (stat, sign) for stat, pair in STAT_NAMES.items() for n, sign in zip(pair, (-1, 1)) if n}
COUNTER_OF["AccDown"] = ("ACC", -1)            # the Reyk spirits' old rider: Blinded 1
STACKS_BY_TIER = {"Halv": 1, "Base": 1, "Mer": 2, "Jatte": 3, "Ur": 3}   # a status move's stacks (Mer adds two)
FADE = (1.0, 0.5, 0.2)    # the fade shape: Frozen's chance to hold, action by action; Scorched's tick, round by round
KVAD_CAP = 3              # Song (Kvad; Nov 20, Joseph): a counter on each ally, up to three; a stack a tier per singing
PIN_ROUNDS = 2            # Pinned: rounds, plus one per extra stack (Mer 3, Jatte 4)
SCORCH_POWER = 1.2        # Scorched (Nov 20, Joseph: 1.2, about two hits over three rounds): one Eld hit at the tier's power x this x
                          # FADE[step], worked out from the caster's MAT against the target's MDF when it lands

# ---------------------------------------------------------------- statuses as data (refactor_plan Wave 1)
# The engine reads these rows; it doesn't know a status by name. Fields:
#   duration   rounds: a number, a (lo, hi) range rolled when applied, or None (until consumed)
#   reapply    "refuse" (already on: nothing happens) or "overwrite" (rolled fresh)
#   stats      {stat: stages} while on; or pick=(pool, n): n stats rolled from the pool, one stage down each (Cursed)
#   tick       share of max HP lost: when="round_start" or "action", with the log line ({name}, {dmg})
#   skip       loses the action: chance, whether the status is used up, the log line; checked in SKIP_ORDER
#   breaks_bide  a wind-up is lost if the unit carries it when the wind-up would fire
#   bide_pops  ...and losing the wind-up uses this status up (the net)
#   no_orders  the player isn't asked for an order (they couldn't act)
#   group      actions below the protection group drop to this group (Fear)
#   blocks_mp  MP moves can't be used (Silence)
#   shatter    a hit (not absorbed) multiplies its damage by this, and ends the status
#   fade       the fade shape: the skip's chance by step (FADE); a failed roll ends it ("thaw"); used up after the last
#   boss_immune  a Drott shrugs it off (turn-enders)
#   chain      a rider of this status, landing on someone who already has it, becomes this status (Chilled -> Frozen)
#   per_stack  rounds added per stack beyond the first (a Mer Pin lasts longer)
#   rooted     "cell": it can't leave its cell: no Move, Swap, Advance or glide, and no one can swap with it (Pinned;
#              Nov 20, Joseph). Cover moves no one, so it doesn't care. Forced moves (Kasta) will treat it as a wall
#   tick power the tick is a hit, not a share of HP: the caster's blow at the tier's power x this, worked out when it
#              lands (with the element and the target's affinity), x the fade step (Scorched)
#   flare      a hit of this element (not a graze) sets the fade back to its first step, keeping the blow (wind on a Scorch)
#   reapply "refresh": the longer of the two durations; "stack": a counter (Song): stacks add to `cap`, the heal is the
#              latest singer's, and a round nobody touched it, it loses a stack
#   tick heal  the tick heals instead (Song): stacks x the heal its last singer gave, at round start
STATUSES = {
    "Poisoned": dict(duration=STATUS_DURATION, reapply="refuse",
                     tick=dict(when="round_start", share=POISON_TICK, line="{name} takes {dmg} poison damage.")),
    "Bleeding": dict(duration=STATUS_DURATION, reapply="refuse",
                     tick=dict(when="action", share=BLEED_TICK, line="{name} bleeds for {dmg}.")),
    "Stunned":  dict(duration=STATUS_DURATION, reapply="refuse", breaks_bide=True, boss_immune=True,
                     skip=dict(chance=STUN_LOSE_CHANCE, used_up=True, line="{name} is stunned and loses the action!")),
    "Chilled":  dict(duration=CHILL_DURATION, reapply="overwrite", stats={"SPD": -1}, chain="Frozen"),
    "Frozen":   dict(duration=None, reapply="refuse", breaks_bide=True, no_orders="sure", shatter=SHATTER_MULT, boss_immune=True,
                     fade=FADE, skip=dict(chance=1.0, used_up=False, line="{name} is frozen solid."),
                     thaw="{name} thaws!"),
    "Bound":    dict(duration=None, reapply="refuse", breaks_bide=True, bide_pops=True, no_orders=True, boss_immune=True,
                     skip=dict(chance=1.0, used_up=True, line="{name} is caught in the net and loses the action!")),
    "Feared":   dict(duration=STATUS_DURATION, reapply="refuse", group=FEAR_GROUP),
    "Disarmed": dict(duration=STATUS_DURATION, reapply="refuse", stats={"ATK": -1, "MAT": -1}),
    "Cursed":   dict(duration=STATUS_DURATION, reapply="refuse", pick=(["ATK", "MAT", "DEF", "MDF"], 2)),
    "Silenced": dict(duration=STATUS_DURATION, reapply="refuse", blocks_mp=True),
    "Pinned":   dict(duration=PIN_ROUNDS, per_stack=1, reapply="refresh", stats={"SPD": -1}, rooted="cell"),   # Wave 4a
    "Song":     dict(duration=None, reapply="stack", cap=KVAD_CAP,     # Kvad: heals at round start, fades a stack when untouched
                     tick=dict(when="round_start", heal=True, line="{name}'s Song heals {dmg}.")),
    "Scorched": dict(duration=None, reapply="overwrite", fade=FADE, flare="Blast", element="Eld",   # a new Sveda: its own blow
                     tick=dict(when="round_start", power=SCORCH_POWER, line="{name} burns for {dmg}.")),
}
SKIP_ORDER = ["Bound", "Frozen", "Stunned"]
UNTIL_USED = 99           # the rounds a status with no duration carries (it ends when used)

# ---------------------------------------------------------------- the board (combat_spec Parts 5 and 6)
# Two rows of three per side. Every basic attack is single-target; shapes (row, column) belong to skills.
#   melee (Slash, Crush): reaches the enemy Front only; full from your Front, REAR_MELEE_MULT from your Rear.
#   reach (Pierce):       from your Front reaches Front or Rear; from your Rear reaches the Front.
#   any   (Skott, bows):  anywhere, full.   Spells, heals, buffs: anywhere, full.
# Protection: while anyone stands in a side's Front, its Rear can't be reached by melee.
# Exposure: a side with an empty Front has its Rear count as its Front for targeting.
USE_BOARD = True
# Range comes from the weapon (Nov 10), not the damage type: a wolf's teeth Pierce at Short range, a goblin's bow
# Pierces at Long, a Drattr's trident at Medium. A move with no weapon behind it is Short.
RANGES = {"Short": "melee", "Medium": "reach", "Long": "any"}    # the names players see -> the board's reach rules
RANGE_NAME = {v: k for k, v in RANGES.items()}
WEAPONS = {   # weapon: (damage type, range)
    "Bow": ("Pierce", "Long"), "Javelin": ("Pierce", "Long"), "Spear": ("Pierce", "Medium"), "Stikk": ("Pierce", "Short"),
    "Greatsword": ("Slash", "Short"), "Sword": ("Slash", "Short"), "Axe": ("Slash", "Short"),
    "Club": ("Crush", "Short"), "Hammer": ("Crush", "Short"), "Staff": ("Crush", "Short"),
}
# A root's own weapons, and its range in anyone else's hands: an Ullar who learns Krosh clubs with the bow (Short);
# an Ullar who learns Spett jabs with an arrow (Short). Skott is a shot: bows only, not learnable without one.
ROOT_WEAPONS = {"Skar": {"Greatsword", "Sword", "Axe"}, "Krosh": {"Club", "Hammer", "Staff"},
                "Spett": {"Stikk", "Spear"}, "Skott": {"Bow"}}
ROOT_RANGE = {"Skar": "Short", "Krosh": "Short", "Spett": "Short", "Skott": "Long"}
def root_range(root, weapon):
    """A martial root's range in these hands: the weapon's own when the root belongs to it, else the root's."""
    return WEAPONS[weapon][1] if weapon in ROOT_WEAPONS.get(root, ()) else ROOT_RANGE[root]
REACH_BY_TYPE = {"Slash": "melee", "Crush": "melee", "Pierce": "melee"}   # the fallback: no weapon, Short
REAR_MELEE_MULT = 0.5
SHAPE_MULT = {"row": 0.75, "column": 0.85}      # per target, for skills that carry a shape (tune)

# ---------------------------------------------------------------- martial grammar (spellbook Part 2)
MARTIAL_ROOT = {"Slash": "Skar", "Crush": "Krosh", "Pierce": "Spett"}   # bows: Skott

# ---------------------------------------------------------------- manners (spellbook Part 2; numbers live in grammar.py)
# The sim AI scores moves by expected damage, which can't see tempo. These weights stand in for it (AI knob, tune):
# a Snar move is worth more than its damage (it lands before the target acts), a Tung or Bid move less (it may never land).
AI_MANNER_VALUE = {"Snar": 1.15, "Tung": 0.80, "Bid": 0.45}   # Bid spends two rounds

# ---------------------------------------------------------------- rotation and Cover (combat_spec Parts 7-8; AI knobs, tune)
USE_ROTATION = True
ROT_HURT, ROT_HEALTHY = 0.40, 0.60   # a Front unit under 40% HP swaps with a melee unit over 60% behind it
ROT_SWAP_VALUE = 1.0                 # x the HP-share gap x ref damage
ROT_STEP_VALUE = 0.6                 # a Rear melee unit stepping into an empty Front spot
ROT_FALLBACK_VALUE = 0.4             # a caster in the Front falling back to an empty Rear spot
ROT_COVER_VALUE, ROT_COVER_HURT = 0.7, 0.30   # cover an ally under 30% HP
ROT_COVER_BIDE = 0.8                 # x the expected damage of a wind-up aimed at the ally
ROT_DEFEND_BIDE = 0.5                # brace: x the expected damage of a wind-up aimed at me
ROT_DODGE_BIDE = 0.8                 # swap out of a wind-up's path (it re-checks reach when it fires)

# Enemy bow and thrown moves follow the hero rule: a bow (Skott) reaches anywhere (combat_spec Part 6).
def strike_range(m, rank_weapon=None):
    """An enemy strike row's range name: its own weapon (an options dict's "weapon"), else the rank's weapon when
    the damage types agree, else Short (teeth, claws, horns, a fist)."""
    w = m[-1].get("weapon") if isinstance(m[-1], dict) else None
    if w is None and rank_weapon and WEAPONS[rank_weapon][0] == m[1]: w = rank_weapon
    return WEAPONS[w][1] if w else "Short"

# ---------------------------------------------------------------- painted spots (Mark-; the Mogel's slime paint) -- tune
MOGEL_PAINT_RANKS = {"Mogel", "Stor", "Drott"}
SPOT_IMPACT = 0.5         # x the move's damage, on whoever stands on the spot when it lands (affinity ignored)
SPOT_TICK = 0.5           # x the move's damage, at the start of each round, on whoever stands there
SPOT_ROUNDS = 3
AI_SPOT_TICKS = 1.0       # how many ticks the painter's AI expects to land (targets usually step off)
ROT_SPOT_VALUE = 1.2      # x the expected tick damage avoided, for stepping off a painted spot

# ---------------------------------------------------------------- the Barrow's folklore rules (bestiary Part 3; tune)
NET_VALUE = 1.0               # Net Throw's AI worth: x the best blow the netted hero would have struck...
NET_BIDE = 1.0                # ...plus x its wind-up's expected damage (netting a wind-up loses it)
BEIN_GUARDIANS = {"Halvbeinbryn", "Beinbryn", "Storbeinbryn", "Fornbein"}   # shield-bearers: Cover is their job
GUARDIAN_COVER = 2.0          # x a guardian's Cover value, and it covers allies under this much HP:
GUARDIAN_COVER_HURT = 0.5
BEINSEIDR_ELEMENTS = ["Natt", "Aska", "Eld", "Hrim", "Blixt"]   # bone-mages that adopt an element (not Sol: bone hates it)
BEIN_PILE_ROUNDS = 2          # a fallen Bein lies in a pile this many rounds, then stands again...
BEIN_REASSEMBLE_HP = 0.5      # ...at this share of its HP, unless a Crush blow scatters the pile first. Once only.
PILE_VALUE = 0.5              # AI: x the HP a pile would stand up with, for spending a Crush on it
DRAUGR_CRAWL_HP = 0.35        # a Draugr not beheaded (Slash) or burned (Eld) crawls on at this share of its HP. Once.
DRAUGR_FINAL = {"Slash", "Eld"}

# ---------------------------------------------------------------- Dying, Wounded, Dead (combat_spec Part 10; tune)
USE_DYING = True
HERO_BREATHS = 5              # a hero at 0 HP is Dying: a breath goes at the end of each round (not the one they fell in) and with each hit
WOUNDED_CUT = 0.25            # Wounded: max HP and MP cut by this share until Rest; Dying again while Wounded is death
AI_FINISH_VALUE = 1.5         # AI: x ref damage / breaths left, for a finishing blow on the Dying (worth most when it kills)
VAKNA = {                     # the revive ladder: who it reaches, what they stand up with, whether they're Wounded
    "Halv":  dict(reaches="Dying", hp=0.0,  wound=False),   # stabilises at 1 HP
    "Base":  dict(reaches="Dying", hp=0.20, wound=False),   # 1 HP and 20% of max
    "Mer":   dict(reaches="Dead",  hp=0.0,  wound=True),    # raises the Dead at 1 HP, Wounded
    "Jatte": dict(reaches="Dead",  hp=0.20, wound=True),
    "Ur":    dict(reaches="Dead",  hp=1.0,  wound=False),   # gear only
}

# ---------------------------------------------------------------- items (loop_spec Part 11; prices and powers tune)
# An item is a move with a fixed power rather than a stat: damage items hit as an average person of the user's level.
POUCH_SLOTS = 3
ITEMS = {
    "small_life":   dict(name="Small Life Draught",  kind="heal",   amount=0.25, stack=3, price=20),
    "life":         dict(name="Life Draught",        kind="heal",   amount=0.50, stack=2, price=50),
    "strong_life":  dict(name="Strong Life Draught", kind="heal",   amount=1.00, stack=1, price=100),
    "small_spirit": dict(name="Small Spirit Draught", kind="mp",    amount=0.25, stack=3, price=20),
    "spirit":       dict(name="Spirit Draught",      kind="mp",     amount=0.50, stack=2, price=50),
    "strong_spirit": dict(name="Strong Spirit Draught", kind="mp",  amount=1.00, stack=1, price=100),
    "surgeons_kit": dict(name="Surgeon's Kit",       kind="revive", tier="Halv", stack=3, price=60),
    "mead":         dict(name="Mead of Waking",      kind="revive", tier="Mer",  stack=1, price=150),
    "pocket_sand":  dict(name="Pocket Sand",         kind="stat",   stat="ACC", direction=-1, stack=3, price=30),
    "firecracker":  dict(name="Firecracker",         kind="damage", element="Force", power=20, stack=3, price=40),
    "thunderpot":   dict(name="Thunderpot",          kind="damage", element="Force", power=28, all=True, stack=1, price=200),
    "iron_knife":   dict(name="Iron Throwing Knife", kind="damage", element="Pierce", power=20, stack=3, price=40),
    "iron_axe":     dict(name="Iron Throwing Axe",   kind="damage", element="Slash",  power=20, stack=3, price=40),
    "iron_hammer":  dict(name="Iron Throwing Hammer", kind="damage", element="Crush", power=20, stack=3, price=40),
    "smoke_pot":    dict(name="Smoke Pot",           kind="flee",   stack=3, price=30),
}
ELEMENT["Force"] = dict(power=1.0, cost=1.0, var=0.1, hits=1, rider=None)   # affinity-free blast (Firecracker, Thunderpot)
AI_ITEM_THRIFT = 0.8          # AI: items are worth a little less than their effect (they cost money)

# ---------------------------------------------------------------- the Fight Lab (fight_lab_spec.md)
FLEE_BASE = 0.50            # Flee at even SPD (party average against enemy average)
FLEE_PER_QUARTER = 0.10     # +/- per 25% faster or slower
FLEE_MIN, FLEE_MAX = 0.10, 0.90
KNOW_HP_KILLS = 20          # fell this many of a family and rank to see its HP on Inspect
KNOW_MP_KILLS = 40          # ...and its MP

# ================================================================ the five classes' words (classes.md; refactor_plan Wave 2b)
# A verb is a class's basic move: its kind, what it touches, and its designated rider. Parts grow it (pillars Part 5c):
#   tier (Halv, Mer, Jatte; Ur on gear), target (Flok, All), manners (Snar, Tung, Bid, Jarf, Drif), Styng (adds damage),
#   Lonn (adds the designated rider). A rider is (what it adds, the name part it's spoken with): Skott's Bleeding is
#   spoken Blot (Blotskott); Peka's Sundered is spoken Lonn (Lonnpeka); Krosh's Sundered is spoken Brak (Brakrosh).
# Fields: kind; root (the damage type's word, for range and the board: Skott is a bow shot); element (damage type or
# element); status / stat / up (what it inflicts); target ("self", "ally", "allies", "enemy", "all"); rider; weight
# (cost steps built into the verb: the untie spells); knots (knot cost); free (costs nothing: Lya, Djupanda);
# styng (Styng is legal); targets (the target parts it may carve: none unless listed, review C09); pays_on (a status the move pays off on: Banskott on the Pinned); hits; group.
# pays (the multiplier a pays_on / pays_below move deals); answer (Hevn: stronger per hit taken); amount (Djupanda's MP);
# halv (it has a Halv fork: damage verbs only, Nov 20, Joseph: a free attack is fine, a free heal, taunt or knot breaks
# things); manner_power (this verb's own multiplier for a manner: Hevn's Bid doubles, the rest keep MANNERS').
# Kinds the engine doesn't resolve yet (song, knot, displace) arrive in Waves 4b and 4c.
DJUPANDA_SHARE = 0.40     # Djupanda: a wind-up (Bid), then this share of max MP
KVAD_SHARE = 4 / 9        # each stack heals its ally this share of the singer's Base Lak at round start (single target;
                          # Flokvad and Allkvad take their reach's share: a third, and ALL_SHARE of 4/9)
VERBS = {
    # Brennumar (Eld school; magical)
    "Eld":      dict(halv=True, targets=("Flok", "All"), cls="Brennumar", kind="damage", element="Eld", rider=("Scorched", "Sveda")),
    "Reyk":     dict(targets=("Flok", "All"), cls="Brennumar", kind="status", element="Reyk", status="Blinded", rider=("Poisoned", "Eitr"), styng=True),
    "Sveda":    dict(targets=("Flok", "All"), cls="Brennumar", kind="status", element="Eld", status="Scorched", rider=("Feeble", "Lonn"), styng=True),
    "Aukseid":  dict(cls="Brennumar", kind="stat", stat="MAT", up=True, target="self"),
    "Djupanda": dict(cls=None, kind="windfall", manners=("Bid",), free=True, target="self", amount=DJUPANDA_SHARE),   # any magical
    # Ullar (Bow; martial)
    "Skott":    dict(halv=True, targets=("Flok", "All"), cls="Ullar", kind="damage", root="Skott", element="Pierce", rider=("Bleeding", "Blot")),
    "Naglskott": dict(targets=("Flok", "All"), cls="Ullar", kind="status", root="Skott", element="Pierce", status="Pinned", styng=True),
    "Peka":     dict(targets=("Flok", "All"), cls="Ullar", kind="status", root="Skott", element="Pierce", status="Marked", rider=("Sundered", "Lonn"), styng=True),
    "Banskott": dict(targets=("Flok", "All"), cls="Ullar", kind="damage", root="Skott", element="Pierce", pays_on="Pinned", pays=1.5, halv=True),   # x1.5 on the Pinned
    "Avliva":   dict(cls="Ullar", kind="damage", root="Skott", element="Pierce", pays_below=0.5, pays=2.0, halv=True),   # Swedish "to put down": x2 under half HP
    "Skrida":   dict(cls="Ullar", kind="glide", stat="EVA", up=True, target="cell", group=1),   # aimed at a cell, like Move
    # Vasara (Hammer; martial)
    "Krosh":    dict(halv=True, targets=("Flok", "All"), cls="Vasara", kind="damage", root="Krosh", element="Crush", rider=("Sundered", "Brak")),
    "Egga":     dict(targets=("Flok",), cls="Vasara", kind="taunt", root="Krosh", target="enemy", rider=("Blinded", "Lonn"), styng=True),   # taunts one foe, or a row
    "Lya":      dict(cls="Vasara", kind="cover", target="ally", free=True),
    "Aukskold": dict(targets=("Flok", "All"), cls="Vasara", kind="stat", stat="DEF", up=True, target="self"),   # herself; Flok her row; All everyone
    "Hevn":     dict(cls="Vasara", kind="damage", answer=True, root="Krosh", element="Crush", halv=True,
                     manner_power={"Bid": 2.0}),   # +HEVN_PER_HIT a hit taken; Bidhevn releases double (Nov 20)
    # Dagskald (Sol school, child Lak; magical)
    "Lak":      dict(targets=("Flok", "All"), cls="Dagskald", kind="heal", element="Lak", target="ally", rider=(("EVA", 1), "Sol")),   # Solak: and Nimble (Nov 20)
    "Sol":      dict(halv=True, targets=("Flok", "All"), cls="Dagskald", kind="damage", element="Sol", rider=("Blinded", "Blinda")),   # Blindasol
    "Kvad":     dict(targets=("Flok", "All"), cls="Dagskald", kind="song", target="ally"),   # a Song stack a tier on one ally (Nov 20)
    "Skolja":   dict(targets=("All",), cls="Dagskald", kind="cleanse", target="ally"),
    "Vakna":    dict(cls="Dagskald", kind="revive", target="fallen"),
    "Aukraft":  dict(targets=("All",), cls="Dagskald", kind="stat", stat="ATK", up=True, target="ally", rider=(("DEF", 1), "Lonn")),
    # Skurmar (Blast school, child Blixt; magical)
    "Blast":    dict(halv=True, targets=("Flok", "All"), cls="Skurmar", kind="damage", element="Blast"),
    "Knyta":    dict(cls="Skurmar", kind="knot", target="self"),
    "Blixt":    dict(halv=True, targets=("Flok", "All"), cls="Skurmar", kind="damage", element="Blixt", rider=("Stunned", "Lonn")),
    "Kuling":   dict(cls="Skurmar", kind="damage", element="Blast", target="all", weight=1, knots=1),
    "Storm":    dict(cls="Skurmar", kind="damage", element="Blast", target="all", weight=2, knots=2, tier="Mer"),
    "Orkan":    dict(cls="Skurmar", kind="damage", element="Blast", target="all", weight=3, knots=3, tier="Mer", follow="Blixt"),
    "Kasta":    dict(cls="Skurmar", kind="displace", push=True, styng=True),
    "Svepa":    dict(cls="Skurmar", kind="displace", push=False, styng=True),
    "Medvind":  dict(targets=("Flok", "All"), cls="Skurmar", kind="stat", stat="SPD", up=True, target="ally"),   # Swedish "tailwind": Quick
}

# Upgrade parts beyond tier, target and manner (pillars Part 5c). The cap: at most UPGRADE_CAP parts on one move;
# a capstone is a named set beyond it (found, not carved).
STYNG_POWER = 0.7        # Styng: a hit added to a move with no damage of its own, at 70% of the tier's power (Lonn never weakens)
UPGRADE_CAP = 2
CAPSTONES = {            # name: (verb, its parts as a frozen set). Holm and Hasin settle in the mutation session.
    "Tusensplitter": ("Skott", frozenset({"Drif", "Mer", "Lonn"})),
    "Pilskur":       ("Skott", frozenset({"All", "Mer", "Lonn"})),
    "Skogsbrand":    ("Sveda", frozenset({"All", "Mer", "Styng", "Lonn"})),
}
# Bynames: a move within the cap whose spoken name runs past BYNAME_LETTERS gets a name of its own (Nov 20). Which
# parts each verb accepts settles in the mutation session; then every reachable long name needs a byname here.
BYNAME_LETTERS = 15
BYNAMES = {
    "Geirskott": ("Naglskott", frozenset({"Mer", "Styng"})),   # ON geirr, "spear": a pike-length shaft that pins the leg
}

# Costs as a share of the hero's own bar (pillars Part 5c): a plain base move costs the base share; each upgrade part
# multiplies it by the step; Halv is free. MP: 1/16, 1/10, 1/6, ~1/4. HP: 1/36, 1/24, 1/16, ~1/10.
BASE_SHARE = {"MP": 1 / 16, "HP": 1 / 36}
PART_STEP = {"MP": 1.6, "HP": 1.5}
TIER_WEIGHT = {"Halv": 0, "Base": 0, "Mer": 1, "Jatte": 2, "Ur": 3}   # every tier priced on purpose (review C08)

# Where a move comes from decides the highest tier PART it may add (pillars Part 5c; review C08): carving adds Mer,
# a found move (tome, reward) Jatte, gear Ur. A rung climbs from the verb's own (Merorkan: Orkan is Mer, so Jatte), but
# only gear may result in Ur: Storm + a found Jatte is refused, not a cheap Ur.
SOURCE_TIER = {"carve": "Mer", "find": "Jatte", "gear": "Ur"}

# Which manners a move can take, by what its effect can use (review C11, A02). Speed manners conflict: one at most.
# Bid is timing, not speed: Bid with one speed manner is the meteor (Bid + Tung lands Heavy).
SCALES = {"damage", "heal"}                           # effects with a power the manners can scale (Hevn is damage)
HITS = {"damage"}                                     # effects that roll hits (crits, flurries)
MANNER_NEEDS = {"Snar": None, "Tung": SCALES, "Bid": SCALES, "Jarf": HITS, "Drif": HITS}
SPEED_MANNERS = {"Snar", "Tung"}
TARGET_PARTS = {"Flok", "All"}                        # the target parts a class verb can carve (Mark is enemies' paint)
# Reach is a real choice (Nov 20, Joseph): Flok a row at 75% each for one step; All everyone at 60% each for two steps;
# Mer one target at 140% for one. Prices only: the parts count once each against UPGRADE_CAP. Old fights keep 0.75.
TARGET_STEPS = {"Flok": 1, "All": 2}
ALL_SHARE = 0.60          # a carved All's per-target share (damage, heals, a Scorch's blow, a Song's heal)

# Speed-group keywords (pillars Part 5c), printed on move cards; the glossary gives the hover line.
GROUP_KEYWORD = {3: "First", 1: "Swift", -1: "Late", -2: "Heavy", -3: "Last"}
KEYWORDS = {
    "First": "Acts before nearly every other move, whatever its speed.",
    "Swift": "Goes before normal moves. Among Swift moves, the faster character goes first.",
    "Late": "Goes after normal moves.",
    "Heavy": "Goes after nearly everything.",
    "Last": "Goes after everything else.",
    "Patient": "Winds up this round and lands next round. Lost if you're stunned, frozen or netted.",
}

# Kit snapshots for the sweep (agreed Nov 20): (verb, parts). Defend, Meditate, items, Move and Flee are always there.
def W(verb, **parts): return (verb, parts)
KITS = {
    "Vasara":    {1: [W("Krosh"), W("Egga")],
                  2: [W("Krosh"), W("Egga"), W("Krosh", lonn=True), W("Lya")],
                  3: [W("Krosh", lonn=True, manners=("Snar",)), W("Egga", lonn=True), W("Lya"), W("Hevn")]},
    "Ullar":     {1: [W("Skott"), W("Naglskott")],
                  2: [W("Skott", lonn=True), W("Naglskott"), W("Peka")],
                  3: [W("Skott", lonn=True, tier="Mer"), W("Naglskott", styng=True), W("Peka", lonn=True), W("Banskott")]},
    "Brennumar": {1: [W("Eld"), W("Reyk")],
                  2: [W("Eld"), W("Reyk"), W("Sveda"), W("Eld", target="All")],
                  3: [W("Eld", tier="Mer"), W("Eld", target="All"), W("Sveda", lonn=True), W("Djupanda")]},
    "Dagskald":  {1: [W("Lak"), W("Sol")],
                  2: [W("Lak"), W("Sol"), W("Kvad")],
                  3: [W("Lak", lonn=True), W("Sol"), W("Kvad", target="All"), W("Aukraft", target="All")]},   # Allkvad (Nov 20)
    "Skurmar":   {1: [W("Blast"), W("Knyta")],
                  2: [W("Blast"), W("Knyta"), W("Kuling"), W("Blixt")],
                  3: [W("Blast"), W("Knyta", tier="Mer"), W("Storm"), W("Blixt", lonn=True)]},
}

# ================================================================ class sheets (refactor_plan Wave 3)
# Fixed characters (pillars Part 4): each class has one stat block at one power level, and its kit by leg (KITS).
# Stats: an average body (genes 15.5) grown the class's way to SHEET_LEVEL; no Personality, no star sign.
# Affinities (agreed Nov 20): magicals take their school's; martials their weapon weakness plus one authored
# elemental weakness and resistance. SHEET_LEVEL is a knob until the level sweep freezes it.
SHEET_LEVEL = 50          # Nov 20: heroes and enemies at 50 (the sweep: level isn't the lever; 50 keeps numbers 3 digits)
CLASS_AFFINITY = {
    "Ullar":  dict(weak=["Slash", "Eld"], resist=["Hrim"]),     # Ullr of the skis and the winter: frost-hardy
    "Vasara": dict(weak=["Pierce", "Blixt"], resist=["Eld"]),   # the anvil shrugs off fire; lightning finds the iron
}
BASIC_VERB = {"Vasara": "Krosh", "Ullar": "Skott", "Brennumar": "Eld", "Dagskald": "Sol", "Skurmar": "Blast"}  # its free Halv
MEDITATE_SHARE = 0.15     # Meditate: this share of max MP back; magicals only, a universal action (a knob: the sweep tunes)
AI_MEDITATE_VALUE = 1.2   # AI: x ref x the MP share it would restore
AI_TAUNT_VALUE = 0.6      # AI: x ref per ally Egga would shield (hurt, or a wind-up's target)

# ---------------------------------------------------------------- Wave 4a: the starting three's mechanics (Nov 20 defaults)
PIERCE_GAP = 0.15         # Pierce finds the gaps: +15% Pierce damage per DEF-down stack on the target (new game)
HEVN_PER_HIT = 0.25       # Hevn: +25% per hit she took since her last action...
HEVN_CAP = 1.0            # ...up to +100%
AI_DOT_VALUE = 0.8        # AI: x the HP a Scorch would burn (it lands over three rounds)
AI_ALSO_VALUE = 0.4       # AI: x ref for a second status riding the first (Lonnsveda's Feeble, Lonnpeka's Sundered)
AI_PAYOFF_VALUE = 0.5     # AI: x ref for a status someone on the side can cash in (Pinned, with a Banskott)
AI_SONG_VALUE = 1.2       # AI: x the healing a verse adds at the next round's start (what's missing now)...
AI_SONG_HOPE = 0.25       # ...plus this share of a verse's full healing, for the hits still to come
AI_GLIDE_VALUE = 0.6      # AI: x ref for a glide out of the Front (the Ullar wants the Rear), +0.15 for the Nimble

# ---------------------------------------------------------------- the new game's tuning settings (Nov 20; the sweep tunes)
# They apply only in fights whose whole party is sheet heroes (build_hero), so old recruits and every legacy
# regression are untouched. Hero power is baked into the character (not a buff); enemy damage and HP by tier are
# applied to the enemies when the fight starts, and again when a Mogel re-forms.
ENEMY_LEVEL = 50
HERO_POWER = {c: 1.2 for c in ("Vasara", "Ullar", "Brennumar", "Dagskald", "Skurmar")}   # x damage dealt (not items); Nov 20: 1.2 with the stat blocks
ENEMY_DAMAGE = 2.25       # x damage enemies deal (Nov 20: the solver's 2.23, rounded)
ENEMY_ACTIONS = 1         # each enemy acts once a round (Nov 20); a multi-stage move is authored on the move, not as actions
# The classes' stat blocks (Nov 20, Joseph): multipliers on derived stats, in the families' value scale (HP, ATK, MAT 1;
# DEF, MDF, SPD 0.5; WIL 0.25), each within +0.1 of neutral; a stat the class never uses stays at 1.0.
CLASS_BODIES = {
    "Vasara":    dict(HP=1.25, ATK=0.85, DEF=1.25, MDF=1.0, SPD=0.75),   # the anvil: takes the hits, slow
    "Ullar":     dict(HP=0.85, ATK=1.2, DEF=0.85, MDF=0.9, SPD=1.3),     # fast and deadly, fragile
    "Brennumar": dict(HP=0.8, MAT=1.3, DEF=0.85, MDF=1.0, SPD=1.0),      # glass cannon
    "Dagskald":  dict(HP=1.05, MAT=0.9, DEF=1.0, MDF=1.25, SPD=0.9),     # hardy against magic, steady
    "Skurmar":   dict(HP=0.85, MAT=1.15, DEF=0.85, MDF=1.0, SPD=1.3),    # tempo: quick, light
}
TIER_HP = {"Trash": 1.0, "Regular": 1.0, "Elite": 1.65, "Boss": 1.75}   # x enemy HP by tier: the rank reshape (Nov 20)
def enemy_tier(u):
    """The pace table's tier of an enemy (pillars Part 5b): the 3-cost Drott is Boss, Halv and Litel Trash, Stor Elite."""
    if getattr(u, "rank", None) == "Drott" or getattr(u, "actions_per_round", 1) >= 3: return "Boss"
    n = getattr(u, "rank_name", None) or getattr(u, "mogel_rank", None) or getattr(u, "rank", None) or u.name
    if n.startswith(("Halv", "Litel")): return "Trash"
    if n.startswith("Stor"): return "Elite"
    return "Regular"
