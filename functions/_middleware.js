/**
 * Cloudflare Pages middleware for stkittsshoreexcursion.com.
 * - www → apex 301 (path preserved)
 * - Block source/data/scripts and deploy metadata from public serving
 */
const APEX = "stkittsshoreexcursion.com";

const BLOCKED = [
  /^\/content(\/|$)/i,
  /^\/partials(\/|$)/i,
  /^\/scripts(\/|$)/i,
  /^\/data(\/|$)/i,
  /^\/package(-lock)?\.json$/i,
  /^\/wrangler\.jsonc$/i,
  /^\/deploy\.sh$/i,
  /^\/README\.md$/i,
  /^\/\.assetsignore$/i,
  /^\/\.gitignore$/i,
];

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === `www.${APEX}`) {
    url.hostname = APEX;
    return Response.redirect(url.toString(), 301);
  }

  if (BLOCKED.some((re) => re.test(url.pathname))) {
    let body =
      '<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8"/><meta name="robots" content="noindex,follow"/><title>Page not found | St Kitts Shore Excursions</title></head><body><h1>Page not found</h1><p><a href="/">St Kitts home</a></p></body></html>';
    let contentType = "text/html; charset=utf-8";
    try {
      if (context.env && context.env.ASSETS) {
        const asset = await context.env.ASSETS.fetch(
          new Request(new URL("/404.html", url.origin), context.request)
        );
        if (asset.ok) {
          body = await asset.text();
          contentType = asset.headers.get("content-type") || contentType;
        }
      }
    } catch (_) {
      /* fallback body */
    }
    return new Response(body, {
      status: 404,
      headers: {
        "content-type": contentType,
        "cache-control": "private, no-store",
        "x-robots-tag": "noindex, follow",
      },
    });
  }

  return context.next();
}
