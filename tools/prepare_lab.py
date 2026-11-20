"""Prepare the Fight Lab's Python runtime from a clean checkout (AGENT_CODE_REVIEW C03).

    python3 tools/prepare_lab.py           # fetch Pyodide (pinned), build fight_lab/py/, verify every checksum
    python3 tools/prepare_lab.py --check   # verify an existing fight_lab/py/ against the manifest, fetch nothing

Everything it needs is in fight_lab/runtime_manifest.json: the Pyodide version, the npm tarball and its published
integrity hash, the standard-library files the Lab ships, and the SHA-256 of every file it writes. The download is
verified before anything is extracted, and every output is verified after. Plain Python 3, no npm. The same files
serve local development and publishing (fight_lab/README.md).
"""
import base64, hashlib, io, json, os, sys, tarfile, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAB = os.path.join(ROOT, "fight_lab")
MAN = json.load(open(os.path.join(LAB, "runtime_manifest.json")))
RUNTIME = ("pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "pyodide-lock.json")   # copied as published

def sha256(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()

def check():
    bad = []
    for rel, want in MAN["files"].items():
        p = os.path.join(LAB, rel)
        if not os.path.exists(p): bad.append(f"{rel}: missing")
        elif sha256(p) != want: bad.append(f"{rel}: checksum differs")
    return bad

def fetch():
    cache = os.path.join(os.path.expanduser("~"), ".cache", "norse_game", os.path.basename(MAN["tarball"]))
    if os.path.exists(cache): data = open(cache, "rb").read()
    else:
        print(f"fetching {MAN['tarball']}")
        data = urllib.request.urlopen(MAN["tarball"], timeout=300).read()
    algo, want = MAN["integrity"].split("-", 1)
    got = base64.b64encode(hashlib.new(algo, data).digest()).decode()
    if got != want: raise SystemExit(f"the Pyodide tarball doesn't match its published {algo} integrity: refusing it")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    if not os.path.exists(cache): open(cache, "wb").write(data)
    return tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")

def build():
    tar = fetch()
    out = os.path.join(LAB, "py"); os.makedirs(out, exist_ok=True)
    for name in RUNTIME:
        open(os.path.join(out, name), "wb").write(tar.extractfile(f"package/{name}").read())
    z = zipfile.ZipFile(io.BytesIO(tar.extractfile("package/python_stdlib.zip").read()))
    keep = set(MAN["stdlib"]["names"])
    missing = keep - set(z.namelist())
    if missing: raise SystemExit(f"python_stdlib.zip lacks {sorted(missing)[:5]}")
    lib = {n: z.read(n).decode("utf-8") for n in z.namelist() if n in keep}     # the zip's order
    open(os.path.join(out, "stdlib.json"), "w", encoding="utf-8").write(json.dumps(lib, separators=(",", ":")))

if __name__ == "__main__":
    if "--check" not in sys.argv: build()
    bad = check()
    if bad: raise SystemExit("fight_lab/py doesn't match the manifest:\n  " + "\n  ".join(bad))
    print(f"fight_lab/py ready: Pyodide {MAN['pyodide']}, {len(MAN['stdlib']['names'])} stdlib files, all checksums match")
