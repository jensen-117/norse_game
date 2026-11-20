"""The one compiler (refactor_plan Wave 2a): every builder goes through words.compile_move."""
import unittest
from engine import *
from grammar import compile_word

class TestWords(unittest.TestCase):
    def test_seam_rule(self):
        self.assertEqual(word_name("Krosh", target=None, rider="Brak"), "Brakrosh")
        self.assertEqual(word_name("Kraft", direction="Auk"), "Aukraft")
        self.assertEqual(word_name("Vakna", "Halv"), "Halvakna")
        self.assertEqual(spell_name("Lak", "Base", True), "Allak")

    def test_builders_are_compiled(self):
        self.assertEqual(damage_spell("Eld", "Mer", True), compile_move("damage", "Eld", "Mer", "All", cost_type="MP"))
        self.assertEqual(stat_spell("DEF", True)["name"], "Aukskold")
        self.assertEqual(status_spell("Blinded", "Base")["name"], "Blinda")
        self.assertEqual(skill("Pierce", "Blotspett", "Base", status="Bleeding", power=14)["cost_type"], "HP")

    def test_grammar_words_are_compiled(self):
        w = compile_word("Krosh", "Mer", rider="Eitr")
        self.assertEqual({k: v for k, v in w.items() if k != "english"},
                         compile_move("damage", "Krosh", "Mer", rider="Eitr", parts=True))

if __name__ == "__main__": unittest.main()
