# -*- coding: utf-8 -*-
r"""Design system for studiolab.co.il — lifted from the live Base44 site.

Measured off the running site rather than invented, because the first rebuild
looked like an audit report (bordered boxes, teal, tight spacing, no hero) and
the owner rightly said it did not look like his site.

What the original actually does:

  hero        linear-gradient(to bottom right, #0F172A, #1E3A8A, #1E293B)
              h1 60px / 800 / white / centred, 128px vertical padding
  page        white, with alternating #F8FAFC sections at 80px padding
  headings    h2 36px / 700 / #0F172A / CENTRED     h3 20px / 700
  text        #334155 body, #64748B muted, #0F172A ink
  primary CTA #F59E0B background with #0F172A text, weight 700, radius 6-12px
  icon tiles  80x80, radius 16px, three gradients:
                #EF4444->#DB2777   #F59E0B->#EA580C   #2563EB->#4338CA
  cards       white, radius 12px, hairline #E5E5E5 border
  container   ~1265px (max-w-7xl)

Only deliberate departure: the original uses the Tailwind system-font stack,
which renders Hebrew poorly on Windows and Android. Heebo carries the 800-weight
headings the design calls for, with Assistant for body copy.
"""

CSS = r"""
:root{
  --navy-900:#0F172A; --navy-800:#1E293B; --blue-900:#1E3A8A;
  --page:#FFFFFF; --alt:#F8FAFC;
  --ink:#0F172A; --body:#334155; --muted:#64748B; --line:#E5E7EB;
  --amber:#F59E0B; --amber-400:#FBBF24; --amber-600:#D97706;
  --blue:#2563EB; --green:#16A34A;
  --card:#FFFFFF; --card-line:#E5E5E5;
  --wa:#0F7A3D; --wa-fg:#FFFFFF;
  --shadow:0 1px 3px rgba(15,23,42,.06), 0 8px 24px -12px rgba(15,23,42,.12);
}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
  --page:#0B1017; --alt:#111823;
  --ink:#F1F5F9; --body:#CBD5E1; --muted:#94A3B8; --line:#1E293B;
  --card:#141C26; --card-line:#22303F;
  --wa:#25D366; --wa-fg:#0B1017;
  --shadow:0 1px 3px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
}}
:root[data-theme=dark]{
  --page:#0B1017; --alt:#111823;
  --ink:#F1F5F9; --body:#CBD5E1; --muted:#94A3B8; --line:#1E293B;
  --card:#141C26; --card-line:#22303F;
  --wa:#25D366; --wa-fg:#0B1017;
  --shadow:0 1px 3px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
}

*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--page);color:var(--body);
  font-family:'Assistant',system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:17px;line-height:1.75;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:'Heebo',system-ui,sans-serif;color:var(--ink);
  margin:0;text-wrap:balance;letter-spacing:-.015em}
p{margin:0 0 16px}
strong{color:var(--ink);font-weight:600}
a{color:var(--amber-600)}
img{max-width:100%;height:auto;display:block}
.mono,td.f{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums}

/* ---------- nav ---------- */
.nav{position:sticky;top:0;z-index:50;background:var(--navy-900);color:#fff}
.nav-in{max-width:1200px;margin:0 auto;padding:0 20px;display:flex;
  align-items:center;gap:20px;min-height:60px}
.nav-brand{display:flex;align-items:center;gap:9px;text-decoration:none;color:#fff;
  font-family:'Heebo',sans-serif;font-weight:800;font-size:18px;flex:0 0 auto}
.nav-brand img{height:26px;width:auto}
.nav-links{display:flex;gap:19px;flex:1 1 auto;overflow-x:auto;scrollbar-width:none}
.nav-links::-webkit-scrollbar{display:none}
.nav-links a{color:#CBD5E1;text-decoration:none;font-size:15px;white-space:nowrap}
.nav-links a:hover,.nav-links a[aria-current=page]{color:var(--amber-400)}
.nav-cta{flex:0 0 auto;background:var(--amber);color:var(--navy-900);
  text-decoration:none;padding:8px 16px;border-radius:6px;font-weight:700;font-size:14px}

/* ---------- sections ---------- */
section{padding:80px 0}
section.alt{background:var(--alt)}
.in{max-width:1200px;margin:0 auto;padding:0 20px}
.in.narrow{max-width:820px}
section h2{font-size:clamp(28px,4vw,36px);font-weight:700;text-align:center;margin:0 0 12px}
section .sub{text-align:center;color:var(--muted);font-size:18px;max-width:60ch;
  margin:0 auto 42px}
h3{font-size:20px;font-weight:700;margin:0 0 8px}

/* ---------- hero ---------- */
.hero{background:linear-gradient(to bottom right,var(--navy-900),var(--blue-900),var(--navy-800));
  color:#fff;padding:108px 0 96px;text-align:center}
.hero h1{font-size:clamp(34px,6.4vw,60px);font-weight:800;color:#fff;line-height:1.12;
  max-width:20ch;margin:0 auto}
.hero .lead{color:#CBD5E1;font-size:clamp(17px,2.2vw,21px);max-width:56ch;
  margin:22px auto 0;line-height:1.6}
.hero .btns{margin-top:38px}
.hero .strip{margin-top:52px;display:flex;flex-wrap:wrap;gap:9px;justify-content:center}
.hero .strip span{border:1px solid rgba(255,255,255,.22);color:#E2E8F0;
  padding:6px 14px;border-radius:999px;font-size:14px;font-family:'IBM Plex Mono',monospace}

/* ---------- buttons ---------- */
.btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-block;text-decoration:none;font-family:'Heebo',sans-serif;
  font-weight:700;border-radius:10px;padding:16px 32px;font-size:17px;transition:.15s}
.btn-primary{background:var(--amber);color:var(--navy-900)}
.btn-primary:hover{background:var(--amber-600)}
.btn-ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.35)}
.btn-ghost:hover{background:rgba(255,255,255,.1)}
.btn-wa{background:var(--wa);color:var(--wa-fg)}
.btn-dark{background:var(--ink);color:var(--page)}

/* ---------- cards ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.grid-4{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.card{background:var(--card);border:1px solid var(--card-line);border-radius:12px;
  padding:30px 26px;box-shadow:var(--shadow)}
.card p{margin:0;color:var(--body);font-size:16px}
.card h3{margin:0 0 8px}
a.card{display:block;text-decoration:none;color:inherit;transition:.15s}
a.card:hover{transform:translateY(-2px);border-color:var(--amber)}
a.card .go{display:block;margin-top:14px;color:var(--amber-600);font-weight:700;font-size:15px}
.tile{width:64px;height:64px;border-radius:16px;margin-bottom:18px;
  display:flex;align-items:center;justify-content:center;font-size:27px}
.t-1{background:linear-gradient(to bottom right,#EF4444,#DB2777)}
.t-2{background:linear-gradient(to bottom right,#F59E0B,#EA580C)}
.t-3{background:linear-gradient(to bottom right,#2563EB,#4338CA)}
.step{text-align:center}
.step .num{width:56px;height:56px;border-radius:999px;margin:0 auto 16px;
  background:linear-gradient(to bottom right,#F59E0B,#EA580C);color:#fff;
  font-family:'Heebo',sans-serif;font-weight:800;font-size:22px;
  display:flex;align-items:center;justify-content:center}

/* ---------- formats ---------- */
.fmt{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.fmt div{background:var(--card);border:1px solid var(--card-line);border-radius:10px;
  padding:16px 14px;text-align:center}
.fmt b{display:block;font-family:'IBM Plex Mono',monospace;font-size:15px;
  color:var(--ink);font-weight:500}
.fmt small{color:var(--muted);font-size:13px}

/* ---------- pricing ---------- */
.price{background:var(--card);border:1px solid var(--card-line);border-radius:12px;
  overflow:hidden;box-shadow:var(--shadow)}
.price h3{padding:18px 24px;margin:0;background:var(--alt);
  border-bottom:1px solid var(--card-line);font-size:17px}
.price table{width:100%;border-collapse:collapse;font-size:16px}
.price td{padding:14px 24px;border-bottom:1px solid var(--line);color:var(--body)}
.price tr:last-child td{border-bottom:0}
.price td.f{text-align:left;color:var(--ink);font-weight:600;white-space:nowrap}
.note{text-align:center;color:var(--muted);font-size:15px;margin-top:18px}

/* ---------- article / service body ---------- */
.wrap{max-width:820px;margin:0 auto;padding:0 20px}
.pg-head{background:var(--alt);border-bottom:1px solid var(--line);
  padding:52px 0 46px;margin-bottom:44px;text-align:center}
.pg-head h1{font-size:clamp(28px,4.8vw,42px);font-weight:800;line-height:1.18}
.pg-head .tagline{color:var(--muted);font-size:18px;margin:14px auto 0;max-width:58ch}
nav.crumb{font-size:14px;color:var(--muted);padding:18px 0 0;max-width:820px;
  margin:0 auto;padding-inline:20px}
nav.crumb a{color:var(--muted);text-decoration:none}
nav.crumb a:hover{color:var(--amber-600)}
.wrap h2{font-size:27px;font-weight:700;text-align:right;margin:46px 0 14px}
.wrap h3{font-size:20px;margin:28px 0 8px}
.wrap ul,.wrap ol{margin:0 0 18px;padding-right:24px}
.wrap li{margin-bottom:9px}

.answer{background:var(--alt);border-right:4px solid var(--amber);border-radius:10px;
  padding:24px 26px;margin:0 0 34px;font-size:18px}
.answer b{color:var(--ink)}
.key{background:#FFFBEB;border-right:4px solid var(--amber);border-radius:10px;
  padding:18px 22px;margin:26px 0}
.key b{color:var(--amber-600)}
.alert{background:#FEF2F2;border-right:4px solid #DC2626;border-radius:10px;
  padding:18px 22px;margin:26px 0}
.alert b{color:#B91C1C}
.rel{background:var(--alt);border-radius:10px;padding:16px 20px;margin:28px 0;font-size:16px}
.rel a{font-weight:700}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .key{background:#2A2110}
  :root:not([data-theme=light]) .alert{background:#2A1414}}
:root[data-theme=dark] .key{background:#2A2110}
:root[data-theme=dark] .alert{background:#2A1414}

.tw{overflow-x:auto;border:1px solid var(--card-line);border-radius:12px;
  background:var(--card);margin:22px 0}
.tw table{border-collapse:collapse;width:100%;font-size:16px;min-width:460px}
.tw th{background:var(--alt);text-align:right;padding:13px 18px;font-size:14px;
  font-weight:700;color:var(--ink);border-bottom:1px solid var(--card-line);white-space:nowrap}
.tw td{padding:13px 18px;border-bottom:1px solid var(--line);vertical-align:top}
.tw tr:last-child td{border-bottom:0}
.tw td.f{color:var(--ink);font-weight:600;white-space:nowrap}

.faq-item{background:var(--card);border:1px solid var(--card-line);border-radius:10px;
  padding:20px 24px;margin-bottom:12px}
.faq-item h3{margin:0 0 6px;font-size:18px}
.faq-item p{margin:0;font-size:16px}

/* ---------- quote composer ---------- */
.quote{background:var(--card);border:1px solid var(--card-line);border-radius:14px;
  padding:34px;box-shadow:var(--shadow);max-width:720px;margin:0 auto}
.q-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:16px;margin-bottom:16px}
.q-f label{display:block;font-size:14px;color:var(--muted);margin-bottom:6px;font-weight:600}
.q-f input,.q-f select,.quote textarea{width:100%;padding:12px 14px;font-size:16px;
  font-family:inherit;background:var(--page);color:var(--ink);
  border:1px solid var(--card-line);border-radius:8px}
.quote textarea{min-height:84px;resize:vertical;margin-bottom:20px}
.q-f input:focus,.q-f select:focus,.quote textarea:focus{
  outline:2px solid var(--amber);outline-offset:1px;border-color:var(--amber)}

/* ---------- cta band ---------- */
.band{background:linear-gradient(to bottom right,var(--navy-900),var(--blue-900));
  color:#fff;text-align:center}
.band h2{color:#fff}
.band .sub{color:#CBD5E1}
.band .fine{color:#94A3B8;font-size:15px;margin-top:22px}

/* ---------- footer ---------- */
footer.site{background:var(--navy-900);color:#CBD5E1}
.foot-in{max-width:1200px;margin:0 auto;padding:52px 20px 34px;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:30px}
.foot-in h4{font-size:15px;margin:0 0 12px;color:#fff}
.foot-in a{color:#CBD5E1;text-decoration:none;display:block;font-size:15.5px;margin-bottom:7px}
.foot-in a:hover{color:var(--amber-400)}
.foot-in p{font-size:15.5px;margin:0 0 7px;color:#94A3B8}
.foot-b{border-top:1px solid rgba(255,255,255,.1);padding:18px 20px;
  text-align:center;font-size:14px;color:#94A3B8}
.meta{font-size:14px;color:var(--muted);margin-top:38px;padding-top:18px;
  border-top:1px solid var(--line)}

@media(max-width:640px){
  section{padding:56px 0}
  .hero{padding:72px 0 64px}
  .quote{padding:24px}
  .card{padding:24px 20px}
}
"""
