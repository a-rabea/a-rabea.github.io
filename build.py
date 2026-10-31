"""Builds the static site from content/projects.json + image_meta.json.

Run:  python3 build.py
To add a project: add its images in assets_manifest.py, run process_images.py,
add an entry to content/projects.json, then run build.py.
"""
import json, html, os

SITE = {
    "name": "Ahmed Rabea",
    "arabic": "أحمد ربيع",
    "url": open("CNAME").read().strip().join(["https://", ""]) if __import__("os").path.exists("CNAME") else "https://a-rabea.github.io",  # CNAME overrides
    "email": "ahmed.r.bisher@gmail.com",
    "linkedin": "https://www.linkedin.com/in/a-rabea",
    "behance": "https://www.behance.net/a-rabea",
    "cv": "assets/Ahmed-Rabea-CV.pdf",
}
projects = json.load(open("content/projects.json", encoding="utf-8"))
meta = json.load(open("image_meta.json"))
e = lambda s: html.escape(s, quote=True)

FONTS = '<link rel="preload" href="{root}assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>'


def img(m, root, sizes, alt, cls="", eager=False, big=1800, small=1000):
    f = m["files"]
    k = sorted(f.keys(), key=int)
    srcset = ", ".join(f"{root}{f[w]} {min(int(w), m['w'])}w" for w in k)
    w = min(int(k[-1]), m["w"]); h = round(m["h"] * w / m["w"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{root}{f[k[-1]]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def head(title, desc, root, og=None):
    og_tag = f'<meta property="og:image" content="{SITE["url"]}/{og}">' if og and SITE["url"] else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
{og_tag}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
{FONTS.format(root=root)}
<link rel="stylesheet" href="{root}assets/site.css">
</head>
"""


def header(root, here=""):
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <a class="bar__name" href="{root}index.html">Ahmed Rabea</a>
  <nav class="bar__nav" aria-label="Main">
    <a href="{root}index.html#work"{' aria-current="page"' if here == "work" else ''}>Work</a>
    <a href="{root}index.html#about">About</a>
    <a href="{root}index.html#contact">Contact</a>
    <a href="{root}{SITE['cv']}" download>CV</a>
  </nav>
</header>
"""


def footer(root):
    return f"""<footer class="foot">
  <p>Ahmed Rabea, brand designer in Cairo.</p>
  <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
  <p><a href="{SITE['linkedin']}">LinkedIn</a> <a href="{SITE['behance']}">Behance</a> <a href="{root}{SITE['cv']}" download>CV (PDF)</a></p>
</footer>
"""


def tile(p, root, cls, sizes):
    m = meta[p["slug"]]["cover"]
    ar = f'<span class="tile__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else ""
    return f"""<li class="tile {cls}">
  <a href="{root}work/{p['slug']}/index.html">
    <div class="tile__img">{img(m, root, sizes, p['title'] + ' project cover')}</div>
    <div class="tile__text">
      <h3 class="tile__title"><span>{e(p['title'])}</span>{ar}</h3>
      <p class="tile__line">{e(p['line'])}</p>
      <p class="tile__kind">{e(p['kind'])}</p>
    </div>
  </a>
</li>"""


def build_home():
    root = ""
    first, rest = projects[0], projects[1:]
    pattern = ["tile--wide", "tile--narrow", "tile--narrow", "tile--wide"]
    tiles = "\n".join(tile(p, root, pattern[i % 4], "(max-width: 760px) 100vw, 60vw") for i, p in enumerate(rest))
    fm = meta[first["slug"]]["cover"]
    feature = f"""<a class="feature" href="work/{first['slug']}/index.html">
  <div class="feature__img">{img(fm, root, '(max-width: 760px) 100vw, 66vw', first['title'] + ' project cover', eager=True)}</div>
  <div class="feature__text">
    <p class="tile__kind">{e(first['kind'])}, 2025 to 2026</p>
    <h3 class="feature__title"><span>{e(first['title'])}</span><span class="tile__ar" lang="ar" dir="rtl">{e(first['arabic'])}</span></h3>
    <p class="feature__line">{e(first['line'])}</p>
    <span class="feature__cta">Read the case study</span>
  </div>
</a>"""
    portrait = img(meta["portrait"], root, "(max-width: 760px) 80vw, 30vw", "Portrait of Ahmed Rabea")
    page = head("Ahmed Rabea, brand designer",
                "Senior brand designer building Arabic-first, bilingual brand systems and campaigns for the UAE, KSA and Egypt.",
                root, meta[first["slug"]]["cover"]["files"]["1400"]) + f"""<body>
{header(root)}
<main id="main">
<section class="hero" aria-labelledby="hero-name">
  <h1 id="hero-name" class="hero__name">
    <span class="hero__latin">Ahmed Rabea</span>
    <span class="hero__arabic" lang="ar" dir="rtl">{SITE['arabic']}</span>
  </h1>
  <div class="hero__foot">
    <p class="hero__lede">Senior brand designer. I build Arabic-first, bilingual brand systems and campaigns for companies in the UAE, Saudi Arabia and Egypt, and run the creative operations that keep them consistent at volume.</p>
    <p class="hero__status">Based in Cairo.<br>Open to remote art director and design lead roles.</p>
  </div>
</section>

<section id="work" class="work" aria-labelledby="work-h">
  <div class="sec-head"><h2 id="work-h">Selected work</h2><p>{len(projects)} projects, client work first</p></div>
  {feature}
  <ul class="tiles" role="list">
{tiles}
  </ul>
</section>

<section id="about" class="about" aria-labelledby="about-h">
  <div class="about__img">{portrait}</div>
  <div class="about__body">
    <h2 id="about-h">About</h2>
    <p class="about__lede">I design brands that have to work in two scripts at once. Arabic is never a translation tag under the English: it gets its own typography, its own reading direction and its own voice.</p>
    <p>For more than five years I have worked across B2B SaaS, language services, healthcare and construction. I currently design for ELIXIR MD, where I wrote the 68-page brand guidelines and the Arabic typography system that extends them. Before that I led the visual direction at mazeed, and at Bayantech I led a team of five designers across five brands at once.</p>
    <h3>How I work</h3>
    <dl class="ways">
      <div><dt>Systems before assets</dt><dd>One idea, a few hard rules, then scale. At mazeed a single campaign system reached 80 assets across two languages and five formats.</dd></div>
      <div><dt>Arabic-first, not Arabic-also</dt><dd>English, UAE Arabic and Saudi Arabic each get their own layout, mirrored for reading direction rather than translated in place.</dd></div>
      <div><dt>Creative operations</dt><dd>Feedback, QA and asset management that let a team ship 250+ designs a month. I built CreativeVault, which cut file retrieval time by 90%.</dd></div>
    </dl>
    <h3>Experience</h3>
    <ol class="cv" role="list">
      <li><span>2026 to now</span><span>Senior Brand Designer, ELIXIR MD (remote)</span></li>
      <li><span>2025 to 2026</span><span>Senior Designer, mazeed (B2B SaaS, UAE and KSA)</span></li>
      <li><span>2024 to 2025</span><span>Creative Lead, Bayantech (language services)</span></li>
      <li><span>2023 to 2024</span><span>Graphic Designer, ATOP Arab (healthcare, MENA)</span></li>
      <li><span>2021 to 2023</span><span>Graphic Designer, CORE (construction)</span></li>
    </ol>
    <p class="about__more"><a href="{SITE['cv']}" download>Download the full CV (PDF)</a></p>
  </div>
</section>

<section id="contact" class="contact" aria-labelledby="contact-h">
  <h2 id="contact-h">Hiring a brand designer or art director? Let's talk.</h2>
  <p><a class="contact__mail" href="mailto:{SITE['email']}">{SITE['email']}</a></p>
  <ul class="contact__links" role="list">
    <li><a href="{SITE['linkedin']}">LinkedIn</a></li>
    <li><a href="{SITE['behance']}">Behance</a></li>
    <li><a href="{SITE['cv']}" download>CV (PDF)</a></li>
  </ul>
</section>
</main>
{footer(root)}
</body>
</html>
"""
    open("index.html", "w", encoding="utf-8").write(page)


def build_case(i, p):
    root = "../../"
    m = meta[p["slug"]]
    nxt = projects[(i + 1) % len(projects)]
    frames = []
    v = p.get("video")
    for n, f in enumerate(m["frames"], 1):
        frames.append(f'<figure class="frame">{img(f, root, "(max-width: 1600px) 100vw, 1600px", p["title"] + " case study, frame " + str(n), eager=(n == 1))}</figure>')
        if v and n == v["after"]:
            cls = "film film--vertical" if v["vertical"] else "film"
            frames.append(f"""<figure class="{cls}">
  <video controls playsinline preload="none" poster="{root}assets/img/{p['slug']}/poster.webp" src="{root}{m['video']}"></video>
  <figcaption>{e(v['caption'])}</figcaption>
</figure>""")
    ar = f'<span class="case__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else ""
    intro = "\n".join(f"<p>{e(x)}</p>" for x in p["intro"])
    dl = "\n".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["meta"])
    page = head(f"{p['title']}, by Ahmed Rabea", p["line"], root, m["cover"]["files"]["1400"]) + f"""<body>
{header(root, "work")}
<main id="main">
<article class="case">
  <header class="case__head">
    <p class="case__back"><a href="{root}index.html#work">All work</a></p>
    <h1 class="case__title"><span>{e(p['title'])}</span>{ar}</h1>
    <p class="case__kind">{e(p['kind'])}</p>
    <div class="case__intro">
      <div class="case__text">
        <p class="case__line">{e(p['line'])}</p>
        {intro}
      </div>
      <dl class="case__meta">{dl}</dl>
    </div>
  </header>
  <div class="frames">
{chr(10).join(frames)}
  </div>
</article>
<nav class="next" aria-label="Next project">
  <a href="{root}work/{nxt['slug']}/index.html">
    <span class="next__label">Next project</span>
    <span class="next__title">{e(nxt['title'])}</span>
  </a>
</nav>
</main>
{footer(root)}
</body>
</html>
"""
    os.makedirs(f"work/{p['slug']}", exist_ok=True)
    open(f"work/{p['slug']}/index.html", "w", encoding="utf-8").write(page)


build_home()
for i, p in enumerate(projects):
    build_case(i, p)
print("built", 1 + len(projects), "pages")
