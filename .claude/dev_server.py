"""Serveur local qui imite les regles de vercel.json (adresses propres).

- /work, /about          -> work.html, about.html  (cleanUrls)
- /xxx.html              -> redirection 308 vers /xxx
- /project/<slug>        -> project.html (l'adresse reste /project/<slug>)
- /project.html?slug=x   -> redirection 308 vers /project/x
"""
import http.server
import os
import sys
from urllib.parse import urlsplit, parse_qs, quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _redirect(self, location):
        self.send_response(308)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        url = urlsplit(self.path)
        path, query = url.path, url.query

        if path in ("/project", "/project.html"):
            slug = parse_qs(query).get("slug", [None])[0]
            if slug:
                return self._redirect("/project/" + quote(slug))
        if path.endswith(".html") and path != "/index.html" \
                and os.path.isfile(os.path.join(ROOT, path.lstrip("/"))) \
                and not path.startswith("/google"):
            return self._redirect(path[:-5] + (("?" + query) if query else ""))
        if path == "/index.html":
            return self._redirect("/")
        if path.startswith("/project/"):
            self.path = "/project.html"
        elif "." not in os.path.basename(path) and path != "/" \
                and os.path.isfile(os.path.join(ROOT, path.lstrip("/") + ".html")):
            self.path = path + ".html" + (("?" + query) if query else "")
        return super().do_GET()


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
