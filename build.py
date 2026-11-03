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
    ANALYTICS += f'\n<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
if CLOUDFLARE_TOKEN:
    ANALYTICS += f"""\n<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{CLOUDFLARE_TOKEN}"}}'></script>"""

def track(name, title=""):
    """GoatCounter click event: shows up under the "events" list in the dashboard. No cookies, no personal data."""
    if not GOATCOUNTER_CODE: return ""
    t = f' data-goatcounter-title="{title}"' if title else ""
    return f' data-goatcounter-click="{name}"{t}'


def enquire_url(root, need=None, project=None):
    """services/#start with optional ?need=<service name>&from=<project slug>; the form pre-ticks and pre-fills, all editable."""
    q = {}
    if need: q["need"] = need
    if project: q["from"] = project
    qs = ("?" + "&".join(f"{k}={__import__('urllib.parse').parse.quote(v)}" for k, v in q.items())) if q else ""
    return f"{root}services/index.html{qs}#start"


ROLE = "Senior Brand Designer & Art Director"
FEATURED = ["mazeed", "qinwan", "aywa"]  # led on the home page, in this order
BUILD_DATE = __import__("datetime").date.today().isoformat()
projects = json.load(open("content/projects.json", encoding="utf-8"))
services = json.load(open("content/services.json", encoding="utf-8"))
by_slug = {p["slug"]: p for p in projects}
meta = json.load(open("image_meta.json"))
e = lambda s: html.escape(s, quote=True)
import hashlib
# Changes whenever the CSS or JS changes, so browsers never mix new pages with old styles
VER = hashlib.md5(open("assets/site.css", "rb").read() + open("assets/site.js", "rb").read()).hexdigest()[:8]

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
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "audit": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21M8 10.5l2 2 3.5-4"/>',
})
TAGS = {  # id: (label, icon)
    "identity": ("Brand identity", "identity"), "campaign": ("Campaigns", "campaign"), "social": ("Social media", "social"),
    "packaging": ("Packaging", "packaging"), "deck": ("Decks and profiles", "deck"), "app": ("App and digital", "app"),
    "lettering": ("Custom lettering", "lettering"), "icons": ("Icon systems", "icons"), "mascot": ("Mascot", "mascot"),
}


def kind_html(p, cls):
    """Project category, with a quiet marker on self-initiated concepts so they're never mistaken for client work."""
    mark = ' <span class="si">Self-initiated</span>' if p.get("self_initiated") else ""
    return f'<span class="{cls}">{e(p["kind"])}{mark}</span>'


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


def head(title, desc, root, og, path="", ld=None, kind="website", og_alt=None):
    url = f"{SITE['url']}/{path}"
    og_url = f"{SITE['url']}/assets/og/{og}.jpg"
    og_alt = og_alt or f"{title}"
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
<meta property="og:type" content="{kind}">
<meta property="og:locale" content="en_US">
<meta name="author" content="Ahmed Rabea">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_url}">
<meta name="twitter:image:alt" content="{e(og_alt)}">
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
    return f"""<footer class="foot">
  <a class="float" href="{root}services/index.html#start"{track("cta-float", "Floating Start a project")}>
    <span class="float__mark" aria-hidden="true">AR</span><span>Start a project</span><span class="float__arrow" aria-hidden="true">&rarr;</span>
  </a>
  <p>Ahmed Rabea, senior brand designer and art director, Cairo. Taking on select freelance projects.</p>
  <p class="foot__links"><a href="{root}services/index.html">Services</a><a href="mailto:{SITE['email']}"{track("contact-email", "Email link, footer")}>Email</a><a href="{SITE['whatsapp']}"{track("contact-whatsapp", "WhatsApp link, footer")}>WhatsApp</a><a href="tel:{SITE['tel']}"{track("contact-phone", "Phone link, footer")}>{SITE['phone']}</a><a href="{SITE['linkedin']}"{track("out-linkedin", "LinkedIn")}>LinkedIn</a><a href="{SITE['behance']}"{track("out-behance", "Behance")}>Behance</a></p>
  <p class="foot__small">Visits are counted anonymously, without cookies.</p>
</footer>
"""


def enquiry(root, heading="Start a project", lead=None):
    """A short form that writes the enquiry email for the client. No server needed."""
    lead = lead or "Tell me a little about what you need, then send it by email or WhatsApp. Either way your message is written for you, ready to send."
    boxes = "".join(f'<label class="chip"><input type="checkbox" name="need" value="{e(s["name"])}"><span>{e(s["name"])}</span></label>' for s in services["services"])
    return f"""<section id="start" class="start" aria-labelledby="start-h">
  <div class="start__intro">
    <h2 id="start-h">{e(heading)}</h2>
    <p>{e(lead)}</p>
    <p class="start__steps-h" id="next-h">What happens next</p>
    <ol class="start__steps" role="list" aria-labelledby="next-h">
      <li>Send this by email or WhatsApp.</li>
      <li>We talk through the goal, the audience and what already exists.</li>
      <li>I come back with questions, scope and a proposal.</li>
      <li>Work starts once you approve the proposal.</li>
    </ol>
    <ul class="start__alt" role="list">
      <li>Email <a href="mailto:{SITE['email']}"{track("contact-email", "Email link, contact section")}>{SITE['email']}</a> <button type="button" class="copy" data-copy="{SITE['email']}"{track("contact-email-copy", "Copied email address")}>Copy</button></li>
      <li>WhatsApp <a href="{SITE['whatsapp']}"{track("contact-whatsapp", "WhatsApp link, contact section")}>Message me on WhatsApp</a></li>
      <li>Phone <a href="tel:{SITE['tel']}"{track("contact-phone", "Phone link, contact section")}>{SITE['phone']}</a></li>
    </ul>
  </div>
  <form class="start__form" data-email="{SITE['email']}" data-wa="{SITE['tel'].lstrip('+')}" data-projects='{e(json.dumps({p["slug"]: p["title"] for p in projects}, ensure_ascii=False))}'>
    <p class="start__prefill" hidden>Pre-filled from <b></b>. Change or clear anything you like.</p>
    <fieldset>
      <legend>What do you need?</legend>
      <div class="chips">{boxes}<label class="chip"><input type="checkbox" name="need" value="A review or small project"><span>A review or small project</span></label><label class="chip"><input type="checkbox" name="need" value="Not sure yet"><span>Not sure yet</span></label></div>
    </fieldset>
    <div class="start__row">
      <label>Your name<input name="name" autocomplete="name" required></label>
      <label>Company<input name="company" autocomplete="organization"></label>
    </div>
    <div class="start__row">
      <label>Timeline
        <select name="timeline"><option value="">Choose one</option><option>As soon as possible</option><option>Within a month</option><option>In 1 to 3 months</option><option>Just exploring</option></select>
      </label>
      <label>Budget range (optional)
        <select name="budget"><option value="">Not sure yet</option><option>Under USD 1,000</option><option>USD 1,000 to 3,000</option><option>USD 3,000 to 6,000</option><option>Over USD 6,000</option></select>
      </label>
    </div>
    <label>About the project<textarea name="message" rows="4" placeholder="What are you making, and who is it for?"></textarea></label>
    <div class="start__send">
      <div class="start__btns">
        <button class="btn btn--big" type="submit" value="email">Write my email</button>
        <button class="btn btn--big btn--wa" type="submit" value="whatsapp">Send on WhatsApp</button>
      </div>
      <p class="start__note" aria-live="polite">Opens your email app or WhatsApp with the message written. Nothing is sent until you press send there.</p>
    </div>
  </form>
</section>"""


def row(p, root):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else '<span class="row__ar"></span>'
    thumb = img(meta[p["slug"]]["cover"], root, "(max-width: 860px) 84px, 45vw", "", cls="row__thumb")
    return f"""<li class="item" style="--c:{p['color']}" data-tags="{' '.join(p['tags'])}">
  <a class="row" href="{root}work/{p['slug']}/index.html"{track("row-" + p["slug"], "Work list: " + p["title"])}>
    {thumb}
    <span class="row__title"><img class="logo" src="{root}assets/img/logos/{p['slug']}.webp" width="120" height="120" alt="" loading="lazy">{e(p['title'])}</span>
    <span class="row__info">{kind_html(p, 'row__kind')}{e(p['line'])}<span class="tags">{tag_chips(p)}</span></span>
    {ar}
    <span class="row__go" aria-hidden="true">{icon('arrow')}</span>
  </a>
</li>"""


def preview_strip(p, root):
    """Three more images from the project (its highlights after the first). Decorative: the card link carries the meaning."""
    nums = [n for n in p["case"]["highlights"] if n not in set(p.get("skip_frames", []))][1:4]
    thumbs = "".join(f'<img src="{root}{frame_of(p["slug"], n)["thumb320"]}" data-full="{root}{frame_of(p["slug"], n)["files"]["1000"]}" '
                     f'width="160" height="{round(160 * frame_of(p["slug"], n)["h"] / frame_of(p["slug"], n)["w"])}" alt="" loading="lazy" decoding="async">' for n in nums)
    return f'<span class="feat__strip" aria-hidden="true">{thumbs}</span>'


def feature_card(p, root, big=False):
    sizes = "(max-width: 860px) 100vw, (max-width: 1100px) 50vw, 33vw"
    # "card_frame" in projects.json swaps the home card image for one of the project's frames (keeps the three cards visually distinct)
    src = meta[p["slug"]]["frames"][p["card_frame"] - 1] if p.get("card_frame") else meta[p["slug"]]["cover"]
    pic = img(src, root, sizes, "", cls="feat__img")
    if p.get("card_pos"):  # optional crop anchor, e.g. "left center"
        pic = pic.replace("<img ", f'<img style="object-position:{p["card_pos"]}" ', 1)
    return f"""<li class="item feat{' feat--big' if big else ''}" style="--c:{p['color']}" data-tags="{' '.join(p['tags'])}">
  <a class="feat__link" href="{root}work/{p['slug']}/index.html"{track("feat-" + p["slug"], "Featured card: " + p["title"])}>
    <span class="feat__media">{pic}{preview_strip(p, root)}</span>
    <span class="feat__body">
      <span class="feat__title"><img class="logo" src="{root}assets/img/logos/{p['slug']}.webp" width="120" height="120" alt="" loading="lazy">{e(p['title'])}</span>
      {kind_html(p, 'feat__kind')}
      <span class="feat__line">{e(p['line'])}</span>
    </span>
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
        # 320 px for phones and standard screens, 520 px for high-density desktops (columns are 30vw wide, 52vw on phones)
        imgs = "".join(f'<img src="{root}{p}" srcset="{root}{p.replace(".webp", "-320.webp")} 320w, {root}{p} 520w" sizes="(max-width: 860px) 52vw, 30vw" width="{w}" height="{h}" alt="" decoding="async">' for p, w, h, _ in col)
        out.append(f'<div class="wall__col"><div class="wall__run">{imgs}{imgs}</div></div>')
    return "".join(out)


PERSON_ID = SITE["url"] + "/#person"


def person_ld():
    return {"@context": "https://schema.org", "@type": "Person", "@id": PERSON_ID, "name": "Ahmed Rabea",
            "jobTitle": "Senior Brand Designer and Art Director", "image": SITE["url"] + "/assets/og/home.jpg",
            "description": "Senior brand designer and art director in Cairo, working on brand identities, design systems, campaigns and creative direction in English and Arabic.",
            "knowsLanguage": ["en", "ar"], "areaServed": ["United Arab Emirates", "Saudi Arabia", "Egypt"],
            "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
            "url": SITE["url"] + "/", "email": "mailto:" + SITE["email"], "telephone": SITE["tel"],
            "knowsAbout": [s["name"] for s in services["services"]] + ["Arabic typography", "Bilingual design"],
            "sameAs": [SITE["linkedin"], SITE["behance"]]}


def website_ld():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE["url"] + "/#website", "name": "Ahmed Rabea",
            "alternateName": "Ahmed Rabea, brand designer", "url": SITE["url"] + "/", "inLanguage": "en", "publisher": {"@id": PERSON_ID}}


def crumbs_ld(*items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n, "name": name, "item": SITE["url"] + "/" + path} for n, (name, path) in enumerate(items, 1)]}


def services_for(slug):
    """Services whose proof list includes this project, so case studies link back to what was offered."""
    tag_map = {"identity": "brand-identity", "social": "social-media", "campaign": "social-media", "deck": "presentation-design"}
    from_tags = {tag_map[t] for t in by_slug[slug]["tags"] if t in tag_map}
    return [s for s in services["services"] if slug in s["proof"] or s["id"] in from_tags]


def build_home():
    root = ""
    feats = "\n".join(feature_card(by_slug[s], root, k == 0) for k, s in enumerate(FEATURED))
    rows = "\n".join(row(p, root) for p in projects if p["slug"] not in FEATURED)
    portrait = img(meta["portrait"], root, "(max-width: 760px) 90vw, 34vw", "Portrait of Ahmed Rabea, brand designer and art director in Cairo")
    def svc_row(n, s):
        sl, fn = s["image"]
        pic = img(frame_of(sl, fn), root, "(max-width: 860px) 30vw, 300px", "", cls="sv__img")
        meta_line = " · ".join(x for x in (s.get("price"), s.get("timeline_short")) if x)
        return f"""<li class="sv" style="--c:{by_slug[sl]['color']}"><a class="sv__link" href="services/index.html#{s['id']}"{track("svc-row-" + s["id"], "Home services row: " + s["name"])}>
  <span class="sv__n">{n:02d}</span>
  <span class="sv__main"><span class="sv__name">{e(s.get('label') or s['name'])}</span><span class="sv__short">{e(s['short'])}</span></span>
  <span class="sv__meta">{e(meta_line)}<span class="sv__proof">Seen in {e(by_slug[sl]['title'])}</span></span>
  <span class="sv__media">{pic}</span>
  <span class="row__go" aria-hidden="true">{icon('arrow')}</span>
</a></li>"""
    svc = "\n".join(svc_row(n, s) for n, s in enumerate(services["services"], 1))
    page = head(f"Ahmed Rabea | {ROLE}, Cairo",
                "Senior brand designer and art director in Cairo. Brand identities, design systems, campaigns and pitch decks for Gulf and Egyptian companies, in English and Arabic.",
                root, "home", "", [person_ld(), website_ld()], og_alt="Ahmed Rabea, Senior Brand Designer and Art Director, over a grid of his project covers") + f"""<body class="home">
{header(root)}
<main id="main">
<section class="hero" aria-labelledby="hero-name">
  <div class="wall" aria-hidden="true"><div class="wall__tilt">{wall_html(root)}</div></div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__top">
    <p class="hero__role">Hi, I'm Ahmed.<br><strong>Senior brand designer and art director</strong>, Cairo</p>
    <p class="hero__open"><span class="dot" aria-hidden="true"></span>Taking on select freelance projects</p>
  </div>
  <h1 id="hero-name" class="hero__name"><span>Ahmed</span><span>Rabea</span><span class="visually-hidden">, {ROLE}</span></h1>
  <div class="hero__foot">
    <div class="hero__copy">
      <p class="hero__lede">I build brand identities and the design systems behind them, then direct the campaigns that put them to work. In English and Arabic, for companies across the Gulf and Egypt.</p>
      <p class="hero__proof">Owned creative direction for 5 brands at once, overseeing 250+ designs a month</p>
    </div>
    <div class="hero__ctas">
      <a class="btn btn--big" href="services/index.html#start"{track("cta-hero", "Hero Start a project")}>Start a project</a>
      <a class="hero__cue" href="#work">See the work</a>
    </div>
  </div>
</section>

<section id="work" class="work" aria-labelledby="work-h">
  <div class="sec-head"><h2 id="work-h">Selected work</h2><p class="filters__status" aria-live="polite">{len(projects)} projects</p></div>
  <p class="work__thesis">A brand is judged by its hundredth asset, not its first. I design the system behind it.</p>
  {filter_bar()}
  <ul class="feats" role="list">
{feats}
  </ul>
  <h3 class="work__more">More work</h3>
  <ul class="rows" role="list">
{rows}
  </ul>
</section>

<section class="svc" aria-labelledby="svc-h">
  <div class="sec-head"><h2 id="svc-h">Services</h2><p><a href="services/index.html">All services and how I work</a></p></div>
  <ul class="svs" role="list">
{svc}
  </ul>
  <p class="svc__quick">Want to start small? Try a <a href="services/index.html#quick">brand audit, a social media template kit or a deck refresh</a>.</p>
</section>

<section id="about" class="about" aria-labelledby="about-h">
  <h2 id="about-h" class="visually-hidden">About</h2>
  <p class="about__statement">I design the system behind a brand, so every post, deck and campaign after launch still looks like it came from the same place.</p>
  <ul class="own" role="list" aria-label="What I've owned">
    <li><span class="own__n">5</span><span class="own__l">brands run at once as Creative Lead at Bayantech</span></li>
    <li><span class="own__n">250+</span><span class="own__l">designs a month overseen under one set of standards</span></li>
    <li><span class="own__n">1,000+</span><span class="own__l">clients served by mazeed, where I owned the brand's visual output</span></li>
    <li><span class="own__n">EN · AR</span><span class="own__l">Most of my work ships in both, with Arabic designed, not translated</span></li>
  </ul>
  <div class="about__grid">
    <div class="about__img">{portrait}</div>
    <div class="about__body">
      <p>I'm a senior brand designer and art director in Cairo with more than five years across B2B SaaS, healthcare, language services and consumer brands. I've run creative for five brands at once, led a team of designers, and built the guidelines and workflows that keep a brand consistent at volume. Most of my work ships in both English and Arabic. Alongside my role, I take on a small number of freelance projects.</p>
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


def offer_ld(s):
    """Schema.org Offer; adds the starting price when the service has one ("From USD 3,000")."""
    o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["summary"]}}
    import re
    m = re.search(r"USD ([\d,]+)", s.get("price") or "")
    if m:
        o["priceSpecification"] = {"@type": "PriceSpecification", "minPrice": int(m.group(1).replace(",", "")), "priceCurrency": "USD"}
    return o


def build_services():
    root = "../"
    S = services
    blocks = []
    for s in S["services"]:
        proof = "".join(f"""<a class="proof" style="--c:{by_slug[x]['color']}" href="{root}work/{x}/index.html">{img(meta[x]['cover'], root, '(max-width: 860px) 45vw, 220px', '')}<span>{e(by_slug[x]['title'])}</span></a>""" for x in s["proof"])
        price = f'<p class="service__price">{e(s["price"])}</p>' if s.get("price") else ""
        if s.get("range"):  # optional "most projects" range shown under the starting price
            price += f'<p class="service__range">{e(s["range"])}</p>'
        inc = "".join(f"<li>{e(i)}</li>" for i in s["includes"])
        blocks.append(f"""<article class="service" id="{s['id']}">
  <div class="service__head">{icon(s['icon'], 'icon icon--big')}<h2>{e(s['name'])}</h2></div>
  <div class="service__body">
    <p class="service__sum">{e(s['summary'])}</p>{price}
    <div class="service__cols">
      <div><h3>What you get</h3><ul class="ticks">{inc}</ul></div>
      <div><h3>Good for</h3><p>{e(s['for'])}</p>{f'<h3>Typical timeline</h3><p>{e(s["timeline"])}</p>' if s.get("timeline") else ""}</div>
    </div>
    <div class="service__proof"><h3>See it in practice</h3><div class="proofs">{proof}</div></div>
    <p class="service__ask"><a class="quick__cta" href="#start" data-need="{e(s['name'])}"{track("ask-" + s["id"], "Ask about: " + s["name"])}>Ask about {e(s['name'][0].lower() + s['name'][1:])}</a></p>
  </div>
</article>""")
    steps = "".join(f"<li><span class='step__n'>{n}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>" for n, (t, d) in enumerate(S["process"], 1))
    qby = {q["id"]: q for q in S["quick"]}
    def start_card(o):
        items = []
        for q in (qby[x] for x in o["examples"]):
            price = f' <span class="service__price">{e(q["price"])}</span>' if q.get("price") else ""
            if q.get("timeline"): price += f' <span class="quick__time">{e(q["timeline"])}</span>'
            items.append(f'<li id="{q["id"]}"><b>{e(q["name"])}</b> {e(q["summary"])} <span class="quick__get">{e(q["get"])}</span>{price}</li>')
        ex = f'<ul class="start-opt__ex" role="list">{"".join(items)}</ul>' if items else ""
        return (f'<li class="start-opt" id="{o["id"]}">{icon(o["icon"])}<h3>{e(o["name"])}</h3><p>{e(o["summary"])}</p>{ex}'
                f'<a class="quick__cta" href="#start" data-need="{e(o["need"])}"{track(o["id"], "Ways to start: " + o["name"])}>Ask about this</a></li>')
    starts = "".join(start_card(o) for o in S["start"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in S["faq"])
    jump = "".join(f'<li><a href="#{s["id"]}">{icon(s["icon"])}<span>{e(s["name"])}</span></a></li>' for s in S["services"])
    ld = [
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Ahmed Rabea, brand design",
         "url": SITE["url"] + "/services/", "image": SITE["url"] + "/assets/og/home.jpg", "email": SITE["email"], "telephone": SITE["tel"],
         "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
         "areaServed": ["United Arab Emirates", "Saudi Arabia", "Egypt"], "availableLanguage": ["English", "Arabic"],
         "founder": {"@id": PERSON_ID}, "provider": {"@id": PERSON_ID},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Brand design services", "itemListElement": [
             offer_ld(s) for s in S["services"] + S["quick"]]}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in S["faq"]]},
        person_ld(), crumbs_ld(("Home", ""), ("Services", "services/")),
    ]
    ld[0] = {k: v for k, v in ld[0].items() if v is not None}
    page = head("Brand identity, design systems and campaign design services | Ahmed Rabea",
                "Freelance brand identity, brand guidelines and design systems, social media and campaign systems, and pitch deck and company profile design. English and Arabic, from Cairo.",
                root, "home", "services/", ld, og_alt="Ahmed Rabea brand design services") + f"""<body class="services-page">
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

<section id="quick" class="quick" aria-labelledby="quick-h">
  <div class="sec-head"><h2 id="quick-h">Ways to start</h2><p>Pick the size that fits. Not sure? Start with a review.</p></div>
  <ul class="quick__list" role="list">{starts}</ul>
</section>

<div class="services">
{chr(10).join(blocks)}
</div>



<section class="process" aria-labelledby="process-h">
  <div class="sec-head"><h2 id="process-h">How a project runs</h2></div>
  <ol class="steps" role="list">{steps}</ol>
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


def filled(v):
    """Case-study fields starting with TODO are placeholders: kept in the JSON, never shown on the site."""
    return bool(v) and not str(v).startswith("TODO")


def frame_of(slug, n):
    return meta[slug]["frames"][n - 1]


def frame_html(p, n, f, root, sizes, cls="frame"):
    light = " frame--light" if f.get("light") else ""
    shape = " frame--wide" if f["w"] / f["h"] >= 1.6 else " frame--tall"
    alt = f"{p['title']} {p['kind'].lower()}, image {n}"
    return (f'<figure class="{cls}{light}{shape}"><button class="frame__zoom" type="button" data-full="{root}{f["files"]["1800"]}" '
            f'aria-label="Enlarge {e(alt)}">{img(f, root, sizes, alt)}</button></figure>')


def film_html(p, root, v, m):
    cls = "film film--vertical" if v["vertical"] else "film"
    return (f'<figure class="{cls}"><video controls playsinline preload="none" poster="{root}assets/img/{p["slug"]}/poster.webp" '
            f'src="{root}{m["video"]}"></video><figcaption>{e(v["caption"])}</figcaption></figure>')


def nav_row(q, root, label):
    ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(q["arabic"])}</span>' if q["arabic"] else '<span class="row__ar"></span>'
    return f"""<div class="pn__item">
    <p class="next__label">{label}</p>
    <a class="row row--next" href="{root}work/{q['slug']}/index.html" data-peek="{cover_small(q['slug'], root)}">
      <span class="row__title"><img class="logo" src="{root}assets/img/logos/{q['slug']}.webp" width="120" height="120" alt="" loading="lazy">{e(q['title'])}</span>
      <span class="row__info">{kind_html(q, 'row__kind')}{e(q['line'])}</span>
      {ar}
    </a>
  </div>"""


svc_by_id = {s["id"]: s for s in services["services"]}


def related_html(p, root):
    """Hand-picked related projects, each with the reason it's related."""
    items = []
    for slug, why in p.get("related", []):
        q = by_slug[slug]
        ar = f'<span class="row__ar" lang="ar" dir="rtl">{e(q["arabic"])}</span>' if q["arabic"] else '<span class="row__ar"></span>'
        items.append(f"""<div class="pn__item">
    <p class="next__label">{e(why)}</p>
    <a class="row row--next" href="{root}work/{slug}/index.html" data-peek="{cover_small(slug, root)}"{track(f"related-{p['slug']}-{slug}", f"Related: {p['title']} to {q['title']}")}>
      <span class="row__title"><img class="logo" src="{root}assets/img/logos/{slug}.webp" width="120" height="120" alt="" loading="lazy">{e(q['title'])}</span>
      <span class="row__info">{kind_html(q, 'row__kind')}{e(q['line'])}</span>
      {ar}
    </a>
  </div>""")
    return "".join(items)


def build_case(i, p):
    """One template for every case study. Content comes from p["case"] in content/projects.json:
    facts strip, context / challenge / direction / system, five highlights, chapters, outcome, credits."""
    root = "../../"
    m = meta[p["slug"]]
    C = p["case"]
    nxt, prv = projects[(i + 1) % len(projects)], projects[i - 1]
    skip = set(p.get("skip_frames", []))
    v = p.get("video")

    # Facts strip: client and industry first, then role/scope/market/type, then year. Empty fields drop out.
    facts = [("Client", C.get("client")), ("Industry", C.get("industry")), ("Engagement", C.get("engagement"))]
    facts += [(k, val) for k, val in p["meta"]]
    facts += [("Year", C.get("year"))]
    facts_html = "".join(f"<div><dt>{e(k)}</dt><dd>{e(val)}</dd></div>" for k, val in facts if filled(val))

    # Story: short labelled blocks rather than one long essay
    blocks = [("Context", C.get("context")), ("The challenge", C.get("challenge")),
              ("Creative direction", C.get("direction")), ("The system", C.get("system"))]
    story = "".join(f'<div class="story__b"><h3>{e(k)}</h3><p>{e(val)}</p></div>' for k, val in blocks if filled(val))

    # Highlights: one large frame and four supporting ones
    wide_set = sum(f["w"] / f["h"] >= 1.6 for f in m["frames"]) > len(m["frames"]) / 2
    hl = [n for n in C["highlights"] if n not in skip]
    bento = "".join(frame_html(p, n, frame_of(p["slug"], n), root,
                               "(max-width: 860px) 100vw, 60vw" if k == 0 else "(max-width: 860px) 50vw, 25vw",
                               "frame bento__" + ("big" if k == 0 else "sm")) for k, n in enumerate(hl))

    # Chapters: everything else, grouped and collapsed, so nobody has to scroll past 30 slides
    chapters, nav = [], []
    picks_all = C.get("picks") or [[] for _ in C["chapters"]]
    for c, ((title, nums), pk) in enumerate(zip(C["chapters"], picks_all), 1):
        nums = [n for n in nums if n not in skip]
        if not nums: continue
        cid = f"ch-{c}"
        # Picks: the two or three strongest images of the chapter, visible without opening it
        pk = [n for n in pk if n in nums]
        pick_html = "".join(frame_html(p, n, frame_of(p["slug"], n), root, "(max-width: 860px) 50vw, 300px", "frame pick") for n in pk)
        thumbs = "".join(f'<img src="{root}{frame_of(p["slug"], n)["thumb"]}" width="160" height="{round(160 * frame_of(p["slug"], n)["h"] / frame_of(p["slug"], n)["w"])}" alt="" loading="lazy">' for n in nums[:4])
        body = []
        for n in nums:
            f = frame_of(p["slug"], n)
            body.append(frame_html(p, n, f, root, "(max-width: 860px) 100vw, 45vw" if f["w"] / f["h"] >= 1.6 else "(max-width: 860px) 100vw, 70vw"))
            if v and n == v["after"]:
                body.append(film_html(p, root, v, m))
        count = f"{len(nums)} image{'s' if len(nums) > 1 else ''}" + (" and a film" if v and v["after"] in nums else "")
        thumbs_html = "" if pk else f'<span class="chapter__thumbs" aria-hidden="true">{thumbs}</span>'
        more = len(nums) - len(pk)
        picks_block = (f'<div class="chapter__picks picks--{"wide" if wide_set else "tall"}">{pick_html}'
                       f'<button type="button" class="chapter__more" data-open-ch="{cid}">Show all {len(nums)}</button></div>') if pk and more > 0 else (
                       f'<div class="chapter__picks picks--{"wide" if wide_set else "tall"}">{pick_html}</div>' if pk else "")
        chapters.append(f"""<div class="chapter-block"><details class="chapter" id="{cid}">
  <summary><span class="chapter__n">{c:02d}</span><span class="chapter__t">{e(title)}</span><span class="chapter__count">{count}</span>{thumbs_html}<span class="chapter__toggle" aria-hidden="true">{icon('plus')}</span></summary>
  <div class="chapter__body">{''.join(body)}</div>
</details>{picks_block}</div>""")
        nav.append(f'<li><a href="#{cid}" data-open="{cid}"><span>{c:02d}</span>{e(title)}</a></li>')

    # Outcome: real results only. Numbers already in the project are scale facts, shown with it.
    nums = ""
    if p.get("numbers"):
        nums = '<ul class="nums" role="list">' + "".join(
            f'<li><span class="nums__n">{e(n)}</span><span class="nums__l">{e(l)}</span></li>' for n, l in p["numbers"]) + "</ul>"
    outcome = ""
    if filled(C.get("outcome")) or nums:
        txt = f'<p class="outcome__p">{e(C["outcome"])}</p>' if filled(C.get("outcome")) else ""
        outcome = f'<section class="outcome" aria-labelledby="out-h"><h2 id="out-h" class="case-h">{"Outcome" if txt else "In numbers"}</h2>{txt}{nums}</section>'
    credits = f'<p class="credits"><span>Credits</span> {e(C["credits"])}</p>' if filled(C.get("credits")) else ""

    ar = f'<span class="case__ar" lang="ar" dir="rtl">{e(p["arabic"])}</span>' if p["arabic"] else ""
    cover = img(m["cover"], root, "(max-width: 1680px) 100vw, 1680px", f"{p['title']} cover: {p['line']}", cls="case__cover", eager=True)
    svc = services_for(p["slug"])
    svc_links = "".join(f'<a href="{root}services/index.html#{s["id"]}">{icon(s["icon"])}{e(s["name"])}</a>' for s in svc)
    svc_block = f'<div class="case__svc"><h2 class="case__svc-h">Services behind this project</h2><p class="case__svc-list">{svc_links}</p></div>' if svc else ""
    ld = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"], "about": p["kind"], "genre": p["kind"],
           "description": p["line"], "creator": {"@id": PERSON_ID, "@type": "Person", "name": "Ahmed Rabea", "url": SITE["url"] + "/"},
           "keywords": ", ".join(TAGS[t][0] for t in p["tags"]), "inLanguage": "en",
           "image": f"{SITE['url']}/assets/og/{p['slug']}.jpg", "url": f"{SITE['url']}/work/{p['slug']}/"},
          crumbs_ld(("Home", ""), ("Work", "#work"), (p["title"], f"work/{p['slug']}/"))]
    if filled(C.get("year")): ld[0]["dateCreated"] = C["year"][:4]
    desc = f"{p['line']} Case study by Ahmed Rabea, senior brand designer and art director."
    page = head(f"{p['title']}: {p['kind'].lower()} | Ahmed Rabea", desc, root, p["slug"], f"work/{p['slug']}/", ld,
                kind="article", og_alt=f"{p['title']} {p['kind'].lower()} by Ahmed Rabea") + f"""<body class="case-page" style="--c:{p['color']}" data-slug="{p['slug']}">
<div class="progress" aria-hidden="true"></div>
{header(root, 'work')}
<main id="main">
<article class="case">
  <header class="case__head">
    <p class="case__back"><a href="{root}index.html#work">All work</a></p>
    <h1 class="case__title"><span><img class="logo logo--case" src="{root}assets/img/logos/{p['slug']}.webp" width="120" height="120" alt="">{e(p['title'])}</span>{ar}</h1>
  </header>
  {f'<p class="case__idea"><span class="case__idea-k">The idea</span>{e(C["idea"])}</p>' if filled(C.get("idea")) else ""}
  <div class="case__coverwrap">{cover}</div>

  <section class="case__intro" aria-labelledby="ov-h">
    <div class="case__text">
      <h2 id="ov-h" class="case__kind">{e(p['kind'])}{' <span class="si">Self-initiated</span>' if p.get('self_initiated') else ''}</h2>
      <p class="tags tags--case">{tag_chips(p)}</p>
      <p class="case__line">{e(p['line'])}</p>
      <div class="story">{story}</div>
    </div>
    <div class="case__side"><dl class="case__meta">{facts_html}</dl>{svc_block}</div>
  </section>

  <section class="glance" aria-labelledby="glance-h">
    <h2 id="glance-h" class="case-h">Highlights</h2>
    <div class="bento bento--{'wide' if wide_set else 'tall'}">{bento}</div>
  </section>

  {outcome}

  <section class="chapters" aria-labelledby="chapters-h">
    <nav class="chapters__nav" aria-labelledby="chapters-h">
      <h2 id="chapters-h" class="case-h">The full project</h2>
      <ol role="list">{''.join(nav)}</ol>
      <button type="button" class="btn btn--ghost" data-all aria-expanded="false">Open all chapters</button>
    </nav>
    <div class="chapters__list">{''.join(chapters)}</div>
  </section>
  {credits}
</article>
<section class="cta-band" aria-labelledby="cta-h">
  <h2 id="cta-h" class="cta-band__h">Need something like {e(p['title'])} for your brand?</h2>
  <div class="cta-band__btns">
    <a class="btn btn--big" href="{enquire_url(root, svc_by_id[p['primary_service']]['name'], p['slug'])}"{track("cta-case-" + p["slug"], "Case study Start a project: " + p["title"])}>Start a project</a>
    <a class="btn btn--big btn--ghost" href="{SITE['whatsapp']}"{track("contact-whatsapp", "WhatsApp link, case study")}>WhatsApp me</a>
  </div>
</section>
<nav class="pn" aria-labelledby="pn-h">
  <div class="pn__head"><h2 id="pn-h" class="case-h">Related work</h2><a href="{root}index.html#work">All work</a></div>
  {related_html(p, root)}
</nav>
</main>
{footer(root)}
<dialog class="viewer" aria-label="Enlarged image">
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


def build_checklist():
    """Writes content/CONTENT-TODO.md: every placeholder still waiting for real information."""
    lines = ["# Content still needed", "", "Generated by build.py. Fill these in content/projects.json (the `case` block of each project).",
             "Anything starting with TODO is hidden on the site until you replace it.", ""]
    for p in projects:
        C = p["case"]
        todo = [k for k in ("client", "industry", "engagement", "year", "context", "challenge", "direction", "system", "outcome", "credits")
                if not filled(C.get(k))]
        lines.append(f"## {p['title']}")
        lines += [f"- [ ] `{k}` is a draft I wrote from your existing copy. Review or replace: \"{C[k]}\"" for k in C.get("drafts", [])]
        lines += [f"- [ ] `{k}`" + (f": {C[k][6:]}" if C.get(k) else ": optional, leave null to hide") for k in todo] or ["- Nothing missing"]
        lines.append("")
    open("content/CONTENT-TODO.md", "w", encoding="utf-8").write("\n".join(lines))


def build_meta_files():
    urls = ["", "services/"] + [f"work/{p['slug']}/" for p in projects]
    sm = "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc><lastmod>{BUILD_DATE}</lastmod></url>" for u in urls)
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")


build_home()
build_services()
for i, p in enumerate(projects):
    build_case(i, p)
build_meta_files()
build_checklist()
print("built", 2 + len(projects), "pages")
