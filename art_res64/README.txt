Art, Resurrect 64 only (every pixel checked)

heroes/wizard_front   Front-facing wizard, 4 frames, six caster classes. Robes step along each school's ramp.
heroes/wizard_side    Side-facing wizard, 3 frames, six caster classes, right- and left-facing.
spirits/halvande      Halvande (16x16), 4 frames, all twelve elements.
spirits/ande          Standard Ande (16x32), 7 frames, all twelve elements.
animals               Cat, snow leopard, howling wolf, rat (4 poses). Original colors snapped to Resurrect 64,
                      each tone kept distinct within its sprite.
backgrounds           The gold Sol watercolor (a painted image, so not palette-limited).
sheets                Contact sheets, before/after comparisons, and animated previews.

heroes/wizard_side_v2 Side wizard v2 (Joseph's sprite, 17 frames), six caster classes, right- and left-facing.
                      Frames: idle1-3, hit, spell1, run1-4, charge1-3, bomb1-2, downed, defend, defend_hit (file names use these labels).
                      Animations (frame labels, ms):
                        idle   idle1 600, idle2 300, idle3 600, idle2 300
                        hit    idle1 100, hit 400, idle1 300
                        spell  idle1 150, spell1 450, idle1 300
                        run    run1-4 at 125ms each (even 8fps)
                        downed idle1 150, hit 200, downed 1200
                        defend idle1 150, defend 1200
                        defend_hit defend 300, defend_hit 350, defend 600
                        taunt  idle1 150, bomb2 650 (the yell), defend 900
                        charge charge1 300, charge2 300, charge3 450 (loops while charging)
                        bomb   bomb1 150, bomb2 500
                        cast   idle1, charge1-3, bomb1-2, idle1 (full sequence)
                                            Face tones: chin shadow and open mouth #966c6c, mouth depth #694f62.
                      frames/ single PNGs, strips/ one strip per animation in play order (Aseprite: File > Import
                      Sprite Sheet, 16x32 cells), gifs/ 8x previews. Robe = base, fold, deep fold per class:
                      Hafrunar 4d9be6/4d65b4/484a77  Brennumar ea4f36/b33831/6e2727  Skurmar c7dcd0/9babb2/7f708a
                      Lundar a2a947/676633/4c3e24  Dagskald f9c22b/f79617/fb6b1d  Seidar 905ea9/6b3e75/45293f

effects               Two battle effects sheets, recolored to Resurrect 64 per element plus a white Martial set.
                        fx_*      fx_source.png, bdragon1727 "Free Effect and Bullet 16x16"
                                  https://bdragon1727.itch.io/free-effect-and-bullet-16x16
                        bullet_*  bullet_source.png, bdragon1727 "Fire Pixel Bullet 16x16"
                                  https://bdragon1727.itch.io/fire-pixel-bullet-16x16
                      bdragon1727 terms (same on both pages): free for non-commercial use; commercial use asks for a contribution of any
                      amount (the author says credit counts); "Modify as desired"; no reselling or redistributing
                      the asset, so keep these sheets out of any public repo.
                      Recolor: the source's warm ramp ranked dark->light onto 5-step ramps. Layout is unchanged, so
                      the same cell is the same effect in every element sheet.

environment           Joseph's wall (22 x 32x32) and floor (3 x 96x96) tiles snapped to Res64 by value:
                      stone onto 3e3546/625565/7f708a/9babb2, reddish mortar onto 2e222f/45293f. Floors sit one
                      step lighter so slabs read as lit board cells. walls/ and floors/ hold single PNGs;
                      *_strip.png import into Aseprite (File > Import Sprite Sheet).

ui                    font_sheet.png: Joseph's bitmap font, 16 columns of 8x16 cells on a 9x17 pitch; rows 0-5 are
                      ASCII, later rows continue from U+00A0 (assumed). Rendered proportionally, 1px spacing.

mocks                 320x180 battle-screen mocks: Neutral, Vatn (Move: open Rear cells lit) and Eld (one enemy cell
                      targeted). Walls and floors take an area stone ramp (all Res64): Neutral cool grey; Vatn blue
                      stone with wet teal seams; Eld warm stone with smouldering red mortar (walls only).
                      Floor = three courses of foreshortened slabs, one per lane, as one continuous grid sheared
                      0.3px per px of depth (all one direction), slabs laid with 1px mortar joints; every board
                      cell is one slab (34px pitch). Cell highlight is always white.
                      Text box: area-tinted watercolor fill, bevelled band, corner studs, rune plaque, Joseph's font.

slimes                Joseph's Mogel slimes at 32, 24, 16 and 8 px (Mogel/Stor/Drott, Litel, Halv, death droplet),
                      11 frames each: idle1, idle2, surprise, breathe1, breathe2, hit1, hit2, withdraw, cast1-3.
                      Source soft-brush colours sorted into six slots by value: outline 2e222f; deep, shadow, body,
                      sheen, specular from a 5-step ramp. Sheen/specular on the left 40% of each row fades into the
                      body (no rim streak). 24 and 32 px: shadow terminator checker-dithered.
                      Native ramp is Jord (4c3e24 676633 a2a947 b2ba90 c7dcd0); every element ramp is applied
                      (Mogel<size>_<Element>_<frame>.png). Animations: idle 0,1 | hit 5,6,0 | defend 0,7 |
                      charge 0,3,4 | cast 8,9,10,0 | surprise 2,0. mogel_<el>_death_chain.gif: 32 > 24 > 16 > droplet.
dressing              Dungeon dressing from Cainos' "Pixel Art Platformer - Dungeon" (cainos.itch.io; paid; free and
                      commercial use and modification allowed, no redistribution or resale, credit appreciated),
                      cut, scaled x0.5 with a box filter, and snapped by material: stone onto the wall slots
                      (3e3546 625565 7f708a 9babb2, so area recolors carry over), wood/cloth onto 694f62 966c6c
                      ab947a, the pack's brown outline onto 2e222f, flame onto f79617 f9c22b fbff86.
                      props/ 34 pieces (windows, banners, lanterns, alcoves, statues, barrels, doors, wall breaches);
                      decals/ cobwebs (x0.75) and cracks (x1) as masks, coloured per area when placed.
                      dressing_library.png names every piece with its size.
                      Light pools are palette-safe: wall stone inside a pool steps one notch up its own ramp,
                      checker-dithered at the rim. Banners take the area's band colours.
                      mocks/dressed_*: Neutral, Vatn (blue webs, teal seams) and Eld (smouldering mortar, hearth).

slimes/stormogel      DRAFT: the skull and crossbones from Joseph's boss frame carried into all 11 frames, anchored to
                      each frame's body, clipped one pixel inside the skin, and drawn under the sheen and glint.
                      Bones use the ramp's sheen slot and the skull's eyes the deep slot, so they take the slime's
                      colour. Round frames hold up; breathe1, breathe2, hit2 and withdraw want a hand pass.

UNDEAD (Gandalf Hardcore sheets: skeleton, zombie, archer) -- art_res64/undead/
  Source: gandalfhardcore.itch.io (Pixel Art Characters Bundle). License: commercial and non-commercial games OK,
  modification OK; NO reselling, repackaging or redistribution, no AI training, no NFTs. Keep these and every
  converted sheet out of public repos.
  Tool: scratchpad tools/undead_res64.py <outdir>   (material by hue, then lightness rank onto a Res64 ramp)
    skeleton_{plain,aged,drott}  bone tint = rank: plain (Halv), aged/yellowed (Bein), blood-red (Drott)
    zombie_corpse                the Draugr: corpse-pale blue skin, grave rags; gore removed (red -> neighbours)
    archer_hunt                  the Hunt: ectoplasm green, glowing face, the red cross painted out
  frames/<sheet>_<tint>/r<row>c<col>.png  (64x64 cells, as in the source sheet; skeleton and zombie face left,
  the archer faces right and is flipped when used as an enemy)
  Sizes: Halvbein = the skeleton with 6 rows cut (4 leg rows, one rib bar + gap) -> 32px; Bein native 38;
  Stor/Drott +6 rows -> 44. Draugr 38, Hunt archer 43.
  weapons/  generic overlay test (tools/bein_weapons.py): sword = Beinbryn, bow = Beinorv, staff = Beinseidr,
  three frames each (idle r0c0, point r0c9, swipe r4c3), hand anchors picked by hand.
  mocks/barrow_mock.png  two Barrow packs on the dressed Neutral board (battle_mock.py ... barrow)
  beinar/  Joseph's Beinar starters (Nov 7: sword and round shield, mage with Natt-blue orb, short bow, longbow),
  one idle frame each, via tools/beinar_res64.py: only bone colours take the rank tint; weapons keep theirs
  (bows lifted to 694f62/966c6c/ab947a so they read on stone; the orb's white glint stays white).
  beinar_<job>_<plain|aged|drott>_<cut|native|stretch>.png and beinar_ladder.png.
  The Draugr's rags were lifted a step (they vanished on the Neutral floor).
  Nov 7, second pass: stretch adds a rib bar AND its gap as a pair (every bar keeps a 1px ink line); the orb's
  glint is found from the orb itself (biggest blob of gem colour), so it never takes the bone tint; aged bone is
  cooler now (694f62 / ab947a / b2ba90 / c7dcd0; the warm try read as skin). The oval shield on stretched
  sprites stays (Joseph). Beinseidr element orbs: tools/beinar_views.py -> beinseidr_<Element>_joseph.png and
  beinseidr_elements.png; orb, eyes and chest rune take the Mogel's element ramp (one table for the game),
  stepped up for the dark ramps (Natt, Aska, Reyk) so the eyes don't vanish in the sockets.
  draugr/  the Draugr ladder (tools/draugr_res64.py): skin and rag tints walk the ranks --
    pale (nar-folr) Halvdraugr, cut 32 / blar (hel-blar, death-blue) Draugr 38, Stordraugr stretched 44 /
    drott: hel-blar skin in blood-red rags, stretched 44 (the Drott mark across families; gold read as orange,
    see drott_options.png). Rows cut/stretched from the bottom: 3, 6, 8, 10, 15, 22. Frames under 30px (falls,
    crawl) never resize. The baked slash arc is kept effect-white (skin pixels with no outline within 2px);
    its inner rim still picks up the rag colour. frames/draugr_<tint>_<size>/r<row>c<col>.png, draugr_ladder.png.
    Gandraugr (the caster) has no pose yet.
  Draugr, Nov 7 later: the baked slash arc is now fully effect-white (tools/arc_find.py: the biggest pure-white
  blob grown into the arc's shading colours; 2 steps may touch the outline), and the baked yellow hit sparks
  are removed like the gore (our effects draw hits).

effects/martial/   the martial (white) effect set, named, cut from fx_Martial.png by tools/fx_martial.py:
  slash (thin crescent), crush (burst then shockwave ring), pierce (fast streak), shot (arrow in flight) + spark
  (landing), crit (sparkle over the hit), graze (small fading glint), defend (ward ring closing in), taunt (shout
  lines), move (dust puff), flash (a cast going off), down (last breath rising). fx_<name>.png strips (16px
  frames). The sheet layout is the same in every element sheet, so frames(name, element) names elemental
  effects too. martial_fx_demo.gif: each on a Draugr; gandraugr_cast_demo.gif: the stand-in cast (hold the
  raised frame r1c7, flash white twice, Natt bursts in the hand, flies, lands).
  hit_slash / hit_crush / hit_pierce.png: Joseph's hit animations (Nov 7) in martial white (tools/hits_martial.py:
  fcef8d/ffb879/f48d6d/ea6262 -> ffffff/c7dcd0/9babb2/7f708a). Cadence is data (CADENCE: frames, ms per frame,
  impact frame; the target holds its hit pose, nudged 1px, for 3 frames from impact). Slash frame 0 of the source
  is a reference of the crescents and is skipped. hits_demo_tuned.gif vs hits_demo_flat100.gif (his 100ms).
  Second versions (Nov 7): hit_crush2 (the ring pulls in, a beat on the dot, the blow bursts out, shards fly;
  impact on frame 5) and hit_pierce2 (the thrust line runs in and narrows, then the hit sprays along the line;
  impact on frame 4). Both already in Res64 whites (ffffff, c7dcd0). slash_coded: tools/slash_gen.py draws a
  slash from an invisible blade tip travelling an arc (only the smear shows: thick at the tip, tapering at the
  tail, the tail catches up when the tip stops); radius, sweep angles, trail, width, frames and direction are
  parameters. hits_demo_tuned.gif now plays slash, slash_coded, crush, crush2, pierce, pierce2.
  Nov 7, final for now: the second versions replace the first (crush2, pierce2; the firsts are kept for later
  use). crush2's white burst plays one 20ms flicker. Checks: every effect frame is alpha 0 or 255 only (nothing
  semi-transparent to tint the target), compositing changes no pixel outside the effect's own, and the demo GIF
  is quantized onto the Res64 palette undithered (exact colours; earlier demos had anti-aliased labels that
  nudged nearby colours in the GIF palette -- a demo artifact, not the sprites).

TOOLS (Nov 7): every script that made these sprites now lives in /home/claude/art_work/tools (they were in a
session scratchpad, which doesn't last). Run them as  python3 -I tools/<script>.py /home/claude/art_work ...
from inside art_work. art_work/sources holds every file Joseph attached (aseprite files, sheets, packs).
