"""Gera a versão estática do site (GitHub Pages) na pasta docs/.

Uso (na pasta nerd-dev-landing):
    python tools/export_static.py --site-url https://godofin.github.io/nerd-dev-intro

O que faz: sobe a própria API em memória, salva cada página renderizada (home, blog, categorias, artigos, 404,
sitemap, feed) e um data/site.json que o blog.js usa no lugar da API. Os links absolutos (/blog, /assets...)
ganham o prefixo do endereço publicado (por exemplo /nerd-dev-intro).
"""
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

parser = argparse.ArgumentParser()
parser.add_argument("--site-url", required=True, help="endereço final, ex.: https://godofin.github.io/nerd-dev-intro")
parser.add_argument("--out", default="docs")
args = parser.parse_args()

SITE_URL = args.site_url.rstrip("/")
BASE = urlparse(SITE_URL).path.rstrip("/")  # "/nerd-dev-intro" (ou "" em domínio próprio)
OUT = ROOT / args.out

os.environ["NERDDEV_SITE_URL"] = SITE_URL

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402

client = TestClient(app)


def get(path: str, status: int = 200) -> str:
    r = client.get(path)
    if r.status_code != status:
        raise SystemExit(f"{path} respondeu {r.status_code}")
    return r.text


def fix_url(url: str) -> str:
    """Prefixa um caminho absoluto do site (/blog/x) com o BASE e usa barra final nas páginas."""
    m = re.match(r"^(/[^?#]*)([?#].*)?$", url)
    if not m or url.startswith("//"):
        return url
    path, rest = m.group(1), m.group(2) or ""
    last = path.rsplit("/", 1)[-1]
    if not path.startswith("/assets/") and "." not in last and not path.endswith("/"):
        path += "/"
    return BASE + path + rest


def transform(html: str) -> str:
    # og:image e logos em JSON-LD precisam ser URLs completas
    html = re.sub(r'(content|"logo":\s*)(=?")(/assets/[^"]+)"', lambda m: f'{m.group(1)}{m.group(2)}{SITE_URL}{m.group(3)}"', html)
    html = re.sub(r'(\s(?:href|src))="(/[^"]*)"', lambda m: f'{m.group(1)}="{fix_url(m.group(2))}"', html)
    boot = f'<script>window.NERDDEV_STATIC=true;window.NERDDEV_BASE="{BASE}";</script>'
    return html.replace("</head>", f"  {boot}\n</head>", 1)


def write(rel: str, text: str) -> None:
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


# ---------- limpa e copia os arquivos fixos ----------
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
shutil.copytree(ROOT / "assets", OUT / "assets")
write(".nojekyll", "")

# ---------- dados para o blog.js ----------
slugs = []
page = 1
while True:
    data = json.loads(get(f"/api/posts?limit=50&page={page}"))
    slugs += [p["slug"] for p in data["items"]]
    if page >= data["pages"]:
        break
    page += 1

posts = []
for slug in slugs:
    p = json.loads(get(f"/api/posts/{slug}"))
    summary = {k: p[k] for k in ("slug", "title", "excerpt", "tag", "category_slug", "published_at", "reading_minutes", "featured", "cover")}
    summary["text"] = f'{p["title"]} {p["excerpt"]} {p["content"]}'.lower()
    posts.append(summary)
categories = json.loads(get("/api/categories"))
write("data/site.json", json.dumps({"posts": posts, "categories": categories}, ensure_ascii=False))

# ---------- páginas ----------
home = get("/")
home = home.replace("</head>", f'  <link rel="canonical" href="{SITE_URL}/">\n</head>', 1)
write("index.html", transform(home))
write("blog/index.html", transform(get("/blog")))
for c in categories:
    write(f"categoria/{c['slug']}/index.html", transform(get(f"/categoria/{c['slug']}")))
for slug in slugs:
    write(f"blog/{slug}/index.html", transform(get(f"/blog/{slug}")))
write("404.html", transform(get("/blog/nao-existe-404", status=404)))

# sitemap, feed e robots já saem com URLs absolutas
write("sitemap.xml", get("/sitemap.xml").replace(f"{SITE_URL}/blog<", f"{SITE_URL}/blog/<"))
write("feed.xml", get("/feed.xml"))
write("robots.txt", get("/robots.txt"))

print(f"ok: {len(slugs)} artigos, {len(categories)} categorias, base '{BASE}' -> {OUT}")
