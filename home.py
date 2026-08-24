# -*- coding: utf-8 -*-
r"""Homepage markup, rebuilt to the original site's rhythm.

The first attempt rendered every section as a bordered box in one narrow column,
which read as a report rather than a landing page. The original alternates
full-bleed white and #F8FAFC bands at 80px padding, opens on a dark navy hero
with a 60px centred headline, and leads each band with a centred 36px h2.
"""
from build import WA, PHONE_TEL, PHONE_DISPLAY, ADDR

FORMATS = [
    ("VHS", "הפורמט הקלאסי"), ("VHS-C", "קלטת מצלמה"),
    ("Video8", "קלטות מצלמה"), ("Hi8", "אנלוגי משופר"),
    ("Digital8", "דיגיטלי על 8 מ\"מ"), ("MiniDV", "וידאו דיגיטלי"),
    ("8 מ\"מ", "סרטי פילם"), ("Super 8", "סרטי סופר 8"),
    ("Betamax", "פורמט וינטג'"), ("U-matic", "פורמט מקצועי"),
    ("שקופיות", "סריקה ברזולוציה גבוהה"), ("נגטיבים", "סריקה ברזולוציה גבוהה"),
    ("תקליטים", "ויניל 33/45/78"), ("קלטות שמע", "אודיו לדיגיטל"),
]

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

_QUOTE = """<div class="quote" id="quote">
<div class="q-row">
  <div class="q-f"><label for="q-name">שם</label><input id="q-name" type="text" autocomplete="name"></div>
  <div class="q-f"><label for="q-type">סוג המדיה</label><select id="q-type">
    <option>VHS / VHS-C</option><option>Video8 / Hi8 / Digital8</option>
    <option>MiniDV</option><option>סרטי 8 מ&quot;מ / Super 8</option>
    <option>שקופיות / נגטיבים</option><option>לא בטוח / מעורב</option></select></div>
  <div class="q-f"><label for="q-qty">כמות (בערך)</label><input id="q-qty" type="text" inputmode="numeric" placeholder="למשל 12"></div>
</div>
<textarea id="q-note" placeholder="משהו שכדאי שנדע? מצב הקלטות, ריח חומץ, דחיפות…"></textarea>
<div class="btns">
  <a class="btn btn-wa" id="q-send" href="https://wa.me/{wa}" rel="noopener">שליחה בוואטסאפ</a>
  <a class="btn btn-dark" href="tel:{tel}">{disp}</a>
</div>
</div>
<script>
(function(){{
  var b=document.getElementById('q-send');
  // Newline via fromCharCode: this script is emitted through a Python format
  // string, and a backslash escape gets eaten one layer up, leaving a real
  // newline inside a JS string literal — SyntaxError, composer silently dead.
  var NL=String.fromCharCode(10);
  function build(){{
    var n=(document.getElementById('q-name').value||'').trim(),
        t=document.getElementById('q-type').value,
        q=(document.getElementById('q-qty').value||'').trim(),
        x=(document.getElementById('q-note').value||'').trim();
    var m='היי, אשמח להצעת מחיר להמרה.';
    if(n) m+=NL+'שם: '+n;
    m+=NL+'סוג המדיה: '+t;
    if(q) m+=NL+'כמות: '+q;
    if(x) m+=NL+'הערה: '+x;
    b.href='https://wa.me/{wa}?text='+encodeURIComponent(m);
  }}
  ['q-name','q-type','q-qty','q-note'].forEach(function(id){{
    var e=document.getElementById(id);
    e.addEventListener('input',build); e.addEventListener('change',build);
  }});
  build();
}})();
</script>""".format(wa=WA, tel=PHONE_TEL, disp=PHONE_DISPLAY)


BODY = """
<section class="hero">
  <div class="in">
    <h1>המרת קלטות וסרטים ישנים לדיגיטל ברחובות</h1>
    <p class="lead">להציל את הזיכרונות שלכם מהזמן — המרה מקצועית של קלטות וידאו וסרטי פילם לפורמט דיגיטלי.</p>
    <div class="btns">
      <a class="btn btn-primary" href="#quote">קבלו הצעת מחיר</a>
      <a class="btn btn-ghost" href="#pricing">למחירון</a>
    </div>
    <div class="strip">{strip}</div>
  </div>
</section>

<section class="alt">
  <div class="in">
    <h2>למה להמיר עכשיו?</h2>
    <p class="sub">קלטות וסרטי פילם מתכלים, והמכשירים שמנגנים אותם כבר לא מיוצרים.</p>
    <div class="grid">
      <div class="card"><div class="tile t-1">🎞️</div>
        <h3>שימור לדורות הבאים</h3>
        <p>קלטות וידאו וסרטי פילם מתכלים עם הזמן. המרה דיגיטלית מבטיחה שארכיון המשפחה יישמר.</p></div>
      <div class="card"><div class="tile t-2">📱</div>
        <h3>צפייה ושיתוף מיידיים</h3>
        <p>צפו בסרטים הישנים ישירות מהנייד, ושתפו בקלות עם כל המשפחה.</p></div>
      <div class="card"><div class="tile t-3">⚙️</div>
        <h3>טיפול מקצועי וציוד מתקדם</h3>
        <p>ציוד המרה ייעודי ובקרת איכות קפדנית להבטחת שימור האיכות המקסימלית.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="in">
    <h2>השירותים שלנו</h2>
    <p class="sub">לכל פורמט יש סיפור אחר — ולכל אחד יש עמוד שמסביר אותו במלואו.</p>
    <div class="grid">
      <a class="card" href="/vhs-to-digital/">
        <h3>המרת VHS ו-VHS-C</h3>
        <p>הפורמט הביתי הקלאסי. מה באמת אפשר לצפות מהאיכות, ומה עושים עם קלטת מעופשת.</p>
        <span class="go">לעמוד המלא ←</span></a>
      <a class="card" href="/video8-hi8-digital8/">
        <h3>Video8, Hi8 ו-Digital8</h3>
        <p>שלוש קלטות שנראות זהות אבל אינן. איך מזהים, ולמה לא צריך את המצלמה המקורית.</p>
        <span class="go">לעמוד המלא ←</span></a>
      <a class="card" href="/8mm-super8/">
        <h3>סרטי 8 מ&quot;מ ו-Super 8</h3>
        <p>סריקה פריים-אחר-פריים ב-2K/4K, ולמה סרטי אצטט מגיעים דווקא עכשיו לסוף חייהם.</p>
        <span class="go">לעמוד המלא ←</span></a>
      <a class="card" href="/audio-digitization/">
        <h3>תקליטים וקלטות שמע</h3>
        <p>ויניל, קלטות שמע וסלילי הקלטה לדיגיטל — MP3 או WAV, כולל טיפול בחומר ישן ורגיש.</p>
        <span class="go">לעמוד המלא ←</span></a>
    </div>
  </div>
</section>

<section class="alt">
  <div class="in">
    <h2>כל המדיה הישנה שלכם, במקום אחד</h2>
    <p class="sub">לא בטוחים מה יש לכם? זה בסדר גמור — הזיהוי הוא חלק מהעבודה.</p>
    <div class="fmt">{fmt}</div>
  </div>
</section>

<section>
  <div class="in">
    <h2>תהליך ההמרה שלנו</h2>
    <p class="sub">שלושה שלבים, בלי הפתעות.</p>
    <div class="grid">
      <div class="card step"><div class="num">1</div>
        <h3>איסוף ובדיקה</h3>
        <p>אתם מגיעים אלינו עם המדיה, אנחנו בודקים ומעריכים את המצב.</p></div>
      <div class="card step"><div class="num">2</div>
        <h3>המרה מקצועית</h3>
        <p>אנחנו מבצעים המרה זהירה ומדויקת עם ציוד ייעודי.</p></div>
      <div class="card step"><div class="num">3</div>
        <h3>מסירה דיגיטלית</h3>
        <p>אתם מקבלים את הקבצים על דיסק-און-קי או בענן.</p></div>
    </div>
  </div>
</section>

<section class="alt" id="pricing">
  <div class="in">
    <h2>מחירון שקוף ומפורט</h2>
    <p class="sub">המחירים שלנו תחרותיים וכוללים שירות מקצועי מלא.</p>
    <div class="grid">
      <div class="price"><h3>קלטות וידאו</h3><table>
        <tr><td>VHS / VHS-C</td><td class="f">35–70 ₪</td></tr>
        <tr><td>MiniDV / Hi8 / Video8</td><td class="f">35–70 ₪</td></tr>
        <tr><td>Digital8</td><td class="f">35–70 ₪</td></tr>
        <tr><td>לכמות גדולה (10+)</td><td class="f">25–50 ₪</td></tr>
      </table></div>
      <div class="price"><h3>סרטי פילם 8 מ&quot;מ</h3><table>
        <tr><td>גלגל / סליל קטן<br><small style="color:var(--muted)">כ-3–4 דקות</small></td><td class="f">45–69 ₪</td></tr>
        <tr><td>Frame by Frame<br><small style="color:var(--muted)">איכות מקסימלית 2K/4K</small></td><td class="f">13–25 ₪ לדקה</td></tr>
        <tr><td>לפי אורך (50 רגל)<br><small style="color:var(--muted)">ללא פס קול</small></td><td class="f">60 ₪</td></tr>
      </table></div>
      <div class="price"><h3>שירותים נוספים</h3><table>
        <tr><td>תיקון קלטות פגומות</td><td class="f">מ-60 ₪</td></tr>
        <tr><td>דיסק און קי / DVD</td><td class="f">40–70 ₪</td></tr>
        <tr><td>תיקון צבע / ניקוי רעשים</td><td class="f">לפי הערכה</td></tr>
      </table></div>
      <div class="price"><h3>אודיו</h3><table>
        <tr><td>קלטת שמע</td><td class="f">35 ₪</td></tr>
        <tr><td>תקליט ויניל</td><td class="f">לפי הערכה</td></tr>
        <tr><td>סליל הקלטה</td><td class="f">לפי הערכה</td></tr>
      </table></div>
    </div>
    <p class="note">המחיר לקלטת בודדת, ללא תלות באורך (עד גבול מסוים).</p>
  </div>
</section>

<section>
  <div class="in narrow">
    <h2>קבלו הצעת מחיר</h2>
    <p class="sub">ממלאים, לוחצים, וזה נפתח בוואטסאפ עם הפרטים מוכנים. אפשר גם פשוט להתקשר.</p>
    {quote}
  </div>
</section>

<section class="alt" id="faq">
  <div class="in narrow">
    <h2>שאלות נפוצות</h2>
    <p class="sub">ואם לא מצאתם תשובה — פשוט תשאלו בוואטסאפ.</p>
    {faq}
    <div class="rel">רוצים להבין את הנושא לעומק לפני שמתחילים?
      <a href="/articles/lifnei-shemamirim-kalatot/">מה כדאי לדעת לפני שממירים קלטות ישנות</a></div>
  </div>
</section>

<section class="band">
  <div class="in">
    <h2>בואו נתחיל לשמר את הזיכרונות שלכם</h2>
    <p class="sub">אפשר להביא הכל ביחד — גם קלטות שנראות אבודות, וגם ארגז מעורב שלא מיינתם.</p>
    <div class="btns">
      <a class="btn btn-primary" href="https://wa.me/{wa}" rel="noopener">וואטסאפ</a>
      <a class="btn btn-ghost" href="tel:{tel}">{disp}</a>
    </div>
    <p class="fine">STUDIOLAB — {addr} · בתיאום מראש<br>
      שירות לרחובות, נס ציונה, ראשון לציון והסביבה</p>
  </div>
</section>
""".format(
    strip="".join("<span>%s</span>" % f for f, _ in FORMATS),
    fmt="".join("<div><b>%s</b><small>%s</small></div>" % (f, d) for f, d in FORMATS),
    quote=_QUOTE,
    faq="".join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, a)
                for q, a in HOME_FAQ),
    wa=WA, tel=PHONE_TEL, disp=PHONE_DISPLAY, addr=ADDR)
