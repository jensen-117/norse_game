"""What the Company remembers about its enemies (fight_lab_spec Part 3).

Inspect reads a creature's own sheet; what you've learned lifts stickers off its lines:
  - an affinity: hit that kind with that element or damage type once (the floater says what you found);
  - HP: fell KNOW_HP_KILLS of that family and rank; MP: fell KNOW_MP_KILLS.
Affinities vary with element, so they're kept per family, rank and element (an Eld Mogel and a Vatn Mogel differ).
HP and MP don't, so kills count per family and rank, across elements.
Fed from battle events; masks Battle.inspect() cards. Saved as plain JSON.
"""
import json
from data import KNOW_HP_KILLS, KNOW_MP_KILLS

def kind_of(fam, rank, element): return f"{fam}|{rank}|{element or '-'}"
def body_of(fam, rank): return f"{fam}|{rank}"

class Memory:
    def __init__(self):
        self.aff = {}      # kind -> {damage type: weak/resist/null/absorb/normal}
        self.kills = {}    # body -> count felled
        self.seen = set()  # kinds met (inspected or fought)
        self._who = {}     # this fight: uid -> (family, rank, element, side)
        self._felled = set()

    # ------------------------------------------------------------ learning
    def observe(self, events):
        """Read a batch of events (from begin()/commit(), in order). Returns what was newly learned, for the page."""
        learned = []
        for e in events:
            k = e["kind"]
            if k == "start":
                self._who = {u["id"]: (u["family"], u.get("job") or u["rank"], u["element"], u["side"]) for u in e["units"]}
                self._felled = set()          # (uid, rank): a crawler or a reassembled pile isn't felled twice
                for u in e["units"]:
                    if u["side"] == "enemy": self.seen.add(kind_of(u["family"], u.get("job") or u["rank"], u["element"]))
            elif k in ("hit", "absorb"):
                w = self._who.get(e.get("unit_id"))
                if not w or w[3] != "enemy" or e.get("spot"): continue
                dtype = e.get("element")
                if not dtype or dtype == "Force": continue
                result = "absorb" if k == "absorb" else e["affinity"]
                key = kind_of(*w[:3])
                if self.aff.setdefault(key, {}).get(dtype) != result:
                    self.aff[key][dtype] = result
                    learned.append(dict(kind=key, what="affinity", element=dtype, result=result))
            elif k == "transform":                      # a new job: learn under it from now on (review C06)
                uid = e.get("unit_id"); w = self._who.get(uid)
                if not w or w[3] != "enemy" or not e.get("job"): continue
                self._who[uid] = (w[0], e["job"], w[2], w[3])
                self.seen.add(kind_of(w[0], e["job"], w[2]))
            elif k in ("down", "crawl", "pile", "reform"):
                uid = e.get("was_id") if k == "reform" else e.get("unit_id")
                w = self._who.get(uid)
                if not w or w[3] != "enemy": continue
                body = body_of(w[0], w[1])
                if k == "reform":                       # one size smaller now
                    self._who[uid] = (w[0], e["rank"], w[2], w[3])
                    self.seen.add(kind_of(w[0], e["rank"], w[2]))
                if (uid, w[1]) in self._felled: continue
                self._felled.add((uid, w[1]))
                n = self.kills[body] = self.kills.get(body, 0) + 1
                for need, what in ((KNOW_HP_KILLS, "hp"), (KNOW_MP_KILLS, "mp")):
                    if n == need: learned.append(dict(kind=body, what=what))
        return learned

    # ------------------------------------------------------------ reading a sheet
    def knows(self, card):
        body = body_of(card["family"], card.get("job") or card["rank"])
        n = self.kills.get(body, 0)
        return dict(kills=n, hp=n >= KNOW_HP_KILLS, mp=n >= KNOW_MP_KILLS,
                    aff=self.aff.get(kind_of(card["family"], card.get("job") or card["rank"], card["element"]), {}))

    def mask(self, card, know_all=False):
        """The sheet as the Company sees it: unknown lines read None (HP, MP) or '?' (affinities). Heroes are known."""
        if card["side"] != "enemy" or know_all: return dict(card, known=dict(hp=True, mp=True, all=True))
        self.seen.add(kind_of(card["family"], card.get("job") or card["rank"], card["element"]))
        k = self.knows(card)
        out = dict(card)
        if not k["hp"]: out["hp"] = out["maxhp"] = None
        if not k["mp"]: out["mp"] = out["maxmp"] = None
        out["affinities"] = {e: k["aff"].get(e, "?") for e in card["affinities"]}
        out["known"] = dict(hp=k["hp"], mp=k["mp"], kills=k["kills"], all=False)
        return out

    # ------------------------------------------------------------ the bestiary page and saving
    def entries(self):
        out = []
        for key in sorted(self.seen):
            fam, rank, el = key.split("|")
            n = self.kills.get(body_of(fam, rank), 0)
            out.append(dict(kind=key, family=fam, rank=rank, element=None if el == "-" else el, kills=n,
                            hp=n >= KNOW_HP_KILLS, mp=n >= KNOW_MP_KILLS, aff=self.aff.get(key, {})))
        return out

    def to_json(self):
        return json.dumps(dict(aff=self.aff, kills=self.kills, seen=sorted(self.seen)))

    @classmethod
    def from_json(cls, s):
        m = cls()
        if s:
            d = json.loads(s); m.aff, m.kills, m.seen = d.get("aff", {}), d.get("kills", {}), set(d.get("seen", []))
        return m
