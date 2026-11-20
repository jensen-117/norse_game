# The Fight Lab

A page that runs the game's real Python rules (`sim/`) in the browser through Pyodide, and draws the fight.

## Launch from a fresh checkout

```
python3 tools/prepare_lab.py          # fetches Pyodide 0.26.4 (pinned), builds fight_lab/py/, verifies every checksum
cd fight_lab && python3 -m http.server 8765
```

Then open <http://127.0.0.1:8765/index.html>. It needs Python 3 and network access to registry.npmjs.org the first
time (the tarball is cached in `~/.cache/norse_game/`).

- `fight_lab/py/` is generated, not committed: `tools/prepare_lab.py` rebuilds it from `fight_lab/runtime_manifest.json`
  (the Pyodide version, the tarball's published integrity hash, the standard-library files the Lab ships, and the
  SHA-256 of every output). `--check` verifies an existing folder without fetching.
- `fight_lab/sim/` is a copy of the rules the page loads (the `SIM` list in `index.html`); it must match `sim/`.
- **Smoke check:** `python3 sim/checks/s_smoke.py` serves the folder itself, boots to Ready and plays one Auto fight
  (needs Playwright and Chromium).
- **Publishing** uses these same files: `index.html`, `screen.js`, `assets/`, `sim/`, and `py/` as built above.

## If the sim starts importing a new standard-library module

Add its file name to `stdlib.names` in `runtime_manifest.json`, run `tools/prepare_lab.py`, and record the new
`stdlib.json` checksum it prints a mismatch for (update `files["py/stdlib.json"]`).
