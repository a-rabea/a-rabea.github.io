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
