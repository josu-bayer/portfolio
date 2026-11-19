# Irudiak optimizatu: argazki-bandak WebP formatuan bi zabaleratan, erretratua, aplikazioen
# pantaila-argazkiak eta OG irudia. Jatorrizko JPGak public/img karpetan geratzen dira.
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "public", "img")

# Argazki-bandak: 800 eta 1600 px zabal
for izena in ["bridge", "butroi", "gaztelugatxe"]:
    jat = Image.open(os.path.join(IMG, izena + ".jpg")).convert("RGB")
    for w in (800, 1600):
        w2 = min(w, jat.width)
        h2 = round(jat.height * w2 / jat.width)
        jat.resize((w2, h2), Image.LANCZOS).save(os.path.join(IMG, f"{izena}-{w}.webp"), "WEBP", quality=72, method=6)

# Erretratua: 256 px (128 px erakusten da, 2x pantailetarako)
aurp = Image.open(os.path.join(IMG, "josu-2026-12.jpg")).convert("RGB")
aurp.resize((256, 256), Image.LANCZOS).save(os.path.join(IMG, "josu-2026-12-256.webp"), "WEBP", quality=80, method=6)

# Aplikazioen pantaila-argazkiak: assets/aplikazioak/*.png (780 px zabal, 2x) -> 3:5 moztu, 540 px zabal
SRC = os.path.join(HERE, "assets", "aplikazioak")
DST = os.path.join(IMG, "aplikazioak")
os.makedirs(DST, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    if f.endswith(".png"):
        im = Image.open(os.path.join(SRC, f)).convert("RGB")
        im = im.crop((0, 0, im.width, round(im.width * 5 / 3)))
        im = im.resize((540, 900), Image.LANCZOS)
        im.save(os.path.join(DST, f[:-4] + ".webp"), "WEBP", quality=80, method=6)
        im.resize((540, 900)).save(os.path.join(DST, f[:-4] + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)

# OG irudia, 1200x630: zubiaren argazkia gris-eskalan ezkerrean, izena eta rola eskuinean
og = Image.new("RGB", (1200, 630), "#0c4a4a")
zubi = Image.open(os.path.join(IMG, "bridge.jpg")).convert("L").convert("RGB")
zw = round(zubi.width * 630 / zubi.height)
zubi = zubi.resize((zw, 630), Image.LANCZOS)
og.paste(zubi.crop(((zw - 520) // 2, 0, (zw - 520) // 2 + 520, 630)), (0, 0))
d = ImageDraw.Draw(og)
LETRA = os.path.join(HERE, "public", "fonts", "cabinet-grotesk-800.woff2")
def letra(n):
    try:
        return ImageFont.truetype(LETRA, n)
    except OSError:
        return ImageFont.truetype("arialbd.ttf", n)
d.text((580, 170), "Josu Bayer", font=letra(84), fill="#e2e2e2")
d.text((582, 290), "Project manager who", font=letra(40), fill="#a6c8c5")
d.text((582, 342), "builds with AI", font=letra(40), fill="#a6c8c5")
d.text((582, 520), "josu-bayer.web.app", font=letra(30), fill="#e2e2e2")
og.save(os.path.join(IMG, "og.jpg"), "JPEG", quality=85, optimize=True, progressive=True)
# Ikonoak: "jb" letrak kolore nagusiaren gainean (favicon.svg eskuz idatzia dago public/ karpetan)
PUB = os.path.join(HERE, "public")
for izena, n in (("apple-touch-icon.png", 180), ("favicon-32.png", 32), ("icon-512.png", 512)):
    ik = Image.new("RGB", (n * 4, n * 4), "#0c4a4a")
    di = ImageDraw.Draw(ik)
    ft = letra(round(n * 4 * 0.56))
    b = di.textbbox((0, 0), "jb", font=ft)
    di.text(((n * 4 - (b[2] - b[0])) / 2 - b[0], (n * 4 - (b[3] - b[1])) / 2 - b[1]), "jb", font=ft, fill="#e2e2e2")
    ik.resize((n, n), Image.LANCZOS).save(os.path.join(PUB, izena), "PNG", optimize=True)
print("eginda")
