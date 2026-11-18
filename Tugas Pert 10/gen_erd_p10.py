"""Generate ERD v1 (Crow's Foot) untuk P10 - layout 2 kolom, font besar agar terbaca saat dicetak.

Canvas 960x1344 px dipasang pada lebar 6.14 in -> teks nama kolom 15px == ~6.9 pt saat dicetak.
Jalankan: python gen_erd_p10.py  (hasil: diagram_erd_p10.svg + diagram_erd_p10.html)
"""

BOX_W = 420
HEADER = 30
ROW_H = 30
PAD = 6
LEFT_X = 20
RIGHT_X = 520
CANVAS_W = 960
CANVAS_H = 1344

# (type, name, key, desc)
ENTITIES = {
    "KEMENTERIAN": [
        ("INT", "id_kementerian", "PK", ""),
        ("VARCHAR", "nama_kementerian", "", ""),
        ("VARCHAR", "kode_kementerian", "", ""),
    ],
    "PENGGUNA": [
        ("INT", "id_pengguna", "PK", ""),
        ("INT", "id_kementerian", "FK", "(null) staf"),
        ("VARCHAR", "nama_lengkap", "", ""),
        ("VARCHAR", "email", "", ""),
        ("VARCHAR", "password_hash", "", ""),
        ("VARCHAR", "role", "", "3 peran"),
        ("VARCHAR", "spesialisasi", "", "(null)"),
        ("VARCHAR", "no_whatsapp", "", ""),
    ],
    "TIKET_PESANAN": [
        ("VARCHAR", "id_tiket", "PK", "#MED-YYMM"),
        ("INT", "id_pemohon", "FK", "Akun Klien"),
        ("INT", "id_eksekutor", "FK", "(null)"),
        ("VARCHAR", "judul_publikasi", "", ""),
        ("VARCHAR", "kanal_tujuan", "", "Feeds/TikTok"),
        ("DATE", "tanggal_target_tayang", "", ""),
        ("DATETIME", "tanggal_pengajuan", "", ""),
        ("DATETIME", "waktu_penugasan", "", "(null)"),
        ("TEXT", "deskripsi_brief", "", ""),
        ("VARCHAR", "status_tiket", "", "Submitted dst"),
        ("BOOLEAN", "is_rush_order", "", "BR-01"),
        ("TEXT", "alasan_darurat", "", "(null)"),
        ("TEXT", "catatan_penolakan", "", "(null)"),
    ],
    "BERKAS_ASET": [
        ("INT", "id_aset", "PK", ""),
        ("VARCHAR", "id_tiket", "FK", ""),
        ("VARCHAR", "nama_file", "", ""),
        ("VARCHAR", "file_path", "", ""),
        ("INT", "ukuran_mb", "", "maks 50MB"),
        ("VARCHAR", "format_file", "", "PNG/JPG/PDF"),
        ("VARCHAR", "tautan_gdrive", "", "(null)"),
        ("BOOLEAN", "status_purged", "", "BR-05"),
    ],
    "DRAF_KARYA": [
        ("INT", "id_draf", "PK", ""),
        ("VARCHAR", "id_tiket", "FK", ""),
        ("VARCHAR", "versi_draf", "", "v1, v2"),
        ("VARCHAR", "file_path_preview", "", ""),
        ("VARCHAR", "tautan_preview_video", "", "(null)"),
        ("TEXT", "catatan_draf", "", ""),
        ("DATETIME", "tanggal_unggah", "", ""),
    ],
    "RIWAYAT_REVISI": [
        ("INT", "id_revisi", "PK", ""),
        ("VARCHAR", "id_tiket", "FK", ""),
        ("INT", "revisi_ke", "", "1-2 (BR-02)"),
        ("TEXT", "poin_revisi", "", ""),
        ("DATETIME", "tanggal_pengajuan_revisi", "", ""),
    ],
    "PUBLIKASI_KONTEN": [
        ("INT", "id_publikasi", "PK", ""),
        ("VARCHAR", "id_tiket", "FK", ""),
        ("VARCHAR", "url_postingan_medsos", "", "FR-15"),
        ("DATETIME", "tanggal_terbit", "", ""),
        ("INT", "id_staf_medsos", "FK", "Staf Publikasi"),
    ],
}

POS = {
    "KEMENTERIAN": (LEFT_X, 40),
    "PENGGUNA": (LEFT_X, 236),
    "TIKET_PESANAN": (LEFT_X, 622),
    "RIWAYAT_REVISI": (LEFT_X, 1118),
    "BERKAS_ASET": (RIGHT_X, 236),
    "PUBLIKASI_KONTEN": (RIGHT_X, 622),
    "DRAF_KARYA": (RIGHT_X, 938),
}


def box_height(name):
    return HEADER + len(ENTITIES[name]) * ROW_H + PAD


def entity_g(name):
    x, y = POS[name]
    h = box_height(name)
    rows = ENTITIES[name]
    out = [f'  <g transform="translate({x}, {y})">']
    out.append(f'    <rect width="{BOX_W}" height="{h}" class="body-box"/>')
    out.append(f'    <rect width="{BOX_W}" height="{HEADER}" class="header-box"/>')
    out.append(f'    <text x="{BOX_W // 2}" y="21" class="entity-title">{name}</text>')
    out.append(f'    <line x1="104" y1="{HEADER}" x2="104" y2="{h}" class="cell-border"/>')
    out.append(f'    <line x1="322" y1="{HEADER}" x2="322" y2="{h}" class="cell-border"/>')
    for i in range(1, len(rows)):
        yl = HEADER + i * ROW_H
        out.append(f'    <line x1="0" y1="{yl}" x2="{BOX_W}" y2="{yl}" class="cell-border"/>')
    for i, (typ, nm, key, desc) in enumerate(rows):
        base = HEADER + i * ROW_H + 21
        out.append(f'    <text x="10" y="{base}" class="t-type">{typ}</text>')
        out.append(f'    <text x="112" y="{base}" class="t-name">{nm}</text>')
        if key:
            cls = "t-pk" if key == "PK" else "t-fk"
            out.append(f'    <text x="310" y="{base}" class="{cls}">{key}</text>')
        if desc:
            out.append(f'    <text x="330" y="{base}" class="t-desc">{desc.replace("&", "&amp;").replace("<", "&lt;")}</text>')
    out.append("  </g>")
    return "\n".join(out)


def rel(path_d, one_marks, crow_marks, labels):
    """one_marks: list of (x1,y1,x2,y2) dua garis sejajar (mandatory/optional one).
    crow_marks: list of (cx, cy, foot_path_d) or (None, None, path) untuk crow tanpa lingkaran.
    labels: list of (cx, cy, text, pill_width)."""
    out = [f'  <path d="{path_d}" class="rel-line"/>']
    for x1, y1, x2, y2 in one_marks:
        out.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="rel-line"/>')
    for cx, cy, foot in crow_marks:
        if cx is not None:
            out.append(f'  <circle cx="{cx}" cy="{cy}" r="4.5" class="symbol"/>')
        out.append(f'  <path d="{foot}" class="crow"/>')
    for cx, cy, text, w in labels:
        out.append(f'  <rect x="{cx - w // 2}" y="{cy - 11}" width="{w}" height="22" class="pill"/>')
        out.append(f'  <text x="{cx}" y="{cy + 4}" class="rel-label">{text}</text>')
    return "\n".join(out)


RELATIONS = [
    # 1. KEMENTERIAN 1 : N PENGGUNA  [menaungi]
    rel("M 230 166 L 230 236",
        [(222, 172, 238, 172), (222, 178, 238, 178)],
        [(230, 223, "M 222 236 L 230 227 L 238 236")],
        [(230, 204, "menaungi", 58)]),
    # 2. PENGGUNA 1 : N TIKET_PESANAN  [mengajukan / id_pemohon]
    rel("M 150 512 L 150 622",
        [(142, 518, 158, 518), (142, 524, 158, 524)],
        [(150, 609, "M 142 622 L 150 613 L 158 622")],
        [(150, 567, "mengajukan", 72)]),
    # 3. PENGGUNA 0..1 : N TIKET_PESANAN  [mengerjakan / id_eksekutor]
    rel("M 310 512 L 310 622",
        [(302, 530, 318, 530)],
        [(310, 522, "M 302 530 L 310 522 L 318 530"), (310, 609, "M 302 622 L 310 613 L 318 622")],
        [(310, 567, "mengerjakan", 78)]),
    # 4. TIKET_PESANAN 1 : N BERKAS_ASET  [memiliki]
    rel("M 440 660 L 470 660 L 470 374 L 520 374",
        [(446, 652, 446, 668), (452, 652, 452, 668)],
        [(506, 374, "M 508 366 L 520 374 L 508 382")],
        [(470, 430, "memiliki", 58)]),
    # 5. TIKET_PESANAN 1 : N DRAF_KARYA  [menghasilkan]
    rel("M 440 1000 L 520 1000",
        [(446, 992, 446, 1008), (452, 992, 452, 1008)],
        [(506, 1000, "M 508 992 L 520 1000 L 508 1008")],
        [(480, 982, "menghasilkan", 78)]),
    # 6. TIKET_PESANAN 1 : N RIWAYAT_REVISI  [menerima]
    rel("M 230 1048 L 230 1118",
        [(222, 1054, 238, 1054), (222, 1060, 238, 1060)],
        [(230, 1104, "M 222 1118 L 230 1109 L 238 1118")],
        [(230, 1086, "menerima", 58)]),
    # 7. TIKET_PESANAN 1 : 1 PUBLIKASI_KONTEN  [diterbitkan pada]
    rel("M 440 700 L 520 700",
        [(446, 692, 446, 708), (452, 692, 452, 708),
         (508, 692, 508, 708), (514, 692, 514, 708)],
        [],
        [(480, 668, "diterbitkan", 74), (480, 684, "pada", 34)]),
    # 8. PENGGUNA 1 : N PUBLIKASI_KONTEN  [mempublikasikan / id_staf_medsos]
    rel("M 440 480 L 480 480 L 480 560 L 700 560 L 700 622",
        [(446, 472, 446, 488), (452, 472, 452, 488)],
        [(700, 608, "M 692 622 L 700 613 L 708 622")],
        [(590, 548, "mempublikasikan", 106)]),
]

STYLE = """
      .entity-title { font-family: 'Times New Roman', serif; font-size: 17px; font-weight: bold; fill: #000000; text-anchor: middle; }
      .header-box { fill: #D9D9D9; stroke: #000000; stroke-width: 1.6; }
      .body-box { fill: #FFFFFF; stroke: #000000; stroke-width: 1.6; }
      .cell-border { stroke: #D1D5DB; stroke-width: 0.9; }
      .t-type { font-family: 'Times New Roman', serif; font-size: 13px; font-style: italic; fill: #4B5563; }
      .t-name { font-family: 'Consolas', 'Courier New', monospace; font-size: 15px; fill: #000000; }
      .t-pk { font-family: 'Times New Roman', serif; font-size: 13px; font-weight: bold; fill: #000000; text-anchor: middle; }
      .t-fk { font-family: 'Times New Roman', serif; font-size: 13px; font-weight: bold; fill: #1F2937; text-anchor: middle; }
      .t-desc { font-family: 'Times New Roman', serif; font-size: 13px; fill: #4B5563; }
      .rel-line { stroke: #000000; stroke-width: 1.7; fill: none; }
      .rel-label { font-family: 'Times New Roman', serif; font-size: 13px; font-style: italic; fill: #000000; text-anchor: middle; }
      .pill { fill: #FFFFFF; stroke: none; }
      .crow { stroke: #000000; stroke-width: 1.7; fill: none; stroke-linecap: round; }
      .symbol { stroke: #000000; stroke-width: 1.7; fill: #FFFFFF; }
""".strip("\n")


def build_svg():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'width="{CANVAS_W}" height="{CANVAS_H}">',
        "  <defs>",
        "    <style>",
        STYLE,
        "    </style>",
        "  </defs>",
        "",
        f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#FFFFFF"/>',
        "",
        "  <!-- ================= RELASI ================= -->",
    ]
    parts.extend(RELATIONS)
    parts.append("")
    parts.append("  <!-- ================= ENTITAS ================= -->")
    for name in ENTITIES:
        parts.append(entity_g(name))
    parts.append("")
    parts.append("</svg>")
    return "\n".join(parts)


HTML = (
    '<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
    "body{margin:0;padding:0;background:#fff;}svg{display:block;}"
    "</style></head><body>\n__SVG__\n</body></html>"
)

if __name__ == "__main__":
    import pathlib

    svg = build_svg()
    here = pathlib.Path(__file__).parent
    (here / "diagram_erd_p10.svg").write_text(svg, encoding="utf-8")
    (here / "diagram_erd_p10.html").write_text(HTML.replace("__SVG__", svg), encoding="utf-8")
    print(f"OK: {CANVAS_W}x{CANVAS_H}, {len(ENTITIES)} entitas, {len(RELATIONS)} relasi")
