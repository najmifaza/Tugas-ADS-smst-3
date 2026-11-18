"""
Build SDD v1.1 DOCX — Sistem Informasi Medkreminfo BEM FT UNSOED
================================================================
Menggunakan pipeline yang sama dengan build_docx.py (Tugas 2) tetapi
disesuaikan untuk SDD:
  - Font  : Arial (Template SDD), bukan Times New Roman
  - Input : build/SDD_v1.1_build.md  (mermaid sudah diganti PNG)
  - Output: Tugas_3_KelompokXX_AnalysisModels_v1.1.docx
  - Halaman: Letter 8.5×11 in, margin 1 in
"""

import re
import os
import pathlib

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# ── Paths ────────────────────────────────────────────────────────────────────
BUILD_DIR = pathlib.Path(__file__).parent           # Tugas Per 11/build/
ROOT_DIR  = BUILD_DIR.parent                        # Tugas Per 11/

MD_IN   = BUILD_DIR / "SDD_v1.1_build.md"
OUT     = ROOT_DIR  / "Tugas_3_KelompokXX_AnalysisModels_v1.1.docx"

# ── Typography ───────────────────────────────────────────────────────────────
FONT      = "Arial"
C_TITLE   = RGBColor(0x1E, 0x3A, 0x8A)
C_H1      = RGBColor(0x1E, 0x3A, 0x8A)
C_H2      = RGBColor(0x25, 0x63, 0xEB)
C_BODY    = RGBColor(0x0F, 0x17, 0x2A)
C_MUTED   = RGBColor(0x47, 0x55, 0x69)

# Total printable width in dxa (Letter - 2× margin = 6.5 in = 9360 dxa)
TOTAL_W_DXA = 9360   # 6.5 in × 1440


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f"""
        <w:tblBorders {nsdecls("w")}>
            <w:top    w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left   w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right  w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    """)
    tblPr.append(borders)


def plain(s):
    return re.sub(r"[*_`]", "", s)


def col_widths(rows):
    n = len(rows[0])

    def cw(ch):
        if re.match(r"[A-Z0-9#]", ch):   return 140
        if re.match(r"[ilftjr.,:;()/\-]", ch): return 62
        return 98

    mins, weights = [], []
    for c in range(n):
        longest, tot = 0, 0
        for ri, r in enumerate(rows):
            cell_str = plain(r[c] if c < len(r) else "")
            tot += len(cell_str)
            f = 1.12 if (ri == 0 or (c < len(r) and r[c].startswith("**"))) else 1.0
            for w in cell_str.split():
                w_len = f * sum(cw(ch) for ch in w)
                if w_len > longest:
                    longest = w_len
        mins.append(min(longest * 1.0 + 170, 2500))
        weights.append(max(8, min(tot / max(len(rows), 1), 120)))

    sum_min = sum(mins)
    if sum_min >= TOTAL_W_DXA:
        w = [int(m * TOTAL_W_DXA / sum_min) for m in mins]
    else:
        extra = TOTAL_W_DXA - sum_min
        sw = sum(weights)
        w = [int(m + extra * weights[i] / sw) for i, m in enumerate(mins)]

    rem = TOTAL_W_DXA - sum(w)
    w[-1] += rem
    return w


def add_runs(paragraph, text, size=9.5, bold=False, italic=False, color=None):
    """Parse inline markdown (bold, italic, code) and add runs."""
    color = color or C_BODY
    RE = re.compile(r"(\*\*\*([^*]+)\*\*\*|\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`)")
    last = 0
    for m in RE.finditer(text):
        if m.start() > last:
            r = paragraph.add_run(text[last:m.start()])
            r.font.name = FONT; r.font.size = Pt(size)
            r.font.bold = bold; r.font.italic = italic
            r.font.color.rgb = color
        g2, g3, g4, g5 = m.group(2), m.group(3), m.group(4), m.group(5)
        r = paragraph.add_run(g2 or g3 or g4 or g5)
        r.font.name = FONT; r.font.size = Pt(size if g5 is None else size - 1)
        r.font.bold  = bold  or (g2 is not None) or (g3 is not None)
        r.font.italic = italic or (g2 is not None) or (g4 is not None)
        r.font.color.rgb = color
        if g5 is not None:
            r.font.name = "Consolas"
        last = m.end()
    if last < len(text):
        r = paragraph.add_run(text[last:])
        r.font.name = FONT; r.font.size = Pt(size)
        r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color


def make_table(doc, rows):
    widths = col_widths(rows)
    table = doc.add_table(rows=len(rows), cols=len(widths))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)

    for ri, row in enumerate(rows):
        trow = table.rows[ri]
        trPr = trow._tr.get_or_add_trPr()
        trPr.append(parse_xml(f"<w:cantSplit {nsdecls('w')}/>"))
        if ri == 0:
            trPr.append(parse_xml(f"<w:tblHeader {nsdecls('w')}/>"))

        for ci, cell_text in enumerate(row):
            cell = trow.cells[ci]
            cell.width = Inches(widths[ci] / 1440.0)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ri == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(0)

            clean = cell_text.replace("<br>", "\n").replace("&amp;", "&")
            sub_lines = clean.split("\n")
            for sli, sl in enumerate(sub_lines):
                if sli > 0:
                    p = cell.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after  = Pt(0)
                add_runs(p, sl, size=8.5 if ri == 0 else 9,
                         bold=(ri == 0), color=C_BODY)
    return table


# ── Main builder ─────────────────────────────────────────────────────────────

def build(md_path: pathlib.Path, out_path: pathlib.Path):
    lines = md_path.read_text(encoding="utf-8").split("\n")
    img_base = md_path.parent   # images are relative to build/ folder

    doc = Document()

    # Page setup: Letter, 1-inch margins
    sec = doc.sections[0]
    sec.page_width   = Inches(8.5)
    sec.page_height  = Inches(11.0)
    sec.top_margin   = sec.bottom_margin = Inches(1.0)
    sec.left_margin  = sec.right_margin  = Inches(1.0)

    # Base style
    ns = doc.styles["Normal"]
    ns.font.name = FONT
    ns.font.size = Pt(9.5)
    ns.font.color.rgb = C_BODY
    ns.paragraph_format.space_after  = Pt(4)
    ns.paragraph_format.line_spacing = 1.15

    in_table, table_rows = False, []
    i = 0

    def flush_table():
        nonlocal in_table, table_rows
        cleaned = []
        for row in table_rows:
            if re.match(r"^\s*\|?\s*[-:\s|]+\s*\|?\s*$", row):
                continue
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            cleaned.append(cells)
        if cleaned:
            sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(2)
            make_table(doc, cleaned)
            sp2 = doc.add_paragraph(); sp2.paragraph_format.space_after = Pt(4)
        in_table = False
        table_rows.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Tables ──────────────────────────────────────────────────────────
        if stripped.startswith("|") and "|" in stripped[1:]:
            in_table = True
            table_rows.append(stripped)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        if not stripped:
            i += 1
            continue

        if re.match(r"^---+\s*$", stripped):
            i += 1
            continue

        # ── Headings ─────────────────────────────────────────────────────────
        h_match = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if h_match:
            lvl  = len(h_match.group(1))
            text = h_match.group(2).strip()
            # Page break before top-level chapters (# or ##  that start a bab)
            if lvl == 1 or (lvl == 2 and re.match(r"^(1|2|3|4|5|6|7)\.", text)):
                doc.add_page_break()
            p = doc.add_paragraph()
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(10 if lvl <= 2 else 6)
            p.paragraph_format.space_after  = Pt(3)
            if lvl == 1:
                add_runs(p, text, size=20, bold=True, color=C_TITLE)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif lvl == 2:
                add_runs(p, text, size=13.5, bold=True, color=C_H1)
            elif lvl == 3:
                add_runs(p, text, size=11.5, bold=True, color=C_H2)
            else:
                add_runs(p, text, size=9.5, bold=True, color=C_BODY)
            i += 1
            continue

        # ── Skip remaining fenced code blocks (should be none in build MD) ──
        if stripped.startswith("```"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue

        # ── Images ───────────────────────────────────────────────────────────
        img_m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if img_m:
            alt, img_rel = img_m.groups()
            img_path = (img_base / img_rel).resolve()
            if img_path.exists():
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(6)
                p_img.paragraph_format.space_after  = Pt(2)
                p_img.paragraph_format.keep_with_next = True
                r_img = p_img.add_run()
                # Fit image to printable width (6.5 in)
                r_img.add_picture(str(img_path), width=Inches(6.3))
                # Caption
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(0)
                p_cap.paragraph_format.space_after  = Pt(6)
                add_runs(p_cap, alt, size=9, italic=True, color=C_MUTED)
                print(f"  ✓ Gambar: {img_path.name}")
            else:
                p_miss = doc.add_paragraph()
                add_runs(p_miss, f"[Gambar tidak ditemukan: {img_rel}]", size=9, italic=True, color=C_MUTED)
                print(f"  ✗ MISSING: {img_path}")
            i += 1
            continue

        # ── Blockquote ───────────────────────────────────────────────────────
        if stripped.startswith("> "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after  = Pt(2)
            add_runs(p, stripped[2:].strip(), size=9, italic=True, color=C_MUTED)
            i += 1
            continue

        # ── Lists ─────────────────────────────────────────────────────────────
        li_m = re.match(r"^(\s*)([*\-]|\d+\.)\s+(.*)$", stripped)
        # Try matching from raw `line` for proper indentation
        li_m2 = re.match(r"^(\s*)([*\-]|\d+\.)\s+(.*)$", line)
        if li_m2:
            indent_spaces = len(li_m2.group(1))
            bullet = li_m2.group(2)
            content = li_m2.group(3)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(1)
            base_ind = 0.25 * (1 + (indent_spaces // 2))
            p.paragraph_format.left_indent       = Inches(base_ind)
            p.paragraph_format.first_line_indent = Inches(-0.22)
            marker = f"{bullet} " if re.match(r"\d+\.", bullet) else "•  "
            r_m = p.add_run(marker)
            r_m.font.name = FONT; r_m.font.size = Pt(9.5); r_m.font.color.rgb = C_BODY
            add_runs(p, content, size=9.5, color=C_BODY)
            i += 1
            continue

        # ── HTML tags (skip) ─────────────────────────────────────────────────
        if re.match(r"^<[!/]?[a-z]", stripped, re.I):
            i += 1
            continue

        # ── Regular paragraph ────────────────────────────────────────────────
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(4)
        add_runs(p, stripped, size=9.5, color=C_BODY)
        i += 1

    if in_table and table_rows:
        flush_table()

    doc.save(str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"\n✅ Selesai: {out_path.name}  ({size_kb} KB)")
    # Quick stats
    print(f"   Paragraf : {len(doc.paragraphs)}")
    print(f"   Tabel    : {len(doc.tables)}")
    print(f"   Gambar   : {len(doc.inline_shapes)}")


if __name__ == "__main__":
    print(f"Input  : {MD_IN}")
    print(f"Output : {OUT}\n")
    build(MD_IN, OUT)
