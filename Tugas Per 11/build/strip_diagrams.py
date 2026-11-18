"""Kosongkan diagram pada DOCX dan buang semua halaman lanskap.

- Semua inline image dihapus (paragraf gambar dibiarkan kosong sebagai tempat sisip).
- Semua paragraf pemutus seksi (pPr/sectPr) dihapus, sehingga dokumen kembali satu seksi potret.
- Salinan versi bergambar disimpan lebih dulu sebagai *_dengan_diagram.docx.

Jalankan: python strip_diagrams.py
"""

import pathlib
import shutil

from docx import Document
from docx.oxml.ns import qn

D = pathlib.Path(r"D:\SMSTR 3\Tugas ADS\Tugas Per 11")
MAIN = D / "Tugas_3_KelompokXX_AnalysisModels.docx"
KEEP = D / "Tugas_3_KelompokXX_AnalysisModels_dengan_diagram.docx"


def main():
    shutil.copy2(MAIN, KEEP)
    doc = Document(str(MAIN))

    removed_img = 0
    for p in list(doc.paragraphs):
        for dr in p._p.findall(".//" + qn("w:drawing")):
            dr.getparent().remove(dr)
            removed_img += 1
            if not p.text.strip():
                p.alignment = p.alignment            # paragraf kosong jadi ruang sisip

    removed_sect = 0
    for p in list(doc.paragraphs):
        pPr = p._p.pPr
        if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
            if not p.text.strip():
                p._p.getparent().remove(p._p)
                removed_sect += 1

    body_sect = doc.element.body.find(qn("w:sectPr"))
    for tag, val in (("w:pgSz", None),):
        sz = body_sect.find(qn(tag))
        print("seksi akhir:", sz.get(qn("w:w")), "x", sz.get(qn("w:h")), "| orient:", sz.get(qn("w:orient")))

    doc.save(str(MAIN))
    print(f"gambar dihapus: {removed_img} | pemutus seksi lanskap dihapus: {removed_sect}")
    print("seksi tersisa:", len(doc.sections), "| gambar tersisa:", len(doc.inline_shapes))
    print("salinan bergambar:", KEEP.name, f"({KEEP.stat().st_size/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
