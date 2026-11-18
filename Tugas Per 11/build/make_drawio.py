"""Bangun SATU berkas draw.io XML (13 tab) secara native dari data desain.

Bukan konversi dari SVG: setiap sel dibuat langsung dengan tipe bentuk yang benar
(crow's foot ERone/ERmany, shape=umlActor, ellipse use case, rhombus gateway, swinglane ERD,
kompartemen kelas, activation bar, umlFrame) dan label di-escape sekali saja.

Keluaran: ../SDD_Medkreminfo_Diagram.drawio
Jalankan: python make_drawio.py  (setelah gen_upstream2.py, gen_sequences.py, gen_diagrams.py)
"""

import pathlib
import re
import xml.etree.ElementTree as ET

import gen_diagrams as G
import gen_sequences as S

D = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = D / "SDD_Medkreminfo_Diagram.drawio"
CANVAS = 1000


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def lab(t):
    """Label HTML: escape sekali, baris baru -> <br>."""
    return esc(t).replace("\n", "&lt;br&gt;")


def pageno(v):
    if v >= 1000:
        return f"{int(v)}"
    return f"{int(v)}"


class Tab:
    def __init__(self, name, w, h):
        self.name, self.w, self.h, self.cells = name, w, h, []

    def vertex(self, cid, value, style, x, y, w, h, parent="1"):
        self.cells.append(
            f'        <mxCell id="{cid}" value="{lab(value)}" style="{style}" vertex="1" parent="{parent}">\n'
            f'          <mxGeometry x="{round(max(0, x))}" y="{round(max(0, y))}" width="{round(w)}" '
            f'height="{round(h)}" as="geometry"/>\n        </mxCell>')

    def edge(self, cid, value, style, pts=None, src=None, dst=None, extra="", offset=(0, -12)):
        off = (f'<mxPoint x="{offset[0]}" y="{offset[1]}" as="offset"/>' if value and offset else "")
        geo = ""
        if src and dst:
            geo = f'<mxGeometry relative="1" as="geometry">{off}</mxGeometry>{extra}'
        else:
            geo = ('<mxGeometry relative="1" as="geometry">\n            <Array as="points">'
                   + "".join(f'<mxPoint x="{round(x)}" y="{round(y)}"/>' for x, y in pts[1:-1])
                   + f'</Array>\n            <mxPoint x="{round(pts[0][0])}" y="{round(pts[0][1])}" as="sourcePoint"/>\n'
                     f'            <mxPoint x="{round(pts[-1][0])}" y="{round(pts[-1][1])}" as="targetPoint"/>\n'
                     f'            {off}\n          </mxGeometry>')
        attrs = f'source="{src}" target="{dst}" ' if src and dst else ""
        self.cells.append(f'        <mxCell id="{cid}" value="{lab(value)}" style="{style}" {attrs}edge="1" '
                          f'parent="1">\n          {geo}\n        </mxCell>')

    def xml(self):
        return ('  <diagram name="' + esc(self.name) + '" id="' + re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-") + '">\n'
                f'    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pageno(self.w)}" pageHeight="{pageno(self.h)}" '
                'background="#ffffff">\n      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n'
                + "\n".join(self.cells) + "\n      </root>\n    </mxGraphModel>\n  </diagram>")


# ------------------------------------------------------------------ sequence
def seq_tab(key, block, title):
    parts, steps = S.parse(block)
    n = len(parts)
    canvas_w = 950 if n <= 6 else (1024 if n == 7 else 1120)
    ids = [p[0] for p in parts]
    pad = S.pads(canvas_w, n)
    span = canvas_w - 2 * pad
    xs = {pid: pad + (i * span // max(n - 1, 1)) for i, pid in enumerate(ids)}

    rows, y = [], S.TOP + S.HEAD_H + 20
    for st in steps:                                    # pass 1: posisi vertikal tiap pesan/fragmen
        if st["kind"] == "msg":
            rows.append((y, st)); y += S.ROW
        elif st["kind"] in ("alt", "opt"):
            y += 34
        elif st["kind"] == "else":
            y += 26
        elif st["kind"] == "end":
            y += 6
    height = int(y + 40)
    bottom = height - 30
    tab = Tab(title, canvas_w, height)

    # aktivasi
    act, depth, act_rows = {}, {}, []
    for y_, st in rows:
        if st["mtype"] == "call":
            depth[st["dst"]] = depth.get(st["dst"], 0) + 1
            if depth[st["dst"]] == 1:
                act[st["dst"]] = y_
        else:
            d = depth.get(st["src"], 0) - 1
            depth[st["src"]] = d
            if d <= 0:
                start = act.pop(st["src"], None)
                if start is not None and y_ - start > 6:
                    act_rows.append((st["src"], start, y_))

    inner = max(6, min(xs.values()) - 40)                   # bingkai tidak keluar kanvas
    outer = min(canvas_w - 6, max(xs.values()) + 40)

    for pid in ids:                                     # lifeline
        tab.edge(f"l_{pid}", "", "endArrow=none;html=1;dashed=1;dashPattern=6 5;strokeColor=#000000;strokeWidth=1;",
                 pts=[(xs[pid], S.TOP + S.HEAD_H), (xs[pid], bottom)])
    for pid, y0, y1 in act_rows:                        # activation bar
        tab.vertex(f"a_{pid}_{y0}", "", "html=1;fillColor=#FFFFFF;strokeColor=#000000;",
                   xs[pid] - 7, y0, 14, y1 - y0)

    tab.cells.sort(key=lambda c: 0 if 'id="l_' in c else 1)          # garis lifeline di lapisan bawah
    # fragment kotak (alt/opt) + sekat [else]
    for frag in fragment_blocks(steps, rows):
        style = ("shape=umlFrame;whiteSpace=wrap;html=1;pointerEvents=0;fillColor=none;strokeColor=#000000;"
                 "fontSize=13;fontStyle=1;align=left;verticalAlign=top;")
        tab.vertex(f"f{frag['id']}", frag["frag"], style, inner, frag["y0"], outer - inner, frag["y1"] - frag["y0"])
        # kondisi ditulis sebagai sel teks terpisah: teks panjang tidak meluber dari pentagon umlFrame
        tab.vertex(f"fc{frag['id']}", f"[{frag['text']}]",
                   "text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=2;strokeColor=none;"
                   "fillColor=#FFFFFF;",
                   inner + 4, max(0, frag["y0"] - 17), outer - inner - 12, 16)
        for e in frag["elses"]:
            tab.edge(f"e{frag['id']}_{e['y']}", f"[else {e['text']}]",
                     "endArrow=none;html=1;dashed=1;dashPattern=4 3;strokeColor=#000000;fontSize=12;"
                     "fontStyle=2;labelBackgroundColor=#FFFFFF;",
                     pts=[(inner, e["y"]), (outer, e["y"])])

    for i, (y_, st) in enumerate(rows):                 # pesan
        x1, x2 = xs[st["src"]], xs[st["dst"]]
        ret = st["mtype"] == "return"
        style = ("html=1;strokeColor=#000000;strokeWidth=1.5;fontSize=13;labelBackgroundColor=#FFFFFF;"
                 + ("dashed=1;dashPattern=7 5;endArrow=open;endFill=0;" if ret else "endArrow=block;endFill=1;"))
        tab.edge(f"m{i}", st["text"], style, pts=[(x1, y_), (x2, y_)])

    head_w = S.head_width(canvas_w, n)                   # kepala lifeline
    for pid in ids:
        lines = S.wrap(pid, max(8, int(head_w / 6.2)))
        hh = S.HEAD_H + (len(lines) - 1) * 13
        tab.vertex(f"h_{pid}", "\n".join(lines) + "\nlifeline",
                   "html=1;fillColor=#D9D9D9;strokeColor=#000000;fontSize=14;fontStyle=1;rounded=0;",
                   xs[pid] - head_w // 2, S.TOP, head_w, hh)
    return tab


def fragment_blocks(steps, rows):
    """Kumpulkan blok alt/opt lengkap dengan posisi sekat [else]."""
    blocks, stack, y = [], [], S.TOP + S.HEAD_H + 20
    for st in steps:
        if st["kind"] == "msg":
            y += S.ROW
        elif st["kind"] in ("alt", "opt"):
            stack.append(dict(id=len(blocks) + 100, frag=st["kind"], text=st["text"], y0=y - 10,
                              y1=None, elses=[]))
            blocks.append(stack[-1]); y += 34
        elif st["kind"] == "else":
            if stack:
                stack[-1]["elses"].append(dict(y=y + 6, text=st["text"]))
            y += 26
        elif st["kind"] == "end":
            if stack:
                stack.pop()["y1"] = y + 6
            y += 6
    return [b for b in blocks if b["y1"]]


# ----------------------------------------------------------------------- ERD
CROW = {"1..1": "ERmandOne", "0..1": "ERzeroToOne", "0..N": "ERzeroToMany", "1..N": "ERmany"}
ERD_COLS = {0: ["KEMENTERIAN", "PENGGUNA", "TIKET_PESANAN"],
            1: ["BERKAS_ASET", "DRAF_KARYA", "RIWAYAT_REVISI", "RIWAYAT_PENUGASAN", "PUBLIKASI_KONTEN"]}
ERD_X, ERD_W, ERD_TOP, ERD_GAP = {0: 40, 1: 520}, 430, 40, 46


def erd_tab(kind):
    """ERD dengan header di ATAS kotak (horizontal=1) dan relasi berkaki crow's foot
    yang punya titik awal/akhir eksplisit (tidak menembus kotak lain)."""
    logis = kind == "logis"
    title = "Bab 4.2 — ERD Logis 3NF" if logis else "Bab 4.1 — ERD Konseptual"
    tab = Tab(title, 1000, 10)
    pos, coly = {}, {0: ERD_TOP, 1: ERD_TOP}
    for col, names in ERD_COLS.items():
        for name in names:
            lines = []
            for typ, attr, key in G.ENT_ATTR[name]:
                marks = [k for k in ("PK", "FK", "UK") if k == key and (k != "FK" or logis)]
                txt = f"<b>{attr}</b>" if marks else attr
                tag = f"  <i>{' '.join(marks)}</i>" if marks else ""
                lines.append(f"{txt} : {typ}{tag}" if logis else f"{txt}{tag}")
            head, body_h = 28, 18 * len(lines) + 12
            h = head + body_h
            pos[name] = (ERD_X[col], coly[col], ERD_W, h, col)
            cid = f"e_{name}"
            tab.vertex(cid, name, "swimlane;html=1;horizontal=1;startSize=28;fillColor=#D9D9D9;"
                                  "swimlaneFillColor=#FFFFFF;strokeColor=#000000;fontSize=14;fontStyle=1;"
                                  "align=center;verticalAlign=middle;",
                       pos[name][0], pos[name][1], ERD_W, h)
            tab.vertex(f"b_{name}", "<br>".join(lines),
                       "text;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;fontSize=13;"
                       "strokeColor=#000000;fillColor=none;overflow=hidden;",
                       0, head, ERD_W, body_h, parent=cid)
            coly[col] += h + ERD_GAP

    used_src, used_pair = {}, {}
    for (src, dst, verb, sm, dm) in G.RELATIONS:
        sx, sy, sw, sh, sc = pos[src]
        tx, ty, tw, th, tc = pos[dst]
        key_s, key_p = src, (src, dst)
        i_s, i_p = used_src.get(key_s, 0), used_pair.get(key_p, 0)
        used_src[key_s], used_pair[key_p] = i_s + 1, i_p + 1
        if sc == tc:                                    # kolom sama: garis pendek di celah antar kotak
            x = sx + 150 + 74 * i_p
            pts = [(x, sy + sh), (x, ty)]
        else:                                           # beda kolom: lewat koridor antar kolom
            corridor = (sx + sw + tx) / 2
            y_s = sy + 36 + 30 * i_s
            y_d = ty + 36 + 30 * i_p
            pts = [(sx + sw, y_s), (corridor, y_s), (corridor, y_d), (tx, y_d)]
        tab.edge(f"r_{src}_{dst}_{i_p}", f"{verb}\n{sm} : {dm}",
                 "edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#000000;strokeWidth=1.5;"
                 f"startArrow={CROW.get(sm, 'ERone')};startFill=1;endArrow={CROW.get(dm, 'ERone')};endFill=1;"
                 "fontSize=12;fontStyle=2;labelBackgroundColor=#FFFFFF;rounded=0;",
                 pts=pts, offset=(0, -14))
    tab.h = max(coly.values()) + 20
    return tab


# ---------------------------------------------------------------------- class
CLASS_COLS = {0: ["PENGGUNA", "KEMENTERIAN"], 1: ["TIKET_PESANAN"],
              2: ["BERKAS_ASET", "DRAF_KARYA", "RIWAYAT_REVISI", "RIWAYAT_PENUGASAN", "PUBLIKASI_KONTEN"]}
CLS_X, CLS_W, CLS_TOP, CLS_GAP = {0: 22, 1: 442, 2: 862}, 390, 46, 30


def wrap_member(t, width=44, indent="   "):
    if len(t) <= width:
        return [t]
    out, cur = [], ""
    for word in t.split(" "):
        if len(cur) + len(word) + 1 > width and cur:
            out.append(cur); cur = indent + word
        else:
            cur = f"{cur} {word}".strip()
    out.append(cur)
    return out


def class_tab():
    """Kelas diletakkan 3 kolom dengan TIKET_PESANAN di tengah supaya relasi hanya melompat
    ke kolom sebelah; relasi dua kolom dilewatkan kanal di atas diagram, bukan menembus kotak."""
    tab = Tab("Bab 6.1 — UML Class Diagram (8 kelas)", 1274, 10)
    pos, coly = {}, {0: CLS_TOP, 1: CLS_TOP, 2: CLS_TOP}
    for col, names in CLASS_COLS.items():
        for name in names:
            stereo, attrs, ops = G.CLASSES[name]
            wa = [l for a in attrs for l in wrap_member(a)]
            wo = [l for o in ops for l in wrap_member(o)]
            head, ah, oh = 34, 17 * len(wa) + 10, 17 * len(wo) + 10
            h = head + ah + oh
            pos[name] = (CLS_X[col], coly[col], CLS_W, h, col)
            cid = f"k_{name}"
            tab.vertex(cid, f"<b>{name}</b>\n«entity» {stereo}",
                       "swimlane;html=1;horizontal=1;startSize=34;fillColor=#D9D9D9;swimlaneFillColor=#FFFFFF;"
                       "strokeColor=#000000;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;",
                       pos[name][0], pos[name][1], CLS_W, h)
            tab.vertex(f"at_{name}", "<br>".join(wa),
                       "text;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=3;fontSize=12;"
                       "fontFamily=Courier New;strokeColor=#000000;fillColor=none;overflow=hidden;",
                       0, head, CLS_W, ah, parent=cid)
            tab.vertex(f"op_{name}", "<br>".join(wo),
                       "text;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=3;fontSize=12;"
                       "fontFamily=Courier New;strokeColor=#000000;fillColor=none;overflow=hidden;",
                       0, head + ah, CLS_W, oh, parent=cid)
            coly[col] += h + CLS_GAP

    used = {}
    for (src, dst), (sm, dm) in G.MULT.items():
        sx, sy, sw, sh, sc = pos[src]
        tx, ty, tw, th, tc = pos[dst]
        i = used.get(src, 0); used[src] = i + 1
        comp = (src, dst) in G.COMPOSITION
        head = ("startArrow=diamondThin;startFill=1;startSize=14;endArrow=none;startSize=14;" if comp
                else "endArrow=open;endFill=0;")
        style = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;strokeWidth=1.5;"
                 f"fontSize=12;labelBackgroundColor=#FFFFFF;{head}")
        if abs(sc - tc) == 1:                            # kolom bersebelahan: koridor antar kolom
            right = tx > sx
            corridor = (sx + sw + tx) / 2 if right else (tx + tw + sx) / 2
            y_s = sy + 40 + 26 * i
            y_d = ty + 40
            x_a = sx + sw if right else sx
            x_b = tx if right else tx + tw
            pts = [(x_a, y_s), (corridor, y_s), (corridor, y_d), (x_b, y_d)]
        else:                                            # selisih dua kolom: kanal di atas diagram
            chan = 8 + 16 * i
            x_s = sx + 60 + 60 * i
            x_d = tx + 60 + 60 * i
            pts = [(x_s, sy), (x_s, chan), (x_d, chan), (x_d, ty)]
        tab.edge(f"c_{src}_{dst}", f"{sm}   {dm}", style, pts=pts, offset=(0, -12))
    tab.h = max(coly.values()) + 10
    return tab


# --------------------------------------------------------------------- bundle
UPSTREAM = [("bpmn", "Lampiran D.1 — BPMN-01 Proses To-Be"),
            ("ucd", "Lampiran D.2 — UCD-01 Use Case Diagram"),
            ("ad01", "Lampiran D.3 — AD-01 UC-01 Pengajuan Tiket"),
            ("ad02", "Lampiran D.4 — AD-02 Validasi dan Penugasan"),
            ("ad03", "Lampiran D.5 — AD-03 Pengerjaan dan Unggah Draf"),
            ("ad04", "Lampiran D.6 — AD-04 Tinjauan dan Publikasi")]


def upstream_tab(builder, title):
    """Panggil generator artefak hulu langsung (tanpa berkas .drawio perantara)."""
    import gen_upstream2 as U
    canvas, _ = getattr(U, builder)()
    xml = canvas.drawio(title)
    body = re.search(r"<root>(.*?)</root>", xml, re.S).group(1)
    bottom = max([canvas.h] + [c["y"] + c["h"] for c in canvas.cells if "y" in c and "h" in c])
    tab = Tab(title, canvas.w, bottom + 8)
    # sel self-closing (id 0/1) harus ikut terambil pola pertama, kalau tidak sel pertama hilang
    tab.cells = [c for c in re.findall(r"<mxCell\b[^>]*/>|<mxCell\b.*?</mxCell>", body, re.S)
                 if not re.match(r'<mxCell id="[01]"', c)]
    return tab


def main():
    md = (D / "SDD_Medkreminfo_v1.0.md").read_text(encoding="utf-8")
    blocks = [b for b in re.findall(r"```mermaid\n(.*?)```", md, re.S) if b.strip().startswith("sequenceDiagram")]
    tabs = []
    for key, block in zip(["sd01", "sd02", "sd03", "sd04"], blocks):
        tabs.append(seq_tab(key, block, "Bab 3." + str(2 + ["sd01", "sd02", "sd03", "sd04"].index(key)) +
                            " — " + S.TITLES[key]))
    tabs.append(erd_tab("konseptual"))
    tabs.append(erd_tab("logis"))
    tabs.append(class_tab())
    for name, title in UPSTREAM:
        tabs.append(upstream_tab(name, title))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<mxfile host="app.diagrams.net" agent="Antigravity" version="24.0.0">']
    for t in tabs:
        xml.append(t.xml())
    xml.append("</mxfile>")
    BUNDLE.write_text("\n".join(xml) + "\n", encoding="utf-8")

    root = ET.parse(BUNDLE).getroot()
    print(f"{BUNDLE.name}: {BUNDLE.stat().st_size/1024:.1f} KB | {len(list(root))} tab")
    for t in tabs:
        print(f"   {t.name:52} {t.w:>5} x {t.h:>5} px | {len(t.cells):4} sel")
    for f in list(D.rglob("*.drawio")):                    # hanya bundle yang disimpan
        if f != BUNDLE:
            f.unlink()
    for f in (D / "images").glob("*.drawio"):
        f.unlink()
    if (D / "build" / "svg2drawio.py").exists():
        (D / "build" / "svg2drawio.py").unlink()
        print("svg2drawio.py dihapus (digantikan emisi native)")


if __name__ == "__main__":
    main()
