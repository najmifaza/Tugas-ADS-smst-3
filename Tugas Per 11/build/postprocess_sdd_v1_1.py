"""Pasca-proses DOCX SDD v1.1 final:
 1. Tipografi mengikuti Template SDD (Arial: judul 20, bab 13.5, subbab 11.5, isi 9.5; warna #1E3A8A/#2563EB/#0F172A).
 2. Ukuran halaman Letter 8,5x11 in, margin 1 in seperti template.
 3. Setiap gambar diagram ditaruh di halaman LANSKAP tersendiri (margin 0,7 in), heading + caption ikut pindah,
    gambar diperbesar memenuhi area cetak supaya teks diagram terbaca.

Jalankan: python postprocess_sdd_v1_1.py
"""

import pathlib
import shutil
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import etree

BASE       = pathlib.Path(r"D:\Document\GitHub\Tugas-ADS-smst-3\Tugas Per 11")
DOCX_IN    = BASE / "Tugas_3_KelompokXX_AnalysisModels_v1.1.docx"
DOCX_OUT   = BASE / "Tugas_3_KelompokXX_AnalysisModels_v1.1.docx"   # overwrite

FONT = "Arial"
C_TITLE, C_H1, C_H2, C_BODY, C_MUTED = "1E3A8A", "1E3A8A", "2563EB", "0F172A", "475569"

SPEC = {
    "Title":     (20,   True,  C_TITLE),
    "Heading 1": (13.5, True,  C_H1),
    "Heading 2": (11.5, True,  C_H2),
    "Heading 3": (9.5,  True,  C_BODY),
    "Normal":    (9.5,  False, C_BODY),
}

LAND_W, LAND_H, LAND_M = 11.0, 8.5, 0.7
PORT_W, PORT_H, PORT_M = 8.5,  11.0, 1.0


def rgb(hexs):
    return RGBColor(int(hexs[0:2], 16), int(hexs[2:4], 16), int(hexs[4:6], 16))


def set_run(run, size, bold=None, color=C_BODY, italic=None):
    run.font.name = FONT
    rPr = run._element.get_or_add_rPr()
    rf  = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = etree.SubElement(rPr, qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(a), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = rgb(color)


def style_all(doc):
    for name, (size, bold, color) in SPEC.items():
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        st.font.name  = FONT
        st.font.size  = Pt(size)
        st.font.bold  = bold
        st.font.color.rgb = rgb(color)
        rf = st.element.get_or_add_rPr().find(qn("w:rFonts"))
        if rf is not None:
            for a in ("w:ascii", "w:hAnsi", "w:cs"):
                rf.set(qn(a), FONT)
        if name == "Normal":
            st.paragraph_format.space_after   = Pt(4)
            st.paragraph_format.line_spacing  = 1.15


def typography(doc):
    for p in doc.paragraphs:
        sn = p.style.name
        if sn.startswith("Heading"):
            size, bold, color = SPEC.get(sn, SPEC["Heading 3"])
        elif p.text.strip().startswith("Gambar"):
            size, bold, color = 9, False, C_MUTED
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif sn == "Title":
            size, bold, color = SPEC["Title"]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            size, bold, color = 9.5, None, C_BODY
        is_caption = p.text.strip().startswith("Gambar")
        for r in p.runs:
            set_run(r, size, bold, color, italic=True if is_caption else None)
    # Tables
    for t in doc.tables:
        for ri, row in enumerate(t.rows):
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        set_run(r, 8.5 if ri == 0 else 9,
                                True if ri == 0 else None, C_BODY)


def page_setup(doc):
    s = doc.sections[0]
    s.page_width   = Inches(PORT_W)
    s.page_height  = Inches(PORT_H)
    s.left_margin  = s.right_margin = s.top_margin = s.bottom_margin = Inches(PORT_M)


def fit_image(shape):
    ar = shape.width.inches / shape.height.inches
    avail_w = LAND_W - 2 * LAND_M
    avail_h = LAND_H - 2 * LAND_M - 0.85   # ruang heading + caption
    if ar >= avail_w / avail_h:
        w = avail_w;  h = w / ar
    else:
        h = avail_h;  w = h * ar
    shape.width  = Inches(round(w, 2))
    shape.height = Inches(round(h, 2))
    return w, h


def landscape_islands(doc):
    body_sect = doc.element.body.find(qn("w:sectPr"))

    def make_sect(landscape: bool):
        s   = deepcopy(body_sect)
        sz  = s.find(qn("w:pgSz"))
        mar = s.find(qn("w:pgMar"))
        w, h = sz.get(qn("w:w")), sz.get(qn("w:h"))
        if landscape:
            sz.set(qn("w:w"), h); sz.set(qn("w:h"), w)
            sz.set(qn("w:orient"), "landscape")
            m = str(int(LAND_M * 1440))
        else:
            m = str(int(PORT_M * 1440))
        for k in ("w:left", "w:right", "w:top", "w:bottom"):
            mar.set(qn(k), m)
        return s

    def brk(landscape: bool):
        p = doc.add_paragraph()._p
        p.get_or_add_pPr().append(make_sect(landscape))
        return p

    paras   = list(doc.paragraphs)
    islands = []
    for p in paras:
        if p._p.findall(".//" + qn("w:drawing")):
            idx   = paras.index(p)
            first = paras[idx - 1] if idx and paras[idx - 1].style.name.startswith("Heading") else p
            last  = paras[idx + 1] if idx + 1 < len(paras) and paras[idx + 1].text.strip().startswith("Gambar") else p
            islands.append((first, last))
    print(f"Pulau landscape: {len(islands)}")

    for first, last in islands:
        first._p.addprevious(brk(False))
        last._p.addnext(brk(True))

    for sh_i in range(len(doc.inline_shapes)):
        w, h = fit_image(doc.inline_shapes[sh_i])
        print(f"   Gambar {sh_i}: {w:.2f} × {h:.2f} in")


def main():
    # Backup
    bak = pathlib.Path.home() / "AppData/Local/Temp/backup_sdd_v1_1_before_postprocess.docx"
    shutil.copy2(DOCX_IN, bak)
    print(f"Backup: {bak}")

    doc = Document(str(DOCX_IN))
    style_all(doc)
    typography(doc)
    page_setup(doc)
    landscape_islands(doc)
    doc.save(str(DOCX_OUT))

    print(f"\n✅ Pasca-proses selesai: {DOCX_OUT.name}")
    print(f"   Paragraf : {len(doc.paragraphs)}")
    print(f"   Tabel    : {len(doc.tables)}")
    print(f"   Gambar   : {len(doc.inline_shapes)}")
    print(f"   Seksi    : {len(doc.sections)}")
    print(f"   Ukuran   : {DOCX_OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
