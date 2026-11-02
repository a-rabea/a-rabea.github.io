"""Builds the static site (V2) from content/*.json + image_meta.json.

Run:  python3 build.py
Project text, chapters and highlights: content/projects.json
Services page text: content/services.json
"""
import json, html, os, hashlib

SITE = {
    "url": ("https://" + open("CNAME").read().strip()) if os.path.exists("CNAME") else "https://a-rabea.github.io",
    "email": "ahmed.r.bisher@gmail.com",
    "linkedin": "https://www.linkedin.com/in/a-rabea",
    "behance": "https://www.behance.net/a-rabea",
    "phone": "+20 101 057 9844",
    "tel": "+201010579844",
    "whatsapp": "https://wa.me/201010579844",
    "cv": "assets/Ahmed-Rabea-CV.pdf",
}
ROLE = "Senior Brand Designer & Art Director"
projects = json.load(open("content/projects.json", encoding="utf-8"))
services = json.load(open("content/services.json", encoding="utf-8"))
by_slug = {p["slug"]: p for p in projects}
meta = json.load(open("image_meta.json"))
FEATURED = ["mazeed", "aywa", "ideas-that-scale", "aureya"]
e = lambda s: html.escape(s, quote=True)
VER = hashlib.md5(open("assets/site.css", "rb").read() + open("assets/site.js", "rb").read()).hexdigest()[:8]
NOINDEX = os.environ.get("PREVIEW") == "1"
LITE = NOINDEX  # preview host has a file limit: one image size per frame

# ---------- icons (24px grid, drawn for this site) ----------
ICONS = {
    "identity": '<circle cx="9.5" cy="12" r="6"/><rect x="11" y="6" width="9" height="12" rx="1"/>',
    "campaign": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1" fill="currentColor"/>',
    "guidelines": '<path d="M12 6c-2-1.5-5-2-8-1.5v14c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5v-14c-3-.5-6 0-8 1.5z"/><path d="M12 6v14"/>',
    "deck": '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4M7 12V10M11 12V8M15 12V9"/>',
    "direction": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "social": '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10 18.5h4"/><path d="M9 8.5h6v5H9z"/>',
    "packaging": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "app": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="3.75"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="3.75"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    "icons": '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
    "mascot": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14.5c1.8 2 5.2 2 7 0"/><path d="M9 9.5h.01M15 9.5h.01" stroke-width="2.4"/>',
    "lettering": '<path d="M4 20c4-1 6-4 7-8s3-8 9-8"/><path d="M14 20h6"/><circle cx="6" cy="7" r="1.6"/>',
    "arrow": '<path d="M7 17L17 7M9 7h8v8"/>',
    "audit": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21M8 10.5l2 2 3.5-4"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "chat": '<path d="M4 20l1.5-4A8 8 0 1 1 9 19.3z"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "in": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
}
TAGS = {
    "identity": ("Brand identity", "identity"), "campaign": ("Campaigns", "campaign"), "social": ("Social media", "social"),
    "packaging": ("Packaging", "packaging"), "deck": ("Decks and profiles", "deck"), "app": ("App and digital", "app"),
    "lettering": ("Custom lettering", "lettering"), "icons": ("Icon systems", "icons"), "mascot": ("Mascot", "mascot"),
}


def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def tag_chips(p):
    return "".join(f'<span class="tag">{icon(TAGS[t][1])}{e(TAGS[t][0])}</span>' for t in p["tags"])


def img(m, root, sizes, alt, cls="", eager=False, max_w=None):
    f = dict(m["files"])
    if m.get("thumb") and not LITE:
        f["480"] = m["thumb"]
    if LITE:
        f = {k: v for k, v in f.items() if k in ("1000", "800", "1400", "600")}
    k = sorted((w for w in f if not max_w or int(w) <= max_w), key=int)
    srcset = ", ".join(f"{root}{f[w]} {min(int(w), m['w'])}w" for w in k)
    w = min(int(k[-1]), m["w"]); h = round(m["h"] * w / m["w"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{root}{f[k[-1]]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load}>')


def logo(slug, root, cls="logo", eager=False):
    load = "" if eager else ' loading="lazy"'
    return f'<img class="{cls}" src="{root}assets/img/logos/{slug}.webp" width="120" height="120" alt=""{load}>'


def cover_small(slug, root):
    return f"{root}{meta[slug]['cover']['files']['800']}"


def frame_of(slug, n):
    return meta[slug]["frames"][n - 1]


# ---------- shared chrome ----------
def head(title, desc, root, og, path="", ld=None, body_cls="", style=""):
    url = f"{SITE['url']}/{path}"
    og_url = f"{SITE['url']}/assets/og/{og}.jpg"
    lds = "".join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    robots = '\n<meta name="robots" content="noindex">' if NOINDEX else ""
    st = f' style="{style}"' if style else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0D100F">
<meta name="p:domain_verify" content="021ae1545cf424912b139af6310727fe"/>{robots}
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Ahmed Rabea">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_url}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/archivo-wdth.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/site.css?v={VER}">
<script src="{root}assets/site.js?v={VER}" defer></script>{lds}
</head>
<body class="{body_cls}"{st}>
"""


def header(root, here=""):
    cur = lambda k: ' aria-current="page"' if here == k else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <a class="bar__name" href="{root}index.html"><span class="bar__mono" aria-hidden="true">AR</span><span>Ahmed Rabea</span></a>
  <nav class="bar__nav" aria-label="Main">
    <a href="{root}index.html#work"{cur('work')}>Work</a>
    <a href="{root}services/index.html"{cur('services')}>Services</a>
    <a href="{root}index.html#about">About</a>
    <a class="bar__hire" href="{root}index.html#hire">Hiring?</a>
    <a class="bar__cta" href="{root}index.html#contact">Start a project</a>
  </nav>
</header>
<div class="peek" aria-hidden="true"><img alt=""></div>
<div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
"""


def footer(root):
    return f"""<footer class="foot">
  <a class="float" href="{root}index.html#contact" aria-label="Start a project with Ahmed">
    <img src="{root}assets/img/about/avatar.webp" width="36" height="36" alt=""><span>Start a project</span>
  </a>
  <div class="foot__big">
    <p class="foot__role">{ROLE}</p>
    <a class="foot__mail" href="mailto:{SITE['email']}">{SITE['email']}</a>
  </div>
  <ul class="foot__links" role="list">
    <li><a href="{SITE['whatsapp']}">{icon('chat')}WhatsApp</a></li>
    <li><a href="tel:{SITE['tel']}">{icon('phone')}{SITE['phone']}</a></li>
    <li><a href="{SITE['linkedin']}">{icon('in')}LinkedIn</a></li>
    <li><a href="{SITE['behance']}">{icon('arrow')}Behance</a></li>
    <li><a href="{root}{SITE['cv']}" download>{icon('download')}CV (PDF)</a></li>
  </ul>
  <p class="foot__small">Ahmed Rabea, Cairo. <a href="{root}services/index.html">Services</a></p>
</footer>
"""


def contact_block(root, heading="Have a brand, campaign or deck in mind?"):
    """Two clear paths: freelance enquiry (form that writes an email) and hiring (CV, LinkedIn)."""
    boxes = "".join(f'<label class="chip"><input type="checkbox" name="need" value="{e(s["name"])}"><span>{e(s["name"])}</span></label>' for s in services["services"])
    return f"""<section id="contact" class="contact" aria-labelledby="contact-h">
  <div class="contact__lead reveal">
    <p class="kicker">Freelance and projects</p>
    <h2 id="contact-h">{e(heading)}</h2>
    <p>Tell me a little about it. The button writes the email for you, ready to send from your own email app.</p>
    <ul class="direct" role="list">
      <li><a href="mailto:{SITE['email']}">{icon('mail')}<span>{SITE['email']}</span></a><button type="button" class="copy" data-copy="{SITE['email']}">Copy</button></li>
      <li><a href="{SITE['whatsapp']}">{icon('chat')}<span>WhatsApp</span></a></li>
      <li><a href="tel:{SITE['tel']}">{icon('phone')}<span>{SITE['phone']}</span></a></li>
    </ul>
  </div>
  <form class="start__form" data-email="{SITE['email']}">
    <fieldset>
      <legend>What do you need?</legend>
      <div class="chips">{boxes}<label class="chip"><input type="checkbox" name="need" value="A quick start (audit, template kit or deck refresh)"><span>A quick start</span></label><label class="chip"><input type="checkbox" name="need" value="Not sure yet"><span>Not sure yet</span></label></div>
    </fieldset>
    <div class="start__row">
      <label>Your name<input name="name" autocomplete="name" required></label>
      <label>Company<input name="company" autocomplete="organization"></label>
    </div>
    <div class="start__row">
      <label>Timeline
        <select name="timeline"><option value="">Choose one</option><option>As soon as possible</option><option>Within a month</option><option>In 1 to 3 months</option><option>Just exploring</option></select>
      </label>
      <label>Budget range<input name="budget" placeholder="Optional"></label>
    </div>
    <label>About the project<textarea name="message" rows="4" placeholder="What are you making, and who is it for?"></textarea></label>
    <div class="start__send">
      <button class="btn btn--big" type="submit">Write my email</button>
      <p class="start__note" aria-live="polite">Opens your email app. Nothing is sent until you press send there.</p>
    </div>
  </form>
</section>"""


def hire_block(root):
    return f"""<section id="hire" class="hire" aria-labelledby="hire-h">
  <div class="hire__card reveal">
    <div>
      <p class="kicker">For recruiters and hiring managers</p>
      <h2 id="hire-h">Hiring for a senior brand or art direction role?</h2>
      <p>The short version: more than five years in brand and campaign design, including visual direction for a B2B SaaS brand in the UAE and KSA, and a year as Creative Lead running a team of five designers across five brands.</p>
    </div>
    <ul class="hire__links" role="list">
      <li><a class="btn" href="{root}{SITE['cv']}" download>{icon('download')}Download CV (PDF)</a></li>
      <li><a class="btn btn--ghost" href="{SITE['linkedin']}">{icon('in')}LinkedIn</a></li>
      <li><a class="btn btn--ghost" href="mailto:{SITE['email']}?subject=Role%20enquiry">{icon('mail')}Email about a role</a></li>
    </ul>
  </div>
</section>"""


# ---------- home ----------
def row(p, root):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else '<span class="row__ar"></span>'
    return f"""<li class="item" style="--c:{p['color']}" data-tags="{' '.join(p['tags'])}">
  <a class="row" href="{root}work/{p['slug']}/index.html" data-peek="{cover_small(p['slug'], root)}" data-cursor="View">
    {img(meta[p["slug"]]["cover"], root, "100vw", "", cls="row__thumb", max_w=800)}
    <span class="row__title">{logo(p['slug'], root)}<span>{e(p['title'])}</span></span>
    <span class="row__info"><span class="row__kind">{e(p['kind'])}</span>{e(p['line'])}<span class="tags">{tag_chips(p)}</span></span>
    {ar}
    <span class="row__go" aria-hidden="true">{icon('arrow')}</span>
  </a>
</li>"""


def filter_bar():
    counts = {t: sum(t in p["tags"] for p in projects) for t in TAGS}
    order = sorted((t for t in TAGS if counts[t] >= 2), key=lambda t: -counts[t])
    chips = "".join(f'<button type="button" class="fchip" data-filter="{t}" aria-pressed="false">{icon(TAGS[t][1])}{e(TAGS[t][0])}<span class="fchip__n">{counts[t]}</span></button>' for t in order)
    return f'<div class="filters" role="group" aria-label="Filter projects"><button type="button" class="fchip" data-filter="all" aria-pressed="true">All<span class="fchip__n">{len(projects)}</span></button>{chips}</div>'


def feature_card(p, root, size, eager=False):
    sizes = "(max-width: 860px) 100vw, 60vw" if size == "lg" else "(max-width: 860px) 100vw, 40vw"
    return f"""<a class="feat feat--{size} reveal" style="--c:{p['color']}" href="{root}work/{p['slug']}/index.html" data-cursor="View">
  <div class="feat__img">{img(meta[p['slug']]['cover'], root, sizes, p['title'] + ' project cover', eager=eager)}</div>
  <div class="feat__text">
    <p class="feat__title">{logo(p['slug'], root)}<span>{e(p['title'])}</span></p>
    <p class="feat__kind">{e(p['kind'])}</p>
    <p class="feat__line">{e(p['line'])}</p>
  </div>
</a>"""


def wall_html(root):
    items = json.load(open("wall.json"))
    by = {}
    for it in items: by.setdefault(it[3], []).append(it)
    order = []
    while any(by.values()):
        for k in list(by):
            if by[k]: order.append(by[k].pop(0))
    cols = [order[i::3] for i in range(3)]
    out = []
    for col in cols:
        imgs = "".join(f'<img src="{root}{p}" width="{w}" height="{h}" alt="" decoding="async">' for p, w, h, _ in col)
        out.append(f'<div class="wall__col"><div class="wall__run">{imgs}{imgs}</div></div>')
    return "".join(out)


def person_ld():
    return {"@context": "https://schema.org", "@type": "Person", "name": "Ahmed Rabea", "jobTitle": ROLE,
            "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
            "url": SITE["url"] + "/", "email": "mailto:" + SITE["email"], "telephone": SITE["tel"],
            "knowsAbout": ["Brand identity", "Visual systems", "Art direction", "Campaign design", "Social media design",
                           "Brand guidelines", "Presentation design", "Arabic typography"],
            "sameAs": [SITE["linkedin"], SITE["behance"]]}


def build_home():
    root = ""
    f = [by_slug[s] for s in FEATURED]
    feats = (feature_card(f[0], root, "lg", eager=True) + feature_card(f[1], root, "sm") +
             feature_card(f[2], root, "sm") + feature_card(f[3], root, "lg"))
    rows = "\n".join(row(p, root) for p in projects)
    svc = "\n".join(f'<li><a href="services/index.html#{s["id"]}">{icon(s["icon"])}<span class="svc__name">{e(s["name"])}</span><span class="svc__sum">{e(s["summary"])}</span></a></li>' for s in services["services"])
    portrait = img(meta["portrait"], root, "(max-width: 860px) 80vw, 30vw", "Portrait of Ahmed Rabea")
    page = head(f"Ahmed Rabea | {ROLE}, Cairo",
                "Ahmed Rabea is a Senior Brand Designer and Art Director in Cairo: brand identity, visual systems, campaigns, social media and digital design for companies in the UAE, Saudi Arabia and Egypt, in English and Arabic.",
                root, "home", "", [person_ld()], "home") + header(root) + f"""<main id="main">
<section class="hero" aria-labelledby="hero-h">
  <div class="hero__copy">
    <p class="hero__name">Ahmed Rabea<span class="dot" aria-hidden="true"></span><span class="hero__open">Taking on select projects</span></p>
    <h1 id="hero-h">
      <span class="hero__role">{ROLE}</span>
      <span class="hero__head"><span class="w-wide">Built for the</span> <span class="w-tall">hundredth asset.</span></span>
    </h1>
    <p class="hero__lede">I design brand identities and the visual systems behind them, then art-direct the campaigns, social and digital work that keep them consistent long after launch. For companies in the UAE, Saudi Arabia and Egypt, in English and Arabic.</p>
    <ul class="creds" role="list">
      <li><strong>5 brands at once</strong><span>as Creative Lead at Bayantech</span></li>
      <li><strong>250+ designs a month</strong><span>overseen under one set of standards</span></li>
      <li><strong>1,000+ clients</strong><span>served by mazeed, where I led the visual direction</span></li>
    </ul>
    <div class="hero__ctas">
      <a class="btn btn--big" href="#contact">Start a project</a>
      <a class="btn btn--ghost btn--big" href="#work">See the work</a>
      <a class="hero__hire" href="#hire">Hiring? Get my CV</a>
    </div>
  </div>
  <div class="wall" aria-hidden="true"><div class="wall__tilt">{wall_html(root)}</div></div>
</section>

<section id="work" class="work" aria-labelledby="work-h">
  <header class="sec reveal">
    <h2 id="work-h" class="sec__title">Selected work</h2>
    <p class="sec__note">Four projects that show the range: a SaaS brand system, a fintech identity, social systems for nine brands, and a bilingual luxury brand world.</p>
  </header>
  <div class="feats">{feats}</div>

  <header class="sec sec--sub reveal">
    <h3 class="sec__title sec__title--sm">All projects</h3>
    <p class="sec__note filters__status" aria-live="polite">{len(projects)} projects</p>
  </header>
  {filter_bar()}
  <ul class="rows" role="list">
{rows}
  </ul>
</section>

<section class="svc" aria-labelledby="svc-h">
  <header class="sec reveal">
    <h2 id="svc-h" class="sec__title">What I do</h2>
    <p class="sec__note">Five services, and three smaller ways to start. <a href="services/index.html">See services and how I work</a></p>
  </header>
  <ul class="svc__list" role="list">
{svc}
  </ul>
</section>

<section id="about" class="about" aria-labelledby="about-h">
  <div class="about__img reveal">{portrait}</div>
  <div class="about__body">
    <h2 id="about-h" class="about__statement reveal">I care most about the hundredth asset: the post, deck or campaign that ships a year after launch and still looks like it came from the same place.</h2>
    <p>I'm a senior brand designer and art director in Cairo with more than five years in B2B SaaS, language services, healthcare and construction. I've led visual direction for an accounting platform in the UAE and KSA, run creative for five brands at once with a team of five designers, and built the guidelines, QA and asset systems that keep a brand consistent at volume.</p>
    <h3>Background</h3>
    <ol class="cv" role="list">
      <li><span>2026 to now</span><span>Senior Brand Designer, ELIXIR MD</span></li>
      <li><span>2025 to 2026</span><span>Senior Designer, mazeed</span></li>
      <li><span>2024 to 2025</span><span>Creative Lead, Bayantech</span></li>
      <li><span>2023 to 2024</span><span>Graphic Designer, ATOP Arab</span></li>
      <li><span>2021 to 2023</span><span>Graphic Designer, CORE</span></li>
    </ol>
  </div>
</section>

{contact_block(root)}
{hire_block(root)}
</main>
{footer(root)}
</body>
</html>
"""
    open("index.html", "w", encoding="utf-8").write(page)


# ---------- services ----------
SERVICE_IMG = {"brand-identity": ("aywa", 7), "social-media": ("ideas-that-scale", 3), "brand-guidelines": ("aureya", 9),
               "presentation-design": ("sheikh-khalifa-hospital", 13), "creative-direction": ("mazeed", 4)}


def build_services():
    root = "../"
    S = services
    blocks = []
    for i, s in enumerate(S["services"]):
        sl, n = SERVICE_IMG[s["id"]]
        pic = img(frame_of(sl, n), root, "(max-width: 860px) 100vw, 55vw", f"{s['name']}: from the {by_slug[sl]['title']} project")
        proof = "".join(f'<a class="proof" style="--c:{by_slug[x]["color"]}" href="{root}work/{x}/index.html" data-cursor="View">{logo(x, root)}<span>{e(by_slug[x]["title"])}</span></a>' for x in s["proof"])
        inc = "".join(f"<li>{e(t)}</li>" for t in s["includes"])
        blocks.append(f"""<article class="band{' band--flip' if i % 2 else ''}" id="{s['id']}">
  <a class="band__img reveal" href="{root}work/{sl}/index.html" style="--c:{by_slug[sl]['color']}" data-cursor="View" aria-label="{e(by_slug[sl]['title'])} case study">{pic}</a>
  <div class="band__body">
    <p class="band__icon">{icon(s['icon'], 'icon icon--big')}</p>
    <h2 class="band__title">{e(s['name'])}</h2>
    <p class="band__sum">{e(s['summary'])}</p>
    <h3>What you get</h3>
    <ul class="ticks">{inc}</ul>
    <h3>Good for</h3>
    <p class="band__for">{e(s['for'])}</p>
    <h3>See it in practice</h3>
    <div class="proofs">{proof}</div>
  </div>
</article>""")
    quick = "".join(f'<li id="{q["id"]}">{icon(q["icon"])}<h3>{e(q["name"])}</h3><p>{e(q["summary"])}</p><p class="quick__get">{e(q["get"])}</p><a class="quick__cta" href="#contact">Ask about this</a></li>' for q in S["quick"])
    steps = "".join(f"<li><span class='step__n'>{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>" for n, (t, d) in enumerate(S["process"], 1))
    ways = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in S["ways"])
    faq = "".join(f"<details><summary>{e(q)}{icon('plus')}</summary><p>{e(a)}</p></details>" for q, a in S["faq"])
    jump = "".join(f'<li><a href="#{s["id"]}">{icon(s["icon"])}<span>{e(s["name"])}</span></a></li>' for s in S["services"])
    ld = [
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Ahmed Rabea, brand design and art direction",
         "url": SITE["url"] + "/services/", "image": SITE["url"] + "/assets/og/home.jpg", "email": SITE["email"], "telephone": SITE["tel"],
         "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
         "areaServed": ["United Arab Emirates", "Saudi Arabia", "Egypt"], "availableLanguage": ["English", "Arabic"],
         "founder": {"@type": "Person", "name": "Ahmed Rabea", "jobTitle": ROLE},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Brand design services", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["summary"]}} for s in S["services"] + S["quick"]]}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in S["faq"]]},
    ]
    page = head("Brand identity, social media and art direction services | Ahmed Rabea",
                "Brand identity design, social media and campaigns, brand guidelines, pitch deck design and creative direction by Ahmed Rabea, Senior Brand Designer and Art Director in Cairo. For companies in the UAE, Saudi Arabia and Egypt.",
                root, "home", "services/", ld, "services-page") + header(root, "services") + f"""<main id="main">
<section class="s-hero">
  <p class="kicker">Services</p>
  <h1 class="s-hero__title"><span class="w-wide">Identity, systems</span> <span class="w-tall">and the direction that holds them together.</span></h1>
  <div class="s-hero__foot">
    <p class="s-hero__lede">I work with companies and teams in the UAE, Saudi Arabia and Egypt on brand identity, social media and campaigns, guidelines, decks and creative direction, in English and Arabic. Every service below links to real work.</p>
    <div class="hero__ctas"><a class="btn btn--big" href="#contact">Start a project</a><a class="btn btn--ghost btn--big" href="#quick">Start small</a></div>
  </div>
  <ul class="jump" role="list">{jump}</ul>
</section>

<section class="who" aria-labelledby="who-h">
  <h2 id="who-h" class="visually-hidden">Who I work with</h2>
  <div class="who__card reveal"><h3>Companies and founders</h3><p>You need a brand that looks credible on day one and still holds together a year later, without hiring a full team.</p></div>
  <div class="who__card reveal"><h3>In-house teams and agencies</h3><p>You have designers, but need senior direction, a system to work from, or extra hands that already know how to keep a brand consistent.</p></div>
</section>

<div class="bands">
{chr(10).join(blocks)}
</div>

<section id="quick" class="quick" aria-labelledby="quick-h">
  <header class="sec reveal"><h2 id="quick-h" class="sec__title">Quick starts</h2><p class="sec__note">Smaller, fixed-scope ways to work together.</p></header>
  <ul class="quick__list" role="list">{quick}</ul>
</section>

<section class="process" aria-labelledby="process-h">
  <header class="sec reveal"><h2 id="process-h" class="sec__title">How a project runs</h2></header>
  <ol class="steps" role="list">{steps}</ol>
</section>

<section class="ways-sec" aria-labelledby="ways-h">
  <header class="sec reveal"><h2 id="ways-h" class="sec__title">Ways to work together</h2></header>
  <ul class="ways3" role="list">{ways}</ul>
</section>

<section class="faq" aria-labelledby="faq-h">
  <header class="sec reveal"><h2 id="faq-h" class="sec__title">Questions</h2></header>
  <div class="faq__list">{faq}</div>
</section>

{contact_block(root, "Tell me what you're working on.")}
{hire_block(root)}
</main>
{footer(root)}
</body>
</html>
"""
    os.makedirs("services", exist_ok=True)
    open("services/index.html", "w", encoding="utf-8").write(page)


# ---------- case studies ----------
def frame_btn(p, n, f, root, sizes, cls="frame"):
    light = " frame--light" if f.get("light") else ""
    wide = " frame--wide" if f["w"] / f["h"] >= 1.6 else " frame--tall"
    return (f'<figure class="{cls}{light}{wide}"><button class="frame__zoom" type="button" data-full="{root}{f["files"]["1000" if LITE else "1800"]}" '
            f'data-cursor="Zoom" aria-label="Enlarge frame {n} of {e(p["title"])}">'
            f'{img(f, root, sizes, p["title"] + ", frame " + str(n))}</button></figure>')


def nav_row(q, root, label):
    return f"""<a class="pn__item" style="--c:{q['color']}" href="{root}work/{q['slug']}/index.html" data-peek="{cover_small(q['slug'], root)}" data-cursor="View">
    <span class="pn__label">{label}</span>
    <span class="pn__title">{logo(q['slug'], root)}<span>{e(q['title'])}</span></span>
    <span class="pn__kind">{e(q['kind'])}</span>
  </a>"""


def build_case(i, p):
    root = "../../"
    m = meta[p["slug"]]
    nxt, prv = projects[(i + 1) % len(projects)], projects[i - 1]
    skip = set(p.get("skip_frames", []))
    v = p.get("video")
    S = p["summary"]

    # visual overview: one large frame and four supporting ones
    wide_set = sum(f["w"] / f["h"] >= 1.6 for f in m["frames"]) > len(m["frames"]) / 2
    hl = [h for h in p["highlights"] if h not in skip]
    bento = "".join(frame_btn(p, n, frame_of(p["slug"], n), root,
                              "(max-width: 860px) 100vw, 60vw" if k == 0 else "(max-width: 860px) 50vw, 25vw",
                              "frame bento__" + ("big" if k == 0 else "sm")) for k, n in enumerate(hl))

    chapters, nav = [], []
    for c, (title, nums) in enumerate(p["chapters"], 1):
        nums = [n for n in nums if n not in skip]
        if not nums: continue
        cid = f"ch-{c}"
        thumbs = "".join(f'<img src="{root}{frame_of(p["slug"], n)["files"]["1000"] if LITE else frame_of(p["slug"], n)["thumb"]}" width="160" height="{round(160 * frame_of(p["slug"], n)["h"] / frame_of(p["slug"], n)["w"])}" alt="" loading="lazy">' for n in nums[:4])
        body = []
        for n in nums:
            f = frame_of(p["slug"], n)
            body.append(frame_btn(p, n, f, root, "(max-width: 860px) 100vw, 45vw" if f["w"] / f["h"] >= 1.6 else "(max-width: 860px) 100vw, 70vw"))
            if v and n == v["after"]:
                cls = "film film--vertical" if v["vertical"] else "film"
                body.append(f"""<figure class="{cls}"><video controls playsinline preload="none" poster="{root}assets/img/{p['slug']}/poster.webp" src="{root}{m['video']}"></video><figcaption>{e(v['caption'])}</figcaption></figure>""")
        count = f"{len(nums)} frame{'s' if len(nums) > 1 else ''}" + (" and a film" if v and v["after"] in nums else "")
        chapters.append(f"""<details class="chapter" id="{cid}">
  <summary><span class="chapter__n">{c:02d}</span><span class="chapter__t">{e(title)}</span><span class="chapter__count">{count}</span><span class="chapter__thumbs" aria-hidden="true">{thumbs}</span><span class="chapter__toggle" aria-hidden="true">{icon('plus')}</span></summary>
  <div class="chapter__body">{''.join(body)}</div>
</details>""")
        nav.append(f'<li><a href="#{cid}" data-open="{cid}"><span>{c:02d}</span>{e(title)}</a></li>')

    ar = f'<span class="case__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else ""
    nums = ""
    if p.get("numbers"):
        nums = '<ul class="nums reveal" role="list" aria-label="In numbers">' + "".join(
            f'<li><span class="nums__n">{e(n)}</span><span class="nums__l">{e(l)}</span></li>' for n, l in p["numbers"]) + "</ul>"
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(val)}</dd></div>" for k, val in p["meta"] if k not in ("Role",))
    story = "".join(f"<p>{e(x)}</p>" for x in p["intro"])
    cover = img(m["cover"], root, "(max-width: 1680px) 100vw, 1680px", p["title"] + " cover", cls="case__cover", eager=True)
    ld = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"], "about": p["kind"],
           "description": p["line"], "creator": {"@type": "Person", "name": "Ahmed Rabea", "jobTitle": ROLE},
           "image": f"{SITE['url']}/assets/og/{p['slug']}.jpg", "url": f"{SITE['url']}/work/{p['slug']}/"}]
    page = head(f"{p['title']}: {p['kind'].lower()} | Ahmed Rabea", p["line"], root, p["slug"], f"work/{p['slug']}/", ld,
                "case-page", f"--c:{p['color']}") + '<div class="progress" aria-hidden="true"></div>\n' + header(root, "work") + f"""<main id="main">
<article class="case">
  <header class="case__head">
    <p class="case__back"><a href="{root}index.html#work">All work</a></p>
    <h1 class="case__title"><span class="case__name">{logo(p['slug'], root, 'logo logo--case', eager=True)}<span>{e(p['title'])}</span></span>{ar}</h1>
    <div class="case__sub"><p class="case__kind">{e(p['kind'])}</p><p class="tags">{tag_chips(p)}</p></div>
  </header>
  <div class="case__coverwrap">{cover}</div>

  <section class="overview" aria-label="Project overview">
    <div class="overview__lead reveal">
      <p class="kicker">Overview</p>
      <p class="overview__line">{e(p['line'])}</p>
      <dl class="overview__facts">{facts}</dl>
    </div>
    <dl class="overview__grid reveal">
      <div><dt>The challenge</dt><dd>{e(S['challenge'])}</dd></div>
      <div><dt>My role</dt><dd>{e(S['role'])}</dd></div>
      <div><dt>Creative direction</dt><dd>{e(S['direction'])}</dd></div>
      <div><dt>Deliverables</dt><dd>{e(S['deliverables'])}</dd></div>
    </dl>
    <details class="story"><summary>Read the full write-up{icon('plus')}</summary><div>{story}</div></details>
  </section>
  {nums}

  <section class="glance" aria-labelledby="glance-h">
    <header class="sec reveal"><h2 id="glance-h" class="sec__title sec__title--sm">At a glance</h2><p class="sec__note">The strongest frames. Tap any image to see it full size.</p></header>
    <div class="bento bento--{'wide' if wide_set else 'tall'}">{bento}</div>
  </section>

  <section class="chapters" aria-labelledby="chapters-h">
    <nav class="chapters__nav" aria-labelledby="chapters-h">
      <h2 id="chapters-h" class="chapters__h">The full project</h2>
      <ol role="list">{''.join(nav)}</ol>
      <button type="button" class="btn btn--ghost" data-all>Open all chapters</button>
    </nav>
    <div class="chapters__list">{''.join(chapters)}</div>
  </section>
</article>

<section class="cta-band reveal" aria-label="Start a project">
  <p>Need something like {e(p['title'])} for your brand?</p>
  <div class="hero__ctas"><a class="btn btn--big" href="{root}index.html#contact">Start a project</a><a class="btn btn--ghost btn--big" href="{root}services/index.html">See services</a></div>
</section>
<nav class="pn" aria-label="More projects">
  {nav_row(prv, root, "Previous project")}
  {nav_row(nxt, root, "Next project")}
</nav>
</main>
{footer(root)}
<dialog class="viewer" aria-label="Enlarged frame">
  <div class="viewer__scroll"><img class="viewer__img" alt=""></div>
  <div class="viewer__bar">
    <button type="button" data-v="prev">Previous</button>
    <span class="viewer__count" aria-live="polite"></span>
    <button type="button" data-v="next">Next</button>
    <button type="button" data-v="close">Close</button>
  </div>
</dialog>
</body>
</html>
"""
    os.makedirs(f"work/{p['slug']}", exist_ok=True)
    open(f"work/{p['slug']}/index.html", "w", encoding="utf-8").write(page)


def build_404():
    root = "/"
    picks = "".join(f'<a class="proof" style="--c:{by_slug[s]["color"]}" href="/work/{s}/index.html">{logo(s, root)}<span>{e(by_slug[s]["title"])}</span></a>' for s in FEATURED)
    page = head("Page not found | Ahmed Rabea", "This page doesn't exist.", root, "home", "404.html", None, "nf") + header(root) + f"""<main id="main" class="nf__main">
  <p class="kicker">Error 404</p>
  <h1 class="nf__title"><span class="w-wide">This page</span> <span class="w-tall">moved or never existed.</span></h1>
  <p class="nf__lede">The work is still here. Try one of these, or go back to the <a href="/index.html">home page</a>.</p>
  <div class="proofs">{picks}</div>
  <div class="hero__ctas"><a class="btn btn--big" href="/index.html#work">See all work</a><a class="btn btn--ghost btn--big" href="/index.html#contact">Start a project</a></div>
</main>
{footer(root)}
</body>
</html>
"""
    open("404.html", "w", encoding="utf-8").write(page)


def build_meta_files():
    urls = ["", "services/"] + [f"work/{p['slug']}/" for p in projects]
    sm = "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc></url>" for u in urls)
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


build_home()
build_services()
for i, p in enumerate(projects):
    build_case(i, p)
build_404()
build_meta_files()
print("built", 3 + len(projects), "pages")
