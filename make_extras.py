"""Derived assets: share cards (JPG 1200x630), home-screen icon, light-frame flags.
Run after process_images.py:  python3 make_extras.py
"""
import json, os
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont, ImageStat

meta = json.load(open("image_meta.json"))
projects = json.load(open("content/projects.json", encoding="utf-8"))
os.makedirs("assets/og", exist_ok=True)

# Static TTF of Archivo at the condensed heavy setting, for drawing type into images
ttf = "/tmp/archivo.ttf"
if not os.path.exists(ttf):
    f = TTFont("assets/fonts/archivo-wdth.woff2"); f.flavor = None; f.save(ttf)
def font(size, wdth=62, wght=800):
    fo = ImageFont.truetype(ttf, size)
    try: fo.set_variation_by_axes([wdth, wght] if fo.get_variation_axes()[0]["name"] in (b"Width", "Width") else [wght, wdth])
    except Exception: pass
    return fo

BG, FG, TEAL = (13, 16, 15), (232, 236, 233), (60, 207, 174)

def fit(im, W, H):
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

# Project cards: the cover, with a slim name band
for p in projects:
    c = Image.open(meta[p["slug"]]["cover"]["files"]["1400"]).convert("RGB")
    card = fit(c, 1200, 630)
    d = ImageDraw.Draw(card)
    d.rectangle((0, 560, 1200, 630), fill=BG)
    d.text((40, 572), p["title"], font=font(44), fill=FG)
    d.text((1160, 578), "Ahmed Rabea", font=font(30, 75, 700), fill=TEAL, anchor="ra")
    card.save(f"assets/og/{p['slug']}.jpg", quality=84, optimize=True)

# Home card: name over a strip of covers
home = Image.new("RGB", (1200, 630), BG)
strip = [p["slug"] for p in projects[:6]]
for i, s in enumerate(strip):
    t = fit(Image.open(meta[s]["cover"]["files"]["800"]).convert("RGB"), 196, 300)
    home.paste(t, (8 + i * 198, 8))
shade = Image.new("RGB", (1200, 630), BG)
mask = Image.linear_gradient("L").resize((1200, 630)).point(lambda v: min(255, int(v * 1.4)))
home = Image.composite(shade, home, mask)
d = ImageDraw.Draw(home)
d.text((40, 300), "AHMED", font=font(170), fill=FG)
d.text((40, 450), "RABEA", font=font(170), fill=TEAL)
d.text((1160, 590), "Senior Brand Designer & Art Director", font=font(30, 90, 500), fill=FG, anchor="rs")
home.save("assets/og/home.jpg", quality=84, optimize=True)

# Home-screen icon
ic = Image.new("RGB", (180, 180), BG)
ImageDraw.Draw(ic).text((90, 96), "AR", font=font(96), fill=TEAL, anchor="mm")
ic.save("assets/apple-touch-icon.png")

# Flag frames that are mostly white so the page can frame them instead of glaring
for p in projects:
    for f in meta[p["slug"]]["frames"]:
        im = Image.open(f["files"]["1000"]).convert("L")
        w, h = im.size
        edges = [im.crop(b) for b in ((0, 0, w, 12), (0, h - 12, w, h), (0, 0, 12, h), (w - 12, 0, w, h))]
        f["light"] = sum(ImageStat.Stat(e).mean[0] for e in edges) / 4 > 200
json.dump(meta, open("image_meta.json", "w"), indent=1)
print({p["slug"]: sum(f["light"] for f in meta[p["slug"]]["frames"]) for p in projects})
