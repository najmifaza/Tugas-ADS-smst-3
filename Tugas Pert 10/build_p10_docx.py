import os
import subprocess
import sys
import gc
import re
import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    top = kwargs.get('top', 'single')
    left = kwargs.get('left', 'single')
    bottom = kwargs.get('bottom', 'single')
    right = kwargs.get('right', 'single')
    xml_str = f'<w:tcBorders {nsdecls("w")}><w:top w:val="{top}" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="{left}" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="{bottom}" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="{right}" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>'
    tcPr.append(parse_xml(xml_str))

def set_cell_shading(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=10, bottom=10, left=40, right=40):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def make_rows_cant_split(table):
    for row in table.rows:
        row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))


def set_document_language(doc, lang="id-ID"):
    rpr_default = doc.styles.element.find(qn('w:docDefaults'))
    if rpr_default is not None:
        rpr = rpr_default.find(qn('w:rPrDefault'))
        if rpr is not None:
            r = rpr.find(qn('w:rPr'))
            if r is not None:
                r.append(parse_xml(f'<w:lang {nsdecls("w")} w:val="{lang}" w:eastAsia="{lang}"/>'))


def add_header_repeat(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def install_numbering(doc, num_ids=(101, 102, 103, 104, 105, 106)):
    """Definisikan satu abstractNum desimal + satu w:num per daftar.

    Tiap daftar memakai numId berbeda supaya penghitungannya berdiri sendiri
    (mulai dari 1) dan tetap ikut berubah kalau isinya disunting di Word.
    """
    numbering = doc.part.numbering_part.element
    abs_id = 100
    lvl0 = (
        '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
        '<w:lvlText w:val="%1."/><w:lvlJc w:val="left"/>'
        '<w:pPr><w:ind w:left="540" w:hanging="360"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:lvl>'
    )
    lvl1 = (
        '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
        '<w:lvlText w:val="%2."/><w:lvlJc w:val="left"/>'
        '<w:pPr><w:ind w:left="900" w:hanging="360"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:lvl>'
    )
    abs_el = parse_xml(
        '<w:abstractNum %s w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>'
        '%s%s</w:abstractNum>' % (nsdecls('w'), abs_id, lvl0, lvl1)
    )
    # abstractNum wajib berada sebelum semua elemen w:num
    first_num = next((c for c in numbering.iterchildren() if c.tag == qn('w:num')), None)
    if first_num is not None:
        first_num.addprevious(abs_el)
    else:
        numbering.append(abs_el)
    # --- daftar berbutir: '•' (lvl0) dan '–' (lvl1) ---
    bul_id = 200

    def _bul_lvl(ilvl, glyph, ind_left):
        return (
            '<w:lvl w:ilvl="%d"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
            '<w:lvlText w:val="%s"/><w:lvlJc w:val="left"/>'
            '<w:pPr><w:ind w:left="%d" w:hanging="360"/></w:pPr>'
            '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:lvl>'
        ) % (ilvl, glyph, ind_left)

    bul_el = parse_xml(
        '<w:abstractNum %s w:abstractNumId="%d"><w:multiLevelType w:val="hybridMultilevel"/>'
        '%s%s</w:abstractNum>' % (nsdecls('w'), bul_id,
                                  _bul_lvl(0, '\u2022', 540), _bul_lvl(1, '\u2013', 900))
    )
    first_num = next((c for c in numbering.iterchildren() if c.tag == qn('w:num')), None)
    if first_num is not None:
        first_num.addprevious(bul_el)
    else:
        numbering.append(bul_el)
    numbering.append(parse_xml(
        '<w:num %s w:numId="107"><w:abstractNumId w:val="%d"/></w:num>' % (nsdecls('w'), bul_id)
    ))

    # sub-judul Bagian C: nomor rata margin, teks langsung setelah nomor
    head_id = 201
    head_lvl0 = (
        '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
        '<w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:suff w:val="space"/>'
        '<w:pPr><w:ind w:left="0" w:hanging="0"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:lvl>'
    )
    head_el = parse_xml(
        '<w:abstractNum %s w:abstractNumId="%d"><w:multiLevelType w:val="singleLevel"/>'
        '%s</w:abstractNum>' % (nsdecls('w'), head_id, head_lvl0)
    )
    first_num = next((c for c in numbering.iterchildren() if c.tag == qn('w:num')), None)
    if first_num is not None:
        first_num.addprevious(head_el)
    else:
        numbering.append(head_el)

    for nid in num_ids:
        # startOverride per daftar: tanpa ini semua numId ikut satu penghitung
        abs_ref = head_id if nid == 106 else abs_id
        numbering.append(parse_xml(
            '<w:num %s w:numId="%d"><w:abstractNumId w:val="%d"/>'
            '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride>'
            '<w:lvlOverride w:ilvl="1"><w:startOverride w:val="1"/></w:lvlOverride>'
            '</w:num>' % (nsdecls('w'), nid, abs_ref)
        ))


def create_document():
    doc = Document()

    # Lock base fonts: theme default is Cambria, which field results (page number) inherit
    for style_name, size in (("Normal", 11), ("Footer", 10), ("Header", 10)):
        st = doc.styles[style_name]
        st.font.name = 'Times New Roman'
        st.font.size = Pt(size)
        rPr = st.element.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is not None:
            rFonts.set(qn('w:eastAsia'), 'Times New Roman')
            rFonts.set(qn('w:cs'), 'Times New Roman')

    install_numbering(doc)
    set_document_language(doc)

    # 1. Page Margins - Standard Academic 2.54 cm all sides
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)
    
    # Footer: nomor halaman (dipasang di section body, bukan halaman judul)
    def add_footer_page_number(sec, start=None):
        pg = sec._sectPr.find(qn('w:pgNumType'))
        if pg is not None:
            sec._sectPr.remove(pg)
        attrs = ' w:fmt="decimal"' + (f' w:start="{start}"' if start is not None else '')
        sec._sectPr.append(parse_xml('<w:pgNumType %s%s/>' % (nsdecls('w'), attrs)))

        f = sec.footer
        f.is_linked_to_previous = False
        fp = f.paragraphs[0]
        fp.text = ""
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp._p.get_or_add_pPr().append(parse_xml(
            '<w:rPr %s><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>' % nsdecls('w')
        ))
        fp._p.append(parse_xml(
            '<w:fldSimple %s w:instr=" PAGE ">'
            '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>1</w:t></w:r>'
            '</w:fldSimple>' % nsdecls('w')
        ))

    def p_fmt(p, space_after=3, line_spacing=1.15):
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing

    def add_p(text="", bold_prefix=None, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT,
              num_id=None, ilvl=0, indent=None):
        p = doc.add_paragraph()
        p.alignment = align
        p_fmt(p, space_after, line_spacing)
        p.paragraph_format.widow_control = True

        if indent is not None:
            p.paragraph_format.left_indent = Twips(indent)

        if num_id is not None:
            numPr = p._p.get_or_add_pPr().get_or_add_numPr()
            numPr.get_or_add_ilvl().val = ilvl
            numPr.get_or_add_numId().val = num_id

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11)
            r_pre.font.color.rgb = RGBColor(0, 0, 0)

        if text:
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`]*`)', text)
            for part in parts:
                if not part:
                    continue
                r = p.add_run()
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(0, 0, 0)
                if part.startswith('**') and part.endswith('**'):
                    r.text = part[2:-2]
                    r.font.bold = True
                elif part.startswith('`') and part.endswith('`'):
                    r.text = part[1:-1]
                    r._element.get_or_add_rPr().append(parse_xml(
                        '<w:shd %s w:val="clear" w:color="auto" w:fill="EDEDED"/>' % nsdecls('w')))
                elif part.startswith('*') and part.endswith('*'):
                    r.text = part[1:-1]
                    r.font.italic = True
                else:
                    r.text = part
        return p

    def add_heading(text, level=1, space_before=None, space_after=None, num_id=None, ilvl=0, rule=False):
        if space_before is None:
            space_before = 6 if level == 1 else 4
        if space_after is None:
            space_after = 3 if level == 1 else 2
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        if level == 1 and rule:
            p._p.get_or_add_pPr().insert_element_before(parse_xml(
                '<w:pBdr %s><w:top w:val="single" w:sz="6" w:space="13" w:color="808080"/></w:pBdr>'
                % nsdecls('w')), 'w:shd', 'w:tabs', 'w:spacing', 'w:ind', 'w:jc')
        if num_id is not None:
            numPr = p._p.get_or_add_pPr().get_or_add_numPr()
            numPr.get_or_add_ilvl().val = ilvl
            numPr.get_or_add_numId().val = num_id
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12 if level == 1 else 11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    # --- JUDUL + KOTAK IDENTITAS (halaman 1, tanpa halaman sampul: budget 6 halaman) ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fmt(p_title, space_after=2)
    r1 = p_title.add_run("LAPORAN TUGAS MANDIRI PERTEMUAN 10 \u2013 PEMODELAN DATA")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fmt(p_sub, space_after=4)
    r2 = p_sub.add_run("IF21307 Analisis dan Desain Sistem")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(0, 0, 0)

    # Kotak identitas: tabel 2 kolom tanpa garis, titik dua rata (skill §8)
    _bio = [
        ("Nama Lengkap", "Adridinan Najmi Faza"),
        ("NIM", "H1D025059"),
        ("Nama TIM", "Medkreminfo"),
        ("Judul Proyek", "Sistem Informasi Layanan Pemesanan Konten Medkreminfo BEM FT UNSOED"),
        ("Use Case yang Dianalisis", "UC-01: Pengajuan Tiket Request Konten (Klien)"),
    ]
    t_bio = doc.add_table(rows=len(_bio), cols=2)
    t_bio.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bio.autofit = False
    for _r, (_k, _v) in enumerate(_bio):
        for _c, _val in enumerate((_k + " :", _v)):
            cell = t_bio.rows[_r].cells[_c]
            cell.width = Cm(5.6) if _c == 0 else Cm(10.0)
            set_cell_margins(cell, top=8, bottom=8, left=0, right=40)
            cp = cell.paragraphs[0]
            p_fmt(cp, space_after=1)
            run = cp.add_run(_val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = (_c == 0)
            run.font.color.rgb = RGBColor(0, 0, 0)
    make_rows_cant_split(t_bio)
    add_footer_page_number(doc.sections[0], start=1)

    # --- BAGIAN A ---
    add_heading("BAGIAN A. USE CASE NARRATIVE (ANALISIS KATA BENDA & KATA KERJA)", level=1)
    add_p("**Keterangan Notasi:**", indent=540)
    add_p("Kata benda dicetak **tebal** sebagai kandidat entitas atau atribut.", num_id=107, ilvl=1)
    add_p("Kata kerja dicetak *miring* sebagai kandidat relasi.", num_id=107, ilvl=1)

    add_heading("UC-01: Pengajuan Tiket Request Konten (Klien)", level=2)
    add_p("**Aktor Utama:** **Klien** (**Perwakilan Kementerian BEM FT**)", num_id=107)
    add_p("**Kebutuhan Terkait:** FR-02, FR-03, FR-04; BR-01, BR-05", num_id=107)
    add_p("**Precondition:** **Pengguna** telah *terautentikasi* ke dalam sistem dengan **akun peran Klien**.", num_id=107)
    add_p("**Trigger:** **Klien** *memilih* **menu** \"Buat Pesanan Konten Baru\".", num_id=107)

    add_heading("Alur Utama (Main Flow):", level=2)
    add_p("**Klien** *membuka* **halaman formulir pemesanan konten**.", num_id=101)
    add_p("**Klien** *mengisi* **judul publikasi**, *memilih* **kanal tujuan** (**Instagram Feeds** / **Story** / **LinkedIn** / **TikTok**), dan *memilih* **tanggal target tayang**.", num_id=101)
    add_p("Sistem *memverifikasi* **selisih hari** **tanggal target tayang** terhadap **aturan SLA** (BR-01).", num_id=101)
    add_p("**Klien** *mengunggah* **berkas materi pendukung** (**gambar**/**dokumen**/**video**) atau *menyematkan* **tautan Google Drive**, serta *memasukkan* **deskripsi brief naskah**.", num_id=101)
    add_p("**Klien** *menekan* **tombol** \"Kirim Permohonan\".", num_id=101)
    add_p("Sistem *memvalidasi* **kelengkapan isian formulir** dan *menerima* **berkas aset pendukung** (termasuk **berkas video** > 50 MB sesuai BR-05).", num_id=101)
    add_p("Sistem *menerbitkan* **ID tiket unik** (format `#MED-YYYYMM-XXX`), *menyimpan* **data tiket** dengan **status** `Submitted`, dan *mengirimkan* **notifikasi konfirmasi**.", num_id=101)

    add_heading("Alur Alternatif (Alternate Flow):", level=2)
    add_p("**3a. Pengajuan Mendadak (< Batas Hari SLA):**", num_id=107)
    add_p("Sistem *menampilkan* **peringatan** bahwa **target tanggal tayang** *melanggar* **batas waktu standar pengerjaan** (BR-01).", num_id=102, ilvl=1)
    add_p("Sistem *membuka* **kolom isian wajib**: \"**Alasan Kebutuhan Darurat** (**Dispensasi Urgent**)\"." , num_id=102, ilvl=1)
    add_p("**Klien** *mengisi* **justifikasi darurat**, **tiket** *diberi* **label** `Rush Order`, dan alur *berlanjut* ke langkah 4.", num_id=102, ilvl=1)

    add_heading("Alur Pengecualian (Exception Flow):", level=2)
    add_p("**6a. Format Ekstensi Berkas Tidak Didukung:**", num_id=107)
    add_p("Sistem *menolak* **berkas** dan *menampilkan* **pesan galat**: \"Format berkas tidak didukung. Unggah berkas valid atau cantumkan tautan Google Drive\".", num_id=103, ilvl=1)
    add_p("**Pengguna** diminta *memilih* **berkas pengganti** atau *menyematkan* **tautan penyimpanan awan**.", num_id=103, ilvl=1)
    add_p("Alur *kembali* ke langkah 4.", num_id=103, ilvl=1)

    add_heading("Postcondition:", level=2)
    add_p("**Tiket** *tercatat* pada **basis data** dengan **status** `Submitted` dan *muncul* di **antrean verifikasi** **Admin**.")

    # --- BAGIAN B ---
    add_heading("BAGIAN B. TABEL SARING KANDIDAT", level=1)
    
    t_b_data = [
        ("1", "Klien / Perwakilan Kementerian", "Entitas PENGGUNA", "Aktor pembuat pesanan. Ada 14 kementerian pemesan dan staf Medkreminfo. Datanya disimpan lengkap (nama, email, password, peran, kontak, spesialisasi) sesuai FR-01."),
        ("2", "Halaman formulir pemesanan", "Bukan entitas", "Tampilan form input di browser. Datanya sendiri disimpan ke dalam tiket pesanan."),
        ("3", "Tiket / Data tiket", "Entitas TIKET_PESANAN", "Data pesanan utama yang disimpan dan dilacak status pengerjaannya dari baru masuk sampai tayang di media sosial."),
        ("4", "ID tiket (#MED-YYYYMM-XXX)", "Atribut TIKET_PESANAN", "Kunci utama (Primary Key) penanda unik tiap pesanan agar tidak tertukar sesuai FR-02."),
        ("5", "Judul publikasi", "Atribut TIKET_PESANAN", "Nama atau topik konten yang dipesan pada tiket tersebut."),
        ("6", "Kanal tujuan", "Atribut TIKET_PESANAN", "Pilihan media tayang (Feeds, Story, LinkedIn, TikTok) yang menentukan batas SLA di BR-01."),
        ("7", "Tanggal target tayang", "Atribut TIKET_PESANAN", "Batas tanggal kapan konten harus dipublikasikan."),
        ("8", "Selisih hari / Validasi SLA", "Bukan entitas", "Hasil hitungan tanggal tayang dikurangi tanggal pesan saat itu juga. Diatur di aturan bisnis BR-01, tidak perlu tabel sendiri."),
        ("9", "Berkas materi / Aset pendukung", "Entitas BERKAS_ASET", "File materi (foto, video, naskah). Satu pesanan bisa punya banyak file, ukurannya bisa besar (>50MB), dan filenya akan dihapus otomatis kalau sudah tayang (BR-05)."),
        ("10", "Tautan Google Drive", "Atribut BERKAS_ASET", "Link cadangan kalau file video terlalu besar (>50MB) untuk diunggah langsung ke web."),
        ("11", "Deskripsi brief naskah", "Atribut TIKET_PESANAN", "Catatan konsep dan teks materi yang diminta kementerian pemesan."),
        ("12", "Status tiket (Submitted)", "Atribut TIKET_PESANAN", "Penanda progres pengerjaan tiket (Submitted, In Progress, Review, Published)."),
        ("13", "Alasan kebutuhan darurat", "Atribut TIKET_PESANAN", "Keterangan tambahan yang wajib diisi jika kementerian memesan mendadak melewati batas SLA."),
        ("14", "Label Rush Order", "Atribut TIKET_PESANAN", "Penanda (is_rush_order bertipe boolean) apakah pesanan ini order darurat atau reguler."),
        ("15", "Tombol kirim / Pesan galat", "Bukan entitas", "Cuma tombol klik dan teks peringatan di layar browser saat format file salah. Tidak ada data yang disimpan ke basis data."),
        ("16", "Notifikasi konfirmasi", "Bukan entitas (ragu)", "Pesan pemberitahuan saat tiket terkirim. Di SRS belum ada kebutuhan untuk menyimpan riwayat log notifikasi.")
    ]

    tbl_b = doc.add_table(rows=len(t_b_data) + 1, cols=4)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_b = [450, 1850, 2050, 4676]  # total 9026 dxa
    
    h_b = ["No", "Kandidat", "Keputusan", "Alasan"]
    for ci, name in enumerate(h_b):
        cell = tbl_b.cell(0, ci)
        cell.width = Pt(widths_b[ci] / 20)
        p = cell.paragraphs[0]
        p_fmt(p, space_after=0, line_spacing=1.0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci == 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(name)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_border(cell, top='single', bottom='single', left='single', right='single')
        set_cell_shading(cell, "D9D9D9")
        set_cell_margins(cell, top=10, bottom=10, left=40, right=40)
    add_header_repeat(tbl_b.rows[0])

    for ri, row_data in enumerate(t_b_data):
        row = tbl_b.rows[ri + 1]
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            cell.width = Pt(widths_b[ci] / 20)
            p = cell.paragraphs[0]
            p_fmt(p, space_after=0, line_spacing=1.0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci == 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            set_cell_border(cell, top='single', bottom='single', left='single', right='single')
            set_cell_margins(cell, top=10, bottom=10, left=40, right=40)

    # --- BAGIAN C ---
    doc.add_page_break()
    add_heading("BAGIAN C. ERD V1 SELURUH SISTEM & LEGENDA", level=1, space_before=0)
    add_heading("Diagram ERD v1 (Notasi Crow's Foot)", level=2, num_id=106)

    png_path = r"D:\SMSTR 3\Tugas ADS\Tugas Pert 10\diagram_erd_p10.png"
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fmt(p_img, space_after=2)
    p_img.paragraph_format.keep_with_next = True
    r_img = p_img.add_run()
    r_img.add_picture(png_path, width=Inches(6.26))

    doc.add_page_break()
    add_heading("Legenda Notasi (Crow's Foot)", level=2, space_before=0, num_id=106, ilvl=0)
    add_p("||--o{ : Relasi **One-to-Many Optional** (Satu data induk bisa punya nol atau banyak data anak).", num_id=107)
    add_p("||--|| : Relasi **One-to-One Mandatory** (Satu data induk berpasangan tepat dengan satu data anak).", num_id=107)
    add_p("|o--o{ : Relasi **Zero-or-One to Many Optional** (Data anak boleh belum menunjuk data induk, misal tiket baru yang belum ditugaskan eksekutor).", num_id=107)
    add_p("PK : *Primary Key* (Kolom pengenal unik tabel).", num_id=107)
    add_p("FK : *Foreign Key* (Kolom penghubung ke tabel lain).", num_id=107)

    add_heading("Asal Entitas di Luar Use Case UC-01", level=2, num_id=106)
    add_p("Entitas yang tidak ada di alur UC-01 diambil dari kebutuhan fungsional (FR) dan aturan bisnis (BR) lainnya:")
    add_p("**KEMENTERIAN**", num_id=104)
    add_p("*Asal Sumber:* Deskripsi Sistem Bagian 1.2, NFR-SEC-02, dan Hasil Wawancara W01.", num_id=107, ilvl=1)
    add_p("*Alasan:* Ada 14 kementerian di lingkungan BEM FT. Butuh tabel ini agar data pesanan kementerian A tidak bisa diakses atau diubah oleh kementerian B (NFR-SEC-02).", num_id=107, ilvl=1)
    add_p("**DRAF_KARYA**", num_id=104)
    add_p("*Asal Sumber:* FR-11 dan UC-03 (*Pengerjaan dan Unggah Draf Karya*).", num_id=107, ilvl=1)
    add_p("*Alasan:* Staf eksekutor mengunggah hasil desain secara bertahap (versi 1, 2) untuk diperiksa pemesan sebelum tayang.", num_id=107, ilvl=1)
    add_p("**RIWAYAT_REVISI**", num_id=104)
    add_p("*Asal Sumber:* FR-12, BR-02, dan UC-04 (*Peninjauan Draf dan Pengajuan Revisi*).", num_id=107, ilvl=1)
    add_p("*Alasan:* Menampung catatan koreksi dari kementerian pemesan yang dibatasi maksimal 2 kali siklus revisi minor sesuai aturan BR-02.", num_id=107, ilvl=1)
    add_p("**PUBLIKASI_KONTEN**", num_id=104)
    add_p("*Asal Sumber:* FR-15 dan UC-05 (*Penyelesaian dan Publikasi Konten*).", num_id=107, ilvl=1)
    add_p("*Alasan:* Menyimpan bukti tautan publikasi resmi di media sosial, waktu tayang riil, serta mencatat staf media sosial yang mempublikasikannya.", num_id=107, ilvl=1)

    # --- BAGIAN D ---
    add_heading("BAGIAN D. TABEL BUKTI RELASI", level=1)
    
    t_d_data = [
        ("1", "KEMENTERIAN \u2013 menaungi \u2013 PENGGUNA", "1 : N", "Sebagian. NFR-SEC-02: \"Klien dilarang mengakses atau mengedit berkas dan tiket kementerian lain...\" dan Bab 1.2: \"14 kementerian di lingkungan BEM FT...\". Sisi 1 terbukti bahwa satu akun kementerian terikat ke satu kementerian. Sisi N disimpulkan dari struktur organisasi.", "Apakah satu kementerian boleh punya lebih dari satu akun perwakilan pengurus, atau cukup satu akun per kementerian?"),
        ("2", "PENGGUNA (Klien) \u2013 mengajukan \u2013 TIKET_PESANAN", "1 : N", "Lengkap. FR-02: \"Sistem harus memungkinkan Klien membuat tiket pesanan baru melalui formulir terstruktur...\" dan FR-05: \"Sistem harus menampilkan daftar riwayat tiket pesanan milik Klien...\". Satu akun klien bisa membuat banyak pesanan (N), dan satu tiket dibuat oleh tepat 1 orang (1).", "\u2013"),
        ("3", "PENGGUNA (Eksekutor) \u2013 mengerjakan \u2013 TIKET_PESANAN", "0..1 : N", "Lengkap. BR-04: \"Staf eksekutor dibatasi memegang maksimal 3 tiket aktif secara bersamaan pada status In Progress...\" dan FR-08: \"Sistem harus memungkinkan Admin menugaskan staf eksekutor ke tiket yang disetujui...\". Relasi 0..1 karena saat tiket baru diajukan, eksekutornya masih kosong.", "\u2013"),
        ("4", "TIKET_PESANAN \u2013 memiliki \u2013 BERKAS_ASET", "1 : N", "Lengkap. FR-04: \"Sistem harus memungkinkan pengguna mengunggah dan mengunduh berkas aset pendukung (gambar, naskah, maupun video mentahan > 50 MB) selama masa produksi...\" dan BR-05: \"Berkas aset pendukung ... tetap dapat diunggah dan disimpan selama tiket dalam pengerjaan aktif.\". Satu tiket bisa menampung banyak file (N).", "Berapa batas maksimal jumlah file aset yang boleh diunggah dalam satu tiket pesanan?"),
        ("5", "TIKET_PESANAN \u2013 menghasilkan \u2013 DRAF_KARYA", "1 : N", "Lengkap. FR-11: \"Sistem harus memungkinkan Eksekutor memperbarui status pengerjaan tiket (In Progress) dan mengunggah berkas/tautan draf karya (v1, v2) untuk ditinjau.\". Satu tiket pesanan bisa menghasilkan beberapa versi draf (N).", "\u2013"),
        ("6", "TIKET_PESANAN \u2013 menerima \u2013 RIWAYAT_REVISI", "1 : N", "Lengkap. FR-12: \"Sistem harus memfasilitasi Klien untuk mengajukan catatan revisi minor dengan pembatasan maksimal 2 kali siklus revisi (BR-02)...\" dan BR-02: \"Setiap tiket pesanan hanya berhak atas maksimal 2 kali siklus revisi minor...\". Catatan revisi menunjuk pada tiket pesanan terkait.", "\u2013"),
        ("7", "TIKET_PESANAN \u2013 diterbitkan pada \u2013 PUBLIKASI_KONTEN", "1 : 1", "Lengkap. FR-15: \"Sistem harus memungkinkan staf sosmed memasukkan tautan (URL) publikasi resmi di media sosial dan otomatis mengubah status tiket menjadi Published serta mencatat tanggal tayang aktual.\". Satu tiket pesanan tepat menghasilkan satu catatan publikasi.", "\u2013"),
        ("8", "PENGGUNA (Staf) \u2013 mempublikasikan \u2013 PUBLIKASI_KONTEN", "1 : N", "Lengkap. FR-15 dan alur UC-05: Staf media sosial mencatatkan tautan rilis ke sistem. Satu staf dapat mempublikasikan banyak konten dari berbagai kementerian.", "\u2013")
    ]

    tbl_d = doc.add_table(rows=len(t_d_data) + 1, cols=5)
    tbl_d.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_d = [400, 2100, 1100, 3620, 1800]  # total 9026 dxa
    
    h_d = ["No", "Relasi (Entitas \u2013 Kata Kerja \u2013 Entitas)", "Cardinality", "Kutipan Bukti dan ID (FR/BR)", "Jika Tidak Ada Bukti: Pertanyaan ke Stakeholder"]
    for ci, name in enumerate(h_d):
        cell = tbl_d.cell(0, ci)
        cell.width = Pt(widths_d[ci] / 20)
        p = cell.paragraphs[0]
        p_fmt(p, space_after=0, line_spacing=1.0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 2) else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(name)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.bold = True
        set_cell_border(cell, top='single', bottom='single', left='single', right='single')
        set_cell_shading(cell, "D9D9D9")
        set_cell_margins(cell, top=10, bottom=10, left=40, right=40)
    add_header_repeat(tbl_d.rows[0])

    for ri, row_data in enumerate(t_d_data):
        row = tbl_d.rows[ri + 1]
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            cell.width = Pt(widths_d[ci] / 20)
            p = cell.paragraphs[0]
            p_fmt(p, space_after=0, line_spacing=1.0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 2) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            set_cell_border(cell, top='single', bottom='single', left='single', right='single')
            set_cell_margins(cell, top=10, bottom=10, left=40, right=40)

    # --- BAGIAN E ---
    add_heading("BAGIAN E. REFLEKSI", level=1)
    _pq = add_p("Bagian ERD mana yang paling diragukan, dan mengapa?", num_id=105)
    _pq.paragraph_format.keep_with_next = True
    add_p("Pemisahan entitas PUBLIKASI_KONTEN dari TIKET_PESANAN. Relasi keduanya adalah 1 : 1, di mana satu tiket yang selesai tayang hanya menghasilkan tepat satu data publikasi. Saya sempat ragu apakah perlu dipisah menjadi tabel tersendiri atau cukup dijadikan kolom atribut di tabel tiket (url_publikasi dan tanggal_terbit). Namun dipisahkan agar pencatatan waktu terbit aktual dan staf media sosial yang bertugas (id_staf_medsos) terkelola secara rapi dan mandiri dari proses pengerjaan tiket.", indent=540)

    _pq = add_p("Keputusan apa yang diambil berdasarkan tebakan, bukan dokumen?", num_id=105)
    _pq.paragraph_format.keep_with_next = True
    add_p("Menghubungkan entitas RIWAYAT_REVISI langsung ke TIKET_PESANAN (bukan ke DRAF_KARYA). Di SRS memang tertulis aturan kuota maksimal 2 kali revisi minor per tiket pesanan (BR-02), sehingga kuota dan catatan revisi ditautkan langsung ke tiket induk. Namun di alur kerja nyata, kementerian biasanya memberikan catatan revisi yang merujuk pada versi draf tertentu (misal draf v1). Karena SRS tidak merinci keterikatan revisi terhadap ID draf, relasi langsung ke tiket diambil sebagai penyederhanaan desain awal.", indent=540)

    _pq = add_p("Data apa yang mungkin dibutuhkan sistem tetapi belum ada di ERD?", num_id=105)
    _pq.paragraph_format.keep_with_next = True
    add_p("Tabel yang mencatat urutan perpindahan status tiket (mulai Submitted, Disetujui atau Ditolak Admin, Assigned, In Progress, Review, sampai Published). Saat ini status hanya berupa nilai terkini pada kolom status_tiket di tabel pesanan. Jika ada penolakan oleh Menteri atau pemindahtanganan tugas antar staf, riwayat alasan dan waktu perubahannya belum terekam historis secara lengkap. Selain itu, sistem juga belum memiliki tempat untuk mencatat riwayat log pengiriman notifikasi pengingat tayang ke pengguna.", indent=540)

    return doc

if __name__ == "__main__":
    doc = create_document()
    docx_path = r"D:\SMSTR 3\Tugas ADS\Tugas Pert 10\P10_H1D025059_Adridinan_TimMedkreminfo.docx"
    pdf_path = r"D:\SMSTR 3\Tugas ADS\Tugas Pert 10\P10_H1D025059_Adridinan_TimMedkreminfo.pdf"

    try:
        doc.save(docx_path)
        save_target = docx_path
    except PermissionError:
        save_target = docx_path.replace('.docx', '_v2.docx')
        doc.save(save_target)
        print(f"TERKUNCI: disimpan ke {save_target}")
    docx_path = save_target
    print(f"DOCX saved successfully: {os.path.exists(docx_path)} ({os.path.getsize(docx_path)} bytes)")

    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        wdoc = word.Documents.Open(docx_path)
        wdoc.SaveAs(pdf_path, FileFormat=17)
        print(f"PDF GENERATED! {os.path.getsize(pdf_path)} bytes")
        import pymupdf
        _pages = len(pymupdf.open(pdf_path))
        print(f"HALAMAN: {_pages}")
        assert _pages <= 6, f"PDF melebihi batas 6 halaman: {_pages}"
        # Close/Quit menggantung di mesin ini; matikan Word lalu keluar paksa.
        subprocess.run(["taskkill", "/F", "/IM", "WINWORD.EXE"], capture_output=True)
    except Exception as exc:
        print("GAGAL ekspor PDF:", exc)
    finally:
        os._exit(0)
