"""Generator artefak hulu SDD: BPMN-01 (to-be), UCD-01, AD-01..AD-04.

Layout memakai kolom header lane (x 20..170) + grid isi (kolom 200/400/600/800) supaya
label lane tidak tertimpa task, dan router otomatis menjaga label aliran berada di dalam
band lane (tidak menempel garis lane).

Keluaran: SVG + HTML + .drawio di ../diagrams_upstream/.
Jalankan: python gen_upstream.py
"""

import pathlib

FS_LANE, FS_TASK, FS_FLOW, FS_ACTOR, FS_NOTE = 14, 14, 13, 15, 12
LANE_FS = 14                     # ukuran font judul lane draw.io (default)
HEAD_W = 185
COLS = [250, 450, 650]
NODE_W, NODE_H = 175, 58
GW = 84


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


class Canvas:
    def __init__(self, w, h):
        self.w, self.h, self.items, self.cells = w, h, [], []
        self.node_box, self.lane_bands = {}, []

    # ---------------------------------------------------------------- lane
    def swimlane(self, name, y, h):
        self.items.append(f'  <rect x="20" y="{y}" width="{self.w - 50}" height="{h}" class="pool"/>')
        self.items.append(f'  <rect x="20" y="{y}" width="{HEAD_W}" height="{h}" class="lane-head"/>')
        lines = name.split(" | ")
        for i, ln in enumerate(lines):
            self.items.append(f'  <text x="{20 + HEAD_W / 2}" y="{y + h / 2 + 5 + (i - (len(lines) - 1) / 2) * 16}" '
                              f'class="lane-name">{esc(ln)}</text>')
        self.lane_bands.append((y, y + h, name))
        self.cells.append(dict(kind="lane", x=20, y=y, w=self.w - 50, h=h, label=" | ".join(lines)))

    def band_for(self, y):
        for y0, y1, _ in self.lane_bands:
            if y0 <= y < y1:
                return y0, y1
        return 20, self.h - 20

    # --------------------------------------------------------------- node
    def _em(self, text, fs=FS_TASK):
        """Perkiraan lebar teks (px) dengan metrik kasar Times New Roman."""
        w = 0.0
        for ch in text:
            w += 0.28 if ch == " " else (0.62 if (ch.isupper() or ch.isdigit()) else 0.50)
        return w * fs

    def _fit_fs(self, lines, width, fs=FS_TASK, floor=9.0):
        """Font terkecil agar baris terpanjang masih muat; teks tidak boleh luber keluar kotak."""
        longest = max((self._em(l, fs) for l in lines), default=0)
        return fs if longest <= width else max(floor, fs * width / longest)

    @staticmethod
    def _wrap(text, maxchars=23):
        """Pecah label panjang agar lebarnya tidak melewati kotak aktivitas (175 px)."""
        if len(text) <= maxchars:
            return [text]
        words, out, cur = text.split(" "), [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > maxchars and cur:
                out.append(cur); cur = wd
            else:
                cur = f"{cur} {wd}".strip()
        out.append(cur)
        return out

    def task(self, key, label, x, y, kind="task"):
        cls = "bpmn-task" if kind == "task" else "act-node"
        lines = [l for raw in label.split("\n") for l in self._wrap(raw)]      # teks tidak boleh luber dari kotak
        node_h = max(NODE_H, 14 + 16 * len(lines))
        fs = self._fit_fs(lines, NODE_W - 14)
        shrink = f' style="font-size:{fs:.1f}px"' if fs < FS_TASK else ""
        self.items.append(f'  <rect x="{x}" y="{y}" width="{NODE_W}" height="{node_h}" rx="10" class="{cls}"/>')
        for i, ln in enumerate(lines):
            self.items.append(f'  <text x="{x + NODE_W / 2}" y="{y + NODE_H / 2 + 5 + (i - (len(lines) - 1) / 2) * 15}" '
                              f'class="task-text"{shrink}>{esc(ln)}</text>')
        self.node_box[key] = (x, y, x + NODE_W, y + node_h)
        self.cells.append(dict(kind="task", x=x, y=y, w=NODE_W, h=node_h,
                               label="\n".join(lines), fs=fs))

    def gateway(self, key, label, x, y):
        self.items.append(f'  <path d="M {x + GW / 2} {y} L {x + GW} {y + GW / 2} L {x + GW / 2} {y + GW} '
                          f'L {x} {y + GW / 2} Z" class="gw"/>')
        lines = label.split("\n")
        for i, ln in enumerate(lines):
            self.items.append(f'  <text x="{x + GW / 2}" y="{y + GW / 2 + 5 + (i - (len(lines) - 1) / 2) * 14}" '
                              f'class="gw-text">{esc(ln)}</text>')
        self.node_box[key] = (x, y, x + GW, y + GW)
        self.cells.append(dict(kind="gateway", x=x, y=y, w=GW, h=GW, label=label))

    def event(self, key, x, y, kind="start", r=18):
        self.items.append(f'  <circle cx="{x + r}" cy="{y + r}" r="{r}" class="{"ev-start" if kind == "start" else "ev-end"}"/>')
        if kind == "end":
            self.items.append(f'  <circle cx="{x + r}" cy="{y + r}" r="{r - 6}" class="ev-inner"/>')
        self.node_box[key] = (x, y, x + 2 * r, y + 2 * r)
        self.cells.append(dict(kind="event", x=x, y=y, w=2 * r, h=2 * r, label="", start=(kind == "start")))

    def store(self, key, title, x, y, w, h):
        self.items.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="store"/>')
        self.items.append(f'  <text x="{x + 14}" y="{y + 24}" class="store-title">{esc(title)}</text>')
        lines = [l for l in self.extra_store_lines]
        for i, ln in enumerate(lines):
            self.items.append(f'  <text x="{x + 14}" y="{y + 44 + i * 15}" class="store-text">{esc(ln)}</text>')
        self.node_box[key] = (x, y, x + w, y + h)
        self.cells.append(dict(kind="store", x=x, y=y, w=w, h=h, label="\n".join([title] + lines)))

    # --------------------------------------------------------------- flow
    def free_x(self, y0, y1, exclude):
        """Cari x koridor yang tidak menembus kotak mana pun di rentang y0..y1."""
        lo, hi = sorted((y0, y1))
        cand = []
        for x in range(int(HEAD_W) + 40, self.w - 60, 12):
            ok = True
            for key, (a, b, c, d) in self.node_box.items():
                if key in exclude or c < 20:
                    continue
                if a - 16 <= x <= c + 16 and not (d < lo - 4 or b > hi + 4):
                    ok = False
                    break
            if ok:
                cand.append(x)
        return cand

    def flow(self, src, dst, label=None, guard=None, dashed=False, via="auto", side="right"):
        """Router sederhana: keluar dari sisi `side` sumber, masuk sisi kiri/atas tujuan."""
        x1, y1, x2, y2 = self.node_box[src]
        tx1, ty1, tx2, ty2 = self.node_box[dst]
        sy = (y1 + y2) / 2
        ty = (ty1 + ty2) / 2
        same_band = self.band_for(sy)[0] == self.band_for(ty)[0]
        if dashed and same_band:
            # alur balik dilewatkan di bawah baris node, tetap di dalam lane
            y_route = self.band_for(sy)[1] - 22
            sx_c, tx_c = (x1 + x2) / 2, (tx1 + tx2) / 2
            pts = [(sx_c, y2), (sx_c, y_route), (tx_c, y_route), (tx_c, ty2)]
            self.polyline(pts, label, dashed)
            return pts
        if side == "right":
            pts = [(x2, sy)]
        else:
            pts = [(x1, sy)]
        if same_band:
            if ty_target_right := (tx1 > x2):
                pts += [(tx1, sy), (tx1, ty)]
            else:
                pts += [(tx2, sy), (tx2, ty)]
        else:
            if via == "auto":
                cands = self.free_x(sy, ty, {src, dst})
                want = (x2 + tx1) / 2 if tx1 > x2 else x2 + 40
                via_x = min(cands, key=lambda v: abs(v - want)) if cands else want
            else:
                via_x = via
            pts += [(via_x, sy), (via_x, ty)]
            pts += [(tx1 if tx1 > via_x else tx2, ty)]
        self.polyline(pts, label, dashed)
        return pts

    def polyline(self, pts, label=None, dashed=False, arrow=True, closed=False, arrow_open=False):
        self._last_label_pos = None
        pts = [pts[0]] + [p for i, p in enumerate(pts[1:], 1) if p != pts[i - 1]]
        d = " ".join(f"{'M' if i == 0 else 'L'} {p[0]:.0f} {p[1]:.0f}" for i, p in enumerate(pts))
        self.items.append(f'  <path d="{d}" class="{"flow-dashed" if dashed else "flow"}"/>')
        if arrow:
            (x2, y2), (x1, y1) = pts[-1], pts[-2]
            dx, dy = x2 - x1, y2 - y1
            n = max(abs(dx), abs(dy)) or 1
            ux, uy = dx / n, dy / n
            px, py = -uy, ux
            self.items.append(f'  <path d="M {x2:.0f} {y2:.0f} L {x2 - ux * 11 + px * 5:.0f} {y2 - uy * 11 + py * 5:.0f} '
                              f'L {x2 - ux * 11 - px * 5:.0f} {y2 - uy * 11 - py * 5:.0f} Z" '
                              f'class="{"arrow-open" if dashed else "arrow"}"/>')
        if label:
            # label pada segmen terpanjang, digeser tegak lurus 14 px
            best, blen = None, -1
            for a, b in zip(pts[:-1], pts[1:]):
                L = abs(a[0] - b[0]) + abs(a[1] - b[1])
                if L > blen:
                    best, blen = (a, b), L
            (a, b) = best
            vertical = abs(a[0] - b[0]) < 1
            lx = ly = None
            for t in (0.5, 0.35, 0.65, 0.2, 0.8):
                mx, my = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                cand = (mx + (-16 if vertical else 0), my + (0 if vertical else -14))
                w0 = int(len(label) * FS_FLOW * 0.52) + 10
                box = (cand[0] - w0 / 2, cand[1] - 11, cand[0] + w0 / 2, cand[1] + 11)
                if not any(box[2] > a2 and box[0] < c2 and box[3] > b2 and box[1] < d2
                           for (a2, b2, c2, d2) in self.node_box.values()):
                    lx, ly = cand
                    break
            if lx is None:
                lx, ly = (a[0] + b[0]) / 2 + (-16 if vertical else 0), (a[1] + b[1]) / 2 + (0 if vertical else -14)
            y0, y1b = self.band_for(ly)
            ty_lab = min(max(ly, y0 + 22), y1b - 12)
            w = int(len(label) * FS_FLOW * 0.52) + 10
            # geser label bila kotaknya jatuh di atas kotak aktivitas/gateway
            def clash(cx, cy):
                return any(cx - w / 2 < bx2 and cx + w / 2 > bx1 and cy - 9 < by2 and cy + 9 > by1
                           for (bx1, by1, bx2, by2) in self.node_box.values())
            for dx, dy in ((0, 0), (0, -20), (0, -38), (0, 20), (0, 38), (-w, 0), (w, 0)):
                if not clash(lx + dx, ty_lab + dy):
                    lx, ty_lab = lx + dx, ty_lab + dy
                    break
            self.items.append(f'  <rect x="{lx - w / 2}" y="{ty_lab - 11}" width="{w}" height="17" class="label-bg"/>')
            self.items.append(f'  <text x="{lx}" y="{ty_lab + 2}" class="flow-label">{esc(label)}</text>')
            self._last_label_pos = (lx, ty_lab)
        self.cells.append(dict(kind="flow", pts=pts, label=label, dashed=dashed,
                               arrow_open=arrow_open,
                               label_pos=(getattr(self, "_last_label_pos", None) if label else None)))

    def note(self, text, x, y, w):
        lines = text.split("\n")
        h = 20 + len(lines) * 16
        self.h = max(self.h, y + h + 8)          # kanvas ikut tumbuh: catatan tidak boleh terpotong
        self.items.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="note"/>')
        for i, ln in enumerate(lines):
            self.items.append(f'  <text x="{x + 12}" y="{y + 20 + i * 16}" class="note-text">{esc(ln)}</text>')
        self.cells.append(dict(kind="note", x=x, y=y, w=w, h=h, label=text))

    def actor(self, name, x, y):
        self.items += [f'  <circle cx="{x}" cy="{y}" r="13" class="actor"/>',
                       f'  <path d="M {x} {y + 13} L {x} {y + 44} M {x - 18} {y + 24} L {x + 18} {y + 24} '
                       f'M {x} {y + 44} L {x - 14} {y + 68} M {x} {y + 44} L {x + 14} {y + 68}" class="actor"/>']
        for i, ln in enumerate(name.split("\n")):
            self.items.append(f'  <text x="{x}" y="{y + 86 + i * 15}" class="actor-name">{esc(ln)}</text>')
        self.cells.append(dict(kind="actor", x=x - 22, y=y - 14, w=44, h=110, label=name))

    def usecase(self, key, name, cx, cy, w=330, h=58):
        self.items.append(f'  <ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" class="uc"/>')
        for i, ln in enumerate(name.split("\n")):
            self.items.append(f'  <text x="{cx}" y="{cy + 5 + (i - (len(name.splitlines()) - 1) / 2) * 15}" '
                              f'class="task-text">{esc(ln)}</text>')
        self.node_box[key] = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        self.cells.append(dict(kind="usecase", x=cx - w / 2, y=cy - h / 2, w=w, h=h, label=name))

    def boundary(self, label, x, y, w, h):
        self.items.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" class="boundary"/>')
        self.items.append(f'  <text x="{x + w / 2}" y="{y + 26}" class="boundary-name">{esc(label)}</text>')
        self.cells.append(dict(kind="boundary", x=x, y=y, w=w, h=h, label=label))

    # ------------------------------------------------------------- output
    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}">')
        return "\n".join([head, "  <defs>", "    <style>", STYLE.strip(), "    </style>", "  </defs>",
                          f'  <rect width="{self.w}" height="{self.h}" fill="#FFFFFF"/>'] + self.items + ["</svg>"])

    DRAWIO_STYLE = {
        "lane": "swimlane;horizontal=0;html=1;verticalAlign=middle;startSize=160;fillColor=#E8E8E8;"
                "swimlaneFillColor=#FFFFFF;strokeColor=#000000;fontStyle=1;fontSize=14;",
        "task": "rounded=1;whiteSpace=wrap;html=1;arcSize=14;fillColor=#FFFFFF;strokeColor=#000000;fontSize=14;",
        "gateway": "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=14;",
        "event": "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;",
        "store": "shape=datastore;whiteSpace=wrap;html=1;fillColor=#FBFBFB;strokeColor=#000000;align=left;"
                 "verticalAlign=top;spacingLeft=8;spacingTop=6;fontSize=13;",
        "actor": "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fontSize=13;fontStyle=1;",
        "usecase": "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=13;",
        "boundary": "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=1.5;"
                    "align=center;verticalAlign=top;spacingTop=6;dashed=0;fontSize=14;fontStyle=1;",
        "note": "shape=note;whiteSpace=wrap;html=1;size=12;fillColor=#FFFFFF;strokeColor=#000000;align=left;"
                "verticalAlign=top;spacingLeft=8;spacingTop=6;fontSize=12;",
    }

    @staticmethod
    def _label(text):
        """Escape sekali saja; baris baru jadi <br> untuk label HTML draw.io."""
        return esc(text).replace("\n", "&lt;br&gt;")

    def lane_style(self, label, h):
        """Style lane dengan fontSize yang dikecilkan otomatis bila perlu.

        draw.io menggambar judul swimlane horizontal=0 secara terputar di dalam band
        selebar startSize; panjang teks mengikuti TINGGI lane. Label yang lebih panjang
        dari tinggi lane meluber menembus lane tetangga (tampak tumpang tindih), jadi
        font dikecilkan sampai muat.
        """
        fs = LANE_FS
        need = self._em(label, LANE_FS)
        if need > h - 12:
            fs = max(9.0, LANE_FS * (h - 12) / need)
        style = self.DRAWIO_STYLE["lane"]
        return style if fs >= LANE_FS else style.replace(f"fontSize={LANE_FS};", f"fontSize={fs:.1f};")

    def drawio(self, name):
        rows = []
        for i, c in enumerate(self.cells, 1):
            cid = f"c{i}"
            if c["kind"] == "flow":
                pts = c["pts"]
                off = ""
                if c["label"] and c.get("label_pos"):
                    mx = sum(p[0] for p in pts) / len(pts) if False else (pts[0][0] + pts[-1][0]) / 2
                    my = (pts[0][1] + pts[-1][1]) / 2
                    off = (f'<mxPoint x="{int(c["label_pos"][0] - mx)}" y="{int(c["label_pos"][1] - my)}" '
                           f'as="offset"/>')
                dash = 1 if c.get("dashed") else 0
                head = ("endArrow=open;endFill=0;" if c.get("arrow_open")
                        else "endArrow=block;endFill=1;")
                style = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;strokeWidth=1.5;"
                         f"{head}dashed={dash};fontSize=12;fontStyle=2;labelBackgroundColor=#FFFFFF;")
                rows.append(
                    f'        <mxCell id="{cid}" value="{self._label(c["label"] or "")}" style="{style}" edge="1" parent="1">\n'
                    f'          <mxGeometry relative="1" as="geometry">\n            <Array as="points">'
                    + "".join(f'<mxPoint x="{int(x)}" y="{int(y)}"/>' for x, y in pts[1:-1])
                    + f'</Array>\n            <mxPoint x="{int(pts[0][0])}" y="{int(pts[0][1])}" as="sourcePoint"/>\n'
                      f'            <mxPoint x="{int(pts[-1][0])}" y="{int(pts[-1][1])}" as="targetPoint"/>\n'
                      f'            {off}\n          </mxGeometry>\n        </mxCell>')
            else:
                style = self.DRAWIO_STYLE[c["kind"]]
                if c["kind"] == "lane":
                    style = self.lane_style(c.get("label", ""), c["h"])
                if c["kind"] == "task" and c.get("fs", FS_TASK) < FS_TASK:
                    style = style.replace(f"fontSize={FS_TASK};", f"fontSize={c['fs']:.1f};")
                if c["kind"] == "event" and not c.get("start"):
                    style = ("ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;strokeWidth=3;")
                rows.append(f'        <mxCell id="{cid}" value="{self._label(c.get("label", ""))}" style="{style}" '
                            f'vertex="1" parent="1">\n          <mxGeometry x="{int(max(0, c["x"]))}" '
                            f'y="{int(max(0, c["y"]))}" width="{int(c["w"])}" height="{int(c["h"])}" as="geometry"/>\n'
                            f'        </mxCell>')
        return ('<mxfile host="app.diagrams.net" agent="Antigravity" version="24.0.0">\n'
                f'  <diagram name="{esc(name)}" id="d1">\n'
                f'    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" '
                f'background="#ffffff">\n      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n'
                + "\n".join(rows) + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n")


Canvas.extra_store_lines = []

STYLE = f"""
      .pool {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.4; }}
      .lane-head {{ fill: #E8E8E8; stroke: #000000; stroke-width: 1.4; }}
      .lane-name {{ font-family: 'Times New Roman', serif; font-size: {FS_LANE}px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .bpmn-task {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }}
      .act-node {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }}
      .gw {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }}
      .gw-text {{ font-family: 'Times New Roman', serif; font-size: 14px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .ev-start {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.8; }}
      .ev-end {{ fill: #FFFFFF; stroke: #000000; stroke-width: 2.6; }}
      .ev-inner {{ fill: #000000; stroke: none; }}
      .store {{ fill: #FBFBFB; stroke: #000000; stroke-width: 1.5; }}
      .store-title {{ font-family: 'Times New Roman', serif; font-size: 14px; font-weight: bold; fill: #000000; }}
      .store-text {{ font-family: 'Consolas', 'Courier New', monospace; font-size: 12px; fill: #000000; }}
      .task-text {{ font-family: 'Times New Roman', serif; font-size: {FS_TASK}px; fill: #000000; text-anchor: middle; }}
      .actor {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.6; }}
      .actor-name {{ font-family: 'Times New Roman', serif; font-size: {FS_ACTOR}px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .uc {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }}
      .boundary {{ fill: #FCFCFC; stroke: #000000; stroke-width: 1.6; }}
      .boundary-name {{ font-family: 'Times New Roman', serif; font-size: 15px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .flow {{ fill: none; stroke: #000000; stroke-width: 1.6; }}
      .flow-dashed {{ fill: none; stroke: #000000; stroke-width: 1.4; stroke-dasharray: 7 5; }}
      .arrow {{ fill: #000000; stroke: none; }}
      .arrow-open {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.2; }}
      .label-bg {{ fill: #FFFFFF; }}
      .flow-label {{ font-family: 'Times New Roman', serif; font-size: {FS_FLOW}px; font-style: italic; fill: #000000; text-anchor: middle; }}
      .note {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.1; }}
      .note-text {{ font-family: 'Times New Roman', serif; font-size: {FS_NOTE}px; fill: #000000; }}
"""

HTML = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        'body{margin:0;padding:0;background:#fff;}svg{display:block;}</style></head><body>\n__SVG__\n</body></html>')

LANE_H = 150


def row_y(lane_top):
    return lane_top + (LANE_H - NODE_H) // 2


# ------------------------------------------------------------------- BPMN-01
def bpmn():
    """Kanvas 1180 px: 5 lane satu baris, kolom 250/450/650/850/1050 — tidak ada kotak bertumpuk,
    dan alur pada lane Admin berjalan monoton ke kanan (verifikasi -> layak? -> tolak/tugaskan -> beban?)."""
    c = Canvas(1180, 1050)
    lanes = ["Klien", "Admin", "Eksekutor", "Tinjauan Klien", "Staf Medsos"]
    for i, name in enumerate(lanes):
        c.swimlane(name, 30 + i * LANE_H, LANE_H)
    c.event("start", 203, 87)
    c.task("t1", "Isi formulir\nmulti-kanal + aset", 250, 76)
    c.gateway("g1", "SLA?", 450, 63)
    c.task("t2", "Isi alasan darurat\n(Rush Order)", 650, 76)
    c.task("t3", "Verifikasi brief\ndan aset", 250, 226)
    c.gateway("g2", "layak?", 450, 213)
    c.task("t4", "Tolak / minta\nrevisi brief", 650, 226)
    c.task("t5", "Tugaskan eksekutor\n(lihat beban aktif)", 850, 226)
    c.gateway("g3", "beban\n≤ 3?", 1050, 213)
    c.task("t6", "Kerjakan konten\nsesuai brief", 250, 376)
    c.task("t7", "Unggah draf\nv1 / v2", 450, 376)
    c.task("t8", "Tinjau draf: setujui\natau ajukan revisi", 250, 526)
    c.gateway("g4", "revisi\n< 2?", 450, 513)
    c.task("t9", "Catat tautan tayang\n+ tanggal terbit", 250, 676)
    c.event("end", 650, 690, kind="end")
    c.extra_store_lines = ["TIKET_PESANAN, BERKAS_ASET, DRAF_KARYA,", "RIWAYAT_REVISI, RIWAYAT_PENUGASAN, PUBLIKASI_KONTEN"]
    c.store("ds", "Data Store", 30, 820, 1120, 70)

    c.flow("start", "t1")
    c.flow("t1", "g1", "permohonan")
    c.flow("g1", "t2", "tidak")
    c.polyline([(492, 147), (492, 170), (300, 170), (300, 226)], "ya")
    c.polyline([(737, 134), (737, 170), (390, 170), (390, 226)], "lanjut")
    c.flow("t3", "g2", "periksa brief")
    c.flow("g2", "t4", "tidak")
    c.polyline([(492, 213), (492, 196), (937, 196), (937, 226)], "ya")
    c.flow("t5", "g3")
    c.polyline([(1092, 255), (1092, 350), (337, 350), (337, 376)], "ya")
    c.polyline([(1092, 297), (1140, 314), (1140, 365), (937, 365), (937, 284)], "tidak (override)", dashed=True)
    c.flow("t6", "t7", "draf v1 / v2")
    c.polyline([(537, 434), (537, 500), (337, 500), (337, 526)], "unggah draf")
    c.flow("t8", "g4", "tinjau")
    c.polyline([(492, 597), (492, 616), (1120, 616), (1120, 405), (625, 405)], "revisi (BR-02)", dashed=True)
    c.polyline([(534, 555), (700, 555), (700, 705), (425, 705)], "setuju final")
    c.flow("t9", "end", "Published + auto-purge")
    c.polyline([(1025, 255), (1140, 255), (1140, 820), (1120, 820)], "baca & tulis tiket", dashed=True)
    c.note("To-be: seluruh pemesanan lewat sistem (PC-01 §2.0). SLA H-4/H-5/H-7 menurut kanal dan jenis konten (BR-01);\n"
           "kuota revisi maksimal 2 (BR-02); penugasan hanya oleh Admin (BR-03); beban aktif maksimal 3 (BR-04);\n"
           "berkas fisik aset dihapus setelah status Published dengan metadata tetap (BR-05).", 30, 910, 1120)
    return c, "BPMN-01 Proses To-Be Layanan Pemesanan Konten Medkreminfo"


# ------------------------------------------------------------------- UCD-01
def ucd():
    c = Canvas(980, 800)
    c.boundary("Sistem Informasi Layanan Pemesanan Konten Medkreminfo", 250, 60, 480, 660)
    c.actor("Klien\n(14 Kementerian)", 110, 100)
    c.actor("Admin\n(Menteri Medkreminfo)", 110, 300)
    c.actor("Eksekutor\n(staf Medkreminfo)", 870, 240)
    c.actor("Staf Publikasi\nMedsos", 870, 440)
    c.usecase("uc1", "UC-01 Pengajuan Tiket Request Konten", 490, 140)
    c.usecase("uc2", "UC-02 Validasi dan Penugasan Tiket", 490, 260)
    c.usecase("uc3", "UC-03 Pengerjaan dan Unggah Draf Karya", 490, 380)
    c.usecase("uc4", "UC-04 Tinjauan Draf, Persetujuan,\ndan Publikasi", 490, 500)
    c.usecase("uc5", "Validasi SLA & Rush Order", 490, 600, 300, 52)
    c.usecase("uc6", "Validasi kuota revisi", 490, 670, 280, 48)
    c.polyline([(132, 140), (325, 140)])                                    # Klien — UC-01
    c.polyline([(132, 300), (325, 260)])                                    # Admin — UC-02
    c.polyline([(848, 280), (655, 380)])                                    # Eksekutor — UC-03
    c.polyline([(848, 490), (655, 500)])                                    # Staf Publikasi — UC-04
    c.polyline([(110, 190), (205, 190), (205, 500), (325, 500)])            # Klien — UC-04 (SRS §6.2)
    c.polyline([(325, 150), (300, 150), (300, 600), (340, 600)], "<<include>>", dashed=True, arrow_open=True)
    c.polyline([(350, 670), (312, 670), (312, 515), (350, 515)], "<<extend>>", dashed=True, arrow_open=True)
    c.note("Aktor dan use case selaras SRS §2.1 dan §6.2. UC-01 memuat «include» Validasi SLA & Rush Order (BR-01);\n"
           "helper Validasi kuota revisi memperluas UC-04 (BR-02). Klien terhubung ke UC-01 dan UC-04 (peninjauan draf\n"
           "dan persetujuan final). AD-01..AD-04 memodelkan alur tiap use case; SD-01..SD-04 ada di Bab 3.", 30, 738, 700)
    return c, "UCD-01 Use Case Diagram Sistem Layanan Pemesanan Konten"


# ------------------------------------------------------------- activity AD-xx
def activity(title, lanes, build, notes, height):
    c = Canvas(980, height)
    for i, name in enumerate(lanes):
        c.swimlane(name, 30 + i * LANE_H, LANE_H)
    build(c)
    c.note(notes, 30, height - 62, 920)
    return c, title


def ad01():
    def build(c):
        c.event("start", HEAD_W + 18, 30 + (LANE_H - 36) // 2)
        c.task("t1", "Isi kanal, jenis konten,\ntanggal tayang, brief", COLS[0], 30 + 46)
        c.gateway("g1", "SLA?", COLS[1] + 20, 30 + 36)
        c.task("t2", "Isi alasan darurat\n(Rush Order)", COLS[2], 30 + 46)
        c.task("t3", "Unggah aset / tautan\npenyimpanan awan", COLS[0], 180 + 46)
        c.gateway("g2", "valid?", COLS[1] + 20, 180 + 36)
        c.task("t4", "Pilih berkas\npengganti", COLS[2], 180 + 46)
        c.task("t5", "Simpan tiket\n(status Submitted)", COLS[0], 330 + 46)
        c.task("t6", "Terbitkan ID tiket\n#MED-YYYYMM-XXX", COLS[1] - 10, 330 + 46)
        c.task("t7", "Simpan berkas aset\n(status_purge = false)", COLS[2], 330 + 46)
        c.event("end", COLS[2] + 230, 330 + 46, kind="end")
        c.flow("start", "t1")
        c.flow("t1", "g1", "formulir")
        c.flow("g1", "t2", "tidak", side="right")
        c.flow("g1", "t3", "ya", side="left", via=COLS[0] + 90)
        c.flow("t2", "t3", "lanjutkan", side="left", via=COLS[2] + 90)
        c.flow("t3", "g2", "periksa berkas")
        c.flow("g2", "t4", "tidak", side="right")
        c.flow("t4", "t3", "unggah ulang", dashed=True)
        c.flow("g2", "t5", "valid", side="left", via=COLS[0] + 90)
        c.flow("t5", "t6", "20 ajukan(...)")
        c.flow("t6", "t7", "21 simpanBerkas(...)")
        c.flow("t7", "end", "tiket + aset tersimpan")
    return activity("AD-01 Activity Diagram UC-01 Pengajuan Tiket Request Konten (realisasi SD-01)",
                    ["Klien", "Controller", "TIKET_PESANAN"], build,
                    "Turunan dari narasi UC-01 (SRS §6.2) dan SD-01. Gate BR-01 (SLA) dan BR-05 (format/ukuran berkas).", 620)


def ad02():
    def build(c):
        c.event("start", HEAD_W + 18, 30 + (LANE_H - 36) // 2)
        c.task("t1", "Periksa brief\ndan aset", COLS[0], 30 + 46)
        c.gateway("g1", "layak?", COLS[1] + 20, 30 + 36)
        c.task("t2", "Tolak / minta\nrevisi brief", COLS[2], 30 + 46)
        c.task("t3", "Muat daftar eksekutor\n+ beban aktif", COLS[0], 180 + 46)
        c.gateway("g2", "≤ 3?", COLS[1] + 20, 180 + 36)
        c.task("t4", "Konfirmasi\noverride manajerial", COLS[2], 180 + 46)
        c.task("t5", "Tugaskan tiket\n(status Assigned)", COLS[0], 330 + 46)
        c.task("t6", "Catat RIWAYAT_PENUGASAN\n(jenis = awal / mutasi)", COLS[1] - 10, 330 + 46)
        c.event("end", COLS[2] + 230, 330 + 46, kind="end")
        c.flow("start", "t1")
        c.flow("t1", "g1", "antrean Submitted")
        c.flow("g1", "t2", "tidak", side="right")
        c.flow("t2", "t1", "brief diperbaiki Klien", dashed=True)
        c.flow("g1", "t3", "ya", side="left", via=COLS[0] + 90)
        c.flow("t3", "g2", "hitung beban")
        c.flow("g2", "t4", "tidak", side="right")
        c.flow("t4", "t5", "override disetujui", side="left", via=COLS[2] + 90)
        c.flow("g2", "t5", "ya", side="left", via=COLS[0] + 90)
        c.flow("t5", "t6", "23 tugaskan()")
        c.flow("t6", "end", "status Assigned (BR-03)")
    return activity("AD-02 Activity Diagram UC-02 Validasi dan Penugasan Tiket (realisasi SD-02)",
                    ["Admin", "Controller", "TIKET_PESANAN"], build,
                    "Turunan dari narasi UC-02 (SRS §6.2) dan SD-02. Gate BR-03 (otoritas Admin) dan BR-04 (beban ≤ 3 tiket aktif).", 620)


def ad03():
    def build(c):
        c.event("start", HEAD_W + 18, 30 + (LANE_H - 36) // 2)
        c.task("t1", "Buka \"Tugas Saya\",\nunduh aset", COLS[0], 30 + 46)
        c.task("t2", "Mulai pengerjaan\n(status In Progress)", COLS[1] - 10, 30 + 46)
        c.task("t3", "Unggah draf\n(gambar / tautan)", COLS[0], 180 + 46)
        c.gateway("g1", "valid?", COLS[1] + 20, 180 + 36)
        c.task("t4", "Perbaiki tautan\npratinjau", COLS[2], 180 + 46)
        c.task("t5", "Tentukan versi\ndraf (v1 / v2)", COLS[0], 330 + 46)
        c.task("t6", "Ubah status\ntiket", COLS[1] - 10, 330 + 46)
        c.event("end", COLS[2] + 230, 330 + 46, kind="end")
        c.flow("start", "t1")
        c.flow("t1", "t2", "14 ubahStatus(\"In Progress\")")
        c.flow("t2", "t3", "kerjakan konten", side="left", via=COLS[0] + 90)
        c.flow("t3", "g1", "unggah draf")
        c.flow("g1", "t4", "tidak", side="right")
        c.flow("t4", "t3", "unggah ulang", dashed=True)
        c.flow("g1", "t5", "valid", side="left", via=COLS[0] + 90)
        c.flow("t5", "t6", "17 versiBerikutnya()")
        c.flow("t6", "end", "status Review (IC-12)")
    return activity("AD-03 Activity Diagram UC-03 Pengerjaan dan Unggah Draf Karya (realisasi SD-03)",
                    ["Eksekutor", "Controller", "DRAF_KARYA"], build,
                    "Turunan dari narasi UC-03 (SRS §6.2) dan SD-03. Gate BR-04 (hanya tiket yang ditugaskan) dan IC-12 (versi unik).", 620)


def ad04():
    def build(c):
        c.event("start", HEAD_W + 18, 30 + (LANE_H - 36) // 2)
        c.task("t1", "Buka detail tiket\ndan draf terbaru", COLS[0], 30 + 46)
        c.task("t2", "Periksa draf +\nsisa kuota revisi", COLS[1] - 10, 30 + 46)
        c.gateway("g1", "setuju?", COLS[2] + 20, 30 + 36)
        c.task("t3", "Catat revisi\n(revisi_ke = 1 atau 2)", COLS[0], 180 + 46)
        c.task("t4", "Ubah status\nRevision", COLS[1] - 10, 180 + 46)
        c.gateway("g2", "kuota?", COLS[2] + 20, 180 + 36)
        c.task("t5", "Nonaktifkan tombol\nrevisi (kuota habis)", COLS[0], 330 + 46)
        c.task("t6", "Ubah status\nReady to Post", COLS[1] - 10, 330 + 46)
        c.task("t7", "Catat tautan tayang\n+ tanggal terbit", COLS[0], 480 + 46)
        c.task("t8", "Tutup tiket (Published)\ndan auto-purge aset", COLS[1] - 10, 480 + 46)
        c.event("end", COLS[2] + 230, 480 + 46, kind="end")
        c.flow("start", "t1")
        c.flow("t1", "t2", "buka tinjauan")
        c.flow("t2", "g1", "8 hitungSisaKuotaRevisi()")
        c.flow("g1", "t3", "tidak", side="left", via=COLS[0] + 90)
        c.flow("t3", "t4", "9 catatRevisi()")
        c.flow("t4", "g2", "status Revision")
        c.flow("g2", "t5", "tidak", side="left", via=COLS[0] + 90)
        c.flow("t5", "t1", "kembali ke tinjauan Klien", dashed=True)
        c.flow("g2", "t6", "ya → draf diperbaiki", side="left", via=COLS[1] + 120)
        c.flow("g1", "t6", "ya (BR-02)", side="right", via=COLS[2] + 90)
        c.flow("t6", "t7", "16 ubahStatus(\"Ready to Post\")", side="left", via=COLS[0] + 90)
        c.flow("t7", "t8", "21 tutupTiket(url)")
        c.flow("t8", "end", "22 purgeBerkas() (BR-05)")
    return activity("AD-04 Activity Diagram UC-04 Tinjauan Draf, Persetujuan Akhir, dan Publikasi (realisasi SD-04)",
                    ["Klien", "Controller", "TIKET_PESANAN", "Staf Medsos"], build,
                    "Turunan dari narasi UC-04 (SRS §6.2) dan SD-04. Gate BR-02 (kuota revisi maksimal 2) dan BR-05 (auto-purge aset).", 800)


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "diagrams_upstream"
    out.mkdir(exist_ok=True)
    jobs = [("bpmn01", bpmn, "BPMN-01"), ("ucd01", ucd, "UCD-01"),
            ("ad01", ad01, "AD-01"), ("ad02", ad02, "AD-02"), ("ad03", ad03, "AD-03"), ("ad04", ad04, "AD-04")]
    for key, fn, label in jobs:
        c, title = fn()
        svg = c.svg()
        (out / f"{key}.svg").write_text(svg, encoding="utf-8")
        (out / f"{key}.html").write_text(HTML.replace("__SVG__", svg), encoding="utf-8")
        # .drawio per diagram tidak ditulis: bundel 13 tab dibuat oleh make_drawio.py
        print(f"{key}: {c.w}x{c.h} | {len(c.cells)} sel drawio | teks tugas 14px = {14 * 6.2 * 72 / c.w:.1f} pt @6,2in")
