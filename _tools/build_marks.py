"""Night Cheese Labs logo marks.

Writes the source SVGs in assets/, favicon.svg, and renders favicon-32.png,
apple-touch-icon.png and og-image.png with headless Chrome (macOS path below).
The pages inline the same SVG markup, so paste any geometry change into the
header, hero and footer too.

Run from anywhere:  python3 _tools/build_marks.py
"""
import math, pathlib, subprocess, tempfile

INK, CHEESE, TEXT = "#0d1322", "#f5c84c", "#ebe6da"
C1, R1 = (30.0, 34.0), 25.0   # cheese body
C2, R2 = (44.0, 22.0), 21.0   # bite that cuts the crescent
CENTER = (28.5, 35.0)         # optical centre of the crescent (mass sits lower-left)

HOLES = {
    "full": [(17, 38, 4), (27, 50, 3), (12, 26, 2.2), (40, 53, 1.8)],
    "32":   [(17, 38, 4.5), (27, 50, 3.5)],
    "16":   [(17.5, 38.5, 5)],
}

def f(n):
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s

def crescent_path(holes):
    (x1, y1), (x2, y2) = C1, C2
    d = math.hypot(x2 - x1, y2 - y1)
    a = (R1**2 - R2**2 + d**2) / (2 * d)
    h = math.sqrt(R1**2 - a**2)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x1 + a * ux, y1 + a * uy
    p = (bx - h * uy, by + h * ux)   # lower-right tip
    q = (bx + h * uy, by - h * ux)   # upper-left tip
    # Outer edge: the long way round the body; inner edge: back along the bite.
    d_ = (f"M{f(p[0])} {f(p[1])}A{f(R1)} {f(R1)} 0 1 1 {f(q[0])} {f(q[1])}"
          f"A{f(R2)} {f(R2)} 0 0 0 {f(p[0])} {f(p[1])}Z")
    for cx, cy, r in holes:
        d_ += (f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0"
               f"a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0Z")
    return d_

def moon_svg(size="full", cls=None, standalone=False, label=None):
    """Cheese moon on a transparent background. Holes are cut out (evenodd)."""
    attrs = f' class="{cls}"' if cls else ""
    ns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ""
    vb = f"{f(CENTER[0] - 28)} {f(CENTER[1] - 28)} 56 56"
    title = f"<title>{label}</title>" if label else ""
    return (f'<svg{ns}{attrs} viewBox="{vb}">{title}'
            f'<path fill="{CHEESE}" fill-rule="evenodd" d="{crescent_path(HOLES[size])}"/></svg>')

def favicon_svg():
    """16px variant on an ink tile so it reads on light browser chrome."""
    x0, y0 = CENTER[0] - 32, CENTER[1] - 32
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x0)} {f(y0)} 64 64">'
            f'<rect x="{f(x0)}" y="{f(y0)}" width="64" height="64" rx="13" fill="{INK}"/>'
            f'<path fill="{CHEESE}" fill-rule="evenodd" d="{crescent_path(HOLES["16"])}"/></svg>')

def seal_svg(uid, moon="full", cls=None, standalone=False, text_fill=TEXT):
    """Ring + circular wordmark + cheese moon. Never render below ~48px."""
    words = "NIGHT CHEESE LABS · EST. 2026 · "
    r_text = 27
    circ = 2 * math.pi * r_text
    # Rotate so "NIGHT CHEESE LABS" is centred over 12 o'clock.
    rot = -(len("NIGHT CHEESE LABS") / len(words)) * 180
    s = 0.6  # body r25 -> r15
    tx, ty = 38 - CENTER[0] * s, 38 - CENTER[1] * s
    attrs = f' class="{cls}"' if cls else ""
    ns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ""
    return (f'<svg{ns}{attrs} viewBox="0 0 76 76" role="img" aria-label="Night Cheese Labs, established 2026">'
            f'<defs><path id="{uid}" d="M38 {38 - r_text}a{r_text} {r_text} 0 1 1 0 {2 * r_text}a{r_text} {r_text} 0 1 1 0 {-2 * r_text}"/></defs>'
            f'<circle cx="38" cy="38" r="35" fill="none" stroke="{CHEESE}" stroke-width="1.5"/>'
            f'<text font-family="\'IBM Plex Mono\', ui-monospace, Menlo, monospace" font-size="6.8" font-weight="500" fill="{text_fill}" transform="rotate({f(rot)} 38 38)">'
            f'<textPath href="#{uid}" textLength="{f(circ - 0.3)}" lengthAdjust="spacing">{words}</textPath></text>'
            f'<path transform="translate({f(tx)} {f(ty)}) scale({s})" fill="{CHEESE}" fill-rule="evenodd" d="{crescent_path(HOLES[moon])}"/>'
            f'</svg>')


def build():

    site = pathlib.Path(__file__).resolve().parent.parent
    scratch = pathlib.Path(tempfile.mkdtemp(prefix="ncl-marks-"))
    assets = site / "assets"
    assets.mkdir(exist_ok=True)

    (assets / "cheese-moon.svg").write_text(moon_svg("full", standalone=True, label="Night Cheese Labs") + "\n")
    (assets / "cheese-moon-32.svg").write_text(moon_svg("32", standalone=True, label="Night Cheese Labs") + "\n")
    (assets / "cheese-moon-16.svg").write_text(moon_svg("16", standalone=True, label="Night Cheese Labs") + "\n")
    (assets / "seal.svg").write_text(seal_svg("seal-ring", standalone=True) + "\n")
    (site / "favicon.svg").write_text(favicon_svg() + "\n")

    FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap"
    seal_og = seal_svg("og-ring", "full")
    seal_og = seal_og.replace('<svg viewBox="0 0 76 76"', '<svg x="120" y="125" width="380" height="380" viewBox="0 0 76 76"')
    og = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
    <style>@import url("{FONTS}");</style>
    <rect width="1200" height="630" fill="{INK}"/>
    {seal_og}
    <g transform="translate(590 0)">
    <text x="0" y="228" font-family="'IBM Plex Mono', monospace" font-size="22" font-weight="500" letter-spacing="4" fill="{CHEESE}">INDEPENDENT SOFTWARE STUDIO</text>
    <text x="-4" y="328" font-family="Fraunces, Georgia, serif" font-size="92" font-weight="500" letter-spacing="-1.5" fill="{TEXT}">Night Cheese</text>
    <text x="-4" y="426" font-family="Fraunces, Georgia, serif" font-size="92" font-weight="500" letter-spacing="-1.5" fill="{TEXT}">Labs</text>
    </g>
    </svg>
    '''
    (assets / "og-image.svg").write_text(og)

    def tile(name, size, inner, pad_ratio):
        """PNG source: ink square with the moon centred at (1 - 2*pad) of the tile."""
        inner_px = round(size * (1 - 2 * pad_ratio))
        off = (size - inner_px) / 2
        html = (f'<!doctype html><html><body style="margin:0;background:{INK}">'
                f'<div style="position:absolute;left:{off}px;top:{off}px;width:{inner_px}px;height:{inner_px}px">'
                + inner.replace("<svg ", '<svg width="100%" height="100%" ') + '</div></body></html>')
        p = scratch / f"{name}.html"
        p.write_text(html)
        return p

    CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    def shoot(src, out, w, h, scale=1):
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={scale}", f"--window-size={w},{h}",
                        "--virtual-time-budget=8000", f"--screenshot={out}", src.as_uri()],
                       check=True, capture_output=True)

    shoot(tile("favicon-32", 32, moon_svg("32"), 0.06), site / "favicon-32.png", 32, 32)
    shoot(tile("apple-touch-icon", 180, moon_svg("full"), 0.17), site / "apple-touch-icon.png", 180, 180)
    shoot(assets / "og-image.svg", site / "og-image.png", 1200, 630)
    # 4x previews for eyeballing the small marks
    shoot(tile("favicon-32", 32, moon_svg("32"), 0.06), scratch / "favicon-32@8x.png", 32, 32, 8)
    shoot(tile("favicon-16", 16, moon_svg("16"), 0.06), scratch / "favicon-16@8x.png", 16, 16, 8)
    print(f"Wrote assets/, favicon.svg and PNGs. Render sources and 8x previews: {scratch}")


if __name__ == "__main__":
    build()
