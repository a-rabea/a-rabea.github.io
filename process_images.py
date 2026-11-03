import json, os, sys, shutil
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from assets_manifest import SOURCES
OUT = "assets/img"; meta = {}
def save(src, dst_base, widths, q=80):
    im = Image.open(src).convert("RGB"); W, H = im.size; res = {}
    for w in widths:
        w2 = min(w, W); h2 = round(H * w2 / W)
        p = f"{dst_base}-{w}.webp"
        if not os.path.exists(p):
            im.resize((w2, h2), Image.LANCZOS).save(p, "WEBP", quality=q, method=6)
        res[w] = p
    return {"w": W, "h": H, "files": res}
for slug, s in SOURCES.items():
    d = f"{OUT}/{slug}"; os.makedirs(d, exist_ok=True)
    m = {"cover": save(s["cover"], f"{d}/cover", [1400, 800]), "frames": []}
    for i, f in enumerate(s["frames"], 1):
        fr = save(f, f"{d}/{i:02d}", [1800, 1000])
        # small thumbnail for chapter previews in the case-study template
        t = f"{d}/{i:02d}-480.webp"
        if not os.path.exists(t):
            im = Image.open(fr["files"][1000]); im.resize((480, round(480 * im.height / im.width)), Image.LANCZOS).save(t, "WEBP", quality=78, method=6)
        fr["thumb"] = t
        t2 = f"{d}/{i:02d}-320.webp"  # featured-card preview strip
        if not os.path.exists(t2):
            im = Image.open(fr["files"][1000]); im.resize((320, round(320 * im.height / im.width)), Image.LANCZOS).save(t2, "WEBP", quality=74, method=6)
        fr["thumb320"] = t2
        m["frames"].append(fr)
    if "video" in s:
        os.makedirs("assets/video", exist_ok=True); v = f"assets/video/{slug}.mp4"
        shutil.copy(s["video"], v); m["video"] = v
    meta[slug] = m; print(slug, len(m["frames"]))
os.makedirs(f"{OUT}/about", exist_ok=True)
meta["portrait"] = save("/mnt/user-data/uploads/02 Portfolio/Personal Brand/Photoshoot Professional Pics Profile Ahmed Rabea Me/Quiet monochrome portrait, softly lit.png", f"{OUT}/about/portrait", [1000, 600])
json.dump(meta, open("image_meta.json", "w"), indent=1)
