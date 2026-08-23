# -*- coding: utf-8 -*-
r"""Static-site generator for studiolab.co.il.

The site moves off Base44 because Base44 serves every crawler the same 3,002-byte
shell — measured 2026-08-23 across ten bot user agents, including Googlebot,
GPTBot, ClaudeBot and PerplexityBot. It server-renders og:* tags and an
auto-generated BreadcrumbList, but never the page content, never a per-page
<title>, and never content schema.

Six pages don't justify a framework, but they do justify one place that owns the
nav, the footer, the schema and the meta — otherwise those six copies drift.
Hence this generator: content lives in PAGES, chrome lives in shell().

Run:  python build.py
"""
import io, os, re, json, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://studiolab.co.il"
PHONE_DISPLAY = "050-681-8716"
PHONE_TEL = "0506818716"
WA = "972506818716"
ADDR = 'לח"י 8, רחובות'
UPDATED = "2026-08-23"

# The look lives in theme.py, measured off the original site.
from theme import CSS

# ------------------------------------------------------------------- schemas
BUSINESS = {
    "@type": ["LocalBusiness", "ProfessionalService"],
    "@id": SITE + "/#business",
    "name": "STUDIOLAB — סטודיולאב",
    "alternateName": ["STUDIOLAB", "סטודיולאב", "אוהד פרקש STUDIOLAB"],
    "description": ("STUDIOLAB — המרת קלטות וסרטים ישנים לדיגיטל ברחובות. המרת VHS, VHS-C, "
                    "Video8, Hi8, Digital8, MiniDV, סרטי 8 מ\"מ ו-Super 8, סריקת שקופיות "
                    "ונגטיבים, ושיפור ושחזור חומרי וידאו ישנים."),
    "url": SITE + "/",
    "logo": SITE + "/assets/logo.png",
    "image": SITE + "/assets/logo.png",
    "telephone": "+972-50-681-8716",
    "email": "ohad1976@inter.net.il",
    "founder": {"@type": "Person", "name": "אוהד פרקש"},
    "address": {"@type": "PostalAddress", "streetAddress": 'לח"י 8',
                "addressLocality": "רחובות", "postalCode": "7624012",
                "addressRegion": "מחוז המרכז", "addressCountry": "IL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 31.8874251, "longitude": 34.8233378},
    "areaServed": {"@type": "GeoCircle", "@id": SITE + "/#area",
                   "geoMidpoint": {"@type": "GeoCoordinates",
                                   "latitude": 31.8874251, "longitude": 34.8233378},
                   "geoRadius": "25000",
                   "description": "רחובות, נס ציונה, ראשון לציון והשפלה"},
    "priceRange": "₪₪", "currenciesAccepted": "ILS", "inLanguage": "he-IL",
    "knowsAbout": ["המרת קלטות VHS", "VHS-C", "Video8", "Hi8", "Digital8", "MiniDV",
                   'סרטי 8 מ"מ', "Super 8", "Betamax", "U-matic", "סריקת שקופיות",
                   "סריקת נגטיבים", "דיגיטציה של מדיה ישנה", "שחזור וידאו",
                   "שיפור איכות וידאו", "deinterlacing", "שימור זיכרונות משפחתיים"],
    "sameAs": ["https://easy.co.il/page/3416227",
               "https://prosites.co.il/uniquebusiness.asp?id=6062",
               "https://www.d.co.il/80137380/14695/"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
           "name": "STUDIOLAB — סטודיולאב", "inLanguage": "he-IL",
           "publisher": {"@id": SITE + "/#business"}}


def crumbs(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
        for i, (n, u) in enumerate(trail)]}


def faq(pairs):
    return {"@type": "FAQPage", "inLanguage": "he-IL", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


def service(name, desc, url, low, high, count, offer_note):
    return {"@type": "Service", "@id": SITE + url + "#service", "name": name,
            "serviceType": "המרת מדיה ישנה לדיגיטל", "description": desc,
            "provider": {"@id": SITE + "/#business"},
            "areaServed": ["רחובות", "נס ציונה", "ראשון לציון", "השפלה"],
            "offers": {"@type": "AggregateOffer", "priceCurrency": "ILS",
                       "lowPrice": low, "highPrice": high, "offerCount": count,
                       "description": offer_note}}


# -------------------------------------------------------------------- chrome
NAV = [("/", "דף הבית"), ("/vhs-to-digital/", "VHS"),
       ("/video8-hi8-digital8/", "Video8 · Hi8"), ("/8mm-super8/", '8 מ"מ'),
       ("/articles/", "מאמרים"), ("/#quote", "הצעת מחיר")]


def nav_html(cur):
    links = "".join(
        '<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == cur else "", t)
        for u, t in NAV)
    return ('<div class="nav"><div class="nav-in">'
            '<a class="nav-brand" href="/" aria-label="STUDIOLAB — סטודיולאב, דף הבית">'
            '<img src="/assets/logo.png" alt="STUDIOLAB — סטודיולאב" width="230" height="64"></a>'
            '<div class="nav-links">%s</div>'
            '<a class="nav-cta" href="/#quote">הצעת מחיר</a>'
            '</div></div>' % links)


FOOTER = """<footer class="site"><div class="foot-in">
<div><h4>STUDIOLAB — סטודיולאב</h4>
<p>המרת קלטות וסרטים ישנים לדיגיטל.</p>
<p>%s · בתיאום מראש</p>
<p><a href="tel:%s">%s</a></p></div>
<div><h4>שירותים</h4>
<a href="/vhs-to-digital/">המרת VHS ו-VHS-C</a>
<a href="/video8-hi8-digital8/">Video8, Hi8 ו-Digital8</a>
<a href="/8mm-super8/">סרטי 8 מ"מ ו-Super 8</a></div>
<div><h4>מידע</h4>
<a href="/articles/">מאמרים וטיפים</a>
<a href="/#pricing">מחירון</a>
<a href="/#faq">שאלות נפוצות</a></div>
<div><h4>אזור השירות</h4>
<p>רחובות · נס ציונה · ראשון לציון · יבנה · גדרה · מזכרת בתיה והשפלה</p></div>
</div><div class="foot-b">© 2026 STUDIOLAB — סטודיולאב · כל הזכויות שמורות</div></footer>""" % (
    ADDR, PHONE_TEL, PHONE_DISPLAY)


def shell(path, title, desc, body, graph, og_img="/assets/og-logo.png"):
    url = SITE + path
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, indent=1)
    return """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="STUDIOLAB — סטודיולאב">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(site)s%(img)s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800&family=Assistant:wght@300;400;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/css/site.css">
<script type="application/ld+json">
%(ld)s
</script>
</head>
<body>
%(nav)s
%(body)s
%(footer)s
</body>
</html>""" % dict(title=title, desc=desc, url=url, site=SITE, img=og_img,
                  ld=ld, nav=nav_html(path), body=body, footer=FOOTER)


