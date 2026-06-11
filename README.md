# St Kitts Shore Excursions

Static site for [stkittsshoreexcursion.com](https://stkittsshoreexcursion.com) — an independent cruise passenger guide to St Kitts shore excursions.

## Deploy to Cloudflare Pages

1. Push this repository to GitHub (or GitLab).
2. In Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. Select the repository and configure:
   - **Build command:** (leave empty)
   - **Build output directory:** `/` (project root)
4. Add custom domain `stkittsshoreexcursion.com` under **Custom domains**.

No build step required — pure static HTML, CSS and JS.

## Local preview

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Structure

- `index.html` — Homepage with comparison table and featured excursions
- `excursions.html` — All tours grid
- `port-guide.html`, `one-day-in-st-kitts.html` — Planning guides
- `private-tours.html`, `railway-tours.html` — Category pages
- `faq.html`, `contact.html` — Support pages
- 8 tour detail pages (`*-tour.html`, `catamaran-snorkel-cruise.html`)
- `css/styles.css`, `js/main.js` — Shared assets
- `sitemap.xml`, `robots.txt` — SEO
