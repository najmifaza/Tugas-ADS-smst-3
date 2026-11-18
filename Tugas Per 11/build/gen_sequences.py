"""Render diagram sekuens SDD dari blok Mermaid di berkas .md menjadi SVG buatan sendiri.

Alasan: raster Mermaid untuk 6 lifeline melebar ~1816 px, sehingga teks pesan hanya ~3.7 pt
saat dicetak. Generator ini memakai kanvas 950 px dengan teks pesan 14 px == 6.2 pt pada
lebar 5.8 in.

Jalankan: python gen_sequences.py   -> images/seq_diagram_sd0x.svg (render PNG via Edge headless)
"""

import pathlib
import re

CANVAS_W = 950
PART_FS = 15
MSG_FS = 14
ROW = 30
TOP = 16
PAD_X = 20
HEAD_H = 44
CENTER = HEAD_H // 2


def parse(block):
    """Ubah blok mermaid sequenceDiagram menjadi struktur data sederhana."""
    parts, steps = [], []
    for raw in block.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        m = re.match(r"(?:participant|actor)\s+(\w+)\s+as\s+(.+)", s)
        if m:
            parts.append((m.group(1), m.group(2).strip()))
            continue
        m = re.match(r"(\w+)-{1,2}>>?(\w+)\s*:\s*(?:\d+\s+)?(.*)", s)
        if m:
            src, dst, text = m.groups()
            kind = "return" if "--" in s.split(":", 1)[0] else "call"
            steps.append(dict(kind="msg", mtype=kind, src=src, dst=dst, text=text.strip()))
            continue
        m = re.match(r"(alt|opt|else|end)\b\s*(.*)", s)
        if m:
            steps.append(dict(kind=m.group(1), text=m.group(2).strip()))
    return parts, steps


def pads(canvas_w, n):
    """Pad kiri/kanan menyesuaikan lebar header: header paling kiri tidak keluar kanvas."""
    pad = PAD_X
    for _ in range(3):
        spacing = (canvas_w - 2 * pad) / max(n - 1, 1)
        hw = min(150, int(spacing) - 6)
        pad = max(PAD_X, hw // 2 + 8)
    return pad


def head_width(canvas_w, n):
    """Lebar kotak header lifeline (dipakai bersama SVG dan drawio).
    Spasi harus memakai pad dinamis, kalau tidak header 150 px lebih lebar dari jarak antar-lifeline."""
    pad = pads(canvas_w, n)
    spacing = (canvas_w - 2 * pad) / max(n - 1, 1)
    return min(150, int(spacing) - 6)


def layout(parts, steps, canvas_w=CANVAS_W):
    ids = [p[0] for p in parts]
    n = len(ids)
    pad = pads(canvas_w, n)
    span = canvas_w - 2 * pad
    xs = {pid: pad + (i * span // max(n - 1, 1)) for i, pid in enumerate(ids)}
    return ids, xs


def wrap(text, maxchars):
    if len(text) <= maxchars:
        return [text]
    cut = len(text) // 2
    return [text[:cut] + "-", text[cut:]]


def build(parts, steps, title):
    ids, xs = layout(parts, steps, CANVAS_W)
    # hitung tinggi: satu baris per pesan + ruang fragment
    rows, y = [], TOP + HEAD_H + 20
    stack, elses = [], []
    for st in steps:
        if st["kind"] == "msg":
            rows.append((y, st)); y += ROW
        elif st["kind"] in ("alt", "opt"):
            stack.append((st["kind"], st["text"], y - 10))
            y += 34
        elif st["kind"] == "else":
            if stack:
                elses.append((stack[-1][2], y + 6, st["text"]))
            y += 26                                    # beri jarak agar sekat tidak menimpa pesan
        elif st["kind"] == "end":
            if stack:
                k, t, y0 = stack.pop()
                rows.append((None, dict(kind="fragend", y0=y0, y1=y + 6, text=t, frag=k)))
            y += 6
    height = int(y + 40)
    bottom = height - 30

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {height}" '
         f'width="{CANVAS_W}" height="{height}">', "  <defs>", "    <style>", STYLE, "    </style>",
         "  </defs>", f'  <rect width="{CANVAS_W}" height="{height}" fill="#FFFFFF"/>']

    # bar aktivasi (activation) per lifeline, dihitung dari urutan pesan
    act, depth, act_rows = {}, {}, []
    for y_, st in rows:
        if y_ is None:
            continue
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

    # lifeline
    for pid in ids:
        x = xs[pid]
        o.append(f'  <line x1="{x}" y1="{TOP + HEAD_H}" x2="{x}" y2="{bottom}" class="lifeline"/>')

    for pid, y0, y1 in act_rows:
        x = xs[pid]
        o.append(f'  <rect x="{x - 7}" y="{y0}" width="14" height="{y1 - y0}" class="activation"/>')

    # fragment kotak
    frags = [r for r in rows if r[1].get("kind") == "fragend"]
    inner = max(6, min([xs[i] for i in ids]) - 40)          # bingkai tidak keluar kanvas
    outer = min(CANVAS_W - 6, max([xs[i] for i in ids]) + 40)
    for _, f in frags:
        shape = "frag-alt" if f["frag"] == "alt" else "frag-opt"
        o.append(f'  <rect x="{inner}" y="{f["y0"]}" width="{outer - inner}" height="{f["y1"] - f["y0"]}" class="{shape}"/>')
        tag = "alt" if f["frag"] == "alt" else "opt"
        o.append(f'  <rect x="{inner}" y="{f["y0"]}" width="52" height="20" class="frag-tab"/>')
        o.append(f'  <text x="{inner + 26}" y="{f["y0"] + 15}" class="frag-tag">{tag}</text>')
        o.append(f'  <text x="{inner + 62}" y="{f["y0"] + 15}" class="frag-cond">[{f["text"]}]</text>')
    for y0, yelse, etext in elses:                                  # sekat cabang [else]
        o.append(f'  <line x1="{inner}" y1="{yelse}" x2="{outer}" y2="{yelse}" class="frag-else"/>')
        o.append(f'  <text x="{inner + 12}" y="{yelse - 6}" class="frag-cond">[else {etext}]</text>')

    # pesan
    for y_, st in rows:
        if y_ is None:
            continue
        x1, x2 = xs[st["src"]], xs[st["dst"]]
        cls = "msg-return" if st["mtype"] == "return" else "msg-call"
        o.append(f'  <line x1="{x1}" y1="{y_}" x2="{x2}" y2="{y_}" class="{cls}"/>')
        arrow = "arrow-open" if st["mtype"] == "return" else "arrow"
        direction = 1 if x2 > x1 else -1
        tip = x2 if direction > 0 else x2
        o.append(f'  <path d="M {tip} {y_} L {tip - 9 * direction} {y_ - 4} L {tip - 9 * direction} {y_ + 4} Z" class="{arrow}"/>')
        cx = (x1 + x2) // 2
        w = int(len(st["text"]) * MSG_FS * 0.5) + 12
        cx = max(w // 2 + 6, min(CANVAS_W - w // 2 - 6, cx))      # jaga label di dalam kanvas
        o.append(f'  <rect x="{cx - w // 2}" y="{y_ - 20}" width="{w}" height="16" class="msg-bg"/>')
        o.append(f'  <text x="{cx}" y="{y_ - 8}" class="msg-text">{esc(st["text"])}</text>')

    # kepala lifeline
    head_w = head_width(CANVAS_W, len(ids))
    for pid in ids:
        x = xs[pid]
        lines = wrap(pid, max(8, int(head_w / 6.2)))
        hh = HEAD_H + (len(lines) - 1) * 13
        o.append(f'  <rect x="{x - head_w // 2}" y="{TOP}" width="{head_w}" height="{hh}" class="head"/>')
        for i, ln in enumerate(lines):
            o.append(f'  <text x="{x}" y="{TOP + 17 + i * 13}" class="head-name">{esc(ln)}</text>')
        o.append(f'  <line x1="{x - head_w // 2}" y1="{TOP + hh - 16}" x2="{x + head_w // 2}" y2="{TOP + hh - 16}" class="cell-border"/>')
        o.append(f'  <text x="{x}" y="{TOP + hh - 5}" class="head-type">lifeline</text>')

    o.append("</svg>")
    return "\n".join(o), CANVAS_W, height


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def make_style():
    return f"""
      .title {{ font-family: 'Times New Roman', serif; font-size: 16px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .head {{ fill: #D9D9D9; stroke: #000000; stroke-width: 1.5; }}
      .head-name {{ font-family: 'Times New Roman', serif; font-size: {PART_FS}px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .head-type {{ font-family: 'Times New Roman', serif; font-size: 11px; font-style: italic; fill: #333333; text-anchor: middle; }}
      .cell-border {{ stroke: #C9CDD2; stroke-width: 0.9; }}
      .lifeline {{ stroke: #000000; stroke-width: 1.1; stroke-dasharray: 6 5; }}
      .activation {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.2; }}
      .msg-call {{ stroke: #000000; stroke-width: 1.6; }}
      .msg-return {{ stroke: #000000; stroke-width: 1.3; stroke-dasharray: 7 5; }}
      .arrow {{ fill: #000000; stroke: none; }}
      .arrow-open {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.2; }}
      .msg-bg {{ fill: #FFFFFF; }}
      .msg-text {{ font-family: 'Times New Roman', serif; font-size: {MSG_FS}px; fill: #000000; text-anchor: middle; }}
      .frag-alt {{ fill: none; stroke: #000000; stroke-width: 1.3; }}
      .frag-opt {{ fill: none; stroke: #000000; stroke-width: 1.3; stroke-dasharray: 4 3; }}
      .frag-tab {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.3; }}
      .frag-else {{ stroke: #000000; stroke-width: 1.2; stroke-dasharray: 4 3; }}
      .frag-tag {{ font-family: 'Times New Roman', serif; font-size: 13px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .frag-cond {{ font-family: 'Times New Roman', serif; font-size: 13px; font-style: italic; fill: #000000; }}
"""


STYLE = make_style()

HTML = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        'body{margin:0;padding:0;background:#fff;}svg{display:block;}</style></head><body>\n__SVG__\n</body></html>')

TITLES = {
    "sd01": "SD-01 Pengajuan Tiket Request Konten",
    "sd02": "SD-02 Validasi dan Penugasan Tiket Konten",
    "sd03": "SD-03 Pengerjaan dan Unggah Draf Karya",
    "sd04": "SD-04 Tinjauan Draf, Persetujuan Akhir, dan Publikasi",
}

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent
    md = (root / "SDD_Medkreminfo_v1.0.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\n(.*?)```", md, re.S)
    seqs = [b for b in blocks if b.strip().startswith("sequenceDiagram")]
    out = root / "images"
    out.mkdir(exist_ok=True)
    for key, block in zip(["sd01", "sd02", "sd03", "sd04"], seqs):
        parts, steps = parse(block)
        if len(parts) <= 6:
            CANVAS_W, MSG_FS = 950, 14
        elif len(parts) == 7:
            CANVAS_W, MSG_FS = 1024, 14
        else:
            CANVAS_W, MSG_FS = 1120, 13
        STYLE = make_style()
        svg, w, h = build(parts, steps, TITLES[key])
        (out / f"seq_diagram_{key}.svg").write_text(svg, encoding="utf-8")
        (out / f"seq_diagram_{key}.html").write_text(HTML.replace("__SVG__", svg), encoding="utf-8")
        msgs = len([s for s in steps if s.get("kind") == "msg"])
        pt = MSG_FS * 5.8 * 72 / CANVAS_W
        print(f"{key}: {w}x{h} | {len(parts)} lifeline | {msgs} pesan | teks pesan {pt:.1f} pt @5.8in")
