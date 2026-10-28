"""Renders the four app hero images (real add-on screens + their results on the Northpine gradient).

  python3 tools/compose.py <dir with source crops>

Writes assets/hero/<app>.webp (2400 x 1500). Sources are real screenshots and renders of the add-ons;
only the small notification cards and the Google Form are drawn here in HTML.
"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1]).resolve()
OUT = ROOT / "assets" / "hero"
ICONS = ROOT / "assets" / "apps" / "icons"
CONTOURS = ROOT / "assets" / "brand" / "contours.svg"

CSS = """
*{box-sizing:border-box;margin:0}
html,body{width:1600px;height:1000px;overflow:hidden}
body{font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:#1b2a24;position:relative;
  background:radial-gradient(1100px 700px at var(--gx,82%) var(--gy,8%),var(--glow,rgba(227,179,65,.26)),transparent 62%),
             radial-gradient(900px 700px at 0% 100%,rgba(63,163,128,.32),transparent 60%),
             linear-gradient(140deg,#0c251d 0%,#143a2d 42%,#1d5643 100%)}
.contours{position:absolute;inset:0;width:100%;height:100%;opacity:.16}
.grain{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.035) 1px,transparent 1px);background-size:4px 4px}
.chip{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:14px;color:#fff;font-weight:600;font-size:22px;letter-spacing:-.01em}
.chip img{width:52px;height:52px;border-radius:13px;box-shadow:0 0 0 1px rgba(255,255,255,.18),0 8px 20px rgba(0,0,0,.3)}
.chip span{display:block;font-weight:500;font-size:15px;color:#b9d6c8;letter-spacing:.02em}
.shadow{box-shadow:0 2px 4px rgba(0,0,0,.18),0 30px 70px rgba(4,20,14,.55)}
.panel{position:absolute;border-radius:18px;overflow:hidden;background:#fff}
.panel .bar{height:46px;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:16px;font-weight:500;color:#3c4043;border-bottom:1px solid #e3e7e5;background:#fff}
.panel .bar i{font-style:normal;color:#5f6368;font-size:20px}
.panel img{display:block;width:100%}
.card{position:absolute;background:#fff;border-radius:16px;padding:18px 20px;font-size:15px;line-height:1.4}
.toast{display:flex;gap:14px;align-items:center}
.dot{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;flex:none;font-weight:700;color:#fff;font-size:18px}
.t1{font-weight:600;color:#14251e}.t2{color:#5d6d66;font-size:14px}
.paper{position:absolute;background:#fff;border-radius:6px}
"""


def chip(icon, name, where):
    return f'<div class="chip"><img src="{ICONS / icon}"><div>{name}<span>{where}</span></div></div>'


def panel(img, title, x, y, w, tilt=-2.5, crop_h=None):
    h = f"height:{crop_h}px;" if crop_h else ""
    return (f'<div class="panel shadow" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({tilt}deg)">'
            f'<div class="bar">{title}<i>&times;</i></div><div style="{h}overflow:hidden"><img src="{SRC / img}"></div></div>')


NAMES = [("Priya Raman", "218 Alder Street, Unit 4B", "Portland, OR 97214"), ("Marcus Whitfield", "1905 N Lake Shore Dr", "Chicago, IL 60614"),
         ("Hannah O'Connell", "12 Maple Court", "Burlington, VT 05401"), ("Diego Alvarez", "480 Mission Bay Blvd", "San Francisco, CA 94158"),
         ("Grace Liu", "77 Orchard Lane", "Ithaca, NY 14850"), ("Samuel Okafor", "3301 Elm Avenue", "Dallas, TX 75226"),
         ("Ruth Bergstrom", "9 Harbor View Rd", "Duluth, MN 55802"), ("Tomás Ferreira", "1420 Ocean Pkwy, Apt 2", "Brooklyn, NY 11230"),
         ("Aisha Karim", "56 Willow Bend", "Ann Arbor, MI 48104"), ("Ben Takahashi", "2207 Pine Ridge Dr", "Boulder, CO 80302")]


def label_sheet():
    cells = []
    for i in range(30):
        n, a, c = NAMES[i % len(NAMES)]
        cells.append(f'<div style="display:flex;flex-direction:column;justify-content:center;padding:0 12px;border:1px dashed #d6e0da;border-radius:5px;'
                     f'font-size:10.5px;line-height:1.35;color:#1a1a1a;white-space:nowrap;overflow:hidden"><b style="font-weight:600">{n}</b>{a}<br>{c}</div>')
    grid = ''.join(cells)
    return (f'<div class="paper shadow" style="left:150px;top:190px;width:600px;height:776px;transform:rotate(-5deg);padding:38px 14px 0">'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(10,64px);gap:7px 10px">{grid}</div></div>')


def google_form():
    opt = lambda t, note, full=False: (
        f'<div style="display:flex;align-items:center;gap:14px;padding:11px 0;font-size:17px;color:{"#9aa0a6" if full else "#202124"}">'
        f'<span style="width:20px;height:20px;border-radius:50%;border:2px solid {"#c4c7c5" if full else "#5f6368"};flex:none"></span>{t}'
        f'<span style="margin-left:6px;font-size:15px;font-weight:600;color:{"#b3261e" if full else "#1e7a4f"}">{note}</span></div>')
    return ('<div class="paper shadow" style="left:120px;top:200px;width:700px;border-radius:14px;overflow:hidden;background:#f0ebf8;padding-bottom:22px;transform:rotate(-3deg)">'
            '<div style="height:12px;background:#673ab7"></div>'
            '<div style="background:#fff;margin:16px 22px 0;border-radius:10px;padding:26px 28px;border-top:10px solid #673ab7">'
            '<div style="font-size:32px;color:#202124">Saturday workshop sign-up</div>'
            '<div style="margin-top:10px;font-size:16px;color:#3c4043">Pick one session. Places are limited.</div>'
            '<div style="margin-top:14px;display:inline-block;background:#e6f4ea;color:#1e6b43;font-weight:600;font-size:15px;padding:6px 12px;border-radius:999px">9 places left · Closes Friday 5:00 PM</div></div>'
            '<div style="background:#fff;margin:14px 22px 0;border-radius:10px;padding:24px 28px">'
            '<div style="font-size:18px;color:#202124;margin-bottom:8px">Which session would you like? <span style="color:#d93025">*</span></div>'
            + opt('Sat 9:00 AM, Pottery', 'Full · join the waitlist', True)
            + opt('Sat 11:00 AM, Watercolor', '(3 left)')
            + opt('Sat 2:00 PM, Bookbinding', '(5 left)')
            + '</div></div>')


def toast(x, y, color, mark, t1, t2, tilt=0, w=360):
    return (f'<div class="card shadow toast" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({tilt}deg)">'
            f'<div class="dot" style="background:{color}">{mark}</div><div><div class="t1">{t1}</div><div class="t2">{t2}</div></div></div>')


def scene(app):
    parts = ['<img class="contours" src="%s"><div class="grain"></div>' % CONTOURS]
    if app == "label-maker":
        glow = "rgba(227,179,65,.28)"
        parts += [chip("label-maker.svg", "Spreadsheet Labels", "for Google Sheets"), label_sheet(),
                  panel("c-lm-side.png", "Spreadsheet Labels", 1060, 120, 380, 3, 640),
                  f'<div class="panel shadow" style="left:690px;top:600px;width:330px;transform:rotate(-1.5deg);padding:6px 0"><img src="{SRC / "c-lm-done.png"}"></div>',
                  toast(560, 128, "#1e7a4f", "&#10003;", "2 addresses fixed", "Checked with Google Maps", 2)]
    elif app == "certificate-maker":
        glow = "rgba(233,193,90,.30)"
        parts += [chip("certificate-maker.svg", "Certificate Maker", "for Google Sheets"),
                  f'<div class="paper shadow" style="left:150px;top:230px;width:760px;transform:rotate(-4deg);padding:0;overflow:hidden"><img style="display:block;width:100%" src="{SRC / "cert-hi.png"}"></div>',
                  panel("c-cm-side.png", "Certificate Maker", 1030, 100, 380, 3, 700),
                  toast(560, 790, "#1e5a45", "PDF", "Fatima Al-Sayed - Certificate.pdf", "Emailed to fatima@northside.edu", -1.5, 430),
                  toast(250, 140, "#b8860b", "48", "48 certificates made", "Saved to Drive, numbered, with QR codes", 1.5, 400)]
    elif app == "form-payments":
        glow = "rgba(80,190,160,.30)"
        parts += [chip("form-payments.svg", "Form Payments", "for Google Forms"),
                  f'<div class="paper shadow" style="left:140px;top:210px;width:640px;border-radius:16px;overflow:hidden;transform:rotate(-3deg)">'
                  f'<div style="padding:18px 24px;border-bottom:1px solid #e3e7e5;font-size:19px;font-weight:600;color:#202124">Payment for Robotics summer camp: $640.00'
                  f'<div style="font-size:14px;font-weight:400;color:#5f6368;margin-top:4px">Robotics summer camp 2026 &lt;coach@robotics.club&gt;</div></div>'
                  f'<img style="display:block;width:100%" src="{SRC / "c-fp-email.png"}"></div>',
                  panel("c-fp-side.png", "Form Payments", 1040, 110, 380, 3, 680),
                  toast(600, 760, "#1e7a4f", "&#10003;", "Maya Okafor paid $640.00", "By card, through your own Stripe", -1.5, 400),
                  toast(560, 120, "#635bff", "S", "Stripe and PayPal connected", "Money goes straight to you", 2, 380)]
    else:
        glow = "rgba(170,210,150,.26)"
        parts += [chip("form-limits.svg", "Form Limits", "for Google Forms"), google_form(),
                  panel("c-fl-side.png", "Form Limits", 1040, 100, 380, 3, 720),
                  toast(640, 760, "#b3261e", "!", "Pottery is full", "Jordan joined the waitlist, place 1", -2, 380),
                  toast(520, 110, "#1e5a45", "&#10003;", "Form closes itself", "Friday at 5:00 PM, or when all places fill", 2, 400)]
    return f'<!doctype html><meta charset=utf-8><style>{CSS}</style><body style="--glow:{glow}">' + "".join(parts) + "</body>"


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1.5)
        errors = []
        pg.on("requestfailed", lambda r: errors.append(r.url))
        for app in ["label-maker", "certificate-maker", "form-payments", "form-limits"]:
            tmp = SRC / f"scene-{app}.html"
            tmp.write_text(scene(app))
            await pg.goto("file://" + str(tmp))
            await pg.wait_for_timeout(500)
            png = SRC / f"hero-{app}.png"
            await pg.screenshot(path=str(png))
            from PIL import Image
            Image.open(png).convert("RGB").save(OUT / f"{app}.webp", "WEBP", quality=86, method=6)
            print(app, (OUT / f"{app}.webp").stat().st_size // 1024, "KB")
        await b.close()
        if errors:
            print("MISSING:", errors)


asyncio.run(main())
