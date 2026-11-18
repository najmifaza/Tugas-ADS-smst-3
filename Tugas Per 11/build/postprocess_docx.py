"""Pasca-proses DOCX final:
 1. Tipografi mengikuti Template SDD (Arial: judul 20, bab 13.5, subbab 11.5, isi 9.5; warna #1E3A8A/#2563EB/#0F172A).
 2. Ukuran halaman Letter 8,5x11 in, margin 1 in seperti template.
 3. Mengganti 3 gambar class terpisah dengan 1 gambar gabungan (diagram_class_full.png).
 4. Setiap gambar diagram ditaruh di halaman LANSKAP tersendiri (margin 0,7 in), heading + caption ikut pindah,
    gambar diperbesar memenuhi area cetak supaya teks diagram terbaca.

Jalankan: python postprocess_docx.py
"""

import pathlib
import shutil
from copy import deepcopy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import etree

BASE = pathlib.Path(r"D:\SMSTR 3\Tugas ADS\Tugas Per 11")
DOCX = BASE / "Tugas_3_KelompokXX_AnalysisModels.docx"
CLASS_FULL = BASE / "images" / "diagram_class_full.png"

FONT = "Arial"
C_TITLE, C_H1, C_H2, C_BODY, C_MUTED = "1E3A8A", "1E3A8A", "2563EB", "0F172A", "475569"
SPEC = {"Title": (20, True, C_TITLE), "Heading 1": (13.5, True, C_H1), "Heading 2": (11.5, True, C_H2),
        "Heading 3": (9.5, True, C_BODY), "Normal": (9.5, False, C_BODY)}
LAND_W, LAND_H, LAND_M = 11.0, 8.5, 0.7
PORT_W, PORT_H, PORT_M = 8.5, 11.0, 1.0


def rgb(hexs):
    return RGBColor(int(hexs[0:2], 16), int(hexs[2:4], 16), int(hexs[4:6], 16))


def set_run(run, size, bold=None, color=C_BODY, italic=None):
    run.font.name = FONT
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
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
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = rgb(color)
        rf = st.element.get_or_add_rPr().find(qn("w:rFonts"))
        if rf is not None:
            for a in ("w:ascii", "w:hAnsi", "w:cs"):
                rf.set(qn(a), FONT)
        if name == "Normal":
            st.paragraph_format.space_after = Pt(4)
            st.paragraph_format.line_spacing = 1.15


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
        elif p.text.strip().startswith("Tugas 3 ·"):
            size, bold, color = 9.5, False, C_MUTED
        else:
            size, bold, color = 9.5, None, C_BODY
        for r in p.runs:
            set_run(r, size, bold, color, italic=True if p.text.strip().startswith("Gambar") else False)
    for t in doc.tables:
        for ri, row in enumerate(t.rows):
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        set_run(r, 8.5 if ri == 0 else 9, True if ri == 0 else None, C_BODY)


def page_setup(doc):
    s = doc.sections[0]
    s.page_width, s.page_height = Inches(PORT_W), Inches(PORT_H)
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(PORT_M)


def drawing_paras(doc):
    return [p for p in doc.paragraphs if p._p.findall(".//" + qn("w:drawing"))]


def merge_class_figures(doc):
    paras = list(doc.paragraphs)
    pairs = []                                   # (paragraf gambar, paragraf caption)
    for i, p in enumerate(paras):
        if p._p.findall(".//" + qn("w:drawing")) and i + 1 < len(paras) \
                and paras[i + 1].text.strip().startswith("Gambar 6."):
            pairs.append((p, paras[i + 1]))
    if len(pairs) < 2:
        print("class merge: gambar kelas tidak terdeteksi berjumlah >1, dilewati")
        return
    keep_img, keep_cap = pairs[0]
    for img, cap in pairs[1:]:                   # hapus bagian 2 dan 3
        img._p.getparent().remove(img._p)
        cap._p.getparent().remove(cap._p)
    for r in list(keep_img.runs):                # kosongkan paragraf gambar pertama
        r._element.getparent().remove(r._element)
    keep_img.add_run().add_picture(str(CLASS_FULL), width=Inches(LAND_W - 2 * LAND_M))
    keep_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in list(keep_cap.runs):
        r._element.getparent().remove(r._element)
    keep_cap.add_run("Gambar 6.1. UML Class Diagram domain sistem (8 kelas: agregat tiket, draf, riwayat, "
                     "berkas aset, publikasi, pengguna, dan kementerian)")
    print(f"class merge: {len(pairs)} gambar -> 1 gambar gabungan")


def fit_image(shape):
    ar = shape.width.inches / shape.height.inches
    avail_w, avail_h = LAND_W - 2 * LAND_M, LAND_H - 2 * LAND_M - 0.85   # sisakan ruang heading + caption
    if ar >= avail_w / avail_h:
        w = avail_w
        h = w / ar
    else:
        h = avail_h
        w = h * ar
    shape.width, shape.height = Inches(round(w, 2)), Inches(round(h, 2))
    return w, h


def landscape_islands(doc):
    body_sect = doc.element.body.find(qn("w:sectPr"))

    def sect(landscape):
        s = deepcopy(body_sect)
        sz = s.find(qn("w:pgSz"))
        mar = s.find(qn("w:pgMar"))
        w, h = sz.get(qn("w:w")), sz.get(qn("w:h"))
        if landscape:
            sz.set(qn("w:w"), h)
            sz.set(qn("w:h"), w)
            sz.set(qn("w:orient"), "landscape")
            m = str(int(LAND_M * 1440))
        else:
            m = str(int(PORT_M * 1440))
        for k in ("w:left", "w:right", "w:top", "w:bottom"):
            mar.set(qn(k), m)
        return s

    def brk(landscape):
        p = doc.add_paragraph()._p
        p.get_or_add_pPr().append(sect(landscape))
        return p

    paras = list(doc.paragraphs)
    islands = []
    for p in paras:
        if p._p.findall(".//" + qn("w:drawing")):
            i = paras.index(p)
            first = paras[i - 1] if i and paras[i - 1].style.name.startswith("Heading") else p
            last = paras[i + 1] if i + 1 < len(paras) and paras[i + 1].text.strip().startswith("Gambar") else p
            islands.append((first, last))
    print("island lanskap:", len(islands))
    for first, last in islands:
        first._p.addprevious(brk(False))
        last._p.addnext(brk(True))
    for sh_i in range(len(doc.inline_shapes)):
        fit_image(doc.inline_shapes[sh_i])


def main():
    shutil.copy2(DOCX, pathlib.Path.home() / "AppData/Local/Temp/backup_sdd_before_postprocess.docx")
    doc = Document(str(DOCX))
    style_all(doc)
    typography(doc)
    page_setup(doc)
    merge_class_figures(doc)
    landscape_islands(doc)
    doc.save(str(DOCX))
    print("gambar:", len(doc.inline_shapes), "| paragraf:", len(doc.paragraphs), "| seksi:", len(doc.sections))
    for i in range(len(doc.inline_shapes)):
        sh = doc.inline_shapes[i]
        print(f"   gambar {i}: {sh.width.inches:.2f} x {sh.height.inches:.2f} in")


if __name__ == "__main__":
    main()
