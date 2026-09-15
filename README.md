# St Kitts Shore Excursions

Static site for [stkittsshoreexcursion.com](https://stkittsshoreexcursion.com) — an independent cruise passenger guide to St Kitts shore excursions.

## Deploy (Cloudflare Pages)

Project: `st-kitts-shore-excursions`

Production is Git-connected to `main`. Normal path:

1. Commit changes on `main`
2. Push to `origin` — Cloudflare Pages builds from the repo root
3. Confirm deployment in the Pages dashboard

Direct upload (when needed):

```bash
npx wrangler pages deploy . --project-name=st-kitts-shore-excursions --branch=main
```

Config that must stay in repo for World 2.0 completion:

- `404.html` — branded 404
- `_redirects` — legacy `.html` → `/slug/` and source blocks
- `functions/_middleware.js` — www → apex and source/data/scripts blocks
- `wrangler.jsonc` — Pages project metadata (`pages_build_output_dir: "."`)

Canonical URL model: apex + trailing-slash directories (`/port-guide/`).

No site build step is required for HTML. Optional schedule tooling:

```bash
npm run build:all
```

## Local preview

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Structure

- `index.html` — Homepage
- `*/index.html` — Editorial routes (trailing-slash directories)
- `ship-schedule/` — Cruise call hub + year/month pages
- `css/styles.css`, `js/main.js` — Shared assets
- `sitemap.xml`, `robots.txt` — SEO
