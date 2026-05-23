# happy corp

A tiny company that exists to bring you a little more joy than you had a minute ago.

Live site: https://myusuf3.github.io/happy-corp/

## What this repo is

The site shows one tiny moment of joy each day. Today's joy lives at `/`; every seeded day has its own stable URL at `/d/YYYY-MM-DD/` so it's shareable. The content is a hand-written list in [`data/joys.json`](./data/joys.json) and the pages are static HTML — no framework, no runtime dependencies. The only "build step" is a tiny Python script that emits the day pages from the JSON; output is checked into git.

## Content workflow

1. Edit [`data/joys.json`](./data/joys.json) — each entry is `{ "date": "YYYY-MM-DD", "copy": "…", "emoji": "…" }`. Keep the voice warm/tiny/handcrafted (see below).
2. Run `python3 scripts/generate.py`. This rewrites `index.html` and every `d/YYYY-MM-DD/index.html`.
3. Commit and push.

The root page also embeds the joy list inline and uses a tiny inline script to pick today's entry by local date. If JavaScript is off, the page still renders a joy (the first seeded entry) with the caption "a tiny moment of joy" — the core moment still works.

`/d/YYYY-MM-DD/` pages are fully static — no script needed for the core moment. They're the canonical shareable URL for a given day.

## Stack

- **Plain HTML + CSS, no build step.** Smallest credible thing that could be a website. We can graduate to Vite, Astro, or SvelteKit the day we actually have a reason to.
- **Hosted on GitHub Pages.** Free, no payment method required, push-to-deploy is built in.
- **Repo lives at [`myusuf3/happy-corp`](https://github.com/myusuf3/happy-corp).** Public.

## Run it locally

Any one of these:

```bash
# Easiest: just open the file
open index.html

# Or serve it (so favicon and relative paths behave like prod)
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy

GitHub Pages serves the repo's `main` branch from the root. To deploy any change:

```bash
git add .
git commit -m "your message"
git push origin main
```

Within a minute or so the live site updates. No CI, no build step, no extra config.

If you ever need to redo the Pages setup:

```bash
gh api -X POST /repos/myusuf3/happy-corp/pages \
  -f source[branch]=main -f source[path]=/
```

## Analytics + privacy

We use [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/) — free, no cookies, no PII, no fingerprinting. The user-facing privacy note lives at [`privacy.html`](./privacy.html) and is linked from the footer of every page.

To turn it on (one-time, ~30 seconds):

1. Sign in at [dash.cloudflare.com](https://dash.cloudflare.com) → **Analytics & Logs** → **Web Analytics** → **Add a site** → choose **Manual setup**, enter `myusuf3.github.io/happy-corp`.
2. Copy the `token` value out of the snippet Cloudflare gives you (the long hex string inside `data-cf-beacon='{"token":"…"}'`).
3. Replace `REPLACE_WITH_CF_TOKEN` with that token in [`scripts/generate.py`](./scripts/generate.py) (inside the `ANALYTICS_STUB` block), then run `python3 scripts/generate.py` to propagate it into `index.html` and every `d/YYYY-MM-DD/index.html`. Commit and push. The beacon script is a no-op until the token is real, so there is zero risk of stray events before then.

That's it — no build step, no extra dependency.

## Voice

Warm, tiny, handcrafted. No enterprise tone in copy, error states, or UI. If a sentence sounds like it could appear in a SaaS onboarding email, rewrite it.

## License

TBD — see [LICENSE](./LICENSE).
