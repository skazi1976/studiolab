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

# ---------------------------------------------------------------- shared CSS
CSS = r"""
:root{
  --bg:#F4F6F8; --surface:#fff; --surface-2:#EDF0F4;
  --ink:#12161C; --ink-2:#39424F; --muted:#68727F;
  --line:#DBE1E9; --line-strong:#C2CBD6;
  --signal:#0B6E78; --signal-soft:#E2F0F1;
  --warn:#9A5B06; --warn-bg:#FCF0E0;
  --alert:#A32B22; --alert-bg:#FBEAE8;
  /* WhatsApp brand green fails contrast with white text (#25D366 = 1.98:1).
     Light theme darkens it so white passes (5.42:1); the dark theme below keeps
     the bright brand green and flips the text dark instead (9.47:1). */
  --wa:#0F7A3D; --wa-fg:#ffffff;
}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
  --bg:#0E1218; --surface:#151B23; --surface-2:#1C242E;
  --ink:#EAEEF3; --ink-2:#BFC8D3; --muted:#8A96A4;
  --line:#26303C; --line-strong:#36434F;
  --signal:#48C7D2; --signal-soft:#123034;
  --warn:#E0A552; --warn-bg:#2E2416;
  --alert:#F0837A; --alert-bg:#33191A;
  --wa:#25D366; --wa-fg:#0E1218;
}}
:root[data-theme=dark]{
  --bg:#0E1218; --surface:#151B23; --surface-2:#1C242E;
  --ink:#EAEEF3; --ink-2:#BFC8D3; --muted:#8A96A4;
  --line:#26303C; --line-strong:#36434F;
  --signal:#48C7D2; --signal-soft:#123034;
  --warn:#E0A552; --warn-bg:#2E2416;
  --alert:#F0837A; --alert-bg:#33191A;
  --wa:#25D366; --wa-fg:#0E1218;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Assistant',system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:17px;line-height:1.8;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:'Rubik',sans-serif;text-wrap:balance;margin:0}
.mono,td.f,.tag{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums}
a{color:var(--signal)}
img{max-width:100%;height:auto}

/* nav */
.nav{position:sticky;top:0;z-index:50;background:var(--surface);
  border-bottom:1px solid var(--line);backdrop-filter:saturate(1.4) blur(6px)}
.nav-in{max-width:1000px;margin:0 auto;padding:0 18px;display:flex;align-items:center;
  gap:18px;min-height:58px}
.nav-brand{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--ink);
  font-family:'Rubik',sans-serif;font-weight:700;font-size:17px;letter-spacing:.01em;flex:0 0 auto}
.nav-brand img{height:26px;width:auto}
.nav-links{display:flex;gap:16px;flex:1 1 auto;overflow-x:auto;scrollbar-width:none}
.nav-links::-webkit-scrollbar{display:none}
.nav-links a{color:var(--ink-2);text-decoration:none;font-size:15px;white-space:nowrap;padding:4px 0}
.nav-links a:hover,.nav-links a[aria-current=page]{color:var(--signal);
  box-shadow:inset 0 -2px 0 var(--signal)}
.nav-cta{flex:0 0 auto;background:var(--wa);color:var(--wa-fg);text-decoration:none;
  padding:8px 15px;border-radius:3px;font-weight:600;font-size:14.5px;white-space:nowrap}
@media(max-width:720px){.nav-cta span{display:none}}

.wrap{max-width:760px;margin:0 auto;padding:0 20px 80px}
.wide{max-width:1000px}
nav.crumb{font-size:13.5px;color:var(--muted);padding:20px 0 0}
nav.crumb a{color:var(--muted);text-decoration:none}
nav.crumb a:hover{color:var(--signal)}

header.pg{border-bottom:1px solid var(--line);padding:24px 0 28px;margin-bottom:30px}
h1{font-size:clamp(27px,4.6vw,38px);font-weight:700;line-height:1.22;letter-spacing:-.02em}
.tagline{color:var(--muted);font-size:17.5px;margin-top:12px}
h2{font-size:24px;font-weight:600;margin:44px 0 14px;letter-spacing:-.01em}
h3{font-size:18.5px;font-weight:600;margin:26px 0 8px}
p{margin:0 0 15px;color:var(--ink-2)}
strong{color:var(--ink);font-weight:600}
ul,ol{margin:0 0 16px;padding-right:22px}
li{margin-bottom:8px;color:var(--ink-2)}

.answer{background:var(--surface);border:1px solid var(--line);
  border-right:3px solid var(--signal);padding:20px 24px;margin:24px 0 32px;
  font-size:17.5px;color:var(--ink-2)}
.answer b{color:var(--ink)}
.key{background:var(--warn-bg);border-right:2px solid var(--warn);padding:15px 19px;margin:22px 0}
.key b{color:var(--warn)}
.alert{background:var(--alert-bg);border-right:2px solid var(--alert);padding:16px 20px;margin:24px 0}
.alert b{color:var(--alert)}
.rel{background:var(--signal-soft);border-right:2px solid var(--signal);
  padding:14px 18px;margin:26px 0;font-size:15.5px}
.rel a{font-weight:600}

.tw{overflow-x:auto;border:1px solid var(--line);background:var(--surface);margin:20px 0}
table{border-collapse:collapse;width:100%;font-size:15px;min-width:480px}
th{background:var(--surface-2);text-align:right;padding:11px 14px;font-size:13px;
  font-weight:600;color:var(--ink);border-bottom:1px solid var(--line-strong);white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--line);color:var(--ink-2);vertical-align:top}
tr:last-child td{border-bottom:0}
td.f{color:var(--ink);white-space:nowrap;font-size:14px}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:22px 0}
.card{background:var(--surface);border:1px solid var(--line);padding:19px 21px}
.card h3{margin:0 0 6px;font-size:17px}
.card p{margin:0;font-size:15.5px}
.card a{text-decoration:none}
a.card{display:block;color:inherit}
a.card:hover{border-color:var(--signal)}
a.card .go{color:var(--signal);font-size:14.5px;font-weight:600;margin-top:9px;display:block}

.fmt{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}
.fmt span{background:var(--surface);border:1px solid var(--line);padding:7px 13px;
  font-family:'IBM Plex Mono',monospace;font-size:14px;color:var(--ink)}

.faq{border-top:1px solid var(--line);padding:17px 0}
.faq h3{margin:0 0 6px;font-size:17.5px}
.faq p{margin:0;font-size:16px}

.cta{background:var(--surface);border:1px solid var(--line-strong);padding:26px;
  margin:42px 0 0;text-align:center}
.cta h2{margin:0 0 8px;font-size:22px}
.cta p{max-width:48ch;margin:0 auto 18px}
.btns{display:flex;gap:11px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-block;padding:13px 28px;text-decoration:none;
  font-family:'Rubik',sans-serif;font-weight:600;font-size:16.5px;border-radius:3px}
.btn-wa{background:var(--wa);color:var(--wa-fg)}
.btn-tel{background:var(--ink);color:var(--bg)}

/* quote composer — static, hands off to WhatsApp */
.quote{background:var(--surface);border:1px solid var(--line-strong);padding:24px;margin:34px 0}
.quote h2{margin:0 0 6px}
.quote .lead{color:var(--muted);font-size:15.5px;margin-bottom:18px}
.q-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:13px;margin-bottom:14px}
.q-f label{display:block;font-size:13.5px;color:var(--muted);margin-bottom:5px}
.q-f input,.q-f select,.quote textarea{width:100%;padding:10px 12px;font-size:16px;
  font-family:inherit;background:var(--bg);color:var(--ink);
  border:1px solid var(--line-strong);border-radius:3px}
.quote textarea{min-height:76px;resize:vertical;margin-bottom:14px}
.q-f input:focus,.q-f select:focus,.quote textarea:focus{outline:2px solid var(--signal);outline-offset:1px}

footer.site{border-top:1px solid var(--line);background:var(--surface);margin-top:60px}
.foot-in{max-width:1000px;margin:0 auto;padding:34px 20px 40px;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:26px}
.foot-in h4{font-size:14px;margin:0 0 10px;color:var(--ink)}
.foot-in a{color:var(--ink-2);text-decoration:none;display:block;font-size:15px;margin-bottom:6px}
.foot-in a:hover{color:var(--signal)}
.foot-in p{font-size:15px;margin:0 0 6px}
.foot-b{border-top:1px solid var(--line);padding:15px 20px;text-align:center;
  font-size:13.5px;color:var(--muted)}
.meta{font-size:13.5px;color:var(--muted);margin-top:32px;padding-top:16px;
  border-top:1px solid var(--line)}
@media(max-width:640px){body{font-size:16.5px}.wrap{padding:0 15px 60px}}
"""

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
            '<a class="nav-brand" href="/"><img src="/assets/logo.png" alt="" width="26" height="26">STUDIOLAB</a>'
            '<div class="nav-links">%s</div>'
            '<a class="nav-cta" href="https://wa.me/%s" rel="noopener">וואטסאפ<span> %s</span></a>'
            '</div></div>' % (links, WA, PHONE_DISPLAY))


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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&family=Assistant:wght@300;400;600&family=IBM+Plex+Mono:wght@500&display=swap">
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


# ============================================================ PAGE: HOMEPAGE
FORMATS = ["VHS", "VHS-C", "Video8", "Hi8", "Digital8", "MiniDV",
           '8 מ"מ', "Super 8", "Betamax", "U-matic", "שקופיות", "נגטיבים"]

HOME_FAQ = [
 ("כמה זמן לוקח תהליך ההמרה?",
  "זמן ההמרה תלוי בכמות המדיה ובאיכות. בדרך כלל, המרת קלטת בודדת לוקחת מספר ימים."),
 ("באיזה פורמט אקבל את הקבצים?",
  "אנחנו מספקים את הקבצים בפורמטים נפוצים כמו MP4 או AVI."),
 ("מה קורה אם הקלטת שלי פגומה?",
  "אנחנו בודקים כל קלטת לפני ההמרה. במקרים של נזק, נעשה כל שביכולתנו לשחזר את התוכן."),
 ("האם אתם שומרים עותק של הסרטים?",
  "לא. כל הקבצים נמחקים מהמערכות שלנו לאחר מסירתם אליכם."),
 ("כמה עולה השירות?",
  "המחיר משתנה לפי סוג המדיה וכמות. צרו קשר לקבלת הצעת מחיר."),
]

QUOTE = """<div class="quote" id="quote">
<h2>קבלו הצעת מחיר</h2>
<p class="lead">ממלאים, לוחצים, וזה נפתח בוואטסאפ עם הפרטים מוכנים. אפשר גם פשוט להתקשר.</p>
<div class="q-row">
  <div class="q-f"><label for="q-name">שם</label><input id="q-name" type="text" autocomplete="name"></div>
  <div class="q-f"><label for="q-type">סוג המדיה</label><select id="q-type">
    <option>VHS / VHS-C</option><option>Video8 / Hi8 / Digital8</option>
    <option>MiniDV</option><option>סרטי 8 מ&quot;מ / Super 8</option>
    <option>שקופיות / נגטיבים</option><option>לא בטוח / מעורב</option></select></div>
  <div class="q-f"><label for="q-qty">כמות (בערך)</label><input id="q-qty" type="text" inputmode="numeric" placeholder="למשל 12"></div>
</div>
<textarea id="q-note" placeholder="משהו שכדאי שנדע? (מצב הקלטות, ריח חומץ, דחיפות…)"></textarea>
<div class="btns">
  <a class="btn btn-wa" id="q-send" href="https://wa.me/%(wa)s" rel="noopener">שליחה בוואטסאפ</a>
  <a class="btn btn-tel" href="tel:%(tel)s">%(disp)s</a>
</div>
</div>
<script>
(function(){
  var b=document.getElementById('q-send');
  function build(){
    var n=(document.getElementById('q-name').value||'').trim(),
        t=document.getElementById('q-type').value,
        q=(document.getElementById('q-qty').value||'').trim(),
        x=(document.getElementById('q-note').value||'').trim();
    // NL via fromCharCode, never a backslash escape: this JS is emitted
    // through a Python format string, which eats the escape and leaves a
    // real newline inside a JS string literal = SyntaxError, composer dead.
    var NL=String.fromCharCode(10);
    var m='היי, אשמח להצעת מחיר להמרה.';
    if(n) m+=NL+'שם: '+n;
    m+=NL+'סוג המדיה: '+t;
    if(q) m+=NL+'כמות: '+q;
    if(x) m+=NL+'הערה: '+x;
    b.href='https://wa.me/%(wa)s?text='+encodeURIComponent(m);
  }
  ['q-name','q-type','q-qty','q-note'].forEach(function(id){
    var e=document.getElementById(id);
    e.addEventListener('input',build); e.addEventListener('change',build);
  });
  build();
})();
</script>""" % dict(wa=WA, tel=PHONE_TEL, disp=PHONE_DISPLAY)

HOME_BODY = """<div class="wrap wide">
<header class="pg">
<h1>המרת קלטות וסרטים ישנים לדיגיטל ברחובות</h1>
<p class="tagline">להציל את הזיכרונות שלכם מהזמן — המרה מקצועית של קלטות וידאו וסרטי פילם לפורמט דיגיטלי.</p>
</header>

<div class="answer">
<b>קלטות וסרטי פילם מתבלים, והמכשירים שמנגנים אותם כבר לא מיוצרים.</b>
אנחנו ממירים את כל הפורמטים הביתיים לקבצים דיגיטליים — בודקים כל פריט לפני,
מטפלים בחומר פגום, ומוסרים קבצים שאפשר לגבות ולשתף. אין צורך לדעת מראש מה יש לכם.
</div>

<div class="fmt">%(fmt)s</div>

<h2>למה להמיר עכשיו?</h2>
<div class="grid">
<div class="card"><h3>שימור לדורות הבאים</h3><p>קלטות וידאו וסרטי פילם מתכלים עם הזמן. המרה דיגיטלית מבטיחה שארכיון המשפחה יישמר.</p></div>
<div class="card"><h3>צפייה ושיתוף מיידיים</h3><p>צפו בסרטים הישנים ישירות מהנייד, ושתפו בקלות עם כל המשפחה.</p></div>
<div class="card"><h3>טיפול מקצועי וציוד מתקדם</h3><p>ציוד המרה ייעודי ובקרת איכות קפדנית להבטחת שימור האיכות המקסימלית.</p></div>
</div>

<h2>השירותים שלנו</h2>
<div class="grid">
<a class="card" href="/vhs-to-digital/"><h3>המרת VHS ו-VHS-C</h3>
<p>הפורמט הביתי הקלאסי. מה באמת אפשר לצפות מהאיכות, ומה עושים עם קלטת מעופשת.</p>
<span class="go">לעמוד המלא ←</span></a>
<a class="card" href="/video8-hi8-digital8/"><h3>Video8, Hi8 ו-Digital8</h3>
<p>שלוש קלטות שנראות זהות אבל אינן. איך מזהים, ולמה לא צריך את המצלמה המקורית.</p>
<span class="go">לעמוד המלא ←</span></a>
<a class="card" href="/8mm-super8/"><h3>סרטי 8 מ&quot;מ ו-Super 8</h3>
<p>סריקה פריים-אחר-פריים ב-2K/4K, ולמה סרטי אצטט מגיעים דווקא עכשיו לסוף חייהם.</p>
<span class="go">לעמוד המלא ←</span></a>
</div>
<p>ממירים גם <strong>MiniDV</strong>, <strong>Betamax</strong> ו-<strong>U-matic</strong>,
וסורקים <strong>שקופיות ונגטיבים</strong> ברזולוציה גבוהה.</p>

<h2>תהליך ההמרה שלנו</h2>
<div class="grid">
<div class="card"><h3>1 · איסוף ובדיקה</h3><p>אתם מגיעים אלינו עם המדיה, אנחנו בודקים ומעריכים את המצב.</p></div>
<div class="card"><h3>2 · המרה מקצועית</h3><p>אנחנו מבצעים המרה זהירה ומדויקת עם ציוד ייעודי.</p></div>
<div class="card"><h3>3 · מסירה דיגיטלית</h3><p>אתם מקבלים את הקבצים על דיסק-און-קי או בענן.</p></div>
</div>

<h2 id="pricing">מחירון שקוף ומפורט</h2>
<div class="tw"><table>
<tr><th>קלטות וידאו</th><th>מחיר לקלטת</th></tr>
<tr><td>VHS / VHS-C</td><td class="f">35–70 ₪</td></tr>
<tr><td>MiniDV / Hi8 / Video8</td><td class="f">35–70 ₪</td></tr>
<tr><td>Digital8</td><td class="f">35–70 ₪</td></tr>
<tr><td>מבצע לכמות גדולה (10+)</td><td class="f">25–50 ₪</td></tr>
</table></div>
<p style="font-size:15px;color:var(--muted)">המחיר לקלטת בודדת, ללא תלות באורך (עד גבול מסוים).</p>

<div class="tw"><table>
<tr><th>סרטי פילם 8 מ&quot;מ</th><th>מחיר</th><th>הערה</th></tr>
<tr><td>גלגל / סליל קטן</td><td class="f">45–69 ₪</td><td>כ-3–4 דקות לגלגל</td></tr>
<tr><td>Frame by Frame</td><td class="f">13–25 ₪ לדקה</td><td>איכות מקסימלית (2K/4K)</td></tr>
<tr><td>לפי אורך (50 רגל)</td><td class="f">60 ₪</td><td>ללא פס קול</td></tr>
</table></div>

<div class="tw"><table>
<tr><th>שירותים נוספים</th><th>מחיר</th></tr>
<tr><td>תיקון קלטות פגומות</td><td class="f">החל מ-60 ₪</td></tr>
<tr><td>דיסק און קי / DVD</td><td class="f">40–70 ₪</td></tr>
<tr><td>תיקון צבע / ניקוי רעשים</td><td class="f">לפי הערכה</td></tr>
</table></div>

<div class="key"><b>כדי לקבל את המחיר המדויק ביותר:</b>
<p style="margin:8px 0 0">ספרו את כמות הקלטות והסלילים · זהו את סוגם (VHS, MiniDV, 8 מ&quot;מ, סופר 8) · צרו קשר.
ואם אתם לא בטוחים מה יש לכם — זה בסדר גמור, הזיהוי הוא חלק מהעבודה.</p></div>

%(quote)s

<h2 id="faq">שאלות נפוצות</h2>
%(faq)s

<div class="rel">רוצים להבין את הנושא לעומק לפני שמתחילים?
<a href="/articles/lifnei-shemamirim-kalatot/">מה כדאי לדעת לפני שממירים קלטות ישנות</a></div>

<div class="cta">
<h2>בואו נתחיל לשמר את הזיכרונות שלכם</h2>
<p>אפשר להביא הכל ביחד — גם קלטות שנראות אבודות, וגם ארגז מעורב שלא מיינתם.</p>
<div class="btns">
<a class="btn btn-wa" href="https://wa.me/%(wa)s" rel="noopener">וואטסאפ</a>
<a class="btn btn-tel" href="tel:%(tel)s">%(disp)s</a>
</div>
<p style="margin-top:16px;font-size:14.5px;color:var(--muted)">
STUDIOLAB — %(addr)s · בתיאום מראש<br>שירות לרחובות, נס ציונה, ראשון לציון והסביבה</p>
</div>
</div>""" % dict(
    fmt="".join("<span>%s</span>" % f for f in FORMATS),
    quote=QUOTE,
    faq="".join('<div class="faq"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in HOME_FAQ),
    wa=WA, tel=PHONE_TEL, disp=PHONE_DISPLAY, addr=ADDR)
