# Builds index.html for the vitrine (link-in-bio) page. Run: python -I src/build.py
# No external requests: one self-hosted font, local WebP thumbnails, no CDN scripts.
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://barry-amirahmadi.github.io/"

# Contact: fill one or both before publishing. Empty values show a placeholder button.
CONTACT = {
    "telegram": "",   # handle without @
    "whatsapp": "",   # international digits only, e.g. "98912xxxxxxx"
}
PAGE_NAME = "ویترین طراحی سایت"

# (key, repo, name, trade, kind, ground, accent)
# kind: "template" = ready template, customised with the client's brand
#       "sample"   = a custom design, shown as a sample of work
FAMILIES = [
    ("آرام و لوکس", "ادیتوریال",
     "برای کالایی که خریدار رویش مکث می‌کند: جواهر، پوست و زیبایی، مزون، مبلمان، فرش، دکوراسیون.",
     [
        ("zarnegar",   "zarnegar",     "زرنگار",  "طلا و جواهر",            "template", "#F2EEE6", "#8A6E3C"),
        ("mehrava",    "jewelry-site", "مهرآوا",  "جواهرات · دوزبانه",       "sample",   "#FAFAF9", "#A06000"),
        ("parnian",    "cosmetics",    "پرنیان",  "محصولات مراقبت پوست",    "template", "#EAE9E3", "#5F8A85"),
        ("avineh",     "avineh",       "آوینه",   "مزون عروس و مجلسی",      "template", "#E2E5E3", "#B08D57"),
        ("karaneh",    "karaneh",      "کرانه",   "معماری داخلی",           "template", "#EFEFED", "#9E5B3E"),
        ("naarvan",    "naarvan",      "نارون",   "مبلمان چوبی",            "template", "#EFEAE1", "#6C825B"),
        ("naghshineh", "naghshineh",   "نقشینه",  "فرش دستباف",             "template", "#EFEAE0", "#8E4A3F"),
     ]),
    ("سینمایی و پرحرکت", "حرکت و تصویر",
     "برای جایی که حس اول همه‌چیز است: کلینیک، رستوران، عطر، معرفی یک محصول تازه.",
     [
        ("diseh",    "diseh",    "دیسه",  "کلینیک پوست، دندان و مو", "sample", "#F6F1EE", "#8A8A8A"),
        ("shabaneh", "shabaneh", "شبانه", "رستوران",                 "sample", "#0C0A08", "#704010"),
        ("shamim",   "shamim",   "شمیم",  "عطر · یک صفحه",           "sample", "#F2F5F4", "#8A8A8A"),
     ]),
    ("جسور و گرافیکی", "بروتالیست و نقش‌مایه",
     "برای برندی که باید دیده شود: استودیوی طراحی، شیرینی و قنادی، پوشاک، رویداد.",
     [
        ("varagh", "varagh", "ورق",  "استودیوی طراحی گرافیک", "sample", "#F2F2F0", "#FF3B00"),
        ("nabat",  "Nabat",  "نبات", "شیرینی و قند",          "sample", "#FFF8EC", "#E0C070"),
     ]),
    ("دقیق و فنی", "سوئیسی، بنتو، نوشتاری",
     "برای خریداری که مشخصات می‌خواهد: صنعت و قطعات، نرم‌افزار، دفتر حقوقی، خدمات تخصصی.",
     [
        ("sanjeh",  "sanjeh",  "سنجه",   "قطعات صنعتی و ابزار دقیق", "sample", "#FFFFFF", "#0047FF"),
        ("taraz",   "taraz",   "تراز",   "نرم‌افزار مالی",           "sample", "#0B0D12", "#20D0A0"),
        ("dadavar", "dadavar", "دادآور", "دفتر حقوقی",              "sample", "#181F26", "#8A8A8A"),
     ]),
]
KIND = {"template": "قالب آماده", "sample": "طراحی اختصاصی"}

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
fa = lambda v: str(v).translate(FA)
e = html.escape
TOTAL = sum(len(f[3]) for f in FAMILIES)


def card(s, eager):
    key, repo, name, trade, kind, ground, accent = s
    return f"""        <li class="site" style="--g:{ground};--a:{accent}">
          <a href="{BASE}{repo}/" rel="noopener" aria-label="{e(name)}، {e(trade)}، باز کردن سایت">
            <span class="chip" style="--g:{ground}">
              <span class="phone"><img src="media/{key}.webp" width="420" height="840" alt="" loading="{'eager' if eager else 'lazy'}" decoding="async"></span>
            </span>
            <span class="label">
              <span class="kind kind--{kind}">{KIND[kind]}</span>
              <strong>{e(name)}</strong>
              <span class="trade">{e(trade)}</span>
            </span>
          </a>
        </li>"""


def family(i, f):
    title, lang, fits, sites = f
    cards = "\n".join(card(s, i == 0 and j < 2) for j, s in enumerate(sites))
    return f"""  <section class="family" id="f{i + 1}" aria-labelledby="f{i + 1}h">
    <header class="fhead">
      <span class="num">{fa(f'{i + 1:02d}')}</span>
      <div>
        <h2 id="f{i + 1}h">{e(title)} <small>{e(lang)} · {fa(len(sites))} سایت</small></h2>
        <p>{e(fits)}</p>
      </div>
    </header>
    <ul class="rail">
{cards}
    </ul>
  </section>"""


def contact_buttons():
    out = []
    if CONTACT["telegram"]:
        out.append(f'<a class="btn" href="https://t.me/{e(CONTACT["telegram"])}">پیام در تلگرام</a>')
    if CONTACT["whatsapp"]:
        out.append(f'<a class="btn btn--alt" href="https://wa.me/{e(CONTACT["whatsapp"])}">پیام در واتساپ</a>')
    if not out:
        out.append('<a class="btn" href="#how" data-placeholder>راه ارتباطی به‌زودی</a>')
    return "\n    ".join(out)


index = "\n".join(
    f'      <li><a href="#f{i + 1}"><span>{fa(f"{i + 1:02d}")}</span>{e(f[0])}<em>{fa(len(f[3]))}</em></a></li>'
    for i, f in enumerate(FAMILIES))
sections = "\n".join(family(i, f) for i, f in enumerate(FAMILIES))

page = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(PAGE_NAME)}</title>
<meta name="description" content="{fa(TOTAL)} سایت فارسی نمونه در چهار حال‌وهوا؛ قالب آماده با برند شما یا طراحی اختصاصی از صفر.">
<meta name="theme-color" content="#12110F">
<link rel="preload" href="fonts/Vazirmatn.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face {{ font-family: "Vazirmatn"; src: url("fonts/Vazirmatn.woff2") format("woff2"); font-weight: 100 900; font-display: swap; }}
:root {{
  --bg: #12110F; --bg2: #1B1A17; --ink: #F3EEE3; --muted: #ABA597; --line: #2E2C27;
  --saffron: #F0A63A; --pad: 16px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{ font-family: "Vazirmatn", Tahoma, sans-serif; background: var(--bg); color: var(--ink); line-height: 1.8; font-feature-settings: "ss01"; padding-bottom: 104px; overflow-x: hidden; }}
a {{ color: inherit; }}
a:focus-visible {{ outline: 3px solid var(--saffron); outline-offset: 3px; border-radius: 6px; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding: 0 var(--pad); }}

/* hero */
.hero {{ padding: 44px 0 28px; position: relative; }}
.kicker {{ display: inline-flex; gap: 8px; align-items: center; font-size: 13px; font-weight: 700; color: var(--saffron); }}
.kicker::before {{ content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--saffron); }}
h1 {{ font-weight: 900; font-size: clamp(40px, 12.5vw, 96px); line-height: 1.12; margin: 14px 0 18px; word-spacing: .02em; }}
h1 .w {{ display: inline-block; opacity: 0; transform: translateY(.35em); animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards; }}
h1 .w:nth-child(2) {{ animation-delay: .08s; }} h1 .w:nth-child(3) {{ animation-delay: .16s; }}
h1 .w:nth-child(4) {{ animation-delay: .24s; }} h1 .w:nth-child(5) {{ animation-delay: .32s; }}
h1 .hl {{ color: var(--saffron); }}
@keyframes rise {{ to {{ opacity: 1; transform: none; }} }}
.lead {{ color: var(--muted); font-size: 17px; max-width: 32em; }}
.index {{ list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 26px; }}
.index a {{ display: flex; align-items: center; gap: 10px; text-decoration: none; padding: 12px 14px; border: 1px solid var(--line); border-radius: 14px; background: var(--bg2); font-weight: 700; font-size: 15px; min-height: 52px; }}
.index a span {{ color: var(--saffron); font-size: 13px; }}
.index a em {{ margin-inline-start: auto; font-style: normal; color: var(--muted); font-size: 13px; font-weight: 500; }}

/* families */
.family {{ padding: 36px 0 8px; border-top: 1px solid var(--line); margin-top: 28px; }}
.fhead {{ display: flex; gap: 14px; align-items: flex-start; }}
.num {{ font-weight: 900; font-size: 44px; line-height: 1; color: transparent; -webkit-text-stroke: 1.2px var(--saffron); }}
h2 {{ font-size: 24px; font-weight: 900; line-height: 1.4; }}
h2 small {{ display: block; font-size: 13px; font-weight: 500; color: var(--muted); }}
.fhead p {{ color: var(--muted); font-size: 15px; margin-top: 6px; max-width: 36em; }}
.rail {{ list-style: none; display: grid; grid-auto-flow: column; grid-auto-columns: 62%; gap: 14px; overflow-x: auto; overscroll-behavior-x: contain; scroll-snap-type: x mandatory; padding: 22px var(--pad) 10px; margin: 0 calc(-1 * var(--pad)); scrollbar-width: none; }}
.rail::-webkit-scrollbar {{ display: none; }}
.site {{ scroll-snap-align: start; }}
.site a {{ display: block; text-decoration: none; }}
.chip {{ display: grid; place-items: center; aspect-ratio: 4 / 5; border-radius: 22px; background: var(--g); padding: 18px 0 0; overflow: hidden; position: relative; }}
.chip::after {{ content: ""; position: absolute; inset: auto 0 0 0; height: 5px; background: var(--a); }}
.phone {{ display: block; width: 72%; align-self: end; border: 6px solid #0B0B0A; border-bottom: 0; border-radius: 26px 26px 0 0; overflow: hidden; background: #0B0B0A; box-shadow: 0 20px 40px -12px rgba(0,0,0,.45); transition: transform .4s cubic-bezier(.2,.7,.2,1); }}
.phone img {{ display: block; width: 100%; height: auto; aspect-ratio: 1 / 2; object-fit: cover; object-position: top; border-radius: 20px 20px 0 0; }}
.site a:hover .phone, .site a:focus-visible .phone {{ transform: translateY(-8px); }}
.label {{ display: block; padding: 12px 4px 0; }}
.label strong {{ display: block; font-size: 19px; font-weight: 800; line-height: 1.5; }}
.trade {{ display: block; color: var(--muted); font-size: 14px; }}
.kind {{ display: inline-block; font-size: 12px; font-weight: 700; padding: 1px 10px; border-radius: 999px; margin-bottom: 4px; }}
.kind--template {{ background: var(--saffron); color: #1A1306; }}
.kind--sample {{ border: 1px solid var(--muted); color: var(--ink); }}
@media (min-width: 720px) {{ .rail {{ grid-auto-columns: 30%; }} }}
@media (min-width: 1040px) {{ .rail {{ grid-auto-flow: row; grid-template-columns: repeat(4, 1fr); overflow: visible; padding-inline: 0; margin: 0; }} }}

/* offer + how */
.offer {{ display: grid; gap: 12px; margin-top: 44px; }}
.tier {{ border-radius: 22px; padding: 22px 20px; background: var(--bg2); border: 1px solid var(--line); }}
.tier--a {{ background: var(--saffron); color: #1A1306; border: 0; }}
.tier b {{ display: block; font-size: 22px; font-weight: 900; }}
.tier p {{ font-size: 15px; margin-top: 4px; }}
.tier--b p {{ color: var(--muted); }}
@media (min-width: 720px) {{ .offer {{ grid-template-columns: 1fr 1fr; }} }}
.how {{ margin-top: 40px; }}
.how h2 {{ margin-bottom: 14px; }}
.steps {{ list-style: none; counter-reset: s; display: grid; gap: 10px; }}
.steps li {{ counter-increment: s; display: flex; gap: 14px; align-items: baseline; font-size: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); }}
.steps li::before {{ content: counter(s, persian); font-weight: 900; color: var(--saffron); font-size: 22px; min-width: 1.2em; }}
.note {{ color: var(--muted); font-size: 13px; margin: 28px 0 8px; }}

/* sticky contact */
.cta {{ position: fixed; inset: auto 0 0 0; z-index: 5; padding: 14px var(--pad) calc(14px + env(safe-area-inset-bottom)); background: linear-gradient(rgba(18,17,15,0), var(--bg) 35%); display: flex; gap: 10px; justify-content: center; }}
.btn {{ flex: 1; max-width: 360px; min-height: 54px; display: grid; place-items: center; font-weight: 800; font-size: 17px; border-radius: 999px; background: var(--ink); color: var(--bg); text-decoration: none; box-shadow: 0 10px 30px -10px rgba(0,0,0,.6); }}
.btn--alt {{ background: var(--saffron); color: #1A1306; }}

@media (prefers-reduced-motion: reduce) {{
  html {{ scroll-behavior: auto; }}
  h1 .w {{ animation: none; opacity: 1; transform: none; }}
  .phone {{ transition: none; }}
}}
</style>
</head>
<body>
<main class="wrap">
  <header class="hero">
    <p class="kicker">{e(PAGE_NAME)}</p>
    <h1><span class="w">{fa(TOTAL)}</span> <span class="w">سایت،</span> <span class="w hl">چهار</span> <span class="w">حال‌وهوا</span></h1>
    <p class="lead">همه فارسی، راست‌به‌چپ و ساخته‌شده برای گوشی. یکی را باز کنید و ببینید سایت کسب‌وکار شما چه شکلی می‌تواند باشد.</p>
    <ul class="index">
{index}
    </ul>
  </header>
{sections}
  <section class="offer" aria-label="دو راه همکاری">
    <div class="tier tier--a"><b>قالب آماده</b><p>یکی از همین سایت‌ها، با نام، رنگ، عکس و محتوای کسب‌وکار شما.</p></div>
    <div class="tier tier--b"><b>طراحی اختصاصی</b><p>سایتی از صفر، با زبان طراحی‌ای که فقط مال برند شماست.</p></div>
  </section>
  <section class="how" id="how" aria-labelledby="howh">
    <h2 id="howh">چطور شروع می‌کنیم</h2>
    <ol class="steps">
      <li>پیام می‌دهید و از کسب‌وکارتان می‌گویید.</li>
      <li>با هم یک قالب انتخاب می‌کنیم، یا طرح اختصاصی را شروع می‌کنیم.</li>
      <li>سایت با محتوای شما ساخته و روی دامنهٔ خودتان تحویل می‌شود.</li>
    </ol>
  </section>
  <p class="note">همهٔ برندهای این صفحه ساختگی‌اند و فقط برای نمایش طراحی ساخته شده‌اند.</p>
</main>
<nav class="cta" aria-label="تماس">
    {contact_buttons()}
</nav>
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("wrote", ROOT / "index.html", len(page.encode()), "bytes,", TOTAL, "sites")
