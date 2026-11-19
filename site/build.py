import html, os
import json
from content import ROWS, BACKGROUND, T, GH, SCREENS

OUT = os.path.join(os.path.dirname(__file__), "public")
EMAIL = "bayer.josu@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/josu-bayer-agirre-090678208/"
GITHUB = "https://github.com/josu-bayer"
ARROW = '<span class="ar" aria-hidden="true"> ↗</span>'
CVS = {"en": "files/CV_Josu_Bayer_Agirre.pdf", "eu": "files/CV_Josu_Bayer_Agirre_eu.pdf", "es": "files/CV_Josu_Bayer_Agirre_es.pdf"}
SITE = "https://josu-bayer.web.app/"
LANGS = [("en", "English", ""), ("eu", "Euskara", "eu/"), ("es", "Castellano", "es/")]  # default first, then Basque, then Spanish


def e(s):
    return html.escape(s, quote=True)


def page(lang):
    t = T[lang]
    up = "" if lang == "en" else "../"  # path prefix back to the site root
    A = lambda p: up + p

    # ledger rows
    rows = []
    for i, r in enumerate(ROWS):
        name, kind, fig, cap = r[lang]
        inner = (
            f'<span class="nm">{e(name)}{ARROW if r["repo"] else ""}</span><span class="kd">{e(kind)}</span>'
            f'<span class="yr">{e(r["year"])}</span><span class="cp">{e(cap)}</span>'
        )
        attrs = f'class="row" data-t="{r["t"]}" data-fig="{e(fig)}" data-cap="{e(cap)}" data-name="{e(name)}"'
        if r["repo"]:
            href = GH + r["repo"]
            rows.append(f'<li {attrs}><a href="{href}" aria-label="{e(name)}, {e(t["view_repo"])}">{inner}</a></li>')
        else:
            rows.append(f'<li {attrs}><button type="button" class="rowbtn">{inner}</button></li>')
    chips = "".join(
        f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{e(v)}</button>'
        for k, v in t["chips"]
    )
    f0 = ROWS[0][lang]

    # background table
    bg = []
    for grp, items in BACKGROUND[lang]:
        bg.append(f'<div class="g"><h3 class="grp">{e(grp)}</h3>')
        for a, b, c, d in items:
            bg.append(
                f'<div class="tr"><span class="c1">{e(a)}</span><span class="c2">{e(b)}</span>'
                f'<span class="c3">{e(c)}</span><span class="c4">{e(d)}</span></div>'
            )
        bg.append('</div>')

    def lhref(code, path):
        if code == lang:
            return "./"
        return up + path

    CUR = chr(34).join([' aria-current=', 'true', ''])
    switch = "".join(
        f'<a class="lang{" cur" if code == lang else ""}" href="{lhref(code, path)}" hreflang="{code}" lang="{code}"'
        f'{CUR if code == lang else ""}>{e(name)}</a>'
        for code, name, path in LANGS
    )
    foot_langs = "".join(
        f'<li><a href="{lhref(code, path)}" hreflang="{code}" lang="{code}">{e(name)}</a></li>' for code, name, path in LANGS
    )
    alts = "".join(f'<link rel="alternate" hreflang="{code}" href="{SITE}{path}">' + chr(10) for code, name, path in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}">'

    # SEO: kanonikoa, OpenGraph, Twitter eta JSON-LD
    path_self = dict((c, p) for c, _, p in LANGS)[lang]
    url_self = SITE + path_self
    og_alts = "".join(f'<meta property="og:locale:alternate" content="{T[c]["og_locale"]}">' + chr(10) for c, _, _ in LANGS if c != lang)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": "Josu Bayer Agirre",
        "alternateName": "Josu Bayer", "url": SITE, "image": SITE + "img/josu-2026-12.jpg",
        "jobTitle": t["job"], "email": "mailto:" + EMAIL,
        "address": {"@type": "PostalAddress", "addressRegion": "Bizkaia", "addressCountry": "ES"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "UPV/EHU"},
        "sameAs": [GITHUB, LINKEDIN],
    }, ensure_ascii=False)
    seo = (
        f'<link rel="canonical" href="{url_self}">\n'
        f'<meta property="og:type" content="profile">\n'
        f'<meta property="og:site_name" content="Josu Bayer">\n'
        f'<meta property="og:title" content="{e(t["og_title"])}">\n'
        f'<meta property="og:description" content="{e(t["desc"])}">\n'
        f'<meta property="og:url" content="{url_self}">\n'
        f'<meta property="og:image" content="{SITE}img/og.jpg">\n'
        f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{e(t["og_title"])}">\n'
        f'<meta property="og:locale" content="{t["og_locale"]}">\n{og_alts}'
        f'<meta property="profile:first_name" content="Josu">\n<meta property="profile:last_name" content="Bayer Agirre">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="author" content="Josu Bayer Agirre">\n'
        f'<script type="application/ld+json">{ld}</script>'
    )

    # argazki-bandak: WebP bi zabaleratan, JPG ordezko gisa
    def band(izena, w, h, alt, extra=""):
        return (
            f'<picture><source type="image/webp" srcset="{A("img/" + izena + "-800.webp")} 800w, {A("img/" + izena + "-1600.webp")} 1600w" sizes="100vw">'
            f'<img src="{A("img/" + izena + ".jpg")}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"{extra}></picture>'
        )

    # aplikazioen pantailak
    screens = "".join(
        f'<li class="scr"><a href="{GH}{sc["repo"]}" aria-label="{e(sc["name"])}, {e(t["view_repo"])}">'
        f'<picture><source type="image/webp" srcset="{A("img/aplikazioak/" + sc["id"] + ".webp")}">'
        f'<img src="{A("img/aplikazioak/" + sc["id"] + ".jpg")}" width="540" height="900" alt="{e(sc[lang])}" loading="lazy" decoding="async"></picture>'
        f'<span class="scr-n">{e(sc["name"])}{ARROW}</span></a></li>'
        for sc in SCREENS
    )

    mailto = f"mailto:{EMAIL}?subject={e(t['email_subject']).replace(' ', '%20')}"
    cr = t["contact_rows"]

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta name="theme-color" content="#0c4a4a" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e1819" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{A('favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{A('favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{A('apple-touch-icon.png')}">
{seo}
{alts}
<link rel="preload" href="{A('fonts/cabinet-grotesk-800.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{A('site.css')}">
<script>document.documentElement.className="js"</script>
</head>
<body>
<a class="skip" href="#about">{e(t['skip'])}</a>

<header class="top" id="top">
  <div class="bar">
    <a class="mark" href="#top">Josu Bayer</a>
    <div class="bar-r">
      {switch}
      <a class="btn" href="{mailto}">{e(t['hello'])}</a>
    </div>
  </div>
</header>

<main>
<section class="about" id="about">
  <h1 class="hero">{e(t['h1'][0])}<br>{e(t['h1'][1])}</h1>
  <h2 class="sh rv">{e(t['h_about'])}</h2>
  <div class="story rv">
    <p>{t['about'][0]}</p>
  </div>
  <p class="cta rv"><a href="#contact"><mark class="hl1">{e(t['about_cta'])}</mark></a></p>
</section>

<figure class="band" data-drift>
  {band('bridge', 1800, 1087, "Archival photograph of the Bizkaia transporter bridge, two iron towers carrying a walkway over the estuary, a steamer passing beneath")}
  <figcaption>{e(t['bridge_cap'])}</figcaption>
</figure>

<section class="work" id="work">
  <div class="wrap">
    <div class="ledger">
      <h2 class="sh rv">{e(t['h_work'])}</h2>
      <div class="chips rv" role="group" aria-label="{e(t['h_work'])}">{chips}</div>
      <p class="hint rv"><span aria-hidden="true">↗</span> {e(t['repo_hint'])}</p>
      <ul class="rows rv">
        {''.join(rows)}
      </ul>
    </div>
    <aside class="peek" aria-hidden="true">
      <div class="peek-in">
        <p class="pf">{e(f0[2])}</p>
        <p class="pc">{e(f0[3])}</p>
        <p class="pn">{e(f0[0])}</p>
      </div>
    </aside>
  </div>
</section>

<section class="screens" id="screens" aria-labelledby="h-screens">
  <h2 class="sh rv" id="h-screens">{e(t['h_screens'])}</h2>
  <ul class="scr-row rv" tabindex="0" aria-label="{e(t['screens_label'])}">{screens}</ul>
</section>

<figure class="band" data-drift>
  {band('butroi', 1600, 792, "Butroi castle in Gatika, Bizkaia, seen from below, with two round towers and crenellated walls against a blue sky", ' data-oy="40"')}
  <figcaption>{e(t['butroi_cap'])}</figcaption>
</figure>


<section class="bg" id="background">
  <h2 class="sh rv">{e(t['h_bg'])}</h2>
  <div class="table rv">
    {''.join(bg)}
  </div>
</section>



<figure class="band" data-drift>
  {band('gaztelugatxe', 1800, 1171, "The island of Gaztelugatxe, a rocky headland with a small stone chapel on top, joined to the coast by a winding stairway, under a blue sky")}
  <figcaption>{e(t['ria_cap'])}</figcaption>
</figure>

<section class="contact" id="contact">
  <h2 class="sh rv">{e(t['h_contact'])}</h2>
  <div class="crow r1 rv"><span>{e(cr[0])}</span><picture><source type="image/webp" srcset="{A('img/josu-2026-12-256.webp')}"><img class="face" src="{A('img/josu-2026-12.jpg')}" width="600" height="600" alt="{e(t['photo_alt'])}" loading="lazy" decoding="async"></picture></div>
  <a class="crow r2 rv" href="mailto:{EMAIL}"><span>{EMAIL}</span></a>
  <a class="crow r1 rv" href="{LINKEDIN}" rel="me noopener"><span>{e(cr[2])}</span></a>
  <a class="crow r2 rv" href="{GITHUB}" rel="me noopener"><span>{e(cr[3])}</span></a>
  <a class="crow r1 rv" href="{A(CVS[lang])}"><span>{e(cr[4])}</span></a>
  <a class="crow greet rv" href="{mailto}"><span>{e(t['hello_big'])}</span><i class="go" aria-hidden="true"><svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"/></svg></i></a>
</section>
</main>

<footer class="foot">
  <div class="cols">
    <ul><li class="f1">{e(t['f_pages'])}</li><li><a href="#about">{e(t['h_about'])}</a></li><li><a href="#work">{e(t['h_work'])}</a></li><li><a href="#background">{e(t['h_bg'])}</a></li><li><a href="#contact">{e(t['h_contact'])}</a></li></ul>
    <ul><li class="f1">{e(t['f_elsewhere'])}</li><li><a href="{GITHUB}" rel="me noopener">GitHub</a></li><li><a href="{LINKEDIN}" rel="me noopener">LinkedIn</a></li><li><a href="mailto:{EMAIL}">Email</a></li></ul>
    <ul><li class="f1">{e(t['f_lang'])}</li>{foot_langs}</ul>
    <ul><li class="f1">Bizkaia</li><li>{e(t['credits'])}</li></ul>
  </div>
  <div class="word-wrap">
    <svg class="word" viewBox="0 0 1000 230" role="img" aria-label="Josu Bayer"><text x="0" y="175" font-size="236">josu bayer</text></svg>
    <p class="legal">{e(t['legal'])}</p>
  </div>
</footer>

<script src="{A('site.js')}" defer></script>
</body>
</html>
"""


os.makedirs(os.path.join(OUT, "eu"), exist_ok=True)
os.makedirs(os.path.join(OUT, "es"), exist_ok=True)
for lang, path in (("en", "index.html"), ("eu", "eu/index.html"), ("es", "es/index.html")):
    with open(os.path.join(OUT, path), "w", encoding="utf8") as f:
        f.write(page(lang))
# robots.txt eta sitemap.xml
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
urls = []
for code, _, path in LANGS:
    links = "".join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{SITE}{p}"/>' for c, _, p in LANGS)
    urls.append(f'<url><loc>{SITE}{path}</loc>{links}<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}"/></url>')
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
print("built")
