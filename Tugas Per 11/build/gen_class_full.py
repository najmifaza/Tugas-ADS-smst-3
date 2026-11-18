"""UML class diagram domain GABUNGAN (8 kelas) untuk Bab 6.1 — satu gambar, kanvas lanskap.

Memakai ulang gaya dan fungsi gambar dari gen_diagrams.py, tapi:
  * anggota kelas dibungkus (wrap) supaya kotak bisa ramping -> 3 kolom,
  * kanvas 1278 x ~900 px dipasang pada halaman lanskap (lebar cetak 9,6 in) -> teks 13 px = 7 pt.
Keluaran: ../images/diagram_class_full.svg/.html

Jalankan: python gen_class_full.py
"""

import pathlib
import gen_diagrams as G

BOX, ROW, HEAD, PAD, GAP = 390, 16, 26, 6, 30
MARGIN_X, TOP = 22, 18
COLS = [["TIKET_PESANAN"],
        ["BERKAS_ASET", "DRAF_KARYA", "RIWAYAT_REVISI"],
        ["RIWAYAT_PENUGASAN", "PUBLIKASI_KONTEN", "PENGGUNA", "KEMENTERIAN"]]
WRAP = 44
CANVAS = 3 * BOX + 2 * GAP + 2 * MARGIN_X
MEMBER_FS = 13


def wrap(s, width=WRAP, indent="   "):
    if len(s) <= width:
        return [s]
    out, cur = [], ""
    for word in s.split(" "):
        if len(cur) + len(word) + 1 > width and cur:
            out.append(cur)
            cur = indent + word
        else:
            cur = f"{cur} {word}".strip()
    out.append(cur)
    return out


def prepare():
    classes = {}
    for name, (stereo, attrs, ops) in G.CLASSES.items():
        wa = [l for a in attrs for l in wrap(a)]
        wo = [l for o in ops for l in wrap(o)]
        classes[name] = (stereo, wa, wo)
    return classes


def height(attrs, ops):
    return HEAD + (len(attrs) + len(ops) + 2) * ROW + PAD


def draw_class(name, classes, x, y):
    stereo, attrs, ops = classes[name]
    h = height(attrs, ops)
    sep1 = HEAD + 14
    o = [f'  <g transform="translate({x}, {y})">',
         f'    <rect width="{BOX}" height="{h}" class="body-box"/>',
         f'    <rect width="{BOX}" height="{sep1}" class="header-box"/>',
         f'    <text x="{BOX // 2}" y="19" class="cls-title">{G.esc(name)}</text>',
         f'    <text x="{BOX // 2}" y="34" class="cls-stereo">«entity» {G.esc(stereo)}</text>',
         f'    <line x1="0" y1="{sep1}" x2="{BOX}" y2="{sep1}" class="cell-border"/>']
    y0 = sep1 + ROW
    for i, a in enumerate(attrs):
        o.append(f'    <text x="9" y="{y0 + i * ROW}" class="cls-member">{G.esc(a)}</text>')
    ysep = y0 + len(attrs) * ROW
    o.append(f'    <line x1="0" y1="{ysep}" x2="{BOX}" y2="{ysep}" class="cell-border"/>')
    for i, m in enumerate(ops):
        o.append(f'    <text x="9" y="{ysep + i * ROW + 14}" class="cls-member">{G.esc(m)}</text>')
    o.append("  </g>")
    return "\n".join(o)


def main():
    classes = prepare()
    pos, col_x, max_h = {}, [], 0
    for i, col in enumerate(COLS):
        col_x.append(MARGIN_X + i * (BOX + GAP))
    for ci, col in enumerate(COLS):
        y = TOP
        for name in col:
            pos[name] = (col_x[ci], y, ci)
            y += height(*classes[name][1:]) + GAP
        max_h = max(max_h, y - GAP + TOP)

    # hubungan: relasi antar kelas pada kolom berbeda dirutekan lewat koridor antar kolom
    comp = getattr(G, "COMPOSITION", set())
    rels, labels = [], []
    for (s, d), (ms, md) in G.MULT.items():
        sx, sy, sci = pos[s]
        dx, dy, dci = pos[d]
        sh, dh = height(*classes[s][1:]), height(*classes[d][1:])
        if sci == dci and dy > sy:                      # kolom sama -> garis vertikal
            x = sx + (76 if (hash((s, d)) % 2 == 0) else 132)
            y1, y2 = sy + sh, dy
            rels.append(f'  <path d="M {x} {y1} L {x} {y2}" class="rel-line"/>')
            if (s, d) in comp:
                rels.append(f'  <path d="M {x} {y1} L {x - 9} {y1 + 11} L {x} {y1 + 22} L {x + 9} {y1 + 11} Z" class="diamond"/>')
            rels.append(f'  <path d="M {x - 6} {y2} L {x} {y2 - 9} L {x + 6} {y2} Z" class="symbol"/>')
            labels += [dict(x=x - 52, y=y1 + 18, text=ms), dict(x=x + 52, y=y2 - 14, text=md)]
        else:                                           # kolom beda -> lewat koridor
            out_right = dx > sx
            x1 = sx + BOX if out_right else sx
            x2 = dx if out_right else dx + BOX
            corridor = (sx + BOX + GAP / 2) if out_right else (sx - GAP / 2)
            y_s = sy + 26
            y_d = dy + 24
            rels.append(f'  <path d="M {x1} {y_s} L {corridor:.0f} {y_s} L {corridor:.0f} {y_d} L {x2} {y_d}" class="rel-line"/>')
            if (s, d) in comp:
                xd = x1 + (14 if out_right else -14)
                rels.append(f'  <path d="M {x1} {y_s} L {xd} {y_s - 9} L {x1 + (28 if out_right else -28)} {y_s} L {xd} {y_s + 9} Z" class="diamond"/>')
            ax = x2 + (-11 if out_right else 11)
            rels.append(f'  <path d="M {x2} {y_d} L {ax} {y_d - 7} L {ax} {y_d + 7} Z" class="symbol"/>')
            labels += [dict(x=x1 + (34 if out_right else -34), y=y_s - 8, text=ms),
                       dict(x=x2 - (34 if out_right else -34), y=y_d - 8, text=md)]

    h = int(max_h + 12)
    style = G.STYLE.replace(f"font-size: {G.CLS_MEMBER_FS}px", f"font-size: {MEMBER_FS}px")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {h}" width="{CANVAS}" height="{h}">',
             "  <defs>", "    <style>", style.strip(), "    </style>", "  </defs>",
             f'  <rect width="{CANVAS}" height="{h}" fill="#FFFFFF"/>', ""]
    parts += rels
    for lb in labels:
        w = int(len(lb["text"]) * 7 * 0.62) + 8
        parts.append(f'  <rect x="{lb["x"] - w / 2}" y="{lb["y"] - 11}" width="{w}" height="15" class="pill"/>')
        parts.append(f'  <text x="{lb["x"]}" y="{lb["y"]}" class="mult-label">{G.esc(lb["text"])}</text>')
    parts.append("")
    for col in COLS:
        for name in col:
            x, y, _ = pos[name]
            parts.append(draw_class(name, classes, x, y))
    parts.append("</svg>")
    svg = "\n".join(parts)

    out = pathlib.Path(__file__).resolve().parent.parent / "images"
    out.mkdir(exist_ok=True)
    (out / "diagram_class_full.svg").write_text(svg, encoding="utf-8")
    (out / "diagram_class_full.html").write_text(G.HTML.replace("__SVG__", svg), encoding="utf-8")
    print(f"diagram_class_full.svg: {CANVAS}x{h} | {len(G.CLASSES)} kelas | "
          f"teks {MEMBER_FS}px = {MEMBER_FS / CANVAS * 9.6 * 72:.1f} pt pada lebar 9,6 in | "
          f"tinggi di halaman = {h / CANVAS * 9.6:.2f} in")
    print("class COMPOSITION:", sorted(comp) if comp else "(kosong)")


if __name__ == "__main__":
    main()
