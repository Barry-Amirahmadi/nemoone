# Builds index.html for the vitrine (link-in-bio) page. Run: python -I src/build.py
# No external requests: one self-hosted font, local WebP thumbnails, no scripts from CDNs.
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://barry-amirahmadi.github.io/"

# Contact: fill one or both before publishing. Empty values hide the button.
CONTACT = {
    "telegram": "",   # handle without @, e.g. "bardia_web"
    "whatsapp": "",   # international digits only, e.g. "98912xxxxxxx"
}
PAGE_NAME = "طراحی سایت فارسی"

# kind: "template" = ready template, customised with the client's brand
#       "sample"   = a custom design direction, shown as a sample of work
SITES = [
    ("diseh",      "diseh",      "دیسه",    "کلینیک پوست، دندان و مو",   "حرکت طراحی‌شده",   "sample"),
    ("nabat",      "Nabat",      "نبات",    "شیرینی و قند",              "نقش‌مایهٔ ایرانی", "sample"),
    ("varagh",     "varagh",     "ورق",     "استودیوی طراحی گرافیک",     "بروتالیست",       "sample"),
    ("sanjeh",     "sanjeh",     "سنجه",    "قطعات صنعتی و ابزار دقیق",  "شبکهٔ سوئیسی",     "sample"),
    ("taraz",      "taraz",      "تراز",    "نرم‌افزار مالی",            "کارت‌های بنتو",    "sample"),
    ("shabaneh",   "shabaneh",   "شبانه",   "رستوران",                   "سینمایی تیره",     "sample"),
    ("shamim",     "shamim",     "شمیم",    "عطر · معرفی یک محصول",      "تک‌صفحه‌ای اسکرولی", "sample"),
    ("dadavar",    "dadavar",    "دادآور",  "دفتر حقوقی",                "نوشتاری و رسمی",   "sample"),
    ("zarnegar",   "zarnegar",   "زرنگار",  "طلا و جواهر",               "ادیتوریال",        "template"),
    ("parnian",    "cosmetics",  "پرنیان",  "محصولات مراقبت پوست",       "ادیتوریال",        "template"),
    ("avineh",     "avineh",     "آوینه",   "مزون لباس عروس و مجلسی",    "ادیتوریال",        "template"),
    ("karaneh",    "karaneh",    "کرانه",   "معماری داخلی",              "ادیتوریال",        "template"),
    ("naarvan",    "naarvan",    "نارون",   "مبلمان چوبی",               "ادیتوریال",        "template"),
    ("naghshineh", "naghshineh", "نقشینه",  "فرش دستباف",                "ادیتوریال",        "template"),
]
KIND = {"template": "قالب آماده", "sample": "نمونه‌کار اختصاصی"}

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
e = html.escape


def card(i, s):
    key, repo, name, trade, lang, kind = s
    return f"""      <li class="card">
        <a href="{BASE}{repo}/" rel="noopener">
          <img src="media/{key}.webp" width="480" height="640" alt="صفحهٔ اول سایت {e(name)}" loading="{'eager' if i < 2 else 'lazy'}" decoding="async">
          <span class="chip chip--{kind}">{KIND[kind]}</span>
          <span class="meta">
            <strong>{e(name)}</strong>
            <span>{e(trade)}</span>
            <small>سبک: {e(lang)}</small>
          </span>
        </a>
      </li>"""


def contact_buttons():
    out = []
    if CONTACT["telegram"]:
        out.append(f'<a class="btn" href="https://t.me/{e(CONTACT["telegram"])}">پیام در تلگرام</a>')
    if CONTACT["whatsapp"]:
        out.append(f'<a class="btn btn--alt" href="https://wa.me/{e(CONTACT["whatsapp"])}">پیام در واتساپ</a>')
    if not out:
        out.append('<a class="btn" href="#contact" data-placeholder>راه ارتباطی به‌زودی</a>')
    return "\n        ".join(out)


n = str(len(SITES)).translate(FA)
cards = "\n".join(card(i, s) for i, s in enumerate(SITES))
page = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(PAGE_NAME)} · نمونه‌کارها</title>
<meta name="description" content="{n} سایت فارسی نمونه در پنج سبک طراحی؛ قالب آماده با برند شما یا طراحی اختصاصی از صفر.">
<meta name="theme-color" content="#f4f1ea">
<link rel="preload" href="fonts/Vazirmatn.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face {{ font-family: "Vazirmatn"; src: url("fonts/Vazirmatn.woff2") format("woff2"); font-weight: 100 900; font-display: swap; }}
:root {{ --ground: #f4f1ea; --ink: #16140f; --muted: #5b564b; --line: #d9d3c4; --accent: #b4441c; --card: #fffdf8; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ font-family: "Vazirmatn", Tahoma, sans-serif; background: var(--ground); color: var(--ink); line-height: 1.8; padding: 0 16px 112px; }}
main {{ max-width: 720px; margin: 0 auto; }}
header {{ padding: 40px 0 24px; }}
.kicker {{ color: var(--accent); font-weight: 700; font-size: 14px; }}
h1 {{ font-size: clamp(28px, 8vw, 44px); font-weight: 900; line-height: 1.35; margin: 6px 0 12px; }}
.lead {{ color: var(--muted); font-size: 16px; max-width: 34em; }}
.offer {{ display: grid; gap: 12px; grid-template-columns: 1fr 1fr; margin: 24px 0 8px; }}
.offer div {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px; }}
.offer b {{ display: block; font-size: 16px; font-weight: 800; }}
.offer span {{ color: var(--muted); font-size: 14px; line-height: 1.7; }}
h2 {{ font-size: 18px; font-weight: 800; margin: 28px 0 12px; }}
.grid {{ list-style: none; display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
@media (min-width: 640px) {{ .grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }} }}
.card a {{ position: relative; display: block; background: var(--card); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; color: inherit; text-decoration: none; }}
.card a:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
.card img {{ display: block; width: 100%; height: auto; aspect-ratio: 3 / 4; object-fit: cover; object-position: top; background: var(--line); }}
.chip {{ position: absolute; top: 8px; right: 8px; font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 999px; background: var(--ink); color: #fff; }}
.chip--template {{ background: #fff; color: var(--ink); border: 1px solid var(--ink); }}
.meta {{ display: block; padding: 10px 12px 12px; }}
.meta strong {{ display: block; font-size: 17px; font-weight: 800; }}
.meta span, .meta small {{ display: block; font-size: 13px; color: var(--muted); line-height: 1.6; }}
.note {{ color: var(--muted); font-size: 13px; margin-top: 20px; }}
.cta {{ position: fixed; inset: auto 0 0 0; padding: 12px 16px calc(12px + env(safe-area-inset-bottom)); background: linear-gradient(transparent, var(--ground) 30%); display: flex; gap: 10px; justify-content: center; }}
.btn {{ flex: 1; max-width: 340px; text-align: center; font-weight: 800; font-size: 16px; padding: 14px 18px; border-radius: 999px; background: var(--ink); color: #fff; text-decoration: none; }}
.btn--alt {{ background: var(--accent); }}
.btn:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 3px; }}
</style>
</head>
<body>
<main>
  <header>
    <p class="kicker">{e(PAGE_NAME)}</p>
    <h1>{n} سایت فارسی، در پنج سبک طراحی</h1>
    <p class="lead">هر کدام را باز کنید و روی گوشی خودتان ببینید. سایت شما می‌تواند یکی از همین‌ها با برند خودتان باشد، یا از صفر برای کسب‌وکارتان طراحی شود.</p>
    <div class="offer">
      <div><b>قالب آماده</b><span>یکی از قالب‌ها با نام، رنگ، عکس و محتوای شما</span></div>
      <div><b>طراحی اختصاصی</b><span>سایتی از صفر، فقط برای کسب‌وکار شما</span></div>
    </div>
  </header>
  <h2>نمونه‌کارها</h2>
  <ul class="grid">
{cards}
  </ul>
  <p class="note" id="contact">همهٔ برندهای این صفحه ساختگی‌اند و فقط برای نمایش طراحی ساخته شده‌اند.</p>
</main>
<nav class="cta" aria-label="تماس">
        {contact_buttons()}
</nav>
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")
print("wrote", ROOT / "index.html", len(page.encode()), "bytes,", len(SITES), "sites")
