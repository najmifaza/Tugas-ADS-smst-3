"""Bersihkan field nomor otomatis (fldSimple/fldChar) pada paragraf caption "Gambar ...".

Sisa field dari konversi markdown mencetak angka urut ("7Gambar 6.1. ...") karena teks caption
sudah ditulis literal. Jalankan: python fix_caption_fields.py
"""

import pathlib
from docx import Document
from docx.oxml.ns import qn

DOCX = pathlib.Path(r"D:\SMSTR 3\Tugas ADS\Tugas Per 11\Tugas_3_KelompokXX_AnalysisModels.docx")


def strip_fields(par):
    removed = 0
    for tag in ("w:fldSimple", "w:fldChar", "w:instrText"):
        for el in par._p.findall(".//" + qn(tag)):
            parent = el.getparent()
            if tag == "w:instrText":
                continue
            parent.remove(el)
            removed += 1
    # run yang tinggal kosong karena instruksi field dihapus
    for r in list(par._p.findall(qn("w:r"))):
        if not r.findall(qn("w:t")) and not r.findall(".//" + qn("w:drawing")):
            r.getparent().remove(r)
            removed += 1
    return removed


def main():
    doc = Document(str(DOCX))
    total = 0
    for p in doc.paragraphs:
        if p.text.strip().startswith("Gambar") or p.text.strip().startswith("Tabel"):
            total += strip_fields(p)
    doc.save(str(DOCX))
    print("elemen field dihapus pada paragraf caption:", total)


if __name__ == "__main__":
    main()
