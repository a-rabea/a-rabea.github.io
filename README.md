# Ahmed Rabea — portfolio

Static site, no framework. Live at https://a-rabea.github.io (GitHub Pages, deploys from `main`).

## Edit text
- Project copy: `content/projects.json` (title, Arabic name, label, one-liner, intro, details).
- Home page, about and contact text: `build.py` (`build_home`).
- Then run `python3 build.py` and commit.

## Add a project (case-study template)
1. Add its cover and frames to `assets_manifest.py`, then run `python3 process_images.py` (WebP at 1800 / 1000 px plus 480 px thumbnails) and `python3 make_extras.py` (share card, light-frame flags).
2. Add an entry to `content/projects.json`. Order in the file = order on the site. Copy an existing entry and change:
   - `title`, `arabic`, `kind`, `line`, `color`, `tags`, `meta` (Role, Scope, Market, Type).
   - `case`: `client`, `industry`, `engagement`, `year`, `context`, `challenge`, `direction`, `system`, `outcome`, `credits`,
     `highlights` (5 frame numbers: the first is shown large) and `chapters` (`[["Chapter name", [frame numbers]], ...]`).
   - Any `case` text that starts with `TODO` or is `null` is hidden on the site.
3. To feature it on the home page, put its slug in `FEATURED` in `build.py` (three projects).
4. Run `python3 build.py`. It also rewrites `content/CONTENT-TODO.md`, the list of every placeholder still waiting for your input.

## Custom domain
Add a `CNAME` file containing the domain (e.g. `ahmedrabea.com`), point the domain's DNS to GitHub Pages, and update `SITE["url"]` in `build.py`.

Fonts: Archivo and Readex Pro (SIL Open Font License), self-hosted in `assets/fonts`.

## Pricing and timelines (off until approved)
Every service in `content/services.json` has `"price"` and `"timeline"` set to `null`, which hides them. Quick starts have `"price"` too.
Put text in them (for example `"From USD 2,500"`, `"4 to 6 weeks"`) and run `python3 build.py` to show them on the services page.
The three "Ways to start" cards are the `start` list in the same file.

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
