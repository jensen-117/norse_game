"""The glossary: what every word in the game means, where it comes from, and how the game says it (grammar library L1).

Kept out of the engine-hashed files (data, words, engine, lab) on purpose: a change of meaning or reading here never
changes the engine stamp, so it never invalidates a fight record. The code is the truth for what a word *does*;
lexicon.py reads that from the code and joins it to these entries. This file is the truth for what a word *means*.

One entry per atom: a root, a part, a name that stands for a whole move, a class, a family, a status, a keyword, an
item. Compounds the rules build (Brakrosh, Allmereld, Storeldmogel) get no entry: the book takes them apart into their
atoms. The test (test_gloss.py) checks both ways: every atom in the code has an entry, and every entry marked built is
in the code.

Fields
  kind    the book's section (KINDS)
  means   the meaning in a few words, as the player learns it
  origin  the source word, with its own spelling and pronunciation; "?" where Joseph coined it or the source isn't
          written down yet; None for plain English words. The source's pronunciation lives only here (Joseph, Nov 21: the game reading wins).
  say     the game's reading, in plain English respelling, the stressed syllable in capitals. Old-language words only.
          A first draft for Joseph's correction, built on one key (READING_KEY).
  state   built (in the code), planned (agreed, not built), pocket (held for later)
  note    anything a reader needs: renames, collisions, which verb owns a rider word
  was     earlier names, so old docs and fight records still read
  owner   for a planned word with no verb yet: the class it is meant for (roles.md)
"""

READING_KEY = [
    "The stressed syllable is in capitals; it is nearly always the first.",
    "j says y: Jord is YORD, Jarf is YARF.",
    "a says ah, e says eh, i says ih, o says oh, u says oo, y says ee; ey says ay (Reyk is RAKE).",
    "Doubled letters are said once: Natt is NAHT.",
    "A final -r after a consonant gets a light vowel: Draugr is DROW-gur, Drattr is DRAHT-ur.",
    "Seams are said as one word: Brakrosh is BRAHK-rosh, not two words.",
]

KINDS = {   # the book's sections, in the order the book shows them
    "element":   "Elements and damage types",
    "tier":      "Tiers: how strong",
    "target":    "Targets: how wide",
    "manner":    "Manners: how it moves",
    "upgrade":   "Upgrades: what it adds",
    "direction": "Up and down",
    "stat":      "Stat words",
    "status_root": "Status words",
    "rider":     "Rider words",
    "weapon":    "Weapon roots",
    "verb":      "Class verbs",
    "name":      "Names that stand for a whole move",
    "name_part": "Parts of names",
    "class":     "Classes",
    "family":    "Creature families",
    "rank":      "Ranks and jobs",
    "status":    "Statuses (what you wear)",
    "counter":   "Counters (stages, worn as names)",
    "keyword":   "Keywords (when it acts)",
    "affinity":  "Affinity (what a hit does to you)",
    "action":    "Universal actions",
    "item":      "Items",
    "myth":      "Myth",
}

def g(kind, means, origin=None, say=None, state="built", note=None, was=None, owner=None):
    return dict(kind=kind, means=means, origin=origin, say=say, state=state, note=note, was=was, owner=owner)

GLOSS = {
    # ------------------------------------------------------------------ elements (spellbook Part 1; Swedish friends checked them)
    "Eld":   g("element", "fire", "Old Norse eldr, fire (Swedish eld)", "ELD"),
    "Reyk":  g("element", "smoke; Eld's child: blinds, patches fire's weakness", "Old Norse reykr, smoke (Swedish rök)", "RAKE"),
    "Vatn":  g("element", "water", "Old Norse vatn, water (Swedish vatten)", "VAHT-un"),
    "Hrim":  g("element", "rime, frost; Vatn's child: chills, then freezes", "Old Norse hrím, rime", "HREEM",
               note="English rime is the same word."),
    "Blast": g("element", "wind; light, spread, several hits", "Swedish blåst, wind", "BLAHST",
               note="Reads as English blast, which fits."),
    "Blixt": g("element", "lightning; Blast's child: spiky, single target", "Swedish blixt, lightning", "BLIXT"),
    "Jord":  g("element", "earth; steady, cheap", "Old Norse jǫrð, Swedish jord, earth", "YORD",
               note="Teaches the j-is-y reading the other words lean on."),
    "Gro":   g("element", "growth, nature; Jord's child: damage over time", "Swedish gro, to sprout", "GROH",
               note="Keeps its vowel at a seam: Groande, not Grande."),
    "Sol":   g("element", "sun, daylight; smites the dark and the undead", "Swedish and Old Norse sól, sun", "SOHL"),
    "Lak":   g("element", "healing; Sol's child", "Swedish läka, to heal", "LAHK"),
    "Natt":  g("element", "night, shadow", "Swedish natt, night", "NAHT"),
    "Aska":  g("element", "ash, decay; Natt's child: small damage, a chance to curse", "Swedish aska, ash", "AHS-kah"),
    "Slash": g("element", "the blade's damage type"),
    "Pierce": g("element", "the point's damage type"),
    "Crush": g("element", "the blow's damage type"),
    "Force": g("element", "raw force: bombs and bumps, no affinity reads it"),

    # ------------------------------------------------------------------ tiers
    "Halv":  g("tier", "half: the weak, cheap form; every class's basic attack", "Swedish halv, half", "HAHLV",
               note="A kit pick since Nov 21: you have the Halv only if you picked it."),
    "Mer":   g("tier", "more: one rung up", "Swedish mer, more", "MEHR", note="Replaced Stor- as the second tier."),
    "Jatte": g("tier", "giant: two rungs up; found, not carved", "Swedish jätte, giant", "YAHT-teh"),
    "Ur":    g("tier", "primal: the top rung; only on gear", "Swedish and German ur-, primal, first", "OOR"),

    # ------------------------------------------------------------------ targets
    "Flok":  g("target", "a row", "Old Norse flokkr, a band, a troop (Swedish flock)", "FLOHK"),
    "All":   g("target", "everyone on a side", "English and Swedish all", "AHL", note="Said as in English."),
    "Mark":  g("target", "a spot on the ground: whoever stands there is hit", "Swedish mark, ground", "MAHRK",
               note="Reads as English 'mark the spot'. Not the Marked counter."),

    # ------------------------------------------------------------------ manners
    "Snar":  g("manner", "swift: acts a group sooner, a little weaker", "Old Norse snarr, Swedish snar, quick", "SNAHR"),
    "Tung":  g("manner", "heavy: acts late, hits harder", "Swedish tung, heavy", "TOONG"),
    "Bid":   g("manner", "bide: winds up a round, then lands much harder; lost if broken", "Old Norse bíða, Swedish bida, to wait", "BEED",
               note="English bide is the same word."),
    "Jarf":  g("manner", "reckless: weaker, dearer, and crits often and hard", "Old Norse jarfr, the wolverine (Swedish järv)", "YARF",
               was="Djarf (bold), dropped: it trips English readers."),
    "Drif":  g("manner", "flurry: small hits that keep coming on a coin flip", "Old Norse drífa, a shower of missiles", "DRIFF"),

    # ------------------------------------------------------------------ upgrades
    "Styng": g("upgrade", "adds a hit to a move that does no damage of its own", "coined (Joseph): chosen to evoke English sting", "STING"),
    "Lonn":  g("upgrade", "adds the move's own rider: a status or a stage", "Joseph's, from an old search (the second n may be his)", "LOHN",
               note="Shows in a name only where the rider has no word of its own (Lonnpeka); otherwise the rider's word shows (Brakrosh)."),

    # ------------------------------------------------------------------ stat grammar
    "Auk":   g("direction", "up: raises a stat", "Old Norse auka, to increase", "OWK"),
    "Ned":   g("direction", "down: lowers a stat", "Swedish ned, down", "NEHD"),
    "Kraft": g("stat", "ATK, striking power", "Swedish kraft, force", "KRAHFT"),
    "Skold": g("stat", "DEF, armour", "Swedish sköld, shield", "SKOHLD"),
    "Seid":  g("stat", "MAT, spell power", "Old Norse seiðr, sorcery (Swedish sejd)", "SADE"),
    "Stav":  g("stat", "MDF, magic defence", "stave, as in the Icelandic galdrastafir, protective magic staves", "STAHV"),
    "Hitt":  g("stat", "ACC, aim", "Swedish and Old Norse hitta, to find, to hit", "HIT", note="Reads as English hit."),
    "Vig":   g("stat", "EVA, dodging", "Swedish vig, nimble", "VEEG"),
    "Rask":  g("stat", "SPD, speed", "Old Norse rǫskr, Swedish rask, quick", "RAHSK"),

    # ------------------------------------------------------------------ status words
    "Eitr":  g("status_root", "venom: poisons", "Old Norse eitr, venom (Swedish etter); Ymir was born of it, and Thor dies of it", "AY-tur"),
    "Nid":   g("status_root", "scorn-curse: curses", "Old Norse níð, the scorn-pole níðstǫng (Swedish nid, a lampoon)", "NEED",
               note="Planned to give way to Dokkn as Cursed's word (beinar_pilot)."),
    "Ogn":   g("status_root", "terror: fears; planned, also pushes a foe toward weak on an element", "Old Norse ógn, terror (said OG-n; the game reads OH-gun)", "OH-gun",
               note="Ogn is the spell, Feared the status. Ognjord: OH-gun-yord."),
    "Blinda": g("status_root", "to blind (on Sol: dazzled)", "Swedish blinda, to blind", "BLIN-dah",
                note="A rider word on Sol (Blindasol); Egga's Blinded is Rod."),
    "Mogl":  g("status_root", "mould, rot: disarms", "Swedish mögel, mould", "MOH-gul"),
    "Helvad": g("status_root", "Hel's wager: a chance of death", "Hel, the death goddess, + Swedish vad, a bet (Swedish hel also means whole: all-in)", "HEL-vahd"),
    "Bann":  g("status_root", "ban: silences", "Old Norse and Swedish bann, a ban", "BAHN",
               note="Collision to settle: Bann (Silenced), Bannenlykt (a Mark), Banskott (bani, slayer) all start the same."),
    "Lokavad": g("status_root", "Loki's wager: kill, or die trying", "Loki + Swedish vad, a bet; Loki bet his head against Brokkr", "LOH-kah-vahd", state="pocket"),
    "Dokkn": g("status_root", "dark: curses (Hexed and Poisoned)", "Old Norse døkkr, dark", "DOHK-un", state="planned", was="Nid"),
    "Mot":   g("status_root", "against: makes Steadfast; pushes a foe toward resist on an element", "Old Norse mót, Swedish mot, against", "MOHT", state="planned",
               note="No n: Motnjord's 'tnj' is hard in English."),
    "Vingla": g("status_root", "to totter: leaves the target Reeling", "Swedish vingla, to totter", "VING-lah", state="planned",
                note="Not Ving: -ving reads as an English -ing (Snarving, starving).", owner="Berserker"),

    # ------------------------------------------------------------------ rider words (a rider's word belongs to its verb)
    "Blot":  g("rider", "blood: Bleeding (on Skott)", "coined (Joseph): blood; Blotskott is the bloodshot", "BLOHT",
               note="A Swede also hears blot, the old blood-sacrifice (Old Norse blót): a fitting echo for a bleeding wound."),
    "Brak":  g("rider", "a crack: Sundered (on Krosh)", "Swedish and Old Norse brak, a crash", "BRAHK"),
    "Lam":   g("rider", "lame: Feeble (on Sveda)", "Swedish lam, lame, palsied", "LAHM"),
    "Rod":   g("rider", "red: Blinded with rage (on Egga)", "Swedish röd, red: seeing red", "ROHD"),
    "Stel":  g("rider", "stiff: Stunned (on Blixt)", "Swedish stel, stiff", "STEHL"),
    "Sveda": g("rider", "to scorch: Scorched (on Eld)", "Swedish sveda, to singe (Old Norse svíða)", "SVEH-dah",
               note="Also Brennumar's verb."),

    # ------------------------------------------------------------------ weapon roots
    "Skar":  g("weapon", "a cut: the Slash strike", "Swedish skar, cut (from skära)", "SKAHR"),
    "Krosh": g("weapon", "a blow: the Crush strike; the Vasara's hammer", "Swedish krossa, to crush", "KROSH", was="Kross"),
    "Spett": g("weapon", "a skewer: the Pierce strike, with reach", "Swedish spett, a spit", "SPET"),
    "Skott": g("weapon", "a shot: the bow; reaches anywhere", "Swedish skott, a shot", "SKOHT", note="Also the Ullar's verb."),
    "Hugg":  g("weapon", "a chop", "Old Norse hǫgg, a blow", "HOOG", state="pocket", note="Takes Skar's place if Skar doesn't land with players."),
    "Udd":   g("weapon", "a blade's point: pierces through the Front", "Swedish udd, Old Norse oddr, a point", "OOD", state="pocket"),
    "Stikk": g("weapon", "a stab: the Nalarbani's needle", "Swedish sticka, to stab", "STIK", state="planned", owner="Nalarbani"),

    # ------------------------------------------------------------------ class verbs (classes.md Part 7)
    "Naglskott": g("verb", "a pinning shot: Pinned", "Old Norse nagl, a nail, + skott", "NAHG-ul-skoht"),
    "Peka":  g("verb", "to point out: Marked", "Swedish peka, to point", "PEH-kah"),
    "Banskott": g("verb", "the slayer's shot: harder on the Pinned", "Old Norse bani, slayer, + skott", "BAHN-skoht"),
    "Avliva": g("verb", "to put down: harder on a foe under half HP", "Swedish avliva, to put down (what a hunter does for wounded prey)", "AHV-lee-vah"),
    "Skrida": g("verb", "to glide: step to a cell, Swift, and Evasive", "Swedish skrida, Old Norse skríða, to glide (the skiing Finns)", "SKREE-dah"),
    "Egga":  g("verb", "to egg on: a taunt", "Old Norse eggja, to incite (English egg on)", "EG-gah"),
    "Lya":   g("verb", "to cover an ally: take their hits", "coined (Joseph): a borrowed word, shortened", "LEE-ah"),
    "Hevn":  g("verb", "revenge: harder for every hit taken", "Norwegian hevn, revenge (Old Norse hefnd)", "HEV-un"),
    "Kvad":  g("verb", "a lay, a song: the Song's stacks heal each round", "Norwegian and Danish kvad, a poem (Old Norse kvæði)", "KVAHD"),
    "Skolja": g("verb", "to rinse: clears statuses and lowered stats", "Swedish skölja, to rinse", "SKOHL-yah"),
    "Vakna": g("verb", "to wake: brings back the Dying", "Swedish vakna, to wake", "VAHK-nah"),
    "Knyta": g("verb", "to tie: ties a knot of wind for later", "Swedish knyta, Old Norse knýta, to tie", "KNEE-tah"),
    "Kuling": g("verb", "a gale: spends a knot on wind for everyone", "Swedish kuling, a gale (the Swedish wind scale)", "KOO-ling"),
    "Storm": g("verb", "a storm: spends two knots", "Swedish storm (the wind scale)", "STORM", note="Said as in English."),
    "Orkan": g("verb", "a hurricane: spends three knots; wind, then lightning", "Swedish orkan, hurricane (the wind scale)", "OR-kahn"),
    "Kasta": g("verb", "to throw: shoves a foe back a row", "Old Norse kasta, to throw (English cast)", "KAHS-tah"),
    "Svepa": g("verb", "to sweep: pulls a foe forward a row", "Swedish svepa, to sweep", "SVEH-pah"),
    "Medvind": g("verb", "tailwind: an ally gets Quick", "Swedish and Norwegian medvind, tailwind (with-wind)", "MED-vind", was="Byr (read as beer)"),
    "Djupanda": g("verb", "a deep breath: a wind-up that brings back MP", "Swedish djup, deep, + anda, breath", "YOOP-ahn-dah"),
    "Aukseid": g("verb", "spell power up, on himself", "Auk + Seid", "OWK-sade"),
    "Aukskold": g("verb", "armour up: Fortified", "Auk + Skold", "OWK-skohld"),
    "Aukraft": g("verb", "striking power up: Mighty", "Auk + Kraft (the doubled k merges)", "OWK-rahft"),

    # ------------------------------------------------------------------ names that stand for a whole move
    "Daska": g("name", "the taunt that strikes (Egga + Styng)", "Swedish daska, to smack", "DAHS-kah"),
    "Genomskott": g("name", "a shot through the leg that Pins (Naglskott + Styng)", "Swedish genom, through, + skott", "YEH-nom-skoht"),
    "Genomskoda": g("name", "to see through: Marked and Sundered (Peka + its rider)", "Swedish genomskåda, to see through someone", "YEH-nom-skoh-dah"),
    "Gyllenlykt": g("name", "the Golden Lantern: a heal and Evasive 3 (Lak + its rider)", "Swedish gyllen, golden, + lykta, lantern; Kajasken's lantern", "YIL-en-likt",
                    was="Solak, Skimra"),
    "Geirskott": g("name", "a spear-length shot that pins (Mer Naglskott + Styng)", "Old Norse geirr, spear", "GAIR-skoht"),
    "Tusensplitter": g("name", "a thousand splinters: a bleeding flurry (Mer, Drif, Blot, Skott)", "Swedish tusen, thousand, + splitter, splinters", "TOO-sen-split-er"),
    "Pilskur": g("name", "an arrow-shower: bleeding arrows on everyone (All, Mer, Blot, Skott)", "Swedish pil, arrow, + skur, a shower", "PEEL-skoor"),
    "Skogsbrand": g("name", "a forest fire (All, Mer, Styng, Lonn Sveda)", "Swedish skogsbrand, forest fire", "SKOOGS-brahnd"),
    "Skoldborg": g("name", "shield-fort: DEF up on a row (Flok Aukskold)", "Swedish sköld, shield, + borg, fort", "SKOHLD-borg", state="planned", owner="Dagskald"),
    "Bannenlykt": g("name", "the Banishing Lantern: Marks a foe", "coined (Joseph): bannen reads as banned, banishing; + Swedish lykta, lantern; Kajasken's lantern", "BAHN-en-likt", state="planned",
                    note="See Bann.", owner="Dagskald"),
    "Stynglykt": g("name", "the stinging lantern: a hit and the Mark", "Styng + lykt", "STING-likt", state="planned", owner="Dagskald"),
    "Korplykt": g("name", "the Raven Lantern: Marks a row", "Swedish korp, raven, + lykt", "KORP-likt", state="planned", owner="Dagskald"),
    "Allsyn": g("name", "all-sight: Marks everyone", "All + Swedish syn, sight", "AHL-seen", state="planned",
                note="Reads as 'all sin' in English; a short name is needed either way (Allbannenlykt is too long).", owner="Dagskald"),
    "Sava":  g("name", "to save, to sew: Mending 3 on an ally", "coined (Joseph): a borrowed word, close enough", "SAH-vah", state="planned", note="Joseph floated Hava.", owner="Nalarbani"),
    "Besk":  g("name", "the bitter tonic: Evasive 3, then the crash", "Swedish besk, bitter; bäsk, herbal bitters", "BESK", state="planned", owner="Nalarbani"),
    "Hasin": g("name", "the hamstring: a heavy pinning, bleeding shot", "Old Norse hásin, the hock-sinew", "HAH-sin", state="planned", owner="Ullar"),

    # ------------------------------------------------------------------ parts of names (the soft families)
    "Genom": g("name_part", "through", "Swedish genom, through", "YEH-nom", note="A soft family: a later spear class might get Genomspett."),
    "Lykt":  g("name_part", "lantern", "Swedish lykta, lantern", "LIKT"),
    "Gyllen": g("name_part", "golden", "Swedish gyllene, golden", "YIL-en"),

    # ------------------------------------------------------------------ classes
    "Brennumar": g("class", "the arsonist: fire and burns", "Old Norse brennumenn, the burners of the saga house-burnings", "BREN-oo-mahr"),
    "Hafrunar": g("class", "sea-secrets: water and ice", "Old Norse haf, the open sea, + rúnar, runes", "HAHV-roo-nahr"),
    "Skurmar": g("class", "the storm-caller: knots of wind", "Old Norse skúr, Swedish skur, a squall", "SKOOR-mahr"),
    "Lundar": g("class", "the grove-keeper: earth and growth", "Old Norse lundr, Swedish lund, a grove", "LOON-dahr"),
    "Dagskald": g("class", "the day-singer: heals with song, smites with daylight", "Swedish dag, day, + skald", "DAHG-skahld"),
    "Seidar": g("class", "the sorcerer: shadow, curses, decay", "Old Norse seiðr, sorcery", "SADE-ahr"),
    "Ullar": g("class", "the bowman", "Ullr, the god of the bow, skis and the hunt", "OOL-ahr"),
    "Nalarbani": g("class", "the needle: a stiletto and a barber-surgeon", "Old Norse nál, needle, + -ar + bani, slayer", "NAH-lar-bah-nee"),
    "Hersir": g("class", "the champion: a greatsword", "Old Norse hersir, a district war-leader", "HER-seer"),
    "Huskarl": g("class", "the axe and mail coat", "Old Norse húskarl, a household warrior", "HOOS-karl"),
    "Berserker": g("class", "the club, bare-chested", "Old Norse berserkr, bear-shirt", "ber-SER-ker", note="Said as in English."),
    "Vasara": g("class", "the shield-hammer: the front", "Finnish vasara, hammer", "VAH-sah-rah"),
    "Geiras": g("class", "the pikeman", "Old Norse geirr, spear", "GAIR-ahs", state="pocket"),
    "Stikkar": g("class", "the rapier fighter", "Swedish sticka, to stab", "STIK-ahr", state="pocket"),
    "Maekir": g("class", "the blademaster", "Old Norse mækir, a poetic sword", "MY-keer", state="pocket"),
    "Holmgar": g("class", "the duelist", "Old Norse hólmganga, the island duel", "HOHLM-gahr", state="pocket"),
    "Atgeir": g("class", "the ironclad", "Old Norse atgeirr, Gunnar's polearm in Njáls saga", "AHT-gair", state="pocket"),
    "Glimar": g("class", "the wrestler", "Old Norse glíma, Norse folk wrestling", "GLEE-mahr", state="pocket"),

    # ------------------------------------------------------------------ creature families
    "Ande":  g("family", "elemental spirits", "Swedish ande, spirit (Old Norse andi, breath); -ande is also Swedish's -ing", "AHN-deh"),
    "Mogel": g("family", "living mould: the slimes", "Swedish mögel, mould", "MOH-gel"),
    "Draugr": g("family", "the saga dead", "Old Norse draugr, a revenant", "DROW-gur"),
    "Bein":  g("family", "the skeletons (the Beinar, the bone-folk)", "Old Norse bein, Swedish ben, bone", "BAYN"),
    "Drattr": g("family", "the catch: hunted water creatures", "Old Norse dráttr, a haul (of fish)", "DRAHT-ur"),
    "Djur":  g("family", "the beasts", "Swedish djur, animal (Old Norse dýr; English deer)", "YOOR"),
    "Oskorei": g("family", "the Wild Hunt", "Norwegian Oskoreia, the Wild Hunt", "OHS-koh-ray"),

    # ------------------------------------------------------------------ ranks and jobs
    "Litel": g("rank", "little: the annoying small ones (Ande, Mogel)", "Old Swedish litel, little", "LEE-tel"),
    "Stor":  g("rank", "big: the second rank", "Swedish stor, big", "STOHR"),
    "Drott": g("rank", "sovereign: the top rank (Ande, Mogel)", "Old Norse dróttinn, lord (Swedish drottning, queen)", "DROHT"),
    "Forn":  g("rank", "ancient: the top rank (the undead, the beasts)", "Old Norse forn, ancient", "FORN"),
    "Fors":  g("rank", "rapids: the top Drattr", "Swedish fors, rapids", "FORSH"),
    "Gan":   g("rank", "the draugr caster", "Old Norse gandr, a magic staff or spirit", "GAHN"),
    "bryn":  g("rank", "mail-coat: the sword-and-shield skeleton", "Old Norse brynja, mail-coat", "BRIN"),
    "orv":   g("rank", "arrows: the archer skeleton", "Old Norse ǫrvar, arrows", "ORV"),
    "seidr": g("rank", "sorcery: the caster skeleton", "Old Norse seiðr, sorcery", "SAY-dur"),
    "Ryttar": g("rank", "the Hunt's rider", "Swedish ryttare, rider", "RIT-ahr"),
    "Hornblasar": g("rank", "the Hunt's horn-blower", "Swedish hornblåsare, horn-blower", "HORN-blah-sahr"),
    "Huntmaster": g("rank", "the Hunt's leader"),
    "Skralla": g("rank", "rattling: a skeleton type", "Swedish skralla, to rattle", "SKRAHL-lah", state="pocket"),
    "Tork":  g("rank", "dried out: a skeleton type", "Swedish torka, to dry", "TORK", state="pocket"),

    # ------------------------------------------------------------------ statuses (plain English: what you wear)
    "Poisoned": g("status", "takes damage at the start of each round"),
    "Bleeding": g("status", "takes damage when it goes to act"),
    "Stunned":  g("status", "may lose its next action; clears the first time it costs one"),
    "Chilled":  g("status", "slowed by cold; a second chill freezes"),
    "Frozen":   g("status", "loses turns; any hit breaks it and shatters"),
    "Bound":    g("status", "netted: loses its next action"),
    "Feared":   g("status", "acts last; planned: Pinned and DEF down"),
    "Disarmed": g("status", "its weapon is off"),
    "Cursed":   g("status", "stages down; planned: Hexed and Poisoned"),
    "Silenced": g("status", "can't use anything that costs MP"),
    "Pinned":   g("status", "can't move or be moved"),
    "Song":     g("status", "the Dagskald's verses: heals each round"),
    "Scorched": g("status", "burning: damage over time, stoked by wind"),
    "Dying":    g("status", "down at 0 HP, a few breaths left: can be woken"),
    "Wounded":  g("status", "stabilised after a fall; falling again is death; rest clears it"),
    "Dead":     g("status", "gone: only the Mead of Waking or the city brings them back"),
    "Death":    g("status", "dead outright (Helvad)"),
    "Reeling":  g("status", "acts no earlier than Late", state="planned"),
    "Steadfast": g("status", "DEF up, and can't be Pinned or shoved", state="planned"),
    "Venom":    g("status", "Poisoned and Bleeding at once", state="planned"),
    "Mending":  g("status", "heals a little at each round's start", state="planned"),

    # ------------------------------------------------------------------ counters (stages; −3 to +3; opposite ends pull against each other)
    "Mighty":    g("counter", "ATK up"),
    "Feeble":    g("counter", "ATK down", note="Not Weakened: Weak is an affinity."),
    "Fortified": g("counter", "DEF up"),
    "Sundered":  g("counter", "DEF down", was="Cracked"),
    "Keen":      g("counter", "ACC up: your hits crit 1 in 3"),
    "Blinded":   g("counter", "ACC down: your hits whiff 1 in 3"),
    "Evasive":   g("counter", "EVA up: hits on you whiff 1 in 3", was="Nimble"),
    "Marked":    g("counter", "EVA down: hits on you crit 1 in 3"),
    "Quick":     g("counter", "SPD up: earlier in the round"),
    "Slowed":    g("counter", "SPD down: later in the round"),
    "Waxing":    g("counter", "MAT up", state="planned"),
    "Waning":    g("counter", "MAT down", state="planned"),
    "Warded":    g("counter", "MDF up", state="planned"),
    "Hexed":     g("counter", "MDF down", state="planned"),

    # ------------------------------------------------------------------ keywords
    "First":   g("keyword", "acts before nearly everything"),
    "Swift":   g("keyword", "acts sooner than a normal move"),
    "Late":    g("keyword", "acts after normal moves"),
    "Heavy":   g("keyword", "acts late in the round"),
    "Last":    g("keyword", "acts at the very end"),
    "Patient": g("keyword", "winds up a round before it lands"),

    # ------------------------------------------------------------------ affinity
    "Ineffective": g("affinity", "x0.25", state="planned"),
    "Resist":  g("affinity", "x0.5"),
    "Weak!":   g("affinity", "x1.5, and a place in the Bonus Round"),
    "Super!":  g("affinity", "x2, and a place in the Bonus Round", state="planned"),
    "Immune":  g("affinity", "nothing; never moves on the ladder"),
    "Absorb":  g("affinity", "heals the target; never moves on the ladder"),
    "Bonus Round": g("affinity", "an extra round for everyone who hit a weakness"),

    # ------------------------------------------------------------------ universal actions
    "Guard":    g("action", "brace: take less this round"),
    "Meditate": g("action", "a caster's breath: MP back"),
    "Move":     g("action", "step to another cell"),
    "Flee":     g("action", "run from the fight"),

    # ------------------------------------------------------------------ items
    "Small Life Draught": g("item", "a small heal"),
    "Life Draught":    g("item", "a heal"),
    "Strong Life Draught": g("item", "a big heal"),
    "Small Spirit Draught": g("item", "a little MP"),
    "Spirit Draught":  g("item", "MP"),
    "Strong Spirit Draught": g("item", "a lot of MP"),
    "Surgeon's Kit":   g("item", "gets a Dying hero up"),
    "Mead of Waking":  g("item", "wakes the Dying"),
    "Pocket Sand":     g("item", "blinds a foe"),
    "Firecracker":     g("item", "a small bang"),
    "Thunderpot":      g("item", "a bomb on every foe"),
    "Iron Throwing Knife": g("item", "a thrown Pierce"),
    "Iron Throwing Axe": g("item", "a thrown Slash"),
    "Iron Throwing Hammer": g("item", "a thrown Crush"),
    "Smoke Pot":       g("item", "smoke on the foes"),
    "Wind Cord":       g("item", "three knots of wind, tied ahead", state="planned"),
    "Waterfall Rune":  g("item", "a talisman: Meditate becomes Djupanda", state="planned"),
    "Odinseye Effigy": g("item", "a talisman: +50 MP", state="planned"),
    "Shrapnel Bomb":   g("item", "bleeding shrapnel on everyone: Allblottskott as an item", state="planned"),

    # ------------------------------------------------------------------ myth
    "Kajasken": g("myth", "a god of the far north, keeper of two lanterns", "? (Joseph's myth)", "KAI-ahs-ken",
                  note="His lanterns: Gyllenlykt mends and hides; Bannenlykt reveals and weakens."),
}

def entry(word):
    """A word's entry, or None. Case-sensitive: the book's keys are the game's spellings."""
    return GLOSS.get(word)
