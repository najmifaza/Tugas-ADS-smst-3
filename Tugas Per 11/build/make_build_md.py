"""
Buat SDD_v1.1_build.md dari SDD_Medkreminfo_v1.1.md:
- Ganti setiap blok ```mermaid ... ``` dengan referensi gambar PNG.
- Sesuaikan path gambar Lampiran D (diagrams_upstream) supaya relatif dari folder build/.
"""

import re
import pathlib

HERE = pathlib.Path(__file__).parent           # build/
ROOT = HERE.parent                             # Tugas Per 11/

SRC  = ROOT / "SDD_Medkreminfo_v1.1.md"
OUT  = HERE  / "SDD_v1.1_build.md"

# Urutan penggantian mermaid -> gambar (sesuai urutan muncul di file)
IMAGE_REFS = [
    "![Gambar 3.2 Sequence Diagram SD-01: Pengajuan Tiket Request Konten](../images/seq_diagram_sd01.png)",
    "![Gambar 3.3 Sequence Diagram SD-02: Validasi dan Penugasan Tiket Konten](../images/seq_diagram_sd02.png)",
    "![Gambar 3.4 Sequence Diagram SD-03: Pengerjaan dan Unggah Draf Karya](../images/seq_diagram_sd03.png)",
    "![Gambar 3.5 Sequence Diagram SD-04: Tinjauan Draf, Persetujuan Akhir, dan Publikasi](../images/seq_diagram_sd04.png)",
    "![Gambar 4.1 ERD Konseptual (Crow's Foot, tanpa kunci tamu)](../images/diagram_erd_konseptual.png)",
    "![Gambar 4.2 ERD Logis 3NF (Crow's Foot) beserta penanda PK, FK, dan UK](../images/diagram_erd_logis.png)",
    "![Gambar 6.1 UML Class Diagram domain sistem (8 kelas)](../images/diagram_class_full.png)",
]

content = SRC.read_text(encoding="utf-8")

# Temukan semua blok ```mermaid ... ```
MERMAID_RE = re.compile(r"```mermaid\n.*?```", re.DOTALL)
blocks = MERMAID_RE.findall(content)
print(f"Ditemukan {len(blocks)} blok mermaid")
assert len(blocks) == len(IMAGE_REFS), (
    f"Jumlah blok ({len(blocks)}) != jumlah pengganti ({len(IMAGE_REFS)})"
)

# Ganti satu per satu (supaya urutan terjaga)
idx = [0]
def replacer(m):
    r = IMAGE_REFS[idx[0]]
    print(f"  Blok {idx[0]+1}: diganti dengan {r[:60]}...")
    idx[0] += 1
    return r

result = MERMAID_RE.sub(replacer, content)

# Perbaiki path diagrams_upstream di Lampiran D
# Dari: diagrams_upstream/xxx.png  ->  ../diagrams_upstream/xxx.png
result = result.replace(
    "](diagrams_upstream/",
    "](../diagrams_upstream/"
)

OUT.write_text(result, encoding="utf-8")
print(f"\nSelesai! Output: {OUT}")
print(f"Ukuran: {OUT.stat().st_size:,} bytes")
