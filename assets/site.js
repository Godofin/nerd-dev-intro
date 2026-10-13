// Perfis da Nerd Dev. Preencha com as URLs reais; enquanto estiver vazio, os botões rolam até o rodapé.
const SOCIAL = {
  instagram: "",
  youtube: "",
  tiktok: "",
  primary: "" // para onde vão os botões "Seguir a Nerd Dev" (ex.: o Instagram)
};

const root = document.documentElement;
root.classList.add("js");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;

for (const el of document.querySelectorAll("[data-social]")) {
  const url = SOCIAL[el.dataset.social];
  if (!url) continue;
  el.href = url;
  el.target = "_blank";
  el.rel = "noopener noreferrer";
}

// Entrada dos blocos ao rolar (hierarquia: o olho é guiado na ordem de leitura).
const items = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      io.unobserve(e.target);
    }
  }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
  items.forEach((el) => io.observe(el));
} else {
  items.forEach((el) => el.classList.add("in"));
}

// Manifesto: cada palavra vira um span; o CSS acende conforme ela entra na tela (scroll-driven animation).
for (const p of document.querySelectorAll("[data-words]")) {
  const words = p.textContent.trim().split(/\s+/);
  p.setAttribute("aria-label", words.join(" "));
  p.replaceChildren(...words.flatMap((w, i) => {
    const s = document.createElement("span");
    s.className = "w";
    s.setAttribute("aria-hidden", "true");
    s.textContent = w;
    return i < words.length - 1 ? [s, document.createTextNode(" ")] : [s];
  }));
}

if (fine && !reduce) {
  // Botões magnéticos: puxam levemente em direção ao cursor (feedback de que são clicáveis).
  for (const el of document.querySelectorAll("[data-magnetic]")) {
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + "px");
      el.style.setProperty("--my", ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + "px");
    });
    el.addEventListener("pointerleave", () => { el.style.removeProperty("--mx"); el.style.removeProperty("--my"); });
  }

  // Inclinação do logo e paralaxe do símbolo gigante do hero seguem o cursor.
  for (const el of document.querySelectorAll("[data-tilt]")) {
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty("--rx", (-((e.clientY - r.top) / r.height - 0.5) * 12).toFixed(2) + "deg");
      el.style.setProperty("--ry", (((e.clientX - r.left) / r.width - 0.5) * 12).toFixed(2) + "deg");
    });
    el.addEventListener("pointerleave", () => { el.style.setProperty("--rx", "0deg"); el.style.setProperty("--ry", "0deg"); });
  }
  const hero = document.getElementById("hero");
  if (hero) {
    hero.addEventListener("pointermove", (e) => {
      hero.style.setProperty("--px", ((e.clientX / innerWidth - 0.5) * 2).toFixed(3));
      hero.style.setProperty("--py", ((e.clientY / innerHeight - 0.5) * 2).toFixed(3));
    }, { passive: true });
  }
}
