"""Builds the static site from content/projects.json + image_meta.json.

Run:  python3 build.py
To add a project: add its images in assets_manifest.py, run process_images.py,
add an entry to content/projects.json, then run build.py.
"""
import json, html, os

SITE = {
    "name": "Ahmed Rabea",
    "arabic": "أحمد ربيع",
    "url": ("https://" + open("CNAME").read().strip()) if os.path.exists("CNAME") else "https://a-rabea.github.io",
    "email": "ahmed.r.bisher@gmail.com",
    "linkedin": "https://www.linkedin.com/in/a-rabea",
    "behance": "https://www.behance.net/a-rabea",
    "cv": "assets/Ahmed-Rabea-CV.pdf",
}
projects = json.load(open("content/projects.json", encoding="utf-8"))
meta = json.load(open("image_meta.json"))
e = lambda s: html.escape(s, quote=True)


def img(m, root, sizes, alt, cls="", eager=False):
    f = m["files"]
    k = sorted(f.keys(), key=int)
    srcset = ", ".join(f"{root}{f[w]} {min(int(w), m['w'])}w" for w in k)
    w = min(int(k[-1]), m["w"]); h = round(m["h"] * w / m["w"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{root}{f[k[-1]]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def cover_small(slug, root):
    return f"{root}{meta[slug]['cover']['files']['800']}"


def head(title, desc, root, og=None):
    og_tag = f'<meta property="og:image" content="{SITE["url"]}/{og}">' if og else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="p:domain_verify" content="021ae1545cf424912b139af6310727fe"/>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0D100F">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
{og_tag}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/site.css">
<script src="{root}assets/site.js" defer></script>
</head>
"""


def header(root):
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <a class="bar__name" href="{root}index.html">Ahmed Rabea</a>
  <nav class="bar__nav" aria-label="Main">
    <a href="{root}index.html#work">Work</a>
    <a href="{root}index.html#about">About</a>
    <a href="{root}index.html#contact">Contact</a>
  </nav>
</header>
<div class="peek" aria-hidden="true"><img alt=""></div>
"""


def footer(root):
    return f"""<footer class="foot">
  <p>Ahmed Rabea, brand designer, Cairo</p>
  <p><a href="mailto:{SITE['email']}">Email</a><a href="{SITE['linkedin']}">LinkedIn</a><a href="{SITE['behance']}">Behance</a></p>
</footer>
"""


def row(p, root):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else '<span class="row__ar"></span>'
    thumb = img(meta[p["slug"]]["cover"], root, "100vw", "", cls="row__thumb")
    return f"""<li>
  <a class="row" href="{root}work/{p['slug']}/index.html" data-peek="{cover_small(p['slug'], root)}">
    {thumb}
    <span class="row__title">{e(p['title'])}</span>
    <span class="row__info"><span class="row__kind">{e(p['kind'])}</span>{e(p['line'])}</span>
    {ar}
  </a>
</li>"""


def wall_html(root):
    items = json.load(open("wall.json"))
    # interleave projects so neighbours differ, then deal into 5 columns
    by = {}
    for it in items: by.setdefault(it[3], []).append(it)
    order = []
    while any(by.values()):
        for k in list(by):
            if by[k]: order.append(by[k].pop(0))
    cols = [order[i::5] for i in range(5)]
    out = []
    for c, col in enumerate(cols):
        imgs = "".join(f'<img src="{root}{p}" width="{w}" height="{h}" alt="" decoding="async">' for n, (p, w, h, _) in enumerate(col))
        out.append(f'<div class="wall__col"><div class="wall__run">{imgs}{imgs}</div></div>')
    return "".join(out)


def build_home():
    root = ""
    rows = "\n".join(row(p, root) for p in projects)
    portrait = img(meta["portrait"], root, "(max-width: 760px) 90vw, 34vw", "Portrait of Ahmed Rabea")
    page = head("Ahmed Rabea, brand designer and art director",
                "Brand designer and art director in Cairo. Brand identities, campaign systems, guidelines and presentation design for companies across the Gulf and Egypt.",
                root, meta[projects[0]["slug"]]["cover"]["files"]["1400"]) + f"""<body class="home">
{header(root)}
<main id="main">
<section class="hero" aria-labelledby="hero-name">
  <div class="wall" aria-hidden="true"><div class="wall__tilt">{wall_html(root)}</div></div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__top">
    <p>Brand designer and art director<br>Based in Cairo</p>
    <p class="hero__open"><span class="dot" aria-hidden="true"></span>Taking on select projects</p>
  </div>
  <h1 id="hero-name" class="hero__name"><span>Ahmed</span><span>Rabea</span></h1>
  <div class="hero__foot">
    <p class="hero__lede">I design brand identities, campaign systems and guidelines for companies across the Gulf and Egypt, built to hold up long after launch day.</p>
    <a class="hero__cue" href="#work">See the work</a>
  </div>
</section>

<section id="work" class="work" aria-labelledby="work-h">
  <div class="sec-head"><h2 id="work-h">Selected work</h2><p>{len(projects)} projects, client work first</p></div>
  <ul class="rows" role="list">
{rows}
  </ul>
</section>

<section id="about" class="about" aria-labelledby="about-h">
  <h2 id="about-h" class="visually-hidden">About</h2>
  <p class="about__statement">A brand is judged by its hundredth asset, not its first. I design the system behind it, so every post, deck and campaign after launch still looks like it came from the same place.</p>
  <div class="about__grid">
    <div class="about__img">{portrait}</div>
    <div class="about__body">
      <p>I'm a brand designer and art director in Cairo with more than five years across B2B SaaS, healthcare, language services and consumer brands. I've run creative for five brands at once, led a team of designers, and built the guidelines and workflows that keep a brand consistent at volume. Alongside that, I take on a small number of independent projects.</p>
      <h3>What I can help with</h3>
      <dl class="ways">
        <div><dt>Brand identity</dt><dd>Logo, typography, colour and the rules that hold them together, in English and Arabic.</dd></div>
        <div><dt>Campaign systems</dt><dd>One idea built to scale across formats and markets. At mazeed, a single campaign system reached 80 assets in two languages and five formats.</dd></div>
        <div><dt>Brand guidelines</dt><dd>Guidelines teams actually use, from foundations to templates, written so the next designer can pick them up without a briefing.</dd></div>
        <div><dt>Pitch and presentation design</dt><dd>Investor, leadership and company-profile decks that make dense information readable in seconds.</dd></div>
        <div><dt>Creative direction and consulting</dt><dd>Brand audits, visual direction, and the feedback, QA and asset workflows that let a team ship 250+ designs a month.</dd></div>
      </dl>
      <h3>Background</h3>
      <ol class="cv" role="list">
        <li><span>2026 to now</span><span>Senior Brand Designer, ELIXIR MD</span></li>
        <li><span>2025 to 2026</span><span>Senior Designer, mazeed</span></li>
        <li><span>2024 to 2025</span><span>Creative Lead, Bayantech</span></li>
        <li><span>2023 to 2024</span><span>Graphic Designer, ATOP Arab</span></li>
        <li><span>2021 to 2023</span><span>Graphic Designer, CORE</span></li>
      </ol>
    </div>
  </div>
</section>

<section id="contact" class="contact" aria-labelledby="contact-h">
  <h2 id="contact-h">Have a brand, campaign or deck in mind? Tell me about it.</h2>
  <a class="contact__mail" href="mailto:{SITE['email']}">{SITE['email']}</a>
  <ul class="contact__links" role="list">
    <li><a href="{SITE['linkedin']}">LinkedIn</a></li>
    <li><a href="{SITE['behance']}">Behance</a></li>
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
    dl = "\n".join(f"<div><dt>{e(k)}</dt><dd>{e(val)}</dd></div>" for k, val in p["meta"])
    nar = f'<span class="row__ar" lang="ar" dir="rtl">{e(nxt["arabic"])}</span>' if nxt["arabic"] else ""
    page = head(f"{p['title']}, by Ahmed Rabea", p["line"], root, m["cover"]["files"]["1400"]) + f"""<body class="case-page">
<div class="progress" aria-hidden="true"></div>
{header(root)}
<main id="main">
<article class="case">
  <header class="case__head">
    <p class="case__back"><a href="{root}index.html#work">All work</a></p>
    <h1 class="case__title"><span>{e(p['title'])}</span>{ar}</h1>
    <div class="case__intro">
      <div class="case__text">
        <p class="case__kind">{e(p['kind'])}</p>
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
  <p class="next__label">Next project</p>
  <a class="row row--next" href="{root}work/{nxt['slug']}/index.html" data-peek="{cover_small(nxt['slug'], root)}">
    <span class="row__title">{e(nxt['title'])}</span>
    <span class="row__info"><span class="row__kind">{e(nxt['kind'])}</span>{e(nxt['line'])}</span>
    {nar}
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
