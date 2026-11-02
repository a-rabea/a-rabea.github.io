"""Builds the static site from content/*.json + image_meta.json.

Run:  python3 build.py
To add a project: add its images in assets_manifest.py, run process_images.py and
make_extras.py, add an entry to content/projects.json, then run build.py.
Services page text lives in content/services.json.
"""
import json, html, os

SITE = {
    "name": "Ahmed Rabea",
    "url": ("https://" + open("CNAME").read().strip()) if os.path.exists("CNAME") else "https://a-rabea.github.io",
    "email": "ahmed.r.bisher@gmail.com",
    "linkedin": "https://www.linkedin.com/in/a-rabea",
    "behance": "https://www.behance.net/a-rabea",
    "phone": "+20 101 057 9844",
    "tel": "+201010579844",
    "whatsapp": "https://wa.me/201010579844",
}
# Free, cookie-free analytics. GoatCounter: account code "alpattex" (alpattex.goatcounter.com).
# Cloudflare Web Analytics: paste the site token from dash.cloudflare.com > Analytics > Web Analytics.
GOATCOUNTER_CODE = "alpattex"
CLOUDFLARE_TOKEN = "db5cdda8de86485ea56156e62e3d35a8"
ANALYTICS = ""
if GOATCOUNTER_CODE:
    ANALYTICS += f'\n<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
if CLOUDFLARE_TOKEN:
    ANALYTICS += f"""\n<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CLOUDFLARE_TOKEN}"}}'></script>"""
projects = json.load(open("content/projects.json", encoding="utf-8"))
services = json.load(open("content/services.json", encoding="utf-8"))
by_slug = {p["slug"]: p for p in projects}
meta = json.load(open("image_meta.json"))
e = lambda s: html.escape(s, quote=True)
import hashlib
# Changes whenever the CSS or JS changes, so browsers never mix new pages with old styles
VER = hashlib.md5(open("assets/site.css", "rb").read() + open("assets/site.js", "rb").read()).hexdigest()[:8]
FOLD = 12  # slide-format case studies show this many frames before "Show all"

# Line icons, drawn for this site (24px grid, 1.5 stroke)
ICONS = {
    "identity": '<circle cx="9.5" cy="12" r="6"/><rect x="11" y="6" width="9" height="12" rx="1"/>',
    "campaign": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1" fill="currentColor"/>',
    "guidelines": '<path d="M12 6c-2-1.5-5-2-8-1.5v14c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5v-14c-3-.5-6 0-8 1.5z"/><path d="M12 6v14"/>',
    "deck": '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4M7 12V10M11 12V8M15 12V9"/>',
    "direction": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
}
ICONS.update({
    "social": '<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10 18.5h4"/><path d="M9 8.5h6v5H9z"/>',
    "packaging": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "app": '<rect x="3" y="3" width="7.5" height="7.5" rx="2"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="3.75"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="3.75"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2"/>',
    "icons": '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
    "mascot": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14.5c1.8 2 5.2 2 7 0"/><path d="M9 9.5h.01M15 9.5h.01" stroke-width="2.4"/>',
    "lettering": '<path d="M4 20c4-1 6-4 7-8s3-8 9-8"/><path d="M14 20h6"/><circle cx="6" cy="7" r="1.6"/>',
    "arrow": '<path d="M7 17L17 7M9 7h8v8"/>',
    "audit": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21M8 10.5l2 2 3.5-4"/>',
})
TAGS = {  # id: (label, icon)
    "identity": ("Brand identity", "identity"), "campaign": ("Campaigns", "campaign"), "social": ("Social media", "social"),
    "packaging": ("Packaging", "packaging"), "deck": ("Decks and profiles", "deck"), "app": ("App and digital", "app"),
    "lettering": ("Custom lettering", "lettering"), "icons": ("Icon systems", "icons"), "mascot": ("Mascot", "mascot"),
}


def tag_chips(p, cls="tag"):
    return "".join(f'<span class="{cls}">{icon(TAGS[t][1])}{e(TAGS[t][0])}</span>' for t in p["tags"])


def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


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


def head(title, desc, root, og, path="", ld=None):
    url = f"{SITE['url']}/{path}"
    og_url = f"{SITE['url']}/assets/og/{og}.jpg"
    lds = "".join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0D100F">
<meta name="p:domain_verify" content="021ae1545cf424912b139af6310727fe"/>
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
<script src="{root}assets/site.js?v={VER}" defer></script>{lds}{ANALYTICS}
</head>
"""



def header(root, here=""):
    cur = lambda k: ' aria-current="page"' if here == k else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <a class="bar__name" href="{root}index.html">Ahmed Rabea</a>
  <nav class="bar__nav" aria-label="Main">
    <a href="{root}index.html#work"{cur('work')}>Work</a>
    <a href="{root}services/index.html"{cur('services')}>Services</a>
    <a href="{root}index.html#about">About</a>
    <a class="bar__cta" href="{root}services/index.html#start">Start a project</a>
  </nav>
</header>
<div class="peek" aria-hidden="true"><img alt=""></div>
<div class="cursor" aria-hidden="true"><span class="cursor__label"></span></div>
"""


def footer(root):
    return f"""<a class="float" href="{root}services/index.html#start" aria-label="Start a project with Ahmed">
  <span class="float__mark">AR</span><span>Start a project</span><span class="float__arrow" aria-hidden="true">&rarr;</span>
</a>
<footer class="foot">
  <p>Ahmed Rabea, brand designer and art director, Cairo</p>
  <p><a href="{root}services/index.html">Services</a><a href="mailto:{SITE['email']}">Email</a><a href="{SITE['whatsapp']}">WhatsApp</a><a href="tel:{SITE['tel']}">{SITE['phone']}</a><a href="{SITE['linkedin']}">LinkedIn</a><a href="{SITE['behance']}">Behance</a></p>
</footer>
"""


def enquiry(root, heading="Start a project", lead=None):
    """A short form that writes the enquiry email for the client. No server needed."""
    lead = lead or "Tell me a little about what you need. Pressing the button opens your email app with everything filled in, ready to send."
    boxes = "".join(f'<label class="chip"><input type="checkbox" name="need" value="{e(s["name"])}"><span>{e(s["name"])}</span></label>' for s in services["services"])
    return f"""<section id="start" class="start" aria-labelledby="start-h">
  <div class="start__intro">
    <h2 id="start-h">{e(heading)}</h2>
    <p>{e(lead)}</p>
    <ul class="start__alt" role="list">
      <li>Email <a href="mailto:{SITE['email']}">{SITE['email']}</a> <button type="button" class="copy" data-copy="{SITE['email']}">Copy</button></li>
      <li>WhatsApp <a href="{SITE['whatsapp']}">Message me on WhatsApp</a></li>
      <li>Phone <a href="tel:{SITE['tel']}">{SITE['phone']}</a></li>
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


def row(p, root):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else '<span class="row__ar"></span>'
    thumb = img(meta[p["slug"]]["cover"], root, "(max-width: 860px) 100vw, 45vw", "", cls="row__thumb")
    return f"""<li class="item" style="--c:{p['color']}" data-tags="{' '.join(p['tags'])}">
  <a class="row" href="{root}work/{p['slug']}/index.html" aria-label="{e(p['title'])}: {e(p['kind'])}. View case study">
    {thumb}
    <span class="row__title"><img class="logo" src="{root}assets/img/logos/{p['slug']}.webp" width="120" height="120" alt="" loading="lazy">{e(p['title'])}</span>
    <span class="row__info"><span class="row__kind">{e(p['kind'])}</span>{e(p['line'])}<span class="tags">{tag_chips(p)}</span></span>
    {ar}
    <span class="row__go" aria-hidden="true">{icon('arrow')}</span>
  </a>
</li>"""


def filter_bar():
    counts = {t: sum(t in p["tags"] for p in projects) for t in TAGS}
    order = sorted((t for t in TAGS if counts[t] >= 2), key=lambda t: -counts[t])
    chips = "".join(f'<button type="button" class="fchip" data-filter="{t}" aria-pressed="false">{icon(TAGS[t][1])}{e(TAGS[t][0])}<span class="fchip__n">{counts[t]}</span></button>' for t in order)
    return f'<div class="filters" role="group" aria-label="Filter projects"><button type="button" class="fchip" data-filter="all" aria-pressed="true">All work<span class="fchip__n">{len(projects)}</span></button>{chips}</div>'


def wall_html(root):
    items = json.load(open("wall.json"))
    by = {}
    for it in items: by.setdefault(it[3], []).append(it)
    order = []
    while any(by.values()):
        for k in list(by):
            if by[k]: order.append(by[k].pop(0))
    cols = [order[i::5] for i in range(5)]
    out = []
    for col in cols:
        imgs = "".join(f'<img src="{root}{p}" width="{w}" height="{h}" alt="" decoding="async">' for p, w, h, _ in col)
        out.append(f'<div class="wall__col"><div class="wall__run">{imgs}{imgs}</div></div>')
    return "".join(out)


def person_ld():
    return {"@context": "https://schema.org", "@type": "Person", "name": "Ahmed Rabea",
            "jobTitle": "Brand designer and art director",
            "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
            "url": SITE["url"] + "/", "email": "mailto:" + SITE["email"], "telephone": SITE["tel"],
            "knowsAbout": [s["name"] for s in services["services"]] + ["Arabic typography", "Bilingual design"],
            "sameAs": [SITE["linkedin"], SITE["behance"]]}


def build_home():
    root = ""
    rows = "\n".join(row(p, root) for p in projects)
    portrait = img(meta["portrait"], root, "(max-width: 760px) 90vw, 34vw", "Portrait of Ahmed Rabea")
    svc = "\n".join(f'<li><a href="services/index.html#{s["id"]}">{icon(s["icon"])}<span class="svc__name">{e(s["name"])}</span><span class="svc__sum">{e(s["summary"])}</span></a></li>' for s in services["services"])
    page = head("Ahmed Rabea | Brand identity designer and art director, Cairo",
                "Brand designer and art director in Cairo. Brand identity, social media design, campaigns, brand guidelines and pitch deck design for companies in the UAE, Saudi Arabia and Egypt, in English and Arabic.",
                root, "home", "", [person_ld()]) + f"""<body class="home">
{header(root)}
<main id="main">
<section class="hero" aria-labelledby="hero-name">
  <div class="wall" aria-hidden="true"><div class="wall__tilt">{wall_html(root)}</div></div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__top">
    <p>Hi, I'm Ahmed.<br>Brand designer and art director in Cairo</p>
    <p class="hero__open"><span class="dot" aria-hidden="true"></span>Taking on select projects</p>
  </div>
  <h1 id="hero-name" class="hero__name"><span>Ahmed</span><span>Rabea</span></h1>
  <div class="hero__foot">
    <p class="hero__lede">I design brand identities, campaign systems and guidelines for companies across the Gulf and Egypt, built to hold up long after launch day.</p>
    <div class="hero__ctas">
      <a class="btn btn--big" href="services/index.html#start">Start a project</a>
      <a class="hero__cue" href="#work">See the work</a>
    </div>
  </div>
</section>

<section id="work" class="work" aria-labelledby="work-h">
  <div class="sec-head"><h2 id="work-h">Selected work</h2><p class="filters__status" aria-live="polite">{len(projects)} projects</p></div>
  {filter_bar()}
  <ul class="rows" role="list">
{rows}
  </ul>
</section>

<section class="svc" aria-labelledby="svc-h">
  <div class="sec-head"><h2 id="svc-h">Services</h2><p><a href="services/index.html">All services and how I work</a></p></div>
  <ul class="svc__list" role="list">
{svc}
  </ul>
  <p class="svc__quick">Want to start small? Try a <a href="services/index.html#quick">brand audit, a social media template kit or a deck refresh</a>.</p>
</section>

<section id="about" class="about" aria-labelledby="about-h">
  <h2 id="about-h" class="visually-hidden">About</h2>
  <p class="about__statement">A brand is judged by its hundredth asset, not its first. I design the system behind it, so every post, deck and campaign after launch still looks like it came from the same place.</p>
  <div class="about__grid">
    <div class="about__img">{portrait}</div>
    <div class="about__body">
      <p>I'm a brand designer and art director in Cairo with more than five years across B2B SaaS, healthcare, language services and consumer brands. I've run creative for five brands at once, led a team of designers, and built the guidelines and workflows that keep a brand consistent at volume. Alongside that, I take on a small number of independent projects.</p>
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

{enquiry(root, "Have a brand, campaign or deck in mind?")}
</main>
{footer(root)}
</body>
</html>
"""
    open("index.html", "w", encoding="utf-8").write(page)


def build_services():
    root = "../"
    S = services
    blocks = []
    for s in S["services"]:
        proof = "".join(f"""<a class="proof" style="--c:{by_slug[x]['color']}" href="{root}work/{x}/index.html">{img(meta[x]['cover'], root, '(max-width: 860px) 45vw, 220px', by_slug[x]['title'] + ' cover')}<span>{e(by_slug[x]['title'])}</span></a>""" for x in s["proof"])
        inc = "".join(f"<li>{e(i)}</li>" for i in s["includes"])
        blocks.append(f"""<article class="service" id="{s['id']}">
  <div class="service__head">{icon(s['icon'], 'icon icon--big')}<h2>{e(s['name'])}</h2></div>
  <div class="service__body">
    <p class="service__sum">{e(s['summary'])}</p>
    <div class="service__cols">
      <div><h3>What you get</h3><ul class="ticks">{inc}</ul></div>
      <div><h3>Good for</h3><p>{e(s['for'])}</p></div>
    </div>
    <div class="service__proof"><h3>See it in practice</h3><div class="proofs">{proof}</div></div>
  </div>
</article>""")
    steps = "".join(f"<li><span class='step__n'>{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>" for n, (t, d) in enumerate(S["process"], 1))
    ways = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in S["ways"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in S["faq"])
    quick = "".join(f'<li id="{q["id"]}">{icon(q["icon"])}<h3>{e(q["name"])}</h3><p>{e(q["summary"])}</p><p class="quick__get">{e(q["get"])}</p><a class="quick__cta" href="#start">Ask about this</a></li>' for q in S["quick"])
    jump = "".join(f'<li><a href="#{s["id"]}">{icon(s["icon"])}<span>{e(s["name"])}</span></a></li>' for s in S["services"])
    ld = [
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Ahmed Rabea, brand design",
         "url": SITE["url"] + "/services/", "image": SITE["url"] + "/assets/og/home.jpg", "email": SITE["email"], "telephone": SITE["tel"],
         "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
         "areaServed": ["United Arab Emirates", "Saudi Arabia", "Egypt"], "availableLanguage": ["English", "Arabic"],
         "founder": {"@type": "Person", "name": "Ahmed Rabea"},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Brand design services", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["summary"]}} for s in S["services"] + S["quick"]]}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in S["faq"]]},
    ]
    page = head("Brand design services: identity, campaigns, guidelines and pitch decks | Ahmed Rabea",
                "Freelance brand identity design, social media design and campaigns, brand guidelines and pitch deck design for companies in the UAE, Saudi Arabia and Egypt, in English and Arabic. Based in Cairo.",
                root, "home", "services/", ld) + f"""<body class="services-page">
{header(root, 'services')}
<main id="main">
<section class="s-hero">
  <h1 class="s-hero__title">Brand design<br>services</h1>
  <div class="s-hero__foot">
    <p class="s-hero__lede">{e(S['intro'])}</p>
    <div class="hero__ctas"><a class="btn btn--big" href="#start">Start a project</a><a class="hero__cue" href="{root}index.html#work">See the work</a></div>
  </div>
  <ul class="jump" role="list">{jump}</ul>
</section>

<div class="services">
{chr(10).join(blocks)}
</div>

<section id="quick" class="quick" aria-labelledby="quick-h">
  <div class="sec-head"><h2 id="quick-h">Quick starts</h2><p>Smaller, fixed-scope ways to work together</p></div>
  <ul class="quick__list" role="list">{quick}</ul>
</section>

<section class="process" aria-labelledby="process-h">
  <div class="sec-head"><h2 id="process-h">How a project runs</h2></div>
  <ol class="steps" role="list">{steps}</ol>
</section>

<section class="ways-sec" aria-labelledby="ways-h">
  <div class="sec-head"><h2 id="ways-h">Ways to work together</h2></div>
  <ul class="ways3" role="list">{ways}</ul>
</section>

<section class="faq" aria-labelledby="faq-h">
  <div class="sec-head"><h2 id="faq-h">Questions</h2></div>
  <div class="faq__list">{faq}</div>
</section>

{enquiry(root)}
</main>
{footer(root)}
</body>
</html>
"""
    os.makedirs("services", exist_ok=True)
    open("services/index.html", "w", encoding="utf-8").write(page)


def frame_html(p, n, f, root, cls):
    light = " frame--light" if f.get("light") else ""
    full = f"{root}{f['files']['1800']}"
    return (f'<figure class="frame{light}{cls}"><button class="frame__zoom" type="button" data-full="{full}" '
            f'aria-label="Enlarge frame {n} of {e(p["title"])}">'
            f'{img(f, root, "(max-width: 860px) 100vw, 50vw" if "grid" in cls else "(max-width: 1160px) 100vw, 1160px", p["title"] + ", " + p["kind"].lower() + ", frame " + str(n))}</button></figure>')


def nav_row(q, root, label):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(q["arabic"])}</span>' if q["arabic"] else '<span class="row__ar"></span>'
    return f"""<div class="pn__item">
    <p class="next__label">{label}</p>
    <a class="row row--next" href="{root}work/{q['slug']}/index.html" data-peek="{cover_small(q['slug'], root)}">
      <span class="row__title"><img class="logo" src="{root}assets/img/logos/{q['slug']}.webp" width="120" height="120" alt="" loading="lazy">{e(q['title'])}</span>
      <span class="row__info"><span class="row__kind">{e(q['kind'])}</span>{e(q['line'])}</span>
      {ar}
    </a>
  </div>"""


def build_case(i, p):
    root = "../../"
    m = meta[p["slug"]]
    nxt = projects[(i + 1) % len(projects)]
    prv = projects[i - 1]
    skip = set(p.get("skip_frames", []))
    fr = [(n, f) for n, f in enumerate(m["frames"], 1) if n not in skip]
    # Slide decks (wide frames) read better two-up; tall Behance modules stay single, narrower
    wide = sum(f["w"] / f["h"] >= 1.6 for _, f in fr) > len(fr) / 2
    folding = len(fr) > FOLD + 4
    frames, v, shown = [], p.get("video"), 0
    for n, f in fr:
        shown += 1
        extra = " is-extra" if folding and shown > FOLD else ""
        span = " frame--span" if wide and shown == 1 else ""
        frames.append(frame_html(p, n, f, root, (" frame--grid" if wide else "") + span + extra))
        if v and n == v["after"]:
            cls = "film film--vertical" if v["vertical"] else "film"
            frames.append(f"""<figure class="{cls}">
  <video controls playsinline preload="none" poster="{root}assets/img/{p['slug']}/poster.webp" src="{root}{m['video']}"></video>
  <figcaption>{e(v['caption'])}</figcaption>
</figure>""")
    more = f'<div class="more"><button class="btn" type="button" data-more>Show all {len(fr)} frames</button></div>' if folding else ""
    ar = f'<span class="case__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else ""
    intro = "\n".join(f"<p>{e(x)}</p>" for x in p["intro"])
    dl = "\n".join(f"<div><dt>{e(k)}</dt><dd>{e(val)}</dd></div>" for k, val in p["meta"])
    nums = ""
    if p.get("numbers"):
        nums = '<ul class="nums" role="list" aria-label="In numbers">' + "".join(
            f'<li><span class="nums__n">{e(n)}</span><span class="nums__l">{e(l)}</span></li>' for n, l in p["numbers"]) + "</ul>"
    cover = img(m["cover"], root, "(max-width: 1680px) 100vw, 1680px", p["title"] + " cover", cls="case__cover", eager=True)
    ld = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"], "about": p["kind"],
           "description": p["line"], "creator": {"@type": "Person", "name": "Ahmed Rabea"},
           "image": f"{SITE['url']}/assets/og/{p['slug']}.jpg", "url": f"{SITE['url']}/work/{p['slug']}/"}]
    page = head(f"{p['title']}: {p['kind'].lower()} | Ahmed Rabea", p["line"], root, p["slug"], f"work/{p['slug']}/", ld) + f"""<body class="case-page" style="--c:{p['color']}">
<div class="progress" aria-hidden="true"></div>
{header(root, 'work')}
<main id="main">
<article class="case">
  <header class="case__head">
    <p class="case__back"><a href="{root}index.html#work">All work</a></p>
    <h1 class="case__title"><span><img class="logo logo--case" src="{root}assets/img/logos/{p['slug']}.webp" width="120" height="120" alt="">{e(p['title'])}</span>{ar}</h1>
  </header>
  <div class="case__coverwrap">{cover}</div>
  <div class="case__intro">
    <div class="case__text">
      <p class="case__kind">{e(p['kind'])}</p>
      <p class="tags tags--case">{tag_chips(p)}</p>
      <p class="case__line">{e(p['line'])}</p>
      {intro}
    </div>
    <dl class="case__meta">{dl}</dl>
  </div>
  {nums}
  <div class="frames{' frames--grid' if wide else ''}{' is-folded' if folding else ''}">
{chr(10).join(frames)}
  </div>
  {more}
</article>
<section class="cta-band" aria-label="Start a project">
  <p>Need something like {e(p['title'])} for your brand?</p>
  <a class="btn btn--big" href="{root}services/index.html#start">Start a project</a>
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


def build_meta_files():
    urls = ["", "services/"] + [f"work/{p['slug']}/" for p in projects]
    sm = "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc></url>" for u in urls)
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


build_home()
build_services()
for i, p in enumerate(projects):
    build_case(i, p)
build_meta_files()
print("built", 2 + len(projects), "pages")
