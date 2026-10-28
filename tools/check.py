"""Checks the built preview: console errors, missing files, unresolved {{placeholders}}, sideways scrolling.

  python3 tools/check.py [screenshot-dir]
"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent / "preview"
SHOTS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
PAGES = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html"))
WIDTHS = [390, 768, 1280]


async def main():
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in WIDTHS:
            ctx = await b.new_context(viewport={"width": w, "height": 900}, reduced_motion="reduce")
            for rel in PAGES:
                pg = await ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e, rel=rel: errs.append(f"JS error: {e}"))
                pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" and "fonts.g" not in m.text and "TUNNEL" not in m.text else None)
                pg.on("requestfailed", lambda r: errs.append("missing: " + r.url) if r.url.startswith("file:") else None)
                await pg.goto("file://" + str(ROOT / rel))
                await pg.wait_for_timeout(250)
                over = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if over > 1:
                    wide = await pg.evaluate("""() => [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
                        .slice(0, 3).map(e => e.tagName + '.' + e.className)""")
                    errs.append(f"sideways scroll {over}px: {wide}")
                html = await pg.content()
                if "{{" in html.replace("{{Name}}", "").replace("{{Course}}", ""):
                    errs.append("unresolved placeholder")
                broken = await pg.evaluate("[...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.loading !== 'lazy').map(i => i.src)")
                errs += ["broken image: " + s for s in broken]
                for e in errs:
                    problems.append(f"{w}px {rel}: {e}")
                if SHOTS and rel in ("index.html", "guides/how-to-use-form-limits.html"):
                    await pg.screenshot(path=str(SHOTS / f"chk-{w}-{rel.replace('/', '_')}.png"), full_page=True)
                await pg.close()
            await ctx.close()
        await b.close()
    print("\n".join(problems) if problems else f"OK: {len(PAGES)} pages x {len(WIDTHS)} widths, no problems")


asyncio.run(main())
