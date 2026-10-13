"""API do blog da Nerd Dev.

Rodar (na pasta nerd-dev-landing):
    pip install -r api/requirements.txt
    uvicorn api.main:app --reload

Serve o site (/, /blog, /blog/{slug}), a API (/api/...), /feed.xml, /sitemap.xml e /robots.txt.
Docs em /docs. Escrita (POST/PUT/DELETE) exige o header X-Admin-Token igual a NERDDEV_ADMIN_TOKEN.
Defina NERDDEV_SITE_URL (ex.: https://nerddev.com.br) para URLs absolutas corretas em canonical, sitemap e feed.
"""
import html
import json
import os
import re
import secrets
import sqlite3
import unicodedata
from datetime import date
from email.utils import format_datetime
from datetime import datetime, time, timezone
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .seed import SEED_POSTS, SEED_VERSION

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("NERDDEV_DB", ROOT / "api" / "blog.db"))
ADMIN_TOKEN = os.environ.get("NERDDEV_ADMIN_TOKEN", "dev-troque-este-token")
SITE_URL = os.environ.get("NERDDEV_SITE_URL", "").rstrip("/")
AUTHOR = "Equipe Nerd Dev"
SITE_NAME = "Nerd Dev"

SLUG_RE = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"

# ordem e descrição das categorias do portal (categorias novas aparecem depois, em ordem alfabética)
CATEGORY_ORDER = ["Nintendo", "Games", "Cultura Pop", "Mundo de Dados", "IA", "Programação", "Ferramentas", "Carreira"]
CATEGORY_DESC = {
    "Nintendo": "Mario, Zelda, Game Boy e tudo da Nintendo, explicado por quem entende de jogos e de código.",
    "Games": "Engines, design de jogos e como os games funcionam por dentro.",
    "Cultura Pop": "Filmes, séries, animes e quadrinhos pela lente de quem programa.",
    "Mundo de Dados": "SQL, análise e ciência de dados explicados do zero.",
    "IA": "Inteligência artificial sem mistério: o que é, como funciona e como usar melhor.",
    "Programação": "Conceitos de programação passo a passo, para quem está começando.",
    "Ferramentas": "Git, editores e outras ferramentas que valem o seu tempo.",
    "Carreira": "Caminhos, áreas e primeiros passos para entrar no mercado de tecnologia.",
}


# ---------- banco ----------

def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    with connect() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                excerpt TEXT NOT NULL,
                content TEXT NOT NULL,
                tag TEXT NOT NULL,
                published_at TEXT NOT NULL
            )"""
        )
        cols = {r[1] for r in con.execute("PRAGMA table_info(posts)")}
        if "featured" not in cols:
            con.execute("ALTER TABLE posts ADD COLUMN featured INTEGER NOT NULL DEFAULT 0")
        if "cover" not in cols:
            con.execute("ALTER TABLE posts ADD COLUMN cover TEXT")
        con.execute("CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)")
        row = con.execute("SELECT v FROM meta WHERE k='seed'").fetchone()
        if (int(row[0]) if row else 0) < SEED_VERSION:
            # só adiciona os que faltam: nunca recria um post que você apagou depois (a versão sobe só quando há seeds novos)
            con.executemany(
                "INSERT OR IGNORE INTO posts (slug, title, excerpt, content, tag, published_at, featured) "
                "VALUES (:slug, :title, :excerpt, :content, :tag, :published_at, :featured)",
                SEED_POSTS,
            )
            con.execute("INSERT OR REPLACE INTO meta (k, v) VALUES ('seed', ?)", [str(SEED_VERSION)])


def get_db():
    con = connect()
    try:
        yield con
    finally:
        con.close()


DbDep = Annotated[sqlite3.Connection, Depends(get_db)]


# ---------- markdown mínimo (escapa tudo antes de formatar) ----------

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "secao"


def _inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        text,
    )
    return text


def render_markdown(md: str) -> tuple[str, list[dict]]:
    """Devolve (html, sumário). Cada ## vira um h2 com id para o índice lateral."""
    out: list[str] = []
    toc: list[dict] = []
    used: set[str] = set()
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            label = f'<span class="code-lang">{html.escape(lang)}</span>' if lang else ""
            out.append(f'<figure class="codeblock">{label}<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre></figure>')
        elif line.startswith("## "):
            text = line[3:].strip()
            base = slugify(text)
            sid, n = base, 2
            while sid in used:
                sid, n = f"{base}-{n}", n + 1
            used.add(sid)
            toc.append({"id": sid, "text": text})
            out.append(f'<h2 id="{sid}">{_inline(text)}</h2>')
            i += 1
        elif line.startswith("### "):
            out.append(f"<h3>{_inline(line[4:])}</h3>")
            i += 1
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{_inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{_inline(line[2:])}</blockquote>")
            i += 1
        elif line.strip() == "":
            i += 1
        else:
            para = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(## |### |- |> |```)", lines[i]):
                para.append(lines[i])
                i += 1
            out.append(f"<p>{_inline(' '.join(para))}</p>")
    return "\n".join(out), toc


def reading_minutes(content: str) -> int:
    return max(1, round(len(content.split()) / 200))


# ---------- modelos ----------

class PostSummary(BaseModel):
    slug: str
    title: str
    excerpt: str
    tag: str
    category_slug: str
    published_at: date
    reading_minutes: int
    featured: bool
    cover: str | None


class TocItem(BaseModel):
    id: str
    text: str


class Post(PostSummary):
    author: str
    content: str
    html: str
    toc: list[TocItem]


class PostPage(BaseModel):
    items: list[PostSummary]
    total: int
    page: int
    pages: int


class PostIn(BaseModel):
    slug: Annotated[str, Field(pattern=SLUG_RE, max_length=90)]
    title: Annotated[str, Field(min_length=3, max_length=140)]
    excerpt: Annotated[str, Field(min_length=10, max_length=300)]
    content: Annotated[str, Field(min_length=20)]
    tag: Annotated[str, Field(min_length=2, max_length=40)]
    published_at: date | None = None
    featured: bool = False
    cover: Annotated[str | None, Field(max_length=300, pattern=r"^(/assets/|https://)")] = None


class Category(BaseModel):
    name: str
    slug: str
    count: int
    description: str


def summary(row: sqlite3.Row) -> PostSummary:
    return PostSummary(
        slug=row["slug"], title=row["title"], excerpt=row["excerpt"], tag=row["tag"], category_slug=slugify(row["tag"]),
        published_at=row["published_at"], reading_minutes=reading_minutes(row["content"]),
        featured=bool(row["featured"]), cover=row["cover"],
    )


def full(row: sqlite3.Row) -> Post:
    body, toc = render_markdown(row["content"])
    return Post(**summary(row).model_dump(), author=AUTHOR, content=row["content"], html=body, toc=[TocItem(**t) for t in toc])


def require_admin(x_admin_token: Annotated[str | None, Header()] = None) -> None:
    if not x_admin_token or not secrets.compare_digest(x_admin_token, ADMIN_TOKEN):
        raise HTTPException(status_code=401, detail="Token de administrador ausente ou inválido.")


AdminDep = Annotated[None, Depends(require_admin)]

# ---------- rotas da API ----------

router = APIRouter(prefix="/api", tags=["blog"])


@router.get("/posts")
def list_posts(
    db: DbDep,
    category: Annotated[str | None, Query(max_length=60, description="slug da categoria")] = None,
    featured: bool | None = None,
    q: Annotated[str | None, Query(max_length=80)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 9,
) -> PostPage:
    where, args = [], []
    if category:
        name = category_name(db, category)
        if name is None:
            return PostPage(items=[], total=0, page=page, pages=1)
        where.append("tag = ?")
        args.append(name)
    if featured is not None:
        where.append("featured = ?")
        args.append(int(featured))
    if q:
        where.append("(title LIKE ? OR excerpt LIKE ? OR content LIKE ?)")
        args += [f"%{q}%"] * 3
    clause = f"WHERE {' AND '.join(where)}" if where else ""
    total = db.execute(f"SELECT COUNT(*) FROM posts {clause}", args).fetchone()[0]
    rows = db.execute(
        f"SELECT * FROM posts {clause} ORDER BY published_at DESC, id DESC LIMIT ? OFFSET ?",
        [*args, limit, (page - 1) * limit],
    ).fetchall()
    return PostPage(items=[summary(r) for r in rows], total=total, page=page, pages=max(1, -(-total // limit)))


def all_categories(db: sqlite3.Connection) -> list[Category]:
    counts = {r[0]: r[1] for r in db.execute("SELECT tag, COUNT(*) FROM posts GROUP BY tag")}
    names = sorted(counts, key=lambda n: (CATEGORY_ORDER.index(n) if n in CATEGORY_ORDER else 99, n))
    return [Category(name=n, slug=slugify(n), count=counts[n], description=CATEGORY_DESC.get(n, f"Artigos sobre {n}.")) for n in names]


def category_name(db: sqlite3.Connection, slug: str) -> str | None:
    return next((c.name for c in all_categories(db) if c.slug == slug), None)


@router.get("/categories")
def list_categories(db: DbDep) -> list[Category]:
    return all_categories(db)


@router.get("/posts/{slug}")
def read_post(slug: str, db: DbDep) -> Post:
    row = db.execute("SELECT * FROM posts WHERE slug = ?", [slug]).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    return full(row)


@router.get("/posts/{slug}/related")
def related_posts(slug: str, db: DbDep, limit: Annotated[int, Query(ge=1, le=6)] = 3) -> list[PostSummary]:
    row = db.execute("SELECT tag FROM posts WHERE slug = ?", [slug]).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    rows = db.execute(
        "SELECT * FROM posts WHERE slug != ? ORDER BY (tag = ?) DESC, published_at DESC LIMIT ?",
        [slug, row["tag"], limit],
    ).fetchall()
    return [summary(r) for r in rows]


@router.post("/posts", status_code=201)
def create_post(data: PostIn, db: DbDep, _: AdminDep) -> Post:
    when = (data.published_at or date.today()).isoformat()
    try:
        db.execute(
            "INSERT INTO posts (slug, title, excerpt, content, tag, published_at, featured, cover) VALUES (?,?,?,?,?,?,?,?)",
            [data.slug, data.title, data.excerpt, data.content, data.tag, when, int(data.featured), data.cover],
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um post com esse slug.")
    return read_post(data.slug, db)


@router.put("/posts/{slug}")
def update_post(slug: str, data: PostIn, db: DbDep, _: AdminDep) -> Post:
    if db.execute("SELECT 1 FROM posts WHERE slug = ?", [slug]).fetchone() is None:
        raise HTTPException(status_code=404, detail="Post não encontrado.")
    when = (data.published_at or date.today()).isoformat()
    try:
        db.execute(
            "UPDATE posts SET slug=?, title=?, excerpt=?, content=?, tag=?, published_at=?, featured=?, cover=? WHERE slug=?",
            [data.slug, data.title, data.excerpt, data.content, data.tag, when, int(data.featured), data.cover, slug],
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um post com esse slug.")
    return read_post(data.slug, db)


@router.delete("/posts/{slug}", status_code=204)
def delete_post(slug: str, db: DbDep, _: AdminDep) -> None:
    cur = db.execute("DELETE FROM posts WHERE slug = ?", [slug])
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Post não encontrado.")


app = FastAPI(title="Nerd Dev Blog API", version="3.0.0")
init_db()
app.include_router(router)


# ---------- páginas (HTML renderizado no servidor onde importa para SEO) ----------

def base_url(request: Request) -> str:
    return SITE_URL or str(request.base_url).rstrip("/")


def _read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def _page(name: str):
    def handler() -> FileResponse:
        return FileResponse(ROOT / name)
    return handler


app.add_api_route("/", _page("index.html"), methods=["GET"], include_in_schema=False)


def cats_nav(db: sqlite3.Connection, active: str = "") -> str:
    """Barra de categorias (HTML pronto no servidor: bom para SEO e sem piscar)."""
    esc = html.escape
    items = ['<a href="/blog"' + ('' if active else ' aria-current="page"') + '>Todas</a>']
    for c in all_categories(db):
        cur = ' aria-current="page"' if c.slug == active else ""
        items.append(f'<a href="/categoria/{c.slug}" class="cat-{c.slug}"{cur}>{esc(c.name)}</a>')
    return '<nav class="cats" aria-label="Categorias"><div class="wrap cats__in">' + "".join(items) + "</div></nav>"


def blog_page(request: Request, db: sqlite3.Connection, cat: Category | None) -> HTMLResponse:
    esc = html.escape
    base = base_url(request)
    if cat:
        title, desc, url, h1 = f"{cat.name}: artigos e dicas | Blog {SITE_NAME}", cat.description, f"{base}/categoria/{cat.slug}", cat.name
    else:
        title = f"Blog de programação, games e cultura pop | {SITE_NAME}"
        desc = "Notícias, guias e explicações didáticas sobre Nintendo, games, cultura pop, mundo de dados, IA e programação."
        url, h1 = f"{base}/blog", "Blog da Nerd Dev"
    head = f"""<title>{esc(title)}</title>
  <meta name="description" content="{esc(desc, quote=True)}">
  <link rel="canonical" href="{esc(url)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title, quote=True)}">
  <meta property="og:description" content="{esc(desc, quote=True)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{base}/assets/img/og.jpg">
  <script type="application/ld+json">{_json_ld({"@context": "https://schema.org", "@type": "CollectionPage" if cat else "Blog", "name": h1, "description": desc, "url": url, "inLanguage": "pt-BR"})}</script>"""
    page = (
        _read("blog.html")
        .replace("<!--HEAD-->", head)
        .replace("<!--CATS-->", cats_nav(db, cat.slug if cat else ""))
        .replace("<!--H1-->", esc(h1))
        .replace("<!--LEAD-->", esc(desc))
        .replace("<!--CAT-->", cat.slug if cat else "")
    )
    return HTMLResponse(page)


@app.get("/blog", include_in_schema=False)
def blog_home(request: Request, db: DbDep) -> HTMLResponse:
    return blog_page(request, db, None)


@app.get("/categoria/{slug}", include_in_schema=False)
def category_page(slug: str, request: Request, db: DbDep) -> HTMLResponse:
    cat = next((c for c in all_categories(db) if c.slug == slug), None)
    if cat is None:
        return HTMLResponse(_read("404.html"), status_code=404)
    return blog_page(request, db, cat)


@app.get("/index.html", include_in_schema=False)
def old_home() -> RedirectResponse:
    return RedirectResponse("/", status_code=301)


@app.get("/blog.html", include_in_schema=False)
def old_blog() -> RedirectResponse:
    return RedirectResponse("/blog", status_code=301)


def _json_ld(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


@app.get("/blog/{slug}", include_in_schema=False)
def article_page(slug: str, request: Request, db: DbDep) -> HTMLResponse:
    row = db.execute("SELECT * FROM posts WHERE slug = ?", [slug]).fetchone()
    if row is None:
        return HTMLResponse(_read("404.html"), status_code=404)
    post = full(row)
    base = base_url(request)
    url = f"{base}/blog/{post.slug}"
    image = f"{base}/assets/img/og.jpg"
    esc = html.escape
    title = f"{post.title} | {SITE_NAME}"
    head = f"""<title>{esc(title)}</title>
  <meta name="description" content="{esc(post.excerpt, quote=True)}">
  <link rel="canonical" href="{esc(url)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{esc(post.title, quote=True)}">
  <meta property="og:description" content="{esc(post.excerpt, quote=True)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(image)}">
  <meta property="article:published_time" content="{post.published_at.isoformat()}">
  <meta property="article:section" content="{esc(post.tag, quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{_json_ld({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt,
        "image": image,
        "datePublished": post.published_at.isoformat(),
        "dateModified": post.published_at.isoformat(),
        "articleSection": post.tag,
        "inLanguage": "pt-BR",
        "mainEntityOfPage": url,
        "author": {"@type": "Organization", "name": AUTHOR},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": f"{base}/assets/img/logo-tile.jpg"}},
    })}</script>
  <script type="application/ld+json">{_json_ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": f"{base}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{base}/blog"},
            {"@type": "ListItem", "position": 3, "name": post.title, "item": url},
        ],
    })}</script>"""
    toc_items = "".join(f'<li><a href="#{t.id}">{esc(t.text)}</a></li>' for t in post.toc)
    toc = f'<details class="toc"><summary>Neste artigo</summary><ol>{toc_items}</ol></details>' if len(post.toc) >= 3 else ""
    months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    d = post.published_at
    pretty = f"{d.day} {months[d.month - 1]} {d.year}"
    article = f"""<div class="wrap article__wrap">
      <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a> <span aria-hidden="true">/</span> <a href="/blog">Blog</a> <span aria-hidden="true">/</span> <a href="/categoria/{post.category_slug}">{esc(post.tag)}</a></nav>
      <header class="article__head">
        <p class="post__meta"><a class="badge cat-{post.category_slug}" href="/categoria/{post.category_slug}">{esc(post.tag)}</a><time datetime="{d.isoformat()}">{pretty}</time><span>{post.reading_minutes} min de leitura</span></p>
        <h1>{esc(post.title)}</h1>
        <p class="lead">{esc(post.excerpt)}</p>
        <p class="byline">Por <strong>{esc(AUTHOR)}</strong></p>
      </header>
      {toc}
      <div class="prose">{post.html}</div>
      <div class="share" data-title="{esc(post.title, quote=True)}" data-url="{esc(url)}"></div>
      <section class="author"><div class="author__mark"></div><div><p class="author__n">{esc(AUTHOR)}</p><p>Explicamos programação e cultura pop de um jeito simples, para quem está começando ou só quer entender melhor o mundo dev.</p></div></section>
    </div>
    <section class="related" id="related" data-slug="{esc(post.slug)}" hidden><div class="wrap"><h2>Continue lendo</h2><div class="pgrid pgrid--three" id="related-grid"></div></div></section>"""
    page = _read("post.html").replace("<!--HEAD-->", head).replace("<!--ARTICLE-->", article).replace("<!--CATS-->", cats_nav(db, post.category_slug))
    return HTMLResponse(page)


@app.get("/robots.txt", include_in_schema=False)
def robots(request: Request) -> Response:
    return Response(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /docs\n\nSitemap: {base_url(request)}/sitemap.xml\n", media_type="text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap(request: Request, db: DbDep) -> Response:
    base = base_url(request)
    urls = [(f"{base}/", None), (f"{base}/blog", None)] + [(f"{base}/categoria/{c.slug}", None) for c in all_categories(db)]
    for r in db.execute("SELECT slug, published_at FROM posts ORDER BY published_at DESC"):
        urls.append((f"{base}/blog/{r['slug']}", r["published_at"]))
    body = "".join(
        f"<url><loc>{html.escape(u)}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>" for u, d in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'
    return Response(xml, media_type="application/xml")


@app.get("/feed.xml", include_in_schema=False)
def feed(request: Request, db: DbDep) -> Response:
    base = base_url(request)
    items = []
    for r in db.execute("SELECT * FROM posts ORDER BY published_at DESC, id DESC LIMIT 20"):
        when = format_datetime(datetime.combine(date.fromisoformat(r["published_at"]), time(12), tzinfo=timezone.utc))
        link = f"{base}/blog/{r['slug']}"
        items.append(
            f"<item><title>{html.escape(r['title'])}</title><link>{html.escape(link)}</link>"
            f"<guid>{html.escape(link)}</guid><pubDate>{when}</pubDate>"
            f"<category>{html.escape(r['tag'])}</category><description>{html.escape(r['excerpt'])}</description></item>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
        f"<title>{SITE_NAME}</title><link>{html.escape(base)}/blog</link>"
        "<description>Programação e cultura pop de forma didática.</description><language>pt-BR</language>"
        + "".join(items) + "</channel></rss>"
    )
    return Response(xml, media_type="application/rss+xml")


app.mount("/assets", StaticFiles(directory=ROOT / "assets"), name="assets")
