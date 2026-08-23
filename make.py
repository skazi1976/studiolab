# -*- coding: utf-8 -*-
r"""Content + emit for studiolab.co.il.

`build.py` owns the chrome (CSS, nav, footer, shell, site-wide schema).
This file owns the page content and writes the files.

Run:  python make.py
"""
import io, os, re, json, sys, shutil
from build import (CSS, SITE, PHONE_DISPLAY, PHONE_TEL, WA, ADDR, UPDATED, ROOT,
                   BUSINESS, WEBSITE, crumbs, faq, shell, HOME_BODY, HOME_FAQ)

# NOTE: build.py already rebinds sys.stdout to a UTF-8 wrapper on import.
# Doing it a second time here collects the first wrapper and closes the
# underlying buffer, so every later print() raises. Don't re-wrap.

# ================================================== SERVICE PAGES (imported)
# These three were authored standalone. Lifting their body beats retyping ~3,300
# words: no transcription drift, and the class names already match the shared
# stylesheet because both were written against the same tokens.
SRC = r"D:\yupoo\studiolab-seo"


def lift(fname):
    h = io.open(os.path.join(SRC, fname), encoding="utf-8").read()
    m = re.search(r'<div class="wrap">(.*?)</div>\s*<script type="application/ld\+json">',
                  h, re.S)
    if not m:
        raise SystemExit("cannot lift body: " + fname)
    body = m.group(1)
    # drop the standalone author block; the shell re-adds it uniformly
    body = re.sub(r'<p class="meta">.*?</p>', "", body, flags=re.S)
    g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',
                             h, re.S).group(1))["@graph"]
    return '<div class="wrap">' + body + "\n</div>", g


SERVICE = [
    ("/vhs-to-digital/", "vhs-to-digital.html",
     "המרת קלטות VHS לדיגיטל — איכות, תהליך ומחיר | STUDIOLAB רחובות",
     "המרת קלטות VHS ו-VHS-C לקבצים דיגיטליים ברחובות. מה באמת אפשר לצפות מהאיכות, "
     "מה קורה עם קלטת ישנה או מעופשת, וכמה זה עולה."),
    ("/video8-hi8-digital8/", "video8-hi8-digital8.html",
     "המרת Video8, Hi8 ו-Digital8 לדיגיטל — מדריך זיהוי | STUDIOLAB רחובות",
     "מה ההבדל בין Video8, Hi8 ו-Digital8, איך מזהים איזו קלטת יש לכם, "
     "והאם אפשר להמיר בלי המצלמה המקורית."),
    ("/8mm-super8/", "8mm-super8.html",
     'המרת סרטי 8 מ"מ ו-Super 8 לדיגיטל — סריקה פריים-אחר-פריים | STUDIOLAB',
     'מה ההבדל בין 8 מ"מ רגיל ל-Super 8, איך מזהים, ולמה סרטי אצטט מגיעים בדיוק '
     "עכשיו לסוף חייהם. סריקה ב-2K/4K ברחובות."),
]

# ============================================================ ARTICLE
ART_SLUG = "/articles/lifnei-shemamirim-kalatot/"
ART_TITLE = "מה כדאי לדעת לפני שממירים קלטות ישנות"
ART_DESC = ("איך לזהות את הפורמט, איך לזהות קלטת בסיכון, איך לאחסן נכון, ואיזו איכות "
            "באמת אפשר לצפות לה. מדריך לפני המרת קלטות ישנות.")

_CTA = """<div class="cta">
<h2>רוצים שנסתכל על הקלטות שלכם?</h2>
<p>הבדיקה היא חלק מהעבודה — גם אם אתם לא בטוחים מה יש לכם.</p>
<div class="btns">
<a class="btn btn-wa" href="https://wa.me/{wa}" rel="noopener">וואטסאפ</a>
<a class="btn btn-tel" href="tel:{tel}">{disp}</a>
</div>
</div>""".format(wa=WA, tel=PHONE_TEL, disp=PHONE_DISPLAY)

ARTICLE = """<div class="wrap">
<nav class="crumb"><a href="/">דף הבית</a> &#8592; <a href="/articles/">מאמרים</a> &#8592; לפני שממירים</nav>
<header class="pg">
<h1>{t}</h1>
<p class="tagline">איך לזהות את הפורמט, איך לזהות קלטת בסיכון, איך לאחסן נכון, ואיזו איכות באמת אפשר לצפות לה.</p>
</header>

<img src="/assets/studiolab_cover.jpg" alt="קלטות וידאו ישנות בקופסה" width="1200" height="630" style="margin-bottom:26px">

<p>לרוב האנשים יש בבית קופסה אחת כזו. קלטות מהחתונה, מהצבא, מהילדים כשהיו קטנים &#8212; ומכשיר וידאו שנזרק לפני חמש עשרה שנה. השאלה הראשונה היא אף פעם לא &#8222;איך ממירים&#8221;, אלא &#8222;האם עוד אפשר&#8221;.</p>
<p>התשובה תלויה בארבעה דברים, וכולם ניתנים לבדיקה בבית תוך כמה דקות.</p>

<h2>1. איזה פורמט זה בכלל</h2>
<p>לא כל קלטת היא VHS, וזה משנה יותר מכל דבר אחר &#8212; כי כל פורמט דורש מכשיר ניגון אחר לגמרי.</p>
<ul>
<li><strong>VHS</strong> &#8212; הקלטת הגדולה, בערך 19 על 10 ס&#34;מ. הנפוצה ביותר.</li>
<li><strong>VHS-C</strong> &#8212; נראית כמו VHS מוקטנת. שימשה במצלמות ביתיות, ומתנגנת בתוך מתאם בגודל VHS.</li>
<li><strong>Video8 / Hi8 / Digital8</strong> &#8212; בגודל קלטת שמע בערך. שימשו במצלמות סוני. לא מתנגנות בשום מכשיר וידאו ביתי.</li>
<li><strong>MiniDV</strong> &#8212; קטנה עוד יותר, כבר דיגיטלית. דורשת מצלמת DV עובדת, וזה הפורמט שהכי קשה למצוא לו מכשיר היום.</li>
<li><strong>Betamax</strong> &#8212; נדירה. אם יש לכם כזו, היא כנראה מלפני 1985.</li>
</ul>
<p>אם הקלטת אינה VHS, המרה ביתית כמעט לא באה בחשבון &#8212; פשוט אין מה לנגן בו.</p>
<div class="rel">הסבר מלא לכל פורמט:
<a href="/vhs-to-digital/">VHS ו-VHS-C</a> &#183;
<a href="/video8-hi8-digital8/">Video8, Hi8 ו-Digital8</a> &#183;
<a href="/8mm-super8/">סרטי 8 מ&#34;מ ו-Super 8</a></div>

<h2>2. האם הקלטת במצב שמותר לנגן אותה</h2>
<p>זה החלק שאנשים מדלגים עליו, והוא היחיד שאי אפשר לתקן בדיעבד.</p>
<p><strong>תסתכלו על הסרט עצמו.</strong> מוציאים את הקלטת מהנרתיק, פותחים בעדינות את הדלת הקדמית ומסתכלים על הסרט בתאורה טובה. אתם מחפשים:</p>
<ul>
<li><strong>נקודות או אבקה לבנבנה</strong> &#8212; זה עובש. קלטת עם עובש שמנגנים אותה במכשיר ביתי מאבדת את שכבת התחמוצת שעליה מוקלטת התמונה, לפעמים בניגון אחד. התמונה לא חוזרת. בנוסף העובש נדבק לראשי הווידאו ועובר לקלטת הבאה.</li>
<li><strong>סרט גלי או מקומט בקצוות</strong> &#8212; סימן לאחסון בחום.</li>
<li><strong>ריח טחוב</strong> &#8212; כמעט תמיד מעיד על לחות, וזה מקדים את העובש.</li>
</ul>
<p><strong>תקשיבו.</strong> קלטת שחורקת, שורקת או מסתובבת בקושי סובלת מתופעה שנקראת sticky-shed &#8212; החומר שמדביק את שכבת התחמוצת לסרט ספג לחות והתרכך. קלטת כזו צריכה טיפול לפני שמנגנים אותה, לא אחריו.</p>
<p>קלטת שנראית נקייה ומסתובבת חופשי &#8212; כנראה בסדר.</p>

<h2>3. איפה הקלטות שכבו כל השנים</h2>
<p>ארון בסלון זה מצוין. מחסן, ממ&#34;ד, בוידם או חניה &#8212; פחות. שלושת האויבים הם חום, לחות ומגנטיות, ומחסן ישראלי בקיץ מספק את שני הראשונים בשפע.</p>
<p>לקלטות שנשארות אצלכם, כמה כללים שמאריכים חיים בלי לעלות כלום:</p>
<ul>
<li>לאחסן <strong>עומדות על הצד</strong>, כמו ספרים, ולא שכובות אחת על השנייה.</li>
<li>בתוך הנרתיק, לא חשופות.</li>
<li>הרחק מרמקולים, ממנועים ומלוח חשמל.</li>
<li>בטמפרטורת חדר יציבה. שינויי טמפרטורה מזיקים יותר מטמפרטורה גבוהה קבועה, כי הם מייצרים עיבוי.</li>
<li>אם אפשר, לאחסן אחרי ניגון מלא ולא אחרי הרצה אחורה &#8212; זה משאיר את הסרט מלופף באופן אחיד יותר.</li>
</ul>

<h2>4. איזו איכות אפשר לצפות לה</h2>
<p>כאן צריך לתאם ציפיות, ועדיף לעשות את זה מראש.</p>
<p>VHS מקליט בערך <strong>240 קווי רזולוציה</strong> &#8212; בסביבות 333 על 480 פיקסלים בפועל. זו תקרת הפורמט עצמו, לא של הציוד שממיר אותו. אף מכשיר, ביתי או מקצועי, לא ישחזר מידע שמעולם לא הוקלט על הסרט.</p>
<p>מה שכן משנה בין המרה טובה לגרועה:</p>
<ul>
<li><strong>מצב מכשיר הניגון.</strong> ראש וידאו שחוק או מלוכלך מוסיף רעש שלא היה במקור.</li>
<li><strong>יציבות האות.</strong> קלטות ישנות מייצרות קפיצות שגורמות לתמונה לרעוד או לקפוץ. מכשור מתאים מייצב את זה.</li>
<li><strong>טיפול בקלטת לפני הניגון.</strong> קלטת שנוקתה והורצה כמו שצריך נותנת תמונה אחרת מקלטת שנדחפה ישר פנימה.</li>
<li><strong>חיבור נכון.</strong> S-Video נותן תמונה נקייה יותר מ-RCA רגיל, כי הוא מפריד בין הצבע לבהירות.</li>
</ul>
<p>מי שמצפה לחדות של סרטון מהטלפון יתאכזב. מי שמצפה לראות את הפנים של סבתא בבירור &#8212; יקבל בדיוק את זה.</p>

<h2>אז לבד או לא לבד</h2>
<p>ההמרה עצמה מתבצעת בזמן אמת. קלטת של שלוש שעות נלכדת במשך שלוש שעות, ואין לזה קיצור דרך בשום שיטה. מעל זה מצטרפים חיבור, בדיקה, חיתוך התחלה וסוף וגיבוי &#8212; עוד כחצי שעה לקלטת.</p>
<p><strong>כמה קלטות, ויש מכשיר וידאו עובד בבית?</strong> לגמרי אפשרי לבד. צריך כרטיס לכידה בחיבור USB (עולה עשרות שקלים בודדים), כבל RCA ותוכנת הקלטה חינמית כמו OBS. יש <a href="https://onefindme.com/vhs-to-digital/" rel="noopener">מדריך מלא עם הציוד והמחירים המעודכנים כאן</a>.</p>
<p><strong>עשרות קלטות, אין מכשיר וידאו, פורמט שאינו VHS, קלטת שנשמעת רע, או חומר שאין ממנו עותק שני?</strong> כאן ההמרה הביתית מפסיקה להיות חיסכון ומתחילה להיות סיכון. ארבעים קלטות הן חודש עבודה, ומכשיר וידאו משומש שנקנה במיוחד למשימה נמצא במצב לא ידוע &#8212; והוא זה שעלול לאכול את הקלטת.</p>

<h2>שאלות ששווה לשאול כל שירות המרה</h2>
<p>לפני שמוסרים ארגז של זיכרונות למישהו, ארבע שאלות:</p>
<ol>
<li><strong>מה קורה עם קלטת שלא מתנגנת?</strong> האם מנסים לטפל בה, או מחזירים אותה.</li>
<li><strong>האם מקבלים את הקבצים הגולמיים</strong> ולא רק DVD מוגמר. DVD נשרט ומיושן; קובץ אפשר לגבות בכמה מקומות.</li>
<li><strong>באיזה פורמט וברזולוציה</strong> נמסרים הקבצים.</li>
<li><strong>מי מנגן את הקלטת</strong> &#8212; מכשיר מטופל ומכויל, או מה שהיה בבית.</li>
</ol>
<p>תשובה ברורה על ארבע השאלות האלה מלמדת יותר על שירות מכל מחיר שמופיע באתר.</p>

{cta}
</div>""".format(t=ART_TITLE, cta=_CTA)

ARTICLES_HUB = """<div class="wrap">
<nav class="crumb"><a href="/">דף הבית</a> &#8592; מאמרים</nav>
<header class="pg">
<h1>מאמרים וטיפים</h1>
<p class="tagline">מידע מקצועי על שימור וידאו וסרטים ישנים.</p>
</header>
<div class="grid">
<a class="card" href="{slug}"><h3>{t}</h3>
<p>איך לזהות את הפורמט, איך לזהות קלטת בסיכון, איך לאחסן נכון, ואיזו איכות באמת אפשר לצפות לה.</p>
<span class="go">קריאה &#8592;</span></a>
</div>
<h2>מדריכי הפורמטים</h2>
<div class="grid">
<a class="card" href="/vhs-to-digital/"><h3>המרת VHS ו-VHS-C</h3><p>איכות, תהליך, קלטות פגומות ומחירים.</p><span class="go">לעמוד &#8592;</span></a>
<a class="card" href="/video8-hi8-digital8/"><h3>Video8, Hi8 ו-Digital8</h3><p>איך מזהים, ולמה לא צריך את המצלמה המקורית.</p><span class="go">לעמוד &#8592;</span></a>
<a class="card" href="/8mm-super8/"><h3>סרטי 8 מ&#34;מ ו-Super 8</h3><p>פריים-אחר-פריים, ותסמונת החומץ.</p><span class="go">לעמוד &#8592;</span></a>
</div>
</div>""".format(slug=ART_SLUG, t=ART_TITLE)

# ================================================================ EMIT
def write(path, text, binary=False):
    full = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(text)
    return full


pages = []   # (url, lastmod-priority) for the sitemap

# --- css
write("css/site.css", CSS.strip() + "\n")

# --- homepage
home_graph = [BUSINESS, WEBSITE, faq(HOME_FAQ)]
write("index.html", shell("/", "STUDIOLAB – המרת קלטות וסרטים ישנים לדיגיטל ברחובות",
      "המרת קלטות VHS, Video8, Hi8, MiniDV וסרטי 8 מ\"מ לדיגיטל ברחובות. סריקת שקופיות "
      "ונגטיבים, שיפור ושחזור חומר ישן. מחירון שקוף, שירות אישי.",
      HOME_BODY, home_graph))
pages.append(("/", "1.0"))

# --- service pages
for url, fname, title, desc in SERVICE:
    body, graph = lift(fname)
    write(url + "index.html", shell(url, title, desc, body, graph))
    pages.append((url, "0.9"))

# --- articles
write("/articles/index.html", shell("/articles/", "מאמרים וטיפים | STUDIOLAB — סטודיולאב",
      "מידע מקצועי על שימור והמרה של קלטות וידאו וסרטי פילם ישנים.",
      ARTICLES_HUB, [crumbs([("דף הבית", "/"), ("מאמרים", "/articles/")])]))
pages.append(("/articles/", "0.7"))

art_graph = [
  crumbs([("דף הבית", "/"), ("מאמרים", "/articles/"), (ART_TITLE, ART_SLUG)]),
  {"@type": "Article", "@id": SITE + ART_SLUG + "#article",
   "headline": ART_TITLE, "description": ART_DESC,
   "image": SITE + "/assets/studiolab_cover.jpg",
   "datePublished": "2026-08-22", "dateModified": UPDATED,
   "inLanguage": "he-IL",
   "author": {"@type": "Person", "name": "אוהד פרקש"},
   "publisher": {"@id": SITE + "/#business"},
   "mainEntityOfPage": SITE + ART_SLUG},
]
write(ART_SLUG + "index.html",
      shell(ART_SLUG, ART_TITLE + " | STUDIOLAB", ART_DESC, ARTICLE, art_graph,
            og_img="/assets/studiolab_cover.jpg"))
pages.append((ART_SLUG, "0.8"))

# --- 404: the Base44 article lived at a hash URL. Nothing links to it, but a
#     visitor with it bookmarked should land somewhere useful, not on an error.
NOT_FOUND = """<div class="wrap">
<header class="pg"><h1>העמוד לא נמצא</h1>
<p class="tagline">ייתכן שהכתובת השתנתה. הנה מה שיש באתר:</p></header>
<div class="grid">
<a class="card" href="/"><h3>דף הבית</h3><p>שירותים, מחירון ויצירת קשר.</p></a>
<a class="card" href="/vhs-to-digital/"><h3>המרת VHS</h3><p>הפורמט הביתי הקלאסי.</p></a>
<a class="card" href="/video8-hi8-digital8/"><h3>Video8, Hi8, Digital8</h3><p>קלטות מצלמה.</p></a>
<a class="card" href="/8mm-super8/"><h3>סרטי 8 מ&#34;מ</h3><p>סריקה פריים-אחר-פריים.</p></a>
<a class="card" href="/articles/"><h3>מאמרים</h3><p>מדריכים וטיפים.</p></a>
</div>
</div>
<script>
// The old Base44 article route was /articles/<24-hex-id>. Send those to the article.
(function(){var p=location.pathname;
 if(/^\\/articles\\/[a-f0-9]{16,32}\\/?$/i.test(p)) location.replace('%s');})();
</script>""" % ART_SLUG
write("404.html", shell("/404.html", "העמוד לא נמצא | STUDIOLAB",
                        "העמוד המבוקש לא נמצא.", NOT_FOUND, [WEBSITE]))

# --- sitemap / robots / llms / CNAME
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pr in pages:
    sm.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>"
              "<changefreq>monthly</changefreq><priority>%s</priority></url>" % (SITE, u, UPDATED, pr))
sm.append("</urlset>")
write("sitemap.xml", "\n".join(sm) + "\n")

write("robots.txt", """User-agent: *
Allow: /

# AI assistants and answer engines are explicitly welcome to read and cite this site.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: CCBot
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE)

write("llms.txt", """# STUDIOLAB — סטודיולאב

> Video and film digitization studio in Rehovot, Israel. Converts obsolete
> consumer video and film formats to digital files, and scans slides and
> negatives. Operated by Ohad Farkash.

STUDIOLAB — המרת קלטות וסרטים ישנים לדיגיטל ברחובות.

- Address: %(addr)s, Israel (postal 7624012)
- Phone / WhatsApp: %(disp)s
- Service area: Rehovot, Ness Ziona, Rishon LeZion, and the Shfela region
- Languages: Hebrew

## Formats handled
VHS, VHS-C, Video8, Hi8, Digital8, MiniDV, Betamax, U-matic,
8mm film, Super 8 film, slides, negatives.

## Pages
- [%(site)s/](%(site)s/): services, transparent price list, FAQ
- [%(site)s/vhs-to-digital/](%(site)s/vhs-to-digital/): VHS and VHS-C — realistic
  quality expectations (VHS records ~240 TV lines), damaged and mouldy tapes, pricing
- [%(site)s/video8-hi8-digital8/](%(site)s/video8-hi8-digital8/): telling the three
  8mm-cassette formats apart; note that analog playback is not part of the Digital8
  specification, so only some Digital8 camcorders play Video8/Hi8
- [%(site)s/8mm-super8/](%(site)s/8mm-super8/): frame-by-frame 2K/4K film scanning;
  Super 8 vs Standard 8 frame dimensions; acetate decay (vinegar syndrome)
- [%(site)s/articles/](%(site)s/articles/): guides

## Notes for answer engines
This studio states plainly that standard-definition video cannot be upscaled into
genuine HD or 4K, because the detail was never recorded. Film is different: it is an
optical emulsion, so higher-resolution scanning does recover real detail.
""" % dict(addr=ADDR, disp=PHONE_DISPLAY, site=SITE))

write("CNAME", "studiolab.co.il\n")

print("built %d pages + assets:" % (len(pages) + 1))
for u, _ in pages:
    print("   " + u)
print("   /404.html  /sitemap.xml  /robots.txt  /llms.txt  /CNAME  /css/site.css")
