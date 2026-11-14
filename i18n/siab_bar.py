"""Franja común «Software in a Box» encima de la cabecera de cada producto (cognitiv., argos., datos.).

Une los subdominios con www.softwareinabox.eu, como la barra de familia de Google o Atlassian:
  ‹ Software in a Box   Productos: COGNITIV · ARGOS · Espacios de datos   Regulación UE
Todo en el idioma de la página. Además corrige los enlaces a www que apuntan a direcciones antiguas
(logo a la portada en español, avisos legales con la ruta vieja).

Lo llama i18n/build.py: strip_all() antes de construir (para que la franja no entre en las traducciones)
y run() al terminar. También se puede lanzar solo:  python3 i18n/siab_bar.py
"""
import os
import re

WWW = "https://www.softwareinabox.eu"
PRODUCTS = [  # clave, subdominio, idiomas propios
    ("cognitiv", "https://cognitiv.softwareinabox.eu", ["es", "en", "fr", "de", "nl", "pt", "it", "da", "fr-be", "nl-be"]),
    ("argos", "https://argos.softwareinabox.eu", ["es", "en", "fr", "de", "nl", "pt", "it", "da", "fr-be", "nl-be"]),
    ("datos", "https://datos.softwareinabox.eu", ["es", "en", "fr", "de", "nl", "pt", "it", "da", "fr-be", "nl-be"]),
]
FALLBACK = {"da": "en", "fr-be": "fr", "nl-be": "nl"}
# Textos tal y como aparecen en el menú de www (inicio, «Productos», «Regulación UE», «Espacios de datos»)
L = {
    "es": ("/", "Inicio", "Productos", "/regulacion/", "Regulación UE", "Espacios de datos"),
    "en": ("/en/", "Home", "Products", "/en/regulation/", "EU Regulation", "Data spaces"),
    "fr": ("/fr/", "Accueil", "Produits", "/fr/reglementation/", "Réglementation UE", "Espaces de données"),
    "de": ("/de/", "Startseite", "Produkte", "/de/regulierung/", "EU-Regulierung", "Datenräume"),
    "nl": ("/nl/", "Home", "Producten", "/nl/regelgeving/", "EU-regelgeving", "Dataspaces"),
    "pt": ("/pt/", "Início", "Produtos", "/pt/regulamentacao/", "Regulamentação UE", "Espaços de dados"),
    "it": ("/it/", "Home", "Prodotti", "/it/normativa/", "Normativa UE", "Spazi di dati"),
    "da": ("/da/", "Forside", "Produkter", "/da/regulering/", "EU-regulering", "Datarum"),
    "fr-be": ("/fr-be/", "Accueil", "Produits", "/fr-be/reglementation/", "Réglementation UE", "Espaces de données"),
    "nl-be": ("/nl-be/", "Home", "Producten", "/nl-be/regelgeving/", "EU-regelgeving", "Dataspaces"),
}
# Avisos legales: rutas nuevas de www (las antiguas son páginas de redirección)
LEGAL = {
    "/en/aviso-legal.html": "/en/legal-notice.html", "/en/privacidad.html": "/en/privacy.html",
    "/fr/aviso-legal.html": "/fr/mentions-legales.html", "/fr/privacidad.html": "/fr/confidentialite.html",
    "/fr-be/aviso-legal.html": "/fr-be/mentions-legales.html", "/fr-be/privacidad.html": "/fr-be/confidentialite.html",
    "/de/aviso-legal.html": "/de/impressum.html", "/de/privacidad.html": "/de/datenschutz.html",
    "/nl/aviso-legal.html": "/nl/juridische-kennisgeving.html", "/nl/privacidad.html": "/nl/privacy.html",
    "/nl-be/aviso-legal.html": "/nl-be/juridische-kennisgeving.html", "/nl-be/privacidad.html": "/nl-be/privacy.html",
    "/pt/privacidad.html": "/pt/privacidade.html",
    "/it/aviso-legal.html": "/it/note-legali.html", "/it/privacidad.html": "/it/privacy.html",
    "/da/aviso-legal.html": "/da/juridisk-meddelelse.html", "/da/privacidad.html": "/da/privatliv.html",
}
LEGAL_ES = {"/aviso-legal.html", "/privacidad.html", "/cookies.html"}

BEGIN, END = "<!-- SIAB-BAR:BEGIN -->", "<!-- SIAB-BAR:END -->"
CSS = (
    "<style>.siab-bar{background:#071A33;color:#C9D3E0;font:500 13.5px/1 'Hanken Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif;"
    "border-bottom:1px solid rgba(255,255,255,.08);position:relative;z-index:60}"
    ".siab-bar .siab-in{max-width:1240px;margin:0 auto;padding:0 28px;height:38px;display:flex;align-items:center;gap:6px;"
    "overflow-x:auto;scrollbar-width:none;white-space:nowrap}.siab-bar .siab-in::-webkit-scrollbar{display:none}"
    ".siab-bar a{color:#C9D3E0;text-decoration:none;padding:6px 9px;border-radius:6px}"
    ".siab-bar a:hover,.siab-bar a:focus-visible{color:#fff;background:rgba(255,255,255,.08)}"
    ".siab-bar a:focus-visible{outline:2px solid #C9A227;outline-offset:1px}"
    ".siab-bar .siab-home{display:flex;align-items:center;gap:7px;color:#fff;font-weight:700;padding-left:0}"
    ".siab-bar .siab-home svg{flex:none}"
    ".siab-bar .siab-lbl{color:#8FA0B6;margin-left:auto;padding-right:2px}"
    ".siab-bar a[aria-current]{color:#fff;font-weight:700;box-shadow:inset 0 -2px 0 #C9A227;border-radius:0}"
    ".siab-bar .siab-sep{width:1px;height:16px;background:rgba(255,255,255,.18);margin:0 4px}"
    "@media (max-width:760px){.siab-bar .siab-in{padding:0 14px}.siab-bar .siab-lbl,.siab-bar .siab-sep,.siab-bar .siab-reg{display:none}"
    ".siab-bar .siab-home{margin-right:auto}}"
    "@media print{.siab-bar{display:none}}</style>"
)
ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C9A227" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M15 6l-6 6 6 6" stroke="#8FA0B6"/></svg>'
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C9A227" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M3 7l9 5 9-5M12 12v10"/></svg>')


def product_home(base, langs, lang):
    l = lang if lang in langs else FALLBACK.get(lang, "en")
    return base + ("/" if l == "es" else f"/{l}/")


def bar(current, lang):
    home, home_t, prods_t, reg, reg_t, datos_t = L[lang]
    names = {"cognitiv": "COGNITIV", "argos": "ARGOS", "datos": datos_t}
    items = "".join(
        f'<a href="{product_home(b, ls, lang)}"{" aria-current=\"page\"" if k == current else ""}>{names[k]}</a>'
        for k, b, ls in PRODUCTS)
    return (f'{BEGIN}{CSS}<nav class="siab-bar" aria-label="Software in a Box"><div class="siab-in">'
            f'<a class="siab-home" href="{WWW}{home}" aria-label="Software in a Box · {home_t}">{ICON}<span>Software in a Box</span></a>'
            f'<span class="siab-lbl">{prods_t}:</span>{items}<span class="siab-sep"></span>'
            f'<a class="siab-reg" href="{WWW}{reg}">{reg_t}</a></div></nav>{END}')


def strip(s):
    return re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)


def fix_links(s, lang):
    if lang != "es":  # logo y enlaces a la portada de www: a la del idioma de la página
        s = s.replace(f'href="{WWW}/"', f'href="{WWW}{L[lang][0]}"')
    for old, new in LEGAL.items():
        s = s.replace(f'href="{WWW}{old}"', f'href="{WWW}{new}"')
    if lang != "es":  # avisos legales enlazados en español desde una página traducida
        pre = L[lang][0].rstrip("/")
        for p in LEGAL_ES:
            new = LEGAL.get(pre + p, pre + p)
            s = s.replace(f'href="{WWW}{p}"', f'href="{WWW}{new}"')
    fb = FALLBACK.get(lang)
    if fb:  # páginas en danés o belga que enlazaban a la versión inglesa/francesa/neerlandesa de www
        for f in ("", "aviso-legal.html", "privacidad.html", "cookies.html"):
            src = LEGAL.get(f"/{fb}/{f}", f"/{fb}/{f}")
            dst = LEGAL.get(f"/{lang}/{f}", f"/{lang}/{f}")
            s = s.replace(f'href="{WWW}{src}"', f'href="{WWW}{dst}"')
    return s


def current_product(root):
    try:
        host = open(os.path.join(root, "CNAME")).read().strip()
    except OSError:
        return None
    return {"cognitiv": "cognitiv", "argos": "argos", "datos": "datos"}.get(host.split(".")[0])


def pages(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x not in ("i18n", "assets", "node_modules")]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def strip_all(root):
    for p in pages(root):
        s = open(p, encoding="utf-8").read()
        t = strip(s)
        if t != s:
            open(p, "w", encoding="utf-8").write(t)


def run(root):
    cur = current_product(root)
    n = 0
    for p in pages(root):
        s = open(p, encoding="utf-8").read()
        if 'http-equiv="refresh"' in s or "<body" not in s:
            continue
        m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
        lang = (m.group(1) if m else "es").lower()
        lang = lang if lang in L else lang.split("-")[0] if lang.split("-")[0] in L else "es"
        t = fix_links(strip(s), lang)
        b = re.search(r"<body[^>]*>\s*", t)
        k = b.end()
        skip = re.match(r'<a class="skip"[^>]*>.*?</a>\s*', t[k:], flags=re.S)  # tras «Saltar al contenido»
        if skip:
            k += skip.end()
        t = t[:k] + bar(cur, lang) + "\n" + t[k:]
        if t != s:
            open(p, "w", encoding="utf-8").write(t)
            n += 1
    return n


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(run(here), "páginas con la franja Software in a Box")
