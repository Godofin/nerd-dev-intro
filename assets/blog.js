// Blog da Nerd Dev (portal). Lê tudo da API em /api. Para outro servidor, defina window.NERDDEV_API antes deste script.
const API = (window.NERDDEV_API || "") + "/api";
// Versão estática (GitHub Pages): os dados vêm de /data/site.json e as páginas já saem prontas do exportador.
const STATIC = !!window.NERDDEV_STATIC;
const BASE = window.NERDDEV_BASE || "";
const PAGE_SIZE = 8;

const $ = (id) => document.getElementById(id);
const fmtDate = (iso) =>
  new Date(iso + "T12:00:00").toLocaleDateString("pt-BR", { day: "numeric", month: "short", year: "numeric" }).replace(/\./g, "");

let siteData;
async function staticApi(path) {
  if (!siteData) {
    const res = await fetch(BASE + "/data/site.json");
    if (!res.ok) throw Object.assign(new Error("HTTP " + res.status), { status: res.status });
    siteData = await res.json();
  }
  const [route, query = ""] = path.split("?");
  const p = new URLSearchParams(query);
  if (route === "/categories") return siteData.categories;
  const rel = route.match(/^\/posts\/([^/]+)\/related$/);
  if (rel) {
    const cur = siteData.posts.find((x) => x.slug === decodeURIComponent(rel[1]));
    if (!cur) throw Object.assign(new Error("HTTP 404"), { status: 404 });
    return siteData.posts
      .filter((x) => x.slug !== cur.slug)
      .sort((a, b) => (b.tag === cur.tag) - (a.tag === cur.tag))
      .slice(0, Number(p.get("limit") || 3));
  }
  if (route === "/posts") {
    const limit = Number(p.get("limit") || 9), page = Number(p.get("page") || 1);
    const q = (p.get("q") || "").toLowerCase();
    let items = siteData.posts;
    if (p.get("category")) items = items.filter((x) => x.category_slug === p.get("category"));
    if (p.get("featured") === "true") items = items.filter((x) => x.featured);
    if (q) items = items.filter((x) => x.text.includes(q));
    const total = items.length;
    return { items: items.slice((page - 1) * limit, page * limit), total, page, pages: Math.max(1, Math.ceil(total / limit)) };
  }
  throw Object.assign(new Error("HTTP 404"), { status: 404 });
}

async function api(path) {
  if (STATIC) return staticApi(path);
  const res = await fetch(API + path);
  if (!res.ok) {
    const err = new Error("HTTP " + res.status);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
}

/* Capa: se o artigo tem imagem (campo "cover"), usa; senão gera uma arte da marca, sempre igual para o mesmo slug. */
function paintCover(node, slug) {
  let h = 2166136261;
  for (const ch of slug) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
  h >>>= 0;
  node.classList.add("cv" + (h % 4));
  node.style.setProperty("--cx", 45 + (h >> 3) % 50 + "%");
  node.style.setProperty("--cy", 15 + (h >> 7) % 60 + "%");
  node.style.setProperty("--cs", 42 + (h >> 11) % 36 + "%");
  node.style.setProperty("--cr", ((h >> 5) % 40) - 20 + "deg");
}

function cover(p, withBadge) {
  const c = el("div", "cover");
  c.setAttribute("aria-hidden", "true");
  if (p.cover) {
    const img = el("img", "cover__img");
    img.src = p.cover.startsWith("/") ? BASE + p.cover : p.cover; img.alt = ""; img.loading = "lazy";
    c.append(img);
  } else {
    paintCover(c, p.slug);
  }
  if (withBadge) c.append(badge(p, "span"));
  return c;
}

function badge(p, tag = "span") {
  return el(tag, "badge cat-" + p.category_slug, p.tag);
}

function meta(p) {
  const m = el("p", "post__meta");
  m.append(el("span", null, fmtDate(p.published_at)), el("span", null, p.reading_minutes + " min de leitura"));
  return m;
}

const href = (p) => BASE + "/blog/" + encodeURIComponent(p.slug) + (STATIC ? "/" : "");

/* cartão vertical (home e destaques) */
function card(p, lead) {
  const a = el("a", "pcard" + (lead ? " pcard--lead" : ""));
  a.href = href(p);
  const body = el("div", "pcard__body");
  body.append(meta(p), el(lead ? "h2" : "h3", "pcard__title", p.title), el("p", "pcard__ex", p.excerpt));
  a.append(cover(p, true), body);
  return a;
}

/* linha da lista "Últimas notícias" */
function row(p) {
  const a = el("a", "row");
  a.href = href(p);
  const txt = el("div", "row__txt");
  const top = el("p", "post__meta");
  top.append(badge(p), el("span", null, fmtDate(p.published_at)));
  txt.append(top, el("h3", "row__title", p.title), el("p", "row__ex", p.excerpt));
  a.append(cover(p, false), txt);
  return a;
}

/* destaque principal (grande) e laterais (pequenos) */
function featBig(p) {
  const a = el("a", "fbig");
  a.href = href(p);
  const body = el("div", "fbig__body");
  body.append(badge(p), el("h2", "fbig__title", p.title), el("p", "fbig__ex", p.excerpt), meta(p));
  a.append(cover(p, false), body);
  return a;
}
function featSmall(p) {
  const a = el("a", "fsmall");
  a.href = href(p);
  const body = el("div", "fsmall__body");
  body.append(badge(p), el("h3", "fsmall__title", p.title), meta(p));
  a.append(cover(p, false), body);
  return a;
}

function showState(box, title, text, retry) {
  box.hidden = false;
  box.replaceChildren(el("h2", null, title), el("p", null, text));
  if (retry) {
    const b = el("button", "btn btn--ghost", "Tentar de novo");
    b.type = "button";
    b.addEventListener("click", retry);
    box.append(b);
  }
}

/* ---------- portal (/blog e /categoria/{slug}) ---------- */
function initPortal() {
  const cat = document.body.dataset.cat || "";
  const st = { q: "", page: 1, pages: 1 };
  const list = $("list"), state = $("state"), more = $("more"), search = $("q");
  const featSec = $("feat-sec"), hlSec = $("hl-sec");
  let heroSlugs = [];

  const showHome = () => !cat && !st.q;

  function listSkeleton() {
    list.replaceChildren(...Array.from({ length: 4 }, () => el("div", "skeleton skeleton--row")));
  }

  async function loadList(append) {
    state.hidden = true;
    if (!append) listSkeleton();
    const params = new URLSearchParams({ page: st.page, limit: PAGE_SIZE });
    if (cat) params.set("category", cat);
    if (st.q) params.set("q", st.q);
    try {
      const data = await api("/posts?" + params);
      st.pages = data.pages;
      if (!append) list.replaceChildren();
      list.append(...data.items.map(row));
      if (!data.total) showState(state, "Nenhum artigo encontrado", "Tente outra palavra ou escolha outra categoria.");
      more.hidden = st.page >= st.pages;
    } catch {
      list.replaceChildren();
      more.hidden = true;
      showState(state, "Não foi possível carregar os artigos", "A API do blog não respondeu. Confira se o servidor está rodando e tente de novo.", () => loadList(false));
    }
  }

  async function loadFeatured() {
    try {
      let items = (await api("/posts?featured=true&limit=4")).items;
      if (items.length < 4) {
        const latest = (await api("/posts?limit=8")).items.filter((p) => !items.some((f) => f.slug === p.slug));
        items = items.concat(latest).slice(0, 4);
      }
      if (!items.length) return;
      heroSlugs = items.map((p) => p.slug);
      $("feat").replaceChildren(featBig(items[0]), ...items.slice(1).map(featSmall));
      featSec.hidden = false;
    } catch { /* a lista abaixo mostra o erro */ }
  }

  async function loadHighlights(slug, tabs) {
    try {
      const data = await api("/posts?limit=12" + (slug ? "&category=" + slug : ""));
      const items = (slug ? data.items : data.items.filter((p) => !heroSlugs.includes(p.slug))).slice(0, 3);
      $("hl").replaceChildren(...items.map((p) => card(p, false)));
      hlSec.hidden = !items.length && !slug;
    } catch { hlSec.hidden = true; }
    for (const b of tabs.children) b.setAttribute("aria-pressed", String(b.dataset.slug === (slug || "")));
  }

  function renderSide(cats) {
    $("side-cats").replaceChildren(...cats.map((c) => {
      const li = el("li");
      const a = el("a", "cat-" + c.slug);
      a.href = BASE + "/categoria/" + c.slug + (STATIC ? "/" : "");
      if (c.slug === cat) a.setAttribute("aria-current", "page");
      a.append(el("span", null, c.name), el("span", "side__n", String(c.count)));
      li.append(a);
      return li;
    }));
  }

  function applyMode() {
    featSec.hidden = !showHome() || !$("feat").children.length;
    hlSec.hidden = !showHome();
    $("listtitle").lastChild.textContent = st.q ? "Resultados da busca" : cat ? "Todos os artigos" : "Últimas notícias";
  }

  let timer;
  search.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => { st.q = search.value.trim(); st.page = 1; applyMode(); loadList(false); }, 300);
  });
  more.addEventListener("click", () => { st.page += 1; loadList(true); });

  api("/categories").then((cats) => {
    renderSide(cats);
    if (!showHome()) return;
    const tabs = $("tabs");
    for (const t of [{ name: "Todas", slug: "" }, ...cats.slice(0, 5)]) {
      const b = el("button", "tab cat-" + t.slug, t.name);
      b.type = "button"; b.dataset.slug = t.slug;
      b.addEventListener("click", () => loadHighlights(t.slug, tabs));
      tabs.append(b);
    }
    loadFeatured().then(() => { applyMode(); loadHighlights("", tabs); });
  }).catch(() => {});

  applyMode();
  loadList(false);
}

/* ---------- últimos artigos na home ---------- */
async function initLatest() {
  const section = $("blog"), grid = $("latest-grid");
  try {
    const data = await api("/posts?limit=3");
    if (!data.items.length) return;
    data.items.forEach((p, i) => grid.append(card(p, i === 0)));
    if (data.items.length === 1) grid.classList.add("pgrid--solo");
    section.hidden = false;
  } catch { /* sem API, a seção continua escondida */ }
}

/* ---------- artigo (/blog/{slug}, HTML vindo pronto do servidor) ---------- */
function initArticle() {
  const share = document.querySelector(".share");
  if (share) {
    const { title, url } = share.dataset;
    const mk = (icon, label) => {
      const s = el("span", "ico");
      s.style.setProperty("--i", `url(${BASE}/assets/icons/${icon}.svg)`);
      s.setAttribute("aria-hidden", "true");
      return [s, document.createTextNode(label)];
    };
    const wa = el("a"); wa.href = "https://wa.me/?text=" + encodeURIComponent(title + " " + url); wa.target = "_blank"; wa.rel = "noopener noreferrer"; wa.append(...mk("whatsapp-logo", "WhatsApp"));
    const x = el("a"); x.href = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(title) + "&url=" + encodeURIComponent(url); x.target = "_blank"; x.rel = "noopener noreferrer"; x.append(...mk("x-logo", "X"));
    const copy = el("button"); copy.type = "button"; copy.append(...mk("link", "Copiar link"));
    copy.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(url); copy.lastChild.textContent = "Link copiado"; }
      catch { copy.lastChild.textContent = "Copie da barra de endereço"; }
      setTimeout(() => { copy.lastChild.textContent = "Copiar link"; }, 2200);
    });
    share.replaceChildren(el("span", "share__t", "Compartilhar"), wa, x, copy);
  }

  const rel = $("related");
  if (rel) {
    api("/posts/" + encodeURIComponent(rel.dataset.slug) + "/related?limit=3").then((items) => {
      if (!items.length) return;
      $("related-grid").append(...items.map((p) => card(p, false)));
      rel.hidden = false;
    }).catch(() => {});
  }
}

if ($("list")) initPortal();
if ($("latest-grid")) initLatest();
if (document.querySelector("[data-article]")) initArticle();
