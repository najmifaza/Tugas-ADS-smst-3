"""Periksa tata letak SDD_Medkreminfo_Diagram.drawio tanpa membuka draw.io.

Deteksi: teks terpotong/meluber dari kotaknya, judul lane yang lebih panjang dari tinggi
lane (draw.io memutar judul swimlane horizontal=0, jadi panjang teks dibatasi tinggi lane),
sel di luar batas halaman, dan kotak bersaudara yang saling menimpa.

Jalankan: python check_drawio.py [path.drawio]
Keluar dengan kode 1 bila ada temuan.
"""

import pathlib
import re
import sys
import xml.etree.ElementTree as ET

D = pathlib.Path(__file__).resolve().parent.parent
DEFAULT = D / "SDD_Medkreminfo_Diagram.drawio"

EM = {"Courier New": 0.60, "Consolas": 0.60}     # lebar rata-rata 1 karakter (em)
EM_DEFAULT = 0.55
LH = 1.2                                          # tinggi baris (em)


def text_w(text, fs, cw=None):
    """Lebar teks (px). `cw` = lebar per karakter; bila None pakai metrik Times New Roman."""
    if cw is not None:
        return len(text) * cw
    w = 0.0
    for ch in text:
        w += 0.28 if ch == " " else (0.62 if (ch.isupper() or ch.isdigit()) else 0.50)
    return w * fs


def style(s):
    d = {}
    for kv in (s or "").split(";"):
        if not kv:
            continue
        k, v = kv.split("=", 1) if "=" in kv else (kv, True)
        d[k] = v
    return d


def plain(v):
    v = re.sub(r"<br\s*/?>", "\n", v or "")
    v = re.sub(r"<[^>]+>", "", v)
    return (v.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&#39;", "'"))


def wrap_count(text, width, fs, cw=None):
    n = 0
    for line in text.split("\n"):
        cur = 0.0
        n += 1
        for word in line.split(" "):
            w = text_w(word, fs, cw)
            if cur and cur + text_w(" ", fs, cw) + w > width:
                n += 1
                cur = w
            else:
                cur += (text_w(" ", fs, cw) if cur else 0) + w
    return n


def cell_boxes(dia):
    """Vertex dengan geometri absolut + induknya."""
    model = dia.find(".//mxGraphModel")
    if model is None:
        return None, [], {}
    cells = {c.get("id"): c for c in model.iter("mxCell")}
    abs_ = {}
    for cid, c in cells.items():
        if c.get("edge") == "1":
            continue
        g = c.find("mxGeometry")
        if g is None or g.get("width") is None:
            continue
        x, y = float(g.get("x") or 0), float(g.get("y") or 0)
        w, h = float(g.get("width")), float(g.get("height"))
        p = c.get("parent")
        if p in abs_:
            px, py = abs_[p][0], abs_[p][1]
            x, y = px + x, py + y
        abs_[cid] = (x, y, w, h)
    out = []
    for cid, c in cells.items():
        if cid in abs_:
            out.append((cid, c, abs_[cid], c.get("parent")))
    return model, out, abs_


def check(path):
    root = ET.parse(path).getroot()
    problems = []
    for dia in root.findall("diagram"):
        model, boxes, abs_ = cell_boxes(dia)
        if model is None:
            continue
        pw, ph = float(model.get("pageWidth")), float(model.get("pageHeight"))
        msgs = []
        lanes, siblings = [], []
        for cid, c, (x, y, w, h), parent in boxes:
            st = style(c.get("style"))
            label = plain(c.get("value"))
            fs = float(st.get("fontSize", 12))
            if x < -0.5 or y < -0.5 or x + w > pw + 0.5 or y + h > ph + 0.5:
                msgs.append(f"LUAR HALAMAN '{label[:34]}' @({x:.0f},{y:.0f}) {w:.0f}x{h:.0f} "
                            f"-> halaman {pw:.0f}x{ph:.0f}")
            if "swimlane" in st:
                ss = float(st.get("startSize", 30))
                if st.get("horizontal", "1") == "1":                 # judul di atas
                    need = wrap_count(label, w - 10, fs) * fs * LH
                    if label and need > ss + 1:
                        msgs.append(f"JUDUL LANE '{label[:30]}': perlu {need:.0f}px > startSize {ss:.0f}")
                else:                                                # judul terputar di kiri
                    need = text_w(label, fs) + 12
                    if label and need > h + 1:
                        msgs.append(f"JUDUL LANE '{label[:30]}': teks {need:.0f}px > tinggi lane "
                                    f"{h:.0f}px -> meluber ke lane tetangga")
                    lanes.append((y, y + h))
                if parent in ("0", "1", None):
                    siblings.append((label or cid, x, y, w, h))
            elif str(st.get("verticalLabelPosition", "")) == "bottom":
                pass
            else:
                cw = fs * EM.get(st.get("fontFamily", ""), 0) or None
                if label:
                    lines_n = wrap_count(label, w - 8, fs, cw)
                    pad = (float(st.get("spacingTop", 0)) + 4) if st.get("verticalAlign") == "top" else 0
                    need_h = lines_n * fs * LH + pad
                    hidden = st.get("overflow") == "hidden"
                    if need_h > h + 1:
                        msgs.append(("TERPOTONG" if hidden else "MELUBER") +
                                    f" '{label[:34]}' kotak {w:.0f}x{h:.0f} perlu {need_h:.0f}px")
                    wide = max((text_w(l, fs, cw) for l in label.split("\n")), default=0)
                    if not hidden and wide > w - 6:
                        msgs.append(f"TERLALU LEBAR '{label[:34]}' {wide:.0f}px > {w:.0f}px")
                if parent and parent in abs_ and parent not in ("0", "1"):
                    pc = abs_[parent]
                    if x + w > pc[0] + pc[2] + 0.5 or y + h > pc[1] + pc[3] + 0.5:
                        msgs.append(f"KELUAR INDUK '{label[:30]}'")
        for i in range(len(siblings)):
            for j in range(i + 1, len(siblings)):
                a, b = siblings[i], siblings[j]
                ox = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
                oy = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2])
                if ox > 1 and oy > 1:
                    msgs.append(f"TIMPANG '{a[0][:26]}' x '{b[0][:26]}' ({ox:.0f}x{oy:.0f}px)")
        print(f"== {dia.get('name')}")
        if not msgs:
            print("   ok")
        for m in msgs:
            print("  !", m)
        problems += [(dia.get("name"), m) for m in msgs]
    print(f"\n{len(problems)} temuan")
    return problems


if __name__ == "__main__":
    p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    sys.exit(1 if check(p) else 0)
