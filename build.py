"""Builds the Northpine Apps website.

  python3 build.py

Writes two folders:
  docs/     the real site for GitHub Pages (full HTML pages, CNAME, assets)
  preview/  the same pages for a claude.ai preview (home page without the document skeleton)
"""
import html
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
CSS = (SRC / "style.css").read_text()
DOMAIN = "northpineapps.com"
EMAIL = "northpineapps@gmail.com"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=Inter:wght@400;500;600&display=swap">')

TREE = ('<svg viewBox="0 0 64 64" aria-hidden="true">'
        '<path d="M50 4 L51.6 9.4 L57 11 L51.6 12.6 L50 18 L48.4 12.6 L43 11 L48.4 9.4 Z" fill="var(--gold)"/>'
        '<path d="M28 6 L38 19 H33.5 L42 31 H36.5 L46 44 H39.5 L49 56 H7 L16.5 44 H10 L19.5 31 H14 L22.5 19 H18 Z" '
        'fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>'
        '<rect x="25.5" y="55" width="5" height="6" rx="1.2" fill="currentColor"/></svg>')

# Example addresses for the picture of a label sheet. All invented.
ADDRESSES = [
    ("Priya Raman", "218 Alder Street, Unit 4B", "Portland, OR 97214"),
    ("Marcus Whitfield", "1905 N Lake Shore Dr", "Chicago, IL 60614"),
    ("Hannah O'Connell", "12 Maple Court", "Burlington, VT 05401"),
    ("Diego Alvarez", "480 Mission Bay Blvd", "San Francisco, CA 94158"),
    ("Grace Liu", "77 Orchard Lane", "Ithaca, NY 14850"),
    ("Samuel Okafor", "3301 Elm Avenue", "Dallas, TX 75226"),
    ("Ruth Bergstrom", "9 Harbor View Rd", "Duluth, MN 55802"),
    ("Tomás Ferreira", "1420 Ocean Pkwy, Apt 2", "Brooklyn, NY 11230"),
    ("Aisha Karim", "56 Willow Bend", "Ann Arbor, MI 48104"),
    ("Ben Takahashi", "2207 Pine Ridge Dr", "Boulder, CO 80302"),
    ("Clara Novak", "814 Chestnut St", "Philadelphia, PA 19107"),
    ("Owen Gallagher", "45 Birch Hollow", "Asheville, NC 28801"),
    ("Mei Chen", "600 Cedar Lane", "Madison, WI 53703"),
    ("Luis Romero", "1018 Desert Sage Way", "Tucson, AZ 85719"),
    ("Fatima Haddad", "33 Spruce Terrace", "Seattle, WA 98103"),
    ("Jonah Weiss", "250 Riverside Dr", "Austin, TX 78704"),
    ("Elena Petrova", "71 Magnolia Ave", "Savannah, GA 31401"),
    ("Kwame Mensah", "1500 Prairie St", "Omaha, NE 68102"),
    ("Sofia Rossi", "8 Lighthouse Way", "Portland, ME 04101"),
    ("Noah Bennett", "402 Aspen Circle", "Salt Lake City, UT 84102"),
    ("Yuki Tanaka", "19 Juniper Row", "Honolulu, HI 96813"),
    ("Amara Diallo", "620 Linden Blvd", "St. Louis, MO 63108"),
    ("Henry Lowell", "5 Cranberry Rd", "Plymouth, MA 02360"),
    ("Isabel Moreno", "2900 Redwood Hwy", "Eureka, CA 95501"),
    ("Arjun Mehta", "140 Laurel St", "Raleigh, NC 27601"),
    ("Nora Fitzgerald", "36 Hemlock Path", "Bend, OR 97701"),
]
USED = 4  # the first labels on the pictured sheet were used for an earlier job


def label_sheet():
    cells = []
    for i in range(30):
        if i < USED:
            cells.append('<div class="lbl used"></div>')
            continue
        name, line1, line2 = ADDRESSES[(i - USED) % len(ADDRESSES)]
        cls = "lbl next" if i == USED else "lbl"
        cells.append(f'<div class="{cls}"><b>{html.escape(name)}</b><span>{html.escape(line1)}</span><span>{html.escape(line2)}</span></div>')
    return "\n".join(cells)


# Avery sheets the add-on shows, from src/Templates.gs in the label-addon repo.
SHEETS = [
    ("5160", "8160, 5260, 18160", "Address", '2-5/8" × 1"', 3, 10),
    ("5161", "8161, 5261", "Address", '4" × 1"', 2, 10),
    ("5162", "8162, 5262", "Address", '4" × 1-1/3"', 2, 7),
    ("5163", "8163, 5263", "Shipping", '4" × 2"', 2, 5),
    ("5164", "8164, 5264", "Large shipping", '4" × 3-1/3"', 2, 3),
    ("5168", "8168", "Large shipping", '3-1/2" × 5"', 2, 2),
    ("5167", "8167, 5267", "Return address", '1-3/4" × 1/2"', 4, 20),
    ("5195", "8195", "Return address", '1-3/4" × 2/3"', 4, 15),
    ("5366", "8366", "File folder", '3-7/16" × 2/3"', 2, 15),
    ("5371", "8371", "Business card", '3-1/2" × 2"', 2, 5),
    ("5395", "8395", "Name badge", '3-3/8" × 2-1/3"', 2, 4),
]
ENVELOPES = [("#10", '9-1/2" × 4-1/8"'), ("#9", '8-7/8" × 3-7/8"'), ("A7", '7-1/4" × 5-1/4"'),
             ("DL", "220 × 110 mm"), ("C5", "229 × 162 mm"), ("C6", "162 × 114 mm")]


def sheets_table():
    rows = []
    for code, also, use, size, cols, nrows in SHEETS:
        cells = "<i></i>" * (cols * nrows)
        mini = (f'<span class="mini" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({nrows},1fr)" '
                f'aria-hidden="true">{cells}</span>')
        rows.append(f'<tr><td class="code">{mini}Avery {code}<span class="also">also {also}</span></td>'
                    f'<td>{use}</td><td>{size}</td><td class="n">{cols * nrows}</td></tr>')
    return "\n".join(rows)


def envelopes():
    return "".join(f"<li>{n} <span>{s}</span></li>" for n, s in ENVELOPES)


def header(active, links, on_hero=False):
    def a(key, label):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{links[key]}"{cur}>{label}</a>'
    cls = "site-head on-hero" if on_hero else "site-head"
    return (f'<header class="{cls}"><div class="wrap">'
            f'<a class="brand" href="{links["home"]}">{TREE}<span class="word">Northpine <span>Apps</span></span></a>'
            f'<nav class="nav" aria-label="Site">{a("apps", "Apps")}{a("pricing", "Pricing")}{a("guides", "Guides")}{a("support", "Support")}{a("privacy", "Privacy")}{a("terms", "Terms")}</nav>'
            f'</div></header>')


def footer(links):
    return (f'<footer class="site-foot"><div class="wrap">'
            f'<div class="foot-row"><span>© 2026 Northpine Apps</span>'
            f'<span class="foot-links"><a href="{links["apps"]}">Apps</a><a href="{links["guides"]}">Guides</a><a href="{links["support"]}">Support</a><a href="{links["privacy"]}">Privacy policy</a><a href="{links["terms"]}">Terms of service</a>'
            f'<a href="mailto:{EMAIL}">{EMAIL}</a></span></div>'
            f'<p>Label Maker is not affiliated with or endorsed by Avery or Google. Avery and Google Sheets are trademarks of their owners; '
            f'product numbers are used only to describe compatible sheets.</p>'
            f'</div></footer>')


GUIDES = sorted((SRC / "guides").glob("*.html"))
APPS = sorted((SRC / "apps").glob("*.html"))


def guide_meta(path):
    meta = path.read_text().partition("\n---\n")[0]
    return dict(line.split(": ", 1) for line in meta.strip().splitlines())


def guides_list(links):
    items = []
    for g in GUIDES:
        if g.stem == "index":
            continue
        m = guide_meta(g)
        items.append(f'<li><a href="{links["guide:" + g.stem]}"><strong>{html.escape(m["heading"])}</strong></a>'
                     f'<span>{html.escape(m["description"])}</span></li>')
    return '<ul class="guide-list">' + "".join(items) + "</ul>"


def apps_list(links):
    items = []
    for a in APPS:
        if a.stem == "index":
            continue
        m = guide_meta(a)
        items.append(f'<li><a href="{links["app:" + a.stem]}"><strong>{html.escape(m["heading"])}</strong></a>'
                     f'<span>{html.escape(m["blurb"])}</span></li>')
    return "".join(items)


def render(name, links):
    body = (SRC / f"{name}.html").read_text()
    body = body.replace("{{APPS_LIST}}", apps_list(links) if "{{APPS_LIST}}" in body else "")
    body = body.replace("{{GUIDES_LIST}}", guides_list(links) if "{{GUIDES_LIST}}" in body else "")
    body = (body.replace("{{SHEET}}", label_sheet())
                .replace("{{SHEETS_TABLE}}", sheets_table())
                .replace("{{ENVELOPES}}", envelopes())
                .replace("{{EMAIL}}", EMAIL))
    for k, v in sorted(links.items(), key=lambda kv: -len(kv[0])):
        body = body.replace("{{" + k + "}}", v)
    meta, _, content = body.partition("\n---\n")
    info = dict(line.split(": ", 1) for line in meta.strip().splitlines())
    head = (f'<title>{info["title"]}</title>\n'
            f'<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{html.escape(info["description"])}">\n'
            f'<link rel="icon" type="image/png" href="{links["assets"]}favicon.png">\n'
            f'{FONTS}\n<style>\n{CSS}</style>\n')
    page = header(info["active"], links, on_hero=info.get("hero") == "yes") + content.replace("{{assets}}", links["assets"]) + footer(links)
    return head, page


def full(head, page, canonical=None):
    can = f'<link rel="canonical" href="{canonical}">\n' if canonical else ""
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{can}{head}</head>\n<body>\n{page}\n</body>\n</html>\n')


def page_list():
    return ["index", "support", "privacy", "terms"] + ["guides/" + g.stem for g in GUIDES] + ["apps/" + a.stem for a in APPS]


def build():
    pages = page_list()
    # Real site: clean URLs on GitHub Pages.
    live = {"home": "/", "pricing": "/#pricing", "guides": "/guides/", "apps": "/apps/", "support": "/support", "privacy": "/privacy", "terms": "/terms", "assets": "/assets/"}
    for g in GUIDES:
        if g.stem != "index":
            live["guide:" + g.stem] = "/guides/" + g.stem
    for a in APPS:
        if a.stem != "index":
            live["app:" + a.stem] = "/apps/" + a.stem
    dist = ROOT / "docs"
    shutil.rmtree(dist, ignore_errors=True)
    shutil.copytree(ROOT / "assets", dist / "assets")
    urls = []
    for p in pages:
        head, page = render(p, live)
        if p == "index":
            url = f"https://{DOMAIN}/"
        elif p == "guides/index":
            url = f"https://{DOMAIN}/guides/"
        elif p == "apps/index":
            url = f"https://{DOMAIN}/apps/"
        else:
            url = f"https://{DOMAIN}/" + p
        urls.append(url)
        out = dist / f"{p}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(full(head, page, url))
    (dist / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (dist / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    (dist / "CNAME").write_text(DOMAIN + "\n")
    (dist / ".nojekyll").write_text("")

    # Preview: relative links between the published files.
    rel = {"home": "./", "pricing": "./#pricing", "guides": "guides/index.html", "apps": "apps/index.html", "support": "support.html", "privacy": "privacy.html", "terms": "terms.html", "assets": "assets/"}
    for g in GUIDES:
        if g.stem != "index":
            rel["guide:" + g.stem] = "guides/" + g.stem + ".html"
    for a in APPS:
        if a.stem != "index":
            rel["app:" + a.stem] = "apps/" + a.stem + ".html"
    prev = ROOT / "preview"
    shutil.rmtree(prev, ignore_errors=True)
    shutil.copytree(ROOT / "assets", prev / "assets")
    for p in pages:
        head, page = render(p, rel)
        if p == "index":
            (prev / "index.html").write_text(head + page)  # the artifact adds the skeleton to the main page
        else:
            out = prev / f"{p}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(full(head, page))
    print("built", [str(x.relative_to(ROOT)) for x in sorted(dist.rglob("*")) if x.is_file()])


if __name__ == "__main__":
    build()
