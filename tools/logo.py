"""The PlayfulProcess double spiral, drawn by numbers.

Run:  python tools/logo.py      (writes the SVGs under icons/)

One stroke is an outer arc (radius R) that rises up the left side, crosses the
top and turns into an inner curl (radius r). The second stroke is the same
stroke turned half a circle around the centre. The two arcs meet the curl
tangentially at the top, so the line never kinks.

  v0  current   : the monoline of September 2026, kept for comparison
  v1  brush     : the hand-drawn mark in "Schema with logo" (Oct 2026), redrawn:
                  each stroke swells and tapers like a brush, ends rounded
  v2  stillpoint: an even line plus a small still point at the centre,
                  the "Being" the two movements turn around
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, '..', 'icons')

INK = '#5b2a91'      # --link in index.html
INK_DARK = '#c9a8f0' # the lighter lilac the favicon uses on dark tab bars
SOFT = '#9a6fd0'     # --spiral

C = (50.0, 50.0)
R = 40.0


def centreline(r=17.0, phi0=123.0, sweep=225.0, step_out=6.0, step_in=9.0):
    """Points along stroke A: (x, y, nx, ny), n pointing away from each arc's centre."""
    pts = []
    n_out = max(2, int(round((270.0 - phi0) / step_out)))
    for i in range(n_out):
        a = math.radians(phi0 + (270.0 - phi0) * i / n_out)
        pts.append((C[0] + R * math.cos(a), C[1] + R * math.sin(a), math.cos(a), math.sin(a)))
    c2 = (C[0], C[1] - R + r)
    n_in = max(2, int(round(sweep / step_in)))
    for i in range(n_in + 1):
        a = math.radians(270.0 + sweep * i / n_in)
        pts.append((c2[0] + r * math.cos(a), c2[1] + r * math.sin(a), math.cos(a), math.sin(a)))
    return pts


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def brush_outline(wmax, w_tail, w_tip, taper_tail=0.30, taper_tip=0.22, r=17.0):
    pts = centreline(r=r, step_out=7.5, step_in=11.25)
    # arc length
    s = [0.0]
    for (x0, y0, *_), (x1, y1, *_) in zip(pts, pts[1:]):
        s.append(s[-1] + math.hypot(x1 - x0, y1 - y0))
    L = s[-1]
    out_side, in_side = [], []
    for (x, y, nx, ny), si in zip(pts, s):
        u = si / L
        w = wmax
        if u < taper_tail:
            w = w_tail + (wmax - w_tail) * ease(u / taper_tail)
        if u > 1 - taper_tip:
            w = w_tip + (wmax - w_tip) * ease((1 - u) / taper_tip)
        h = w / 2
        out_side.append((x + nx * h, y + ny * h))
        in_side.append((x - nx * h, y - ny * h))

    def cap(p, tx, ty, h, n=4):
        # semicircle around p from the inner side (-n) through t to the outer side (+n)
        res = []
        x, y, nx, ny = p
        for k in range(1, n):
            a = math.pi * k / n
            dx = -nx * math.cos(a) + tx * math.sin(a)
            dy = -ny * math.cos(a) + ty * math.sin(a)
            res.append((x + dx * h, y + dy * h))
        return res

    # tangent at the ends (direction of travel)
    x0, y0, nx0, ny0 = pts[0]
    t0 = (-ny0, nx0)  # clockwise travel on screen: tangent = (-sin, cos) = (-ny, nx)
    xe, ye, nxe, nye = pts[-1]
    te = (-nye, nxe)
    loop = list(out_side)
    # tip cap: from outer side, around the front, to inner side
    loop += list(reversed(cap(pts[-1], te[0], te[1], w_tip / 2)))
    loop += list(reversed(in_side))
    loop += cap(pts[0], -t0[0], -t0[1], w_tail / 2)
    return loop


def catmull_rom_closed(points, prec=1):
    n = len(points)
    f = lambda v: f'{v:.{prec}f}'.rstrip('0').rstrip('.')
    d = [f'M{f(points[0][0])} {f(points[0][1])}']
    for i in range(n):
        p0, p1, p2, p3 = points[i - 1], points[i], points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f'C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}')
    return ''.join(d) + 'Z'


def rotated(points):
    return [(100 - x, 100 - y) for x, y in points]


def brush_d(wmax=7.0, w_tail=1.4, w_tip=1.6):
    a = brush_outline(wmax, w_tail, w_tip)
    return catmull_rom_closed(a) + catmull_rom_closed(rotated(a))


def mono_d(r=17.0):
    """Exact arcs: outer arc to the top, then the curl (225 degrees)."""
    a0 = math.radians(123.0)
    x0, y0 = C[0] + R * math.cos(a0), C[1] + R * math.sin(a0)
    c2y = C[1] - R + r
    ae = math.radians(270.0 + 225.0)
    xe, ye = C[0] + r * math.cos(ae), c2y + r * math.sin(ae)
    g = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    one = f'M{g(x0)} {g(y0)}A{g(R)} {g(R)} 0 0 1 50 {g(C[1]-R)}a{g(r)} {g(r)} 0 1 1 {g(xe-50)} {g(ye-(C[1]-R))}'
    two = f'M{g(100-x0)} {g(100-y0)}A{g(R)} {g(R)} 0 0 1 50 {g(100-(C[1]-R))}a{g(r)} {g(r)} 0 1 1 {g(50-xe)} {g((C[1]-R)-ye)}'
    return one + two


def svg(body, title='PlayfulProcess', extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-labelledby="t"{extra}>\n'
            f'  <title id="t">{title}</title>\n{body}\n</svg>\n')


def main():
    os.makedirs(os.path.join(ICONS, 'logo-options'), exist_ok=True)
    B = brush_d()                                  # header and large sizes
    B_FAV = brush_d(wmax=10.0, w_tail=3.6, w_tip=4.0)  # 16-32 px: heavier, blunter ends
    M = mono_d(17.0)
    S = mono_d(15.0)
    files = {
        'logo-options/v0-current.svg': svg(f'  <path d="{M}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'),
        'logo-options/v1-brush.svg': svg(f'  <path d="{B}" fill="{INK}"/>'),
        'logo-options/v1-brush-small.svg': svg(f'  <path d="{B_FAV}" fill="{INK}"/>'),
        'logo-options/v2-stillpoint.svg': svg(
            f'  <path d="{S}" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>\n'
            f'  <circle cx="50" cy="50" r="4" fill="{SOFT}"/>'),
        # wired in: variant 1
        'playfulprocess-logo.svg': svg(f'  <path d="{B}" fill="{INK}"/>'),
        'playfulprocess-logo-mono.svg': svg(f'  <path d="{B}" fill="currentColor"/>'),
        'favicon.svg': (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="32" height="32">\n'
            '  <title>PlayfulProcess</title>\n'
            f'  <style>path{{fill:{INK}}}@media (prefers-color-scheme:dark){{path{{fill:{INK_DARK}}}}}</style>\n'
            f'  <path d="{B_FAV}"/>\n</svg>\n'),
    }
    for name, text in files.items():
        with open(os.path.join(ICONS, name), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        print(f'{name}: {len(text)} bytes')
    # index.html inlines the brush path as <symbol id="pp-logo"> (fill="currentColor"):
    # paste the d of playfulprocess-logo-mono.svg there after a change.


if __name__ == '__main__':
    main()
