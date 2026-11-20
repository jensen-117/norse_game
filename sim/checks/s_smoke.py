"""Lab smoke check (AGENT_CODE_REVIEW C03): serve a fight_lab folder, boot the page to Ready, play one Auto fight to
the end. Serves the folder itself on a free port, so it works on a fresh checkout.
    python3 sim/checks/s_smoke.py [path/to/fight_lab]"""
import functools, http.server, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

def serve(folder):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=folder)
    srv = socketserver.TCPServer(("127.0.0.1", 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]

def smoke(folder):
    srv, port = serve(folder)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1400, "height": 900})
            errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
            p.route("**/fonts.googleapis.com/**", lambda r: r.abort())
            p.goto(f"http://127.0.0.1:{port}/index.html")
            p.wait_for_function("/^(Ready|Python didn't|The rules didn't|The art didn't)/.test(document.querySelector('#status').textContent)", timeout=180000)
            st = p.text_content("#status")
            if not st.startswith("Ready"): return f"FAIL: {st}"
            p.select_option("#speed", "0"); p.click("#rollparty"); p.wait_for_timeout(50); p.click("#rollpack"); p.wait_for_timeout(50)
            p.click("#auto"); p.wait_for_function("Screen.state && Screen.state.phase === 'over'", timeout=180000)
            w = p.evaluate("Screen.state.winner"); r = p.evaluate("Screen.state.round"); b.close()
            return f"FAIL: page errors {errs[:3]}" if errs else f"PASS: Ready, one Auto fight played ({w} after {r} rounds)"
    finally: srv.shutdown()

if __name__ == "__main__":
    folder = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "fight_lab"))
    out = smoke(folder); print(out); sys.exit(0 if out.startswith("PASS") else 1)
