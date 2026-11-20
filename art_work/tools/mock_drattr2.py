"""Mock fights (Nov 9) with Joseph's second Drattr sheet (20 frames), on the lab backgrounds via the lab geometry."""
exec(open("art_work/tools/mock_32r.py").read().split("scene(\"Neutral\"")[0].split("\nscene(")[0])
D2 = lambda i: Image.open(f"art_work/drattr4/frame{i - 1}.png").convert("RGBA")   # Joseph's 1-based numbers
scene("Vatn", [(D2(1), 0, 0), (D2(16), 1, 0), (D2(5), 0, 1), (D2(11), 1, 1), (D2(2), 0, 2), (D2(8), 1, 2)], "art_work/drattr4/mock_court_x4.png")
scene("Neutral", [(D2(3), 0, 0), (D2(6), 1, 0), (D2(4), 0, 1), (D2(13), 1, 1), (D2(7), 0, 2), (D2(18), 1, 2)], "art_work/drattr4/mock_mix_x4.png")
