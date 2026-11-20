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
    "Brennumar": dict(kind="caster", school="Eld", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Hafrunar":  dict(kind="caster", school="Vatn", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Skurmar":   dict(kind="caster", school="Blast", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "WIS"]),
    "Lundar":    dict(kind="caster", school="Jord", mat={"INT": 1.0}, atk={"STR": 1.0},
                      train=["INT", "CON"]),
    "Dagskald":  dict(kind="caster", school="Sol", mat={"WIS": 1.0}, atk={"STR": 1.0},
                      train=["WIS", "CON"]),
    "Seidar":    dict(kind="caster", school="Natt", mat={"INT": 0.5, "WIL": 0.5},
                      atk={"STR": 1.0}, train=["INT", "WIL"]),
    # martials
    "Ullar":     dict(kind="martial", dmg="Pierce", weak="Slash", atk={"DEX": 1.0},
                      mat={"INT": 1.0}, train=["DEX", "CON"]),
    "Nalarbani": dict(kind="martial", dmg="Pierce", weak="Crush",
                      atk={"DEX": 0.5, "SPD": 0.5}, mat={"INT": 1.0}, train=["DEX", "SPD"]),
    "Hersir":    dict(kind="martial", dmg="Slash", weak="Pierce",
                      atk={"STR": 0.5, "DEX": 0.5}, mat={"INT": 1.0}, train=["STR", "DEX"]),
    "Huskarl":   dict(kind="martial", dmg="Slash", weak="Crush",
                      atk={"STR": 0.75, "CON": 0.25}, mat={"INT": 1.0}, train=["STR", "CON"]),
    "Berserker": dict(kind="martial", dmg="Crush", weak="Slash", atk={"STR": 1.0},
                      mat={"INT": 1.0}, train=["STR", "CON"]),
    "Vasara":    dict(kind="martial", dmg="Crush", weak="Pierce",
                      atk={"STR": 0.5, "CON": 0.5}, mat={"INT": 1.0}, train=["STR", "CON"]),
}
CASTERS = [c for c, d in CLASSES.items() if d["kind"] == "caster"]
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
SPIRIT_DMG_SCALE = 0.5   # multiplies enemy STR and INT (physical families)
ANDE_MAT_SCALE = 0.65    # Ande spirits are pure casters: a little more bite...
ANDE_MP_MULT = 2.0       # ...and deeper MP pools, since they can't fall back on free strikes
HELVAD_CHANCE = 0.25     # base chance of instant death, before WIL and Aska affinity

# ---------------------------------------------------------------- martial families (the undead)
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
                                   ("status", "Feared", "Base"), ("status", "Cursed", "Base")]),
        ]),
    "Bein": dict(
        aff=dict(weak=["Crush", "Sol"], resist=["Slash", "Pierce", "Natt", "Aska"]),
        ranks=[
            ("Halvbein", 1, 1.0, [("strike", "Pierce", "Bone Jab", "Halv"), ("strike", "Pierce", "Volley", "Halv", True)]),
            ("Bein", 2, 2.0, [("strike", "Slash", "Old Sword", "Base"), ("strike", "Pierce", "Spear", "Base"),
                              ("strike", "Pierce", "Volley", "Base", True)]),
            ("Storbein", 2, 2.5, [("strike", "Slash", "Old Sword", "Mer"), ("strike", "Pierce", "Spear", "Mer"),
                                  ("strike", "Pierce", "Volley", "Base", True), ("stat", "DEF", 1, "Base")]),
            ("Fornbein", 3, 3.5, [("strike", "Slash", "Old Sword", "Jatte"), ("strike", "Pierce", "Volley", "Mer", True),
                                  ("strike", "Pierce", "Barbed Arrow", "Mer", False, "Bleeding"),
                                  ("stat", "DEF", 1, "Base", True)]),
        ]),
}

# ---------------------------------------------------------------- the Drattr (the catch)
# Hunted water creatures: weak to the spear. ON drattr, "a pull, a haul"; Swedish fors, "rapids".
FAMILIES["Drattr"] = dict(
    aff=dict(weak=["Pierce", "Jord", "Reyk"], resist=["Slash", "Vatn", "Hrim"]),
    ranks=[
        ("Halvdrattr", 1, 1.0, [("strike", "Crush", "Tail Slap", "Halv"), ("strike", "Crush", "Thrash", "Halv", True)]),
        ("Drattr", 2, 2.0, [("strike", "Crush", "Tail Slap", "Base"), ("spell", "Vatn", "Base"),
                            ("spell", "Vatn", "Base", True), ("cleanse", "Base")]),
        ("Stordrattr", 2, 2.5, [("strike", "Crush", "Breach", "Mer"), ("spell", "Vatn", "Mer"),
                                ("spell", "Vatn", "Base", True), ("spell", "Hrim", "Base")]),
        ("Forsdrattr", 3, 3.5, [("strike", "Crush", "Falls Crash", "Jatte"), ("spell", "Vatn", "Jatte"),
                                ("spell", "Vatn", "Mer", True), ("cleanse", "Base", True)]),
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

# ---------------------------------------------------------------- the Oskorei (the Wild Hunt)
# Fixed formations. Every hunter is Blast school plus the martial weakness of the class it mirrors.
# Hunt Horn: while a horn-bearer lives, every enemy in the formation gets +1 ACC.
# unit: (name, cost, hp, martial weakness, horn?, moves)
OSKOREI_TIERS = {
    1: [("Halvoskorei Axe", 1, 1.0, "Crush", False, [("strike", "Slash", "Axe", "Halv"), ("spell", "Blast", "Halv", True)]),
        ("Halvoskorei Hammer", 1, 1.0, "Pierce", False, [("strike", "Crush", "Hammer", "Halv"), ("spell", "Blast", "Halv", True)]),
        ("Halvoskorei Bow", 1, 1.0, "Slash", False, [("strike", "Pierce", "Arrow", "Halv"), ("spell", "Blast", "Halv", True)]),
        "hound", "hound", "hound"],
    2: [("Ryttar", 2, 2.0, "Pierce", False, [("strike", "Crush", "Ride Down", "Base"),
                                              ("strike", "Slash", "Spectral Blade", "Base"), ("strike", "Crush", "Trample", "Base", True),
                                              ("stat", "DEF", 1, "Base")]),
        ("Hornblasar", 2, 2.0, "Slash", True, [("spell", "Blast", "Base"), ("spell", "Blixt", "Base"),
                                                ("spell", "Blast", "Base", True), ("status", "Silenced", "Base")]),
        "hound", "hound"],
    3: [("Storoskorei Greatsword", 2, 2.5, "Pierce", False, [("strike", "Slash", "Greatsword", "Mer"),
                                                              ("strike", "Slash", "Cleave", "Base", True), ("spell", "Blast", "Mer")]),
        ("Storoskorei Stiletto", 2, 2.5, "Crush", False, [("strike", "Pierce", "Stiletto", "Mer"),
                                                           ("strike", "Pierce", "Blot", "Base", False, "Bleeding"), ("spell", "Blast", "Mer")]),
        ("Storoskorei Maul", 2, 2.5, "Slash", False, [("strike", "Crush", "Maul", "Mer"), ("spell", "Blixt", "Mer"),
                                                       ("stat", "DEF", -1, "Base")])],
    4: [("Huntmaster", 3, 3.5, "Pierce", True, [("strike", "Slash", "Hunt's Edge", "Jatte"),
                                                 ("strike", "Pierce", "Rain of Spears", "Mer", True),
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

# ---------------------------------------------------------------- the board (combat_spec Parts 5 and 6)
# Two rows of three per side. Every basic attack is single-target; shapes (row, column) belong to skills.
#   melee (Slash, Crush): reaches the enemy Front only; full from your Front, REAR_MELEE_MULT from your Rear.
#   reach (Pierce):       from your Front reaches Front or Rear; from your Rear reaches the Front.
#   any   (Skott, bows):  anywhere, full.   Spells, heals, buffs: anywhere, full.
# Protection: while anyone stands in a side's Front, its Rear can't be reached by melee.
# Exposure: a side with an empty Front has its Rear count as its Front for targeting.
USE_BOARD = True
REACH_BY_TYPE = {"Slash": "melee", "Crush": "melee", "Pierce": "reach"}
REAR_MELEE_MULT = 0.5
SHAPE_MULT = {"row": 0.75, "column": 0.85}      # per target, for skills that carry a shape (tune)

# ---------------------------------------------------------------- martial grammar (spellbook Part 2)
MARTIAL_ROOT = {"Slash": "Skar", "Crush": "Kross", "Pierce": "Spett"}   # bows: Skott
