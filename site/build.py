import html, os
from content import ROWS, BACKGROUND, T, GH

OUT = os.path.join(os.path.dirname(__file__), "public")
EMAIL = "bayer.josu@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/josu-bayer-agirre-090678208/"
GITHUB = "https://github.com/josu-bayer"
ARROW = '<span class="ar" aria-hidden="true"> ↗</span>'
CV = "files/CV_Josu_Bayer_Agirre.pdf"


def e(s):
    return html.escape(s, quote=True)


def page(lang):
    t = T[lang]
    up = "../" if lang == "eu" else ""  # path prefix back to the site root
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

    mailto = f"mailto:{EMAIL}?subject={e(t['email_subject']).replace(' ', '%20')}"
    cr = t["contact_rows"]

    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta name="theme-color" content="#0c4a4a">
<link rel="alternate" hreflang="en" href="https://josu-bayer.web.app/">
<link rel="alternate" hreflang="eu" href="https://josu-bayer.web.app/eu/">
<link rel="preload" href="{A('fonts/cabinet-grotesk-800.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{A('site.css')}">
<script>document.documentElement.className="js"</script>
</head>
<body>
<a class="skip" href="#about">{e(t['skip'])}</a>

<header class="top" id="top">
  <h1 class="vh">{e(t['title'])}</h1>
  <div class="bar">
    <a class="mark" href="#top">Josu Bayer</a>
    <div class="bar-r">
      <a class="lang" href="{t['other_href']}" hreflang="{'en' if lang=='eu' else 'eu'}">{e(t['other_lang'])}</a>
      <a class="btn" href="{mailto}">{e(t['hello'])}</a>
    </div>
  </div>
</header>

<main>
<section class="about" id="about">
  <h2 class="sh rv">{e(t['h_about'])}</h2>
  <div class="story rv">
    <p>{t['about'][0]}</p>
  </div>
  <p class="cta rv"><a href="#contact"><mark class="hl1">{e(t['about_cta'])}</mark></a></p>
</section>

<figure class="band" data-drift>
  <img src="{A('img/bridge.jpg')}" width="1800" height="1087" alt="Archival photograph of the Bizkaia transporter bridge, two iron towers carrying a walkway over the estuary, a steamer passing beneath" loading="lazy" decoding="async">
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
    <aside class="peek" aria-live="polite">
      <div class="peek-in">
        <p class="pf">{e(f0[2])}</p>
        <p class="pc">{e(f0[3])}</p>
        <p class="pn">{e(f0[0])}</p>
      </div>
    </aside>
  </div>
</section>

<figure class="band" data-drift>
  <img src="{A('img/butroi.jpg')}" width="1600" height="792" alt="Butroi castle in Gatika, Bizkaia, seen from below, with two round towers and crenellated walls against a blue sky" loading="lazy" decoding="async" data-oy="40">
  <figcaption>{e(t['butroi_cap'])}</figcaption>
</figure>


<section class="bg" id="background">
  <h2 class="sh rv">{e(t['h_bg'])}</h2>
  <div class="table rv">
    {''.join(bg)}
  </div>
</section>



<figure class="band" data-drift>
  <img src="{A('img/gaztelugatxe.jpg')}" width="1800" height="1171" alt="The island of Gaztelugatxe, a rocky headland with a small stone chapel on top, joined to the coast by a winding stairway, under a blue sky" loading="lazy" decoding="async">
  <figcaption>{e(t['ria_cap'])}</figcaption>
</figure>

<section class="contact" id="contact">
  <h2 class="sh rv">{e(t['h_contact'])}</h2>
  <div class="crow r1 rv"><span>{e(cr[0])}</span><img class="face" src="{A('img/josu-2026-11.jpg')}" width="600" height="600" alt="{e(t['photo_alt'])}" loading="lazy" decoding="async"></div>
  <a class="crow r2 rv" href="mailto:{EMAIL}"><span>{EMAIL}</span></a>
  <a class="crow r1 rv" href="{LINKEDIN}" rel="me noopener"><span>{e(cr[2])}</span></a>
  <a class="crow r2 rv" href="{GITHUB}" rel="me noopener"><span>{e(cr[3])}</span></a>
  <a class="crow r1 rv" href="{A(CV)}"><span>{e(cr[4])}</span></a>
  <a class="crow greet rv" href="{mailto}"><span>{e(t['hello_big'])}</span><i class="go" aria-hidden="true"><svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"/></svg></i></a>
</section>
</main>

<footer class="foot">
  <div class="cols">
    <ul><li class="f1">{e(t['f_pages'])}</li><li><a href="#about">{e(t['h_about'])}</a></li><li><a href="#work">{e(t['h_work'])}</a></li><li><a href="#background">{e(t['h_bg'])}</a></li><li><a href="#contact">{e(t['h_contact'])}</a></li></ul>
    <ul><li class="f1">{e(t['f_elsewhere'])}</li><li><a href="{GITHUB}" rel="me noopener">GitHub</a></li><li><a href="{LINKEDIN}" rel="me noopener">LinkedIn</a></li><li><a href="mailto:{EMAIL}">Email</a></li></ul>
    <ul><li class="f1">{e(t['f_lang'])}</li><li><a href="{A('') or './'}" hreflang="en">English</a></li><li><a href="{A('eu/')}" hreflang="eu">Euskara</a></li></ul>
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
for lang, path in (("en", "index.html"), ("eu", "eu/index.html")):
    with open(os.path.join(OUT, path), "w", encoding="utf8") as f:
        f.write(page(lang))
print("built")
