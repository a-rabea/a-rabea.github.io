# Ahmed Rabea — portfolio

Static site, no framework. Live at https://a-rabea.github.io (GitHub Pages, deploys from `main`).

## Edit text
- Project copy: `content/projects.json` (title, Arabic name, label, one-liner, intro, details).
- Home page, about and contact text: `build.py` (`build_home`).
- Then run `python3 build.py` and commit.

## Add a project
1. Add its cover and frames to `assets_manifest.py`.
2. `python3 process_images.py`, then `python3 make_extras.py` (share cards, light-frame flags) (makes WebP at 1800 / 1000 px into `assets/img/<slug>`).
3. Add an entry to `content/projects.json` (order = order on the site).
4. `python3 build.py`.

## Custom domain
Add a `CNAME` file containing the domain (e.g. `ahmedrabea.com`), point the domain's DNS to GitHub Pages, and update `SITE["url"]` in `build.py`.

Fonts: Archivo and Readex Pro (SIL Open Font License), self-hosted in `assets/fonts`.

## Pricing (off until approved)
Every service and quick start in `content/services.json` has a `"price"` field set to `null`, which hides it.
Put text in it (for example `"From USD 2,500"`) and run `python3 build.py` to show it on the services page.

## Analytics
- GoatCounter (cookie-free page views and click events) and Cloudflare Web Analytics (cookie-free visits and Core Web Vitals).
  Settings at the top of `build.py`: `GOATCOUNTER_CODE`, `CLOUDFLARE_TOKEN`. Empty string turns either off.
- Click events, listed under "Events" in GoatCounter:
  `contact-email`, `contact-email-copy`, `contact-whatsapp`, `contact-phone`, `out-linkedin`, `out-behance`,
  `cta-hero`, `cta-case`, `cta-float`, `form-email`, `form-whatsapp`.
- No cookies are set, so no cookie banner is needed.

## Backups
- `v1-nov-2`: the live site as it was on 2 November 2026, before the SEO and conversion pass.
- `v1-live`: the first V1 snapshot. `v2`: the archived V2 redesign (not live).
To restore one, ask for that branch to be merged or reset onto `main`.
