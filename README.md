# Nerd Dev: landing + blog

## Rodar localmente

```bash
pip install -r api/requirements.txt
uvicorn api.main:app --reload
```

Abra http://127.0.0.1:8000 (site), `/blog` (blog), `/blog/{slug}` (artigo), `/docs` (API), `/sitemap.xml`, `/feed.xml` e `/robots.txt`.
Defina `NERDDEV_SITE_URL=https://seu-dominio` para canonical, sitemap e feed com o endereço real.

## API do blog

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/posts?tag=&q=&page=&limit=` | Lista paginada, com filtro por assunto e busca |
| GET | `/api/tags` | Assuntos existentes |
| GET | `/api/posts/{slug}` | Artigo completo (`content` em Markdown, `html` pronto e `toc`) |
| GET | `/api/posts/{slug}/related` | Artigos relacionados (mesmo assunto primeiro) |
| POST | `/api/posts` | Cria artigo (exige `X-Admin-Token`) |
| PUT | `/api/posts/{slug}` | Edita artigo (exige `X-Admin-Token`) |
| DELETE | `/api/posts/{slug}` | Remove artigo (exige `X-Admin-Token`) |

Defina o token antes de publicar de verdade: `NERDDEV_ADMIN_TOKEN=um-segredo-forte`.
O padrão de desenvolvimento é `dev-troque-este-token`.

Exemplo de novo artigo:

```bash
curl -X POST http://127.0.0.1:8000/api/posts \
  -H "X-Admin-Token: dev-troque-este-token" -H "content-type: application/json" \
  -d '{"slug":"meu-artigo","title":"Meu artigo","excerpt":"Resumo curto do artigo.","tag":"Programação","content":"## Título\n\nTexto com **negrito** e `código`."}'
```

Markdown aceito: `##`, `###`, listas com `-`, citações com `>`, blocos de código com três crases, **negrito**, `código` e links.

O banco (`api/blog.db`) é criado no primeiro start com 5 artigos de exemplo e não vai para o Git.

## Pendências
- Preencher `SOCIAL` em `assets/site.js` e os links do rodapé com os perfis reais.

## Publicar no GitHub Pages (versão estática)

O GitHub Pages só serve arquivos, então a API não roda lá. O exportador gera tudo pronto na pasta `docs/`:

```bash
python tools/export_static.py --site-url https://godofin.github.io/nerd-dev-intro
```

Depois é só dar commit e push. Em Settings > Pages do repositório: Source = "Deploy from a branch", branch `main`, pasta `/docs`.
Para publicar um artigo novo na versão estática: cadastre pela API local, rode o exportador de novo e faça o push.
