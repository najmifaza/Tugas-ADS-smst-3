"""Tambahkan Lampiran D (artefak hulu: BPMN-01, UCD-01, AD-01..AD-04) ke DOCX final,
perbarui catatan ketersediaan artefak di Bab 1.2, lalu simpan. Ekspor PDF terpisah."""

import pathlib
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Inches, Pt

BASE = pathlib.Path(r"D:\SMSTR 3\Tugas ADS\Tugas Per 11")
DOCX = BASE / "Tugas_3_KelompokXX_AnalysisModels.docx"
IMG = BASE / "diagrams_upstream"
TNR = "Times New Roman"

NOTE = ("Catatan ketersediaan artefak: seluruh artefak hulu yang dirujuk tabel di atas tersedia di repository "
        "kelompok — PC-01, EL-01, SRS v1.0, RTM v1.0, ERD-P10, serta BPMN-01, UCD-01, dan AD-01..AD-04 yang "
        "disertakan pada Lampiran D (folder diagrams_upstream/). Penurunan desain tetap bersandar pada SRS v1.0 "
        "sebagai sumber kebenaran tunggal kebutuhan, sedangkan artefak proses dan perilaku dipakai untuk menetapkan "
        "urutan serah terima tugas dan pemetaan langkah aksi menjadi pesan.")

ROWS = {
    "BPMN-01": ("BPMN To-Be Proses Bisnis (diagrams_upstream/bpmn01.drawio)",
                "Alur proses bisnis lintas swimlane aktor; gateway SLA, kelayakan brief, beban kerja, dan kuota revisi",
                "Dasar penetapan urutan serah terima tugas (hand-off) Klien → Admin → Eksekutor → Staf Medsos pada Bab 3."),
    "UCD-01": ("Use Case Diagram & Narrative (diagrams_upstream/ucd01.drawio)",
               "Batasan fungsi sistem dan aktor, relasi <<include>> dan <<extend>>",
               "Menentukan ruang lingkup use case yang dimodelkan; narasi UC-01 s.d. UC-04 pada SRS §6.2 dipakai langsung sebagai sumber Bab 2.2 dan Bab 3."),
    "AD-01..AD-04": ("Activity Diagram per Use Case (diagrams_upstream/ad01..ad04.drawio)",
                     "Alur kerja prosedural, swimlane, dan percabangan aksi (guard)",
                     "Dasar pemetaan langkah aksi menjadi pertukaran pesan (messages) antar-lifeline pada Bab 3."),
}

FIGURES = [
    ("D.1 BPMN-01: Proses To-Be Layanan Pemesanan Konten", "bpmn01.png",
     "Gambar D.1 BPMN To-Be proses pemesanan konten lintas swimlane Klien, Admin, Eksekutor, dan Staf Publikasi",
     "Empat lane aktor ditambah data store. Gateway yang dimodelkan: kepatuhan SLA (BR-01), kelayakan brief (FR-07), "
     "batas beban aktif ≤ 3 tiket (BR-04), dan kuota revisi (BR-02). Alur berakhir pada status Published dengan "
     "auto-purge berkas fisik aset (BR-05)."),
    ("D.2 UCD-01: Use Case Diagram", "ucd01.png",
     "Gambar D.2 Use Case Diagram sistem layanan pemesanan konten",
     "Use case bernomor selaras SRS §6.2. Relasi <<include>> pada UC-01 → validasi SLA dan <<extend>> pada UC-04 → "
     "validasi kuota revisi. Narasi tiap use case ada pada SRS §6.2."),
    ("D.3 AD-01: Activity Diagram UC-01 Pengajuan Tiket Request Konten", "ad01.png",
     "Gambar D.3 Activity Diagram UC-01 pengajuan tiket request konten",
     "Turunan dari narasi UC-01 (SRS §6.2) dan SD-01 pada Bab 3.3. Gate BR-01 (SLA) dan BR-05 (format/ukuran berkas)."),
    ("D.4 AD-02: Activity Diagram UC-02 Validasi dan Penugasan Tiket", "ad02.png",
     "Gambar D.4 Activity Diagram UC-02 validasi dan penugasan tiket konten",
     "Turunan dari narasi UC-02 (SRS §6.2) dan SD-02. Gate BR-03 (otoritas Admin) dan BR-04 (beban ≤ 3 tiket aktif)."),
    ("D.5 AD-03: Activity Diagram UC-03 Pengerjaan dan Unggah Draf Karya", "ad03.png",
     "Gambar D.5 Activity Diagram UC-03 pengerjaan dan unggah draf karya",
     "Turunan dari narasi UC-03 (SRS §6.2) dan SD-03. Gate BR-04 (hanya tiket yang ditugaskan) dan IC-12 (versi draf unik)."),
    ("D.6 AD-04: Activity Diagram UC-04 Tinjauan Draf, Persetujuan Akhir, dan Publikasi", "ad04.png",
     "Gambar D.6 Activity Diagram UC-04 tinjauan draf, persetujuan akhir, dan publikasi",
     "Turunan dari narasi UC-04 (SRS §6.2) dan SD-04. Gate BR-02 (kuota revisi maksimal 2) dan BR-05 (auto-purge aset)."),
]


def body(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name, r.font.size = TNR, Pt(11)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name, r.font.size, r.bold, r.italic = TNR, Pt(10), True, True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def main():
    doc = Document(str(DOCX))

    # 1. catatan ketersediaan artefak
    hit = 0
    for p in doc.paragraphs:
        if p.text.startswith("Catatan ketersediaan artefak"):
            for r in list(p.runs)[1:]:
                r._element.getparent().remove(r._element)
            p.runs[0].text = NOTE
            p.runs[0].font.name, p.runs[0].font.size = TNR, Pt(11)
            hit += 1
    print("catatan ketersediaan diperbarui:", hit)

    # 2. tabel 1.2
    for tb in doc.tables:
        for row in tb.rows:
            key = row.cells[0].text.strip()
            if key in ROWS:
                for idx, val in zip((1, 2, 3), ROWS[key]):
                    tgt = row.cells[idx]
                    tgt.paragraphs[0].text = ""
                    run = tgt.paragraphs[0].add_run(val)
                    run.font.name, run.font.size = TNR, Pt(11)
                    for extra in tgt.paragraphs[1:]:
                        extra._element.getparent().remove(extra._element)
                print("baris 1.2 diperbarui:", key)

    # 3. Lampiran D
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    doc.add_heading("Lampiran D. Artefak Hulu: BPMN To-Be, Use Case Diagram, dan Activity Diagram", level=1)
    body(doc, "Artefak pada lampiran ini adalah baseline hulu yang dirujuk Bab 1.2 dan kolom keterlacakan Bab 7.1. "
              "Semuanya diturunkan dari SRS v1.0 (§2.1, §5, §6.2) dan Project Charter (PC-01), lalu dipakai konsisten "
              "oleh sequence diagram pada Bab 3. Berkas sumber tiap diagram (SVG, PNG, dan Draw.io XML) tersedia pada "
              "folder diagrams_upstream/ di repository artefak kelompok.")
    for title, png, cap, desc in FIGURES:
        doc.add_heading(title, level=2)
        body(doc, desc)
        doc.add_picture(str(IMG / png), width=Inches(5.8))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption(doc, cap)

    doc.save(str(DOCX))
    print("tersimpan:", DOCX.name, "| paragraf", len(doc.paragraphs), "| gambar", len(doc.inline_shapes))


if __name__ == "__main__":
    main()
