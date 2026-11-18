"""Generator diagram struktural SDD: ERD konseptual, ERD logis 3NF, dan UML class domain.

Kanvas ERD 1024 px dipasang pada lebar 5.9 in -> teks nama atribut 15 px == 6.2 pt saat
dicetak (ambang keterbacaan diagram 6 pt). Kanvas class 760 px, teks anggota 12 px == 6.7 pt.
Skrip mengaudit dirinya: garis tidak menembus kotak, label tidak menimpa kotak/label lain.

Jalankan: python gen_diagrams.py   -> diagram_*.svg + diagram_*.html di ../images/
"""

import itertools
import pathlib

TITLE_FS, NAME_FS, TYPE_FS, KEY_FS, REL_FS = 16, 15, 12, 13, 14
CLS_NAME_FS, CLS_MEMBER_FS = 15, 12

ENT_ATTR = {
    "KEMENTERIAN": [("Angka", "id_kementerian", "PK"), ("Teks", "nama_kementerian", "UK"),
                    ("Teks", "kode_kementerian", "UK")],
    "PENGGUNA": [("Angka", "id_pengguna", "PK"), ("Angka", "id_kementerian", "FK"),
                 ("Teks", "nama_lengkap", ""), ("Teks", "email", "UK"),
                 ("Teks", "password_hash", ""), ("Enumerasi", "role", ""),
                 ("Teks", "spesialisasi", ""), ("Teks", "no_whatsapp", "")],
    "TIKET_PESANAN": [("Teks", "id_tiket", "PK"), ("Angka", "id_pemohon", "FK"),
                      ("Angka", "id_eksekutor", "FK"), ("Teks", "judul_publikasi", ""),
                      ("Enumerasi", "kanal_tujuan", ""), ("Enumerasi", "jenis_konten", ""),
                      ("Tanggal", "tanggal_target_tayang", ""),
                      ("TanggalWaktu", "tanggal_pengajuan", ""), ("TeksPanjang", "deskripsi_brief", ""),
                      ("Enumerasi", "status_tiket", ""), ("Boolean", "is_rush_order", ""),
                      ("TeksPanjang", "alasan_darurat", ""), ("TeksPanjang", "catatan_penolakan", ""),
                      ("TanggalWaktu", "tanggal_verifikasi", ""), ("TanggalWaktu", "waktu_penugasan", "")],
    "BERKAS_ASET": [("Angka", "id_aset", "PK"), ("Teks", "id_tiket", "FK"), ("Teks", "nama_file", ""),
                    ("Teks", "file_path", ""), ("Angka", "ukuran_mb", ""), ("Enumerasi", "format_file", ""),
                    ("Teks", "tautan_gdrive", ""), ("Boolean", "status_purge", ""),
                    ("TanggalWaktu", "tanggal_unggah", "")],
    "DRAF_KARYA": [("Angka", "id_draf", "PK"), ("Teks", "id_tiket", "FK"), ("Teks", "versi_draf", "UK"),
                   ("Teks", "file_path_preview", ""), ("Teks", "tautan_preview_video", ""),
                   ("TeksPanjang", "catatan_draf", ""), ("TanggalWaktu", "tanggal_unggah", "")],
    "RIWAYAT_REVISI": [("Angka", "id_revisi", "PK"), ("Teks", "id_tiket", "FK"), ("Angka", "revisi_ke", "UK"),
                       ("TeksPanjang", "poin_revisi", ""), ("TanggalWaktu", "tanggal_pengajuan_revisi", "")],
    "PUBLIKASI_KONTEN": [("Angka", "id_publikasi", "PK"), ("Teks", "id_tiket", "FK"),
                         ("Teks", "url_postingan_medsos", ""), ("TanggalWaktu", "tanggal_terbit", ""),
                         ("Angka", "id_staf_medsos", "FK")],
    "RIWAYAT_PENUGASAN": [("Angka", "id_penugasan", "PK"), ("Teks", "id_tiket", "FK"),
                          ("Angka", "id_eksekutor", "FK"), ("Enumerasi", "jenis_penugasan", ""),
                          ("TeksPanjang", "alasan_mutasi", ""), ("TanggalWaktu", "waktu_mutasi", "")],
}

RELATIONS = [
    ("KEMENTERIAN", "PENGGUNA", "menaungi", "1..1", "0..N"),
    ("PENGGUNA", "TIKET_PESANAN", "mengajukan", "1..1", "0..N"),
    ("PENGGUNA", "TIKET_PESANAN", "mengerjakan", "0..1", "0..N"),
    ("TIKET_PESANAN", "BERKAS_ASET", "memiliki", "1..1", "0..N"),
    ("TIKET_PESANAN", "DRAF_KARYA", "menghasilkan", "1..1", "0..N"),
    ("TIKET_PESANAN", "RIWAYAT_REVISI", "menerima", "1..1", "0..N"),
    ("TIKET_PESANAN", "PUBLIKASI_KONTEN", "diterbitkan pada", "1..1", "0..1"),
    ("PENGGUNA", "PUBLIKASI_KONTEN", "mempublikasikan", "1..1", "0..N"),
    ("TIKET_PESANAN", "RIWAYAT_PENUGASAN", "mencatat", "1..1", "0..N"),
    ("PENGGUNA", "RIWAYAT_PENUGASAN", "diberikan kepada", "1..1", "0..N"),
]
MULT = {r[0:2]: (r[3], r[4]) for r in RELATIONS}
COMPOSITION = {("TIKET_PESANAN", "BERKAS_ASET"), ("TIKET_PESANAN", "DRAF_KARYA"),
               ("TIKET_PESANAN", "RIWAYAT_REVISI"), ("TIKET_PESANAN", "RIWAYAT_PENUGASAN")}

ORDER = ["KEMENTERIAN", "PENGGUNA", "TIKET_PESANAN", "RIWAYAT_REVISI",
         "BERKAS_ASET", "DRAF_KARYA", "PUBLIKASI_KONTEN", "RIWAYAT_PENUGASAN"]

ERD = dict(canvas=1024, box=420, left=10, right=594, header=34, row=26, pad=6, top=30, gap=34,
           lanes={("TIKET_PESANAN", "BERKAS_ASET"): 442, ("TIKET_PESANAN", "DRAF_KARYA"): 462,
                  ("TIKET_PESANAN", "PUBLIKASI_KONTEN"): 482,
                  ("TIKET_PESANAN", "RIWAYAT_PENUGASAN"): 502,
                  ("PENGGUNA", "PUBLIKASI_KONTEN"): 534,
                  ("PENGGUNA", "RIWAYAT_PENUGASAN"): 566})

CLASSES = {
    "TIKET_PESANAN": ("akar komposisi", [
        "+id_tiket : Teks", "+id_pemohon : Angka", "+id_eksekutor : Angka", "+judul_publikasi : Teks",
        "+kanal_tujuan : Enumerasi", "+jenis_konten : Enumerasi", "+tanggal_target_tayang : Tanggal", "+tanggal_pengajuan : TanggalWaktu",
        "+deskripsi_brief : TeksPanjang", "+status_tiket : Enumerasi", "+is_rush_order : Boolean",
        "+alasan_darurat : TeksPanjang", "+catatan_penolakan : TeksPanjang",
        "+tanggal_verifikasi : TanggalWaktu", "+waktu_penugasan : TanggalWaktu"], [
        "+cariTiket(filter_status, id_kementerian, kanal)",
        "+generateIdTiket(tanggal) : Teks", "+ajukan(judul, kanal, jenis, target, brief, rush, alasan)",
        "+hitungSelisihHari() : Angka", "+validasiSLA(kanal_tujuan, jenis_konten) : Boolean", "+setujuiBrief(id_admin)",
        "+tolakBrief(catatan)", "+tugaskan(id_eksekutor)", "+ubahStatus(status_baru)",
        "+hitungSisaKuotaRevisi() : Angka", "+tutupTiket(url_postingan)"]),
    "BERKAS_ASET": ("bagian dari tiket", [
        "+id_aset : Angka", "+id_tiket : Teks", "+nama_file : Teks", "+file_path : Teks",
        "+ukuran_mb : Angka", "+format_file : Enumerasi", "+tautan_gdrive : Teks",
        "+status_purge : Boolean", "+tanggal_unggah : TanggalWaktu"], [
        "+validasiFormatBerkas(nama, format, ukuran) : Boolean",
        "+fileBerkas(id_tiket) : List~BERKAS_ASET~",
        "+simpanBerkas(id_tiket, nama, ukuran, tautan)", "+purgeBerkas()"]),
    "DRAF_KARYA": ("bagian dari tiket", [
        "+id_draf : Angka", "+id_tiket : Teks", "+versi_draf : Teks", "+file_path_preview : Teks",
        "+tautan_preview_video : Teks", "+catatan_draf : TeksPanjang", "+tanggal_unggah : TanggalWaktu"], [
        "+cariDrafTerakhir(id_tiket) : DRAF_KARYA", "+versiBerikutnya() : Teks",
        "+unggahDraf(versi, berkas, tautan, catatan)"]),
    "RIWAYAT_REVISI": ("bagian dari tiket", [
        "+id_revisi : Angka", "+id_tiket : Teks", "+revisi_ke : Angka", "+poin_revisi : TeksPanjang",
        "+tanggal_pengajuan_revisi : TanggalWaktu"], [
        "+catatanRevisiTerakhir(id_tiket)", "+catatRevisi(poin) : Angka"]),
    "RIWAYAT_PENUGASAN": ("bagian dari tiket", [
        "+id_penugasan : Angka", "+id_tiket : Teks", "+id_eksekutor : Angka",
        "+jenis_penugasan : Enumerasi", "+alasan_mutasi : TeksPanjang", "+waktu_mutasi : TanggalWaktu"], [
        "+catatPenugasan(jenis, alasan) : Angka"]),
    "KEMENTERIAN": ("referensi", [
        "+id_kementerian : Angka", "+nama_kementerian : Teks", "+kode_kementerian : Teks"], [
        "+daftarPenanggungJawab()"]),
    "PENGGUNA": ("peran klien, eksekutor, admin, staf publikasi", [
        "+id_pengguna : Angka", "+id_kementerian : Angka", "+nama_lengkap : Teks", "+email : Teks",
        "+password_hash : Teks", "+role : Enumerasi", "+spesialisasi : Teks", "+no_whatsapp : Teks"], [
        "+autentikasi(email, sandi) : Boolean", "+cekPeran() : Enumerasi",
        "+daftarEksekutor(spesialisasi)", "+hitungTiketAktif() : Angka",
        "+ubahProfil(nama, no_whatsapp)"]),
    "PUBLIKASI_KONTEN": ("bagian dari tiket", [
        "+id_publikasi : Angka", "+id_tiket : Teks", "+url_postingan_medsos : Teks",
        "+tanggal_terbit : TanggalWaktu", "+id_staf_medsos : Angka"], [
        "+catatPublikasi(id_tiket, url, tanggal)"]),
}
CLASS_FIGURES = {
    "class_a": ["TIKET_PESANAN", "BERKAS_ASET"],
    "class_b": ["DRAF_KARYA", "RIWAYAT_REVISI", "RIWAYAT_PENUGASAN"],
    "class_c": ["KEMENTERIAN", "PENGGUNA", "PUBLIKASI_KONTEN"],
}
CLS = dict(canvas=760, box=620, x=110, top=30, gap=80, head=30, row=20, pad=8)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


STYLE = f"""
      .entity-title {{ font-family: 'Times New Roman', serif; font-size: {TITLE_FS}px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .header-box {{ fill: #D9D9D9; stroke: #000000; stroke-width: 1.6; }}
      .body-box {{ fill: #FFFFFF; stroke: #000000; stroke-width: 1.6; }}
      .cell-border {{ stroke: #C9CDD2; stroke-width: 0.9; }}
      .t-type {{ font-family: 'Times New Roman', serif; font-size: {TYPE_FS}px; font-style: italic; fill: #333333; }}
      .t-name {{ font-family: 'Consolas', 'Courier New', monospace; font-size: {NAME_FS}px; fill: #000000; }}
      .t-pk, .t-fk, .t-uk {{ font-family: 'Times New Roman', serif; font-size: {KEY_FS}px; font-weight: bold; fill: #000000; text-anchor: end; }}
      .cls-title {{ font-family: 'Times New Roman', serif; font-size: {CLS_NAME_FS}px; font-weight: bold; fill: #000000; text-anchor: middle; }}
      .cls-stereo {{ font-family: 'Times New Roman', serif; font-size: {TYPE_FS}px; font-style: italic; fill: #333333; text-anchor: middle; }}
      .cls-member {{ font-family: 'Consolas', 'Courier New', monospace; font-size: {CLS_MEMBER_FS}px; fill: #000000; }}
      .rel-line {{ stroke: #000000; stroke-width: 1.7; fill: none; }}
      .rel-label {{ font-family: 'Times New Roman', serif; font-size: {REL_FS}px; font-style: italic; fill: #000000; text-anchor: middle; }}
      .mult-label {{ font-family: 'Times New Roman', serif; font-size: {KEY_FS}px; fill: #000000; text-anchor: middle; }}
      .pill {{ fill: #FFFFFF; stroke: none; }}
      .crow {{ stroke: #000000; stroke-width: 1.7; fill: none; stroke-linecap: round; }}
      .diamond {{ fill: #000000; stroke: #000000; stroke-width: 1.2; }}
      .symbol {{ stroke: #000000; stroke-width: 1.7; fill: #FFFFFF; }}
"""

HTML = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        'body{margin:0;padding:0;background:#fff;}svg{display:block;}</style></head><body>\n__SVG__\n</body></html>')


def box_height(name, with_attrs=True):
    return ERD["header"] + (len(ENT_ATTR[name]) * ERD["row"] if with_attrs else 0) + ERD["pad"]


def layout_erd(with_attrs=True):
    pos, ly, ry = {}, ERD["top"], ERD["top"]
    for i, name in enumerate(ORDER):
        h = box_height(name, with_attrs)
        if i < 4:
            pos[name] = (ERD["left"], ly); ly += h + ERD["gap"]
        else:
            pos[name] = (ERD["right"], ry); ry += h + ERD["gap"]
    return pos, max(ly, ry)


def boxes_erd(pos, with_attrs=True):
    return {n: (x, y, x + ERD["box"], y + box_height(n, with_attrs)) for n, (x, y) in pos.items()}


def entity_g(name, x, y, with_attrs=True):
    h, rows = box_height(name, with_attrs), (ENT_ATTR[name] if with_attrs else [])
    o = [f'  <g transform="translate({x}, {y})">',
         f'    <rect width="{ERD["box"]}" height="{h}" class="body-box"/>',
         f'    <rect width="{ERD["box"]}" height="{ERD["header"]}" class="header-box"/>',
         f'    <text x="{ERD["box"] // 2}" y="23" class="entity-title">{esc(name)}</text>']
    if with_attrs:
        o.append(f'    <line x1="112" y1="{ERD["header"]}" x2="112" y2="{h}" class="cell-border"/>')
        for i in range(1, len(rows)):
            yl = ERD["header"] + i * ERD["row"]
            o.append(f'    <line x1="0" y1="{yl}" x2="{ERD["box"]}" y2="{yl}" class="cell-border"/>')
        for i, (typ, nm, key) in enumerate(rows):
            base = ERD["header"] + i * ERD["row"] + 19
            o.append(f'    <text x="8" y="{base}" class="t-type">{esc(typ)}</text>')
            o.append(f'    <text x="120" y="{base}" class="t-name">{esc(nm)}</text>')
            if key:
                o.append(f'    <text x="{ERD["box"] - 12}" y="{base}" class="t-{key.lower()}">{key}</text>')
    o.append("  </g>")
    return "\n".join(o)


def mark(x, y, kind, horizontal):
    o = []
    if kind == "one":
        if horizontal:
            o += [f'    <line x1="{x - 7}" y1="{y - 9}" x2="{x - 7}" y2="{y + 9}" class="rel-line"/>',
                  f'    <line x1="{x + 7}" y1="{y - 9}" x2="{x + 7}" y2="{y + 9}" class="rel-line"/>']
        else:
            o += [f'    <line x1="{x - 9}" y1="{y - 7}" x2="{x + 9}" y2="{y - 7}" class="rel-line"/>',
                  f'    <line x1="{x - 9}" y1="{y + 7}" x2="{x + 9}" y2="{y + 7}" class="rel-line"/>']
    elif kind == "zero-one":
        o.append(f'    <circle cx="{x}" cy="{y}" r="4.5" class="symbol"/>')
        if horizontal:
            o.append(f'    <line x1="{x - 12}" y1="{y - 9}" x2="{x - 12}" y2="{y + 9}" class="rel-line"/>')
        else:
            o.append(f'    <line x1="{x - 9}" y1="{y - 12}" x2="{x + 9}" y2="{y - 12}" class="rel-line"/>')
    else:
        if horizontal:
            o.append(f'    <path d="M {x - 14} {y - 11} L {x} {y} L {x - 14} {y + 11}" class="crow"/>')
        else:
            o.append(f'    <path d="M {x - 11} {y - 14} L {x} {y} L {x + 11} {y - 14}" class="crow"/>')
    return o


def card_mark(x, y, spec, horizontal):
    return mark(x, y, {"1..1": "one", "0..1": "zero-one"}.get(spec, "many"), horizontal)


def label_width(text, fs):
    return int(len(text) * fs * 0.52) + 14


def add_label(labels, cx, cy, text, kind="rel"):
    fs = REL_FS if kind == "rel" else KEY_FS
    w = label_width(text, fs)
    labels.append(dict(cx=cx, cy=cy, text=text, kind=kind,
                       rect=[cx - w // 2, cy - 11, cx + w // 2, cy + 11]))


def resolve_labels(labels, bs, step=24, tries=14):
    """Geser label ke atas/bawah sampai tidak menimpa kotak atau label lain."""
    fixed = []
    for i, lb in enumerate(labels):
        for t in range(tries):
            shift = 0 if t == 0 else (step * ((t + 1) // 2) * (1 if t % 2 else -1))
            rect = [lb["rect"][0], lb["rect"][1] + shift, lb["rect"][2], lb["rect"][3] + shift]
            hit = any(not (rect[2] <= x1 or rect[0] >= x2 or rect[3] <= y1 or rect[1] >= y2)
                      for (x1, y1, x2, y2) in bs.values())
            for other in fixed:
                r2 = other["rect"]
                if not (rect[2] <= r2[0] or r2[2] <= rect[0] or rect[3] <= r2[1] or r2[3] <= rect[1]):
                    hit = True
                    break
            if not hit:
                lb["cy"] += shift
                lb["rect"] = rect
                break
        fixed.append(lb)
    return labels


def emit_labels(labels):
    out = []
    for lb in labels:
        x1, y1, x2, y2 = lb["rect"]
        cls = "rel-label" if lb["kind"] == "rel" else "mult-label"
        out.append(f'  <rect x="{x1}" y="{y1}" width="{x2 - x1}" height="{y2 - y1}" class="pill"/>')
        out.append(f'  <text x="{lb["cx"]}" y="{lb["cy"] + 5}" class="{cls}">{esc(lb["text"])}</text>')
    return out


def rel_vertical(src, dst, pos, ss, st, verb, x_off, labels, bh):
    sx, sy = pos[src]; dy = pos[dst][1]
    x, y1, y2 = sx + ERD["box"] // 2 + x_off, sy + bh(src), dy
    o = [f'  <path d="M {x} {y1} L {x} {y2}" class="rel-line"/>']
    o += card_mark(x, y1 + 16, ss, horizontal=False)
    o += card_mark(x, y2 - 16, st, horizontal=False)
    add_label(labels, x - 130 if x_off > 0 else x + 130, (y1 + y2) // 2, verb)
    return o


def rel_corridor(src, dst, pos, ss, st, verb, lane, labels, exit_y, bh):
    """Relasi antar kolom; tiap relasi keluar dari sisi kanan sumber pada ketinggian
    berbeda-beda (`exit_y`) supaya label kata kerja tidak saling menumpuk."""
    sx = pos[src][0]; dx, dy = pos[dst]
    y1, y2 = exit_y, dy + bh(dst) // 2
    x1, x2 = sx + ERD["box"], dx
    o = [f'  <path d="M {x1} {y1} L {lane} {y1} L {lane} {y2} L {x2} {y2}" class="rel-line"/>']
    o += card_mark(x1 + 16, y1, ss, horizontal=True)
    o += card_mark(x2 - 16, y2, st, horizontal=True)
    add_label(labels, (ERD["left"] + ERD["box"] + ERD["right"]) // 2, y1 - 14, verb)
    return o


def seg_in_box(p1, p2, rect, tol=3):
    x1, y1, x2, y2 = rect
    if p1[0] == p2[0]:
        lo, hi = sorted((p1[1], p2[1]))
        return (x1 + tol) < p1[0] < (x2 - tol) and max(lo, y1 + tol) < min(hi, y2 - tol)
    lo, hi = sorted((p1[0], p2[0]))
    return (y1 + tol) < p1[1] < (y2 - tol) and max(lo, x1 + tol) < min(hi, x2 - tol)


def audit(paths, bs, labels):
    errs = []
    for name, rect in bs.items():
        for pts in paths:
            for p, q in zip(pts[:-1], pts[1:]):
                if seg_in_box(p, q, rect):
                    errs.append(f"garis menembus kotak {name}")
    for (i, r1), (j, r2) in itertools.combinations(list(enumerate(labels, 1)), 2):
        if not (r1[2] <= r2[0] or r2[2] <= r1[0] or r1[3] <= r2[1] or r2[3] <= r1[1]):
            errs.append(f"label {i} menimpa label {j}")
    for i, r in enumerate(labels, 1):
        for name, (x1, y1, x2, y2) in bs.items():
            if not (r[2] <= x1 or r[0] >= x2 or r[3] <= y1 or r[1] >= y2):
                errs.append(f"label {i} menimpa kotak {name}")
    return errs


def build_erd(kind):
    with_attrs = kind == "logis"
    pos, bottom = layout_erd(with_attrs)
    h = int(bottom + 20)
    bs = boxes_erd(pos, with_attrs)
    bh = lambda n: box_height(n, with_attrs)                        # noqa: E731
    labels, rels, paths = [], [], []
    # relasi antar kolom keluar dari sisi kanan sumber pada ketinggian berurutan (44 px)
    per_source = {}
    for src, dst, verb, ss, st in RELATIONS:
        if pos[src][0] == pos[dst][0]:
            x_off = -74 if verb == "mengerjakan" else (
                74 if (src, dst) == ("PENGGUNA", "TIKET_PESANAN") else 0)
            rels += rel_vertical(src, dst, pos, ss, st, verb, x_off, labels, bh)
            continue
        lane = ERD["lanes"][(src, dst)]
        k = per_source.get(src, 0)
        per_source[src] = k + 1
        exit_y = pos[src][1] + 46 + k * 44
        rels += rel_corridor(src, dst, pos, ss, st, verb, lane, labels, exit_y, bh)
        dx, dy = pos[dst]
        paths.append([(pos[src][0] + ERD["box"], exit_y), (lane, exit_y),
                      (lane, dy + bh(dst) // 2), (dx, dy + bh(dst) // 2)])
    resolve_labels(labels, bs)
    errs = audit(paths, bs, [tuple(lb["rect"]) for lb in labels])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ERD["canvas"]} {h}" '
             f'width="{ERD["canvas"]}" height="{h}">', "  <defs>", "    <style>", STYLE.strip(),
             "    </style>", "  </defs>",
             f'  <rect width="{ERD["canvas"]}" height="{h}" fill="#FFFFFF"/>', ""]
    parts += rels
    parts += emit_labels(labels)
    parts.append("")
    for name in ORDER:
        x, y = pos[name]
        parts.append(entity_g(name, x, y, with_attrs))
    parts.append("</svg>")
    return "\n".join(parts), ERD["canvas"], h, errs


def cls_height(name):
    _, attrs, ops = CLASSES[name]
    return CLS["head"] + (len(attrs) + len(ops) + 2) * CLS["row"] + CLS["pad"]


def class_g(name, x, y):
    stereo, attrs, ops = CLASSES[name]
    h = cls_height(name)
    sep1 = CLS["head"] + 14
    o = [f'  <g transform="translate({x}, {y})">',
         f'    <rect width="{CLS["box"]}" height="{h}" class="body-box"/>',
         f'    <rect width="{CLS["box"]}" height="{sep1}" class="header-box"/>',
         f'    <text x="{CLS["box"] // 2}" y="20" class="cls-title">{esc(name)}</text>',
         f'    <text x="{CLS["box"] // 2}" y="35" class="cls-stereo">«entity» {esc(stereo)}</text>',
         f'    <line x1="0" y1="{sep1}" x2="{CLS["box"]}" y2="{sep1}" class="cell-border"/>']
    y0 = sep1 + CLS["row"]
    for i, a in enumerate(attrs):
        o.append(f'    <text x="10" y="{y0 + i * CLS["row"] + 2}" class="cls-member">{esc(a)}</text>')
    ysep = y0 + len(attrs) * CLS["row"]
    o.append(f'    <line x1="0" y1="{ysep}" x2="{CLS["box"]}" y2="{ysep}" class="cell-border"/>')
    for i, m in enumerate(ops):
        o.append(f'    <text x="10" y="{ysep + i * CLS["row"] + 16}" class="cls-member">{esc(m)}</text>')
    o.append("  </g>")
    return "\n".join(o)


def build_class(fig):
    names = CLASS_FIGURES[fig]
    pos, y = {}, CLS["top"]
    for n in names:
        pos[n] = (CLS["x"], y); y += cls_height(n) + CLS["gap"]
    h = int(y + 10)
    labels, rels, paths, li = [], [], [], 0
    for (s, d) in [k for k in MULT if k[0] in names and k[1] in names]:
        ss, st = MULT[(s, d)]
        sx, sy = pos[s]; dy = pos[d][1]
        x = sx + (70 if li % 2 == 0 else 130)
        li += 1
        y1, y2 = sy + cls_height(s), dy
        rels.append(f'  <path d="M {x} {y1} L {x} {y2}" class="rel-line"/>')
        if (s, d) in COMPOSITION:                                  # belah ketupat di sisi agregat
            rels.append(f'  <path d="M {x} {y1} L {x - 9} {y1 + 11} L {x} {y1 + 22} L {x + 9} {y1 + 11} Z" class="diamond"/>')
        rels += card_mark(x, y1 + 14, ss, horizontal=False)
        rels += card_mark(x, y2 - 14, st, horizontal=False)
        add_label(labels, x - 54, y1 + 18, ss, kind="mult")
        add_label(labels, x + 54, y2 - 18, st, kind="mult")
        paths.append([(x, y1), (x, y2)])
    resolve_labels(labels, {})
    errs = audit(paths, {}, [tuple(lb["rect"]) for lb in labels])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CLS["canvas"]} {h}" '
             f'width="{CLS["canvas"]}" height="{h}">', "  <defs>", "    <style>", STYLE.strip(),
             "    </style>", "  </defs>",
             f'  <rect width="{CLS["canvas"]}" height="{h}" fill="#FFFFFF"/>', ""]
    parts += rels
    parts += emit_labels(labels)
    parts.append("")
    for n in names:
        x, yy = pos[n]
        parts.append(class_g(n, x, yy))
    parts.append("</svg>")
    return "\n".join(parts), CLS["canvas"], h, errs


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent.parent / "images"
    out.mkdir(exist_ok=True)
    jobs = [("diagram_erd_konseptual", build_erd, "konseptual"),
            ("diagram_erd_logis", build_erd, "logis"),
            ("diagram_class_a", build_class, "class_a"),
            ("diagram_class_b", build_class, "class_b"),
            ("diagram_class_c", build_class, "class_c")]
    for fname, fn, arg in jobs:
        svg, w, h, errs = fn(arg)
        (out / f"{fname}.svg").write_text(svg, encoding="utf-8")
        (out / f"{fname}.html").write_text(HTML.replace("__SVG__", svg), encoding="utf-8")
        print(f"{fname}: {w}x{h} | temuan: {len(errs)}"
              + ("" if not errs else " -> " + "; ".join(sorted(set(errs)))))
