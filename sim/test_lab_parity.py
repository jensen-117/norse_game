"""The Lab's copy of the rules matches the sim (AGENT_CODE_REVIEW, step 3): every module the page loads."""
import os, re, unittest
HERE = os.path.dirname(os.path.abspath(__file__)); LAB = os.path.join(HERE, "..", "fight_lab")

class TestLabParity(unittest.TestCase):
    def test_the_page_loads_the_sims_own_files(self):
        sim = re.search(r"const SIM = \[([^\]]*)\]", open(os.path.join(LAB, "index.html")).read()).group(1)
        names = re.findall(r'"([\w.]+\.py)"', sim)
        self.assertIn("words.py", names)
        for n in names:
            with self.subTest(n):
                self.assertEqual(open(os.path.join(HERE, n), "rb").read(), open(os.path.join(LAB, "sim", n), "rb").read(),
                                 f"fight_lab/sim/{n} differs from sim/{n}: copy it over")

if __name__ == "__main__": unittest.main()
