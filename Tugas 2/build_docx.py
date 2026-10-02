import re
import os
import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def make_callout_box(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Cm(14.0)
    set_cell_shading(cell, "F4F8FC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=140)
    
    # Left thick border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

def create_element(name):
    return OxmlElement(name)

def build_srs_docx(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    doc = Document()

    # Page Setup (A4, Left 4cm, Right 3cm, Top 4cm, Bottom 3cm)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(4.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(3.0)

    # Base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.space_before = Pt(0)

    lines = md_content.split('\n')
    i = 0
    total_lines = len(lines)

    in_table = False
    table_rows = []

    def flush_table(rows):
        if not rows:
            return
        
        # Clean rows
        cleaned_rows = []
        for r in rows:
            # check if separator row
            if re.match(r'^\s*\|?\s*[-:\s|]+\s*\|?\s*$', r):
                continue
            cells = [c.strip() for c in r.strip().strip('|').split('|')]
            cleaned_rows.append(cells)
        
        if not cleaned_rows:
            return

        col_count = max(len(r) for r in cleaned_rows)
        # Pad shorter rows
        for r in cleaned_rows:
            while len(r) < col_count:
                r.append('')

        tbl = doc.add_table(rows=len(cleaned_rows), cols=col_count)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl, color="CCCCCC", sz="4", val="single")

        # Column widths calculation (total width 14cm)
        total_w = 14.0
        # Determine column weights roughly based on headers
        headers = cleaned_rows[0]
        col_widths = []
        if col_count == 2:
            col_widths = [4.5, 9.5]
        elif col_count == 3:
            col_widths = [3.5, 5.0, 5.5]
        elif col_count == 4:
            if 'ID' in headers[0] or 'Req' in headers[0]:
                col_widths = [2.2, 5.8, 3.5, 2.5]
            else:
                col_widths = [3.0, 4.0, 4.0, 3.0]
        elif col_count == 6:
            col_widths = [1.8, 2.7, 3.0, 2.5, 2.5, 1.5]
        elif col_count == 7:
            col_widths = [1.5, 2.2, 2.5, 2.5, 1.8, 2.0, 1.5]
        else:
            w_each = total_w / col_count
            col_widths = [w_each] * col_count

        for row_idx, row_data in enumerate(cleaned_rows):
            row = tbl.rows[row_idx]
            # row cantSplit
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            if row_idx == 0:
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

            for col_idx, cell_value in enumerate(row_data):
                cell = row.cells[col_idx]
                cell.width = Cm(col_widths[col_idx] if col_idx < len(col_widths) else total_w/col_count)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

                if row_idx == 0:
                    set_cell_shading(cell, "F0F4F8")

                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)

                # Process formatting inside cell
                # check bold header
                cell_text = cell_value.replace('<br>', '\n').replace('&amp;', '&')
                
                # Split by newline if present
                sub_lines = cell_text.split('\n')
                for sl_idx, sl in enumerate(sub_lines):
                    if sl_idx > 0:
                        p = cell.add_paragraph()
                        p.paragraph_format.line_spacing = 1.15
                        p.paragraph_format.space_after = Pt(2)
                        p.paragraph_format.space_before = Pt(0)
                    
                    # Parse bold / italic inline
                    # Simple markdown bold inline parser
                    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', sl)
                    for tok in tokens:
                        if tok.startswith('**') and tok.endswith('**'):
                            r = p.add_run(tok[2:-2])
                            r.font.name = 'Times New Roman'
                            r.font.size = Pt(10.5 if row_idx > 0 else 10.5)
                            r.font.bold = True
                            if row_idx == 0:
                                r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
                        elif tok.startswith('*') and tok.endswith('*'):
                            r = p.add_run(tok[1:-1])
                            r.font.name = 'Times New Roman'
                            r.font.size = Pt(10.5)
                            r.font.italic = True
                        else:
                            r = p.add_run(tok)
                            r.font.name = 'Times New Roman'
                            r.font.size = Pt(10.5)
                            if row_idx == 0:
                                r.font.bold = True
                                r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

        # space after table
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6)

    while i < total_lines:
        line = lines[i]
        stripped = line.strip()

        # Check table
        if stripped.startswith('|') and '|' in stripped[1:]:
            in_table = True
            table_rows.append(stripped)
            i += 1
            continue
        else:
            if in_table:
                flush_table(table_rows)
                in_table = False
                table_rows = []

        if not stripped:
            i += 1
            continue

        # Horizontal rule
        if stripped in ['---', '***', '___']:
            i += 1
            continue

        # Images
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
        if img_match:
            alt_text, img_file = img_match.groups()
            img_path = os.path.join(os.path.dirname(md_path), img_file)
            if os.path.exists(img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                run_img = p_img.add_run()
                run_img.add_picture(img_path, width=Cm(14.0))
            i += 1
            continue

        # Headings
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(stripped[2:])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            i += 1
            continue

        if stripped.startswith('## '):
            text = stripped[3:]
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            
            # Subtitle under title vs regular section
            if i < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(13)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(text)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(13)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x0F, 0x24, 0x38)
            i += 1
            continue

        if stripped.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            if i < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(stripped[4:])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x2B, 0x4C, 0x7E)
            i += 1
            continue

        if stripped.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(stripped[5:])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.font.bold = True
            r.font.italic = True
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            i += 1
            continue

        # Bullet lists
        if stripped.startswith('* ') or stripped.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.line_spacing = 1.3
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            content = stripped[2:]
            
            # format inline
            tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', content)
            for tok in tokens:
                if tok.startswith('**') and tok.endswith('**'):
                    r = p.add_run(tok[2:-2])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
                    r.font.bold = True
                elif tok.startswith('*') and tok.endswith('*'):
                    r = p.add_run(tok[1:-1])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
                    r.font.italic = True
                else:
                    r = p.add_run(tok)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
            i += 1
            continue

        # Numbered lists (e.g. 1. 2. 3.)
        num_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if num_match:
            num, content = num_match.groups()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.paragraph_format.line_spacing = 1.3
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)

            r_num = p.add_run(f"{num}. ")
            r_num.font.name = 'Times New Roman'
            r_num.font.size = Pt(12)
            r_num.font.bold = True

            tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', content)
            for tok in tokens:
                if tok.startswith('**') and tok.endswith('**'):
                    r = p.add_run(tok[2:-2])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
                    r.font.bold = True
                elif tok.startswith('*') and tok.endswith('*'):
                    r = p.add_run(tok[1:-1])
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
                    r.font.italic = True
                else:
                    r = p.add_run(tok)
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(12)
            i += 1
            continue

        # Image captions or italic principle notes
        if stripped.startswith('*Gambar') or stripped.startswith('*Prinsip:'):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(8)
            clean_text = stripped.strip('*')
            r = p.add_run(clean_text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue

        # Regular Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', stripped)
        for tok in tokens:
            if tok.startswith('**') and tok.endswith('**'):
                r = p.add_run(tok[2:-2])
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True
            elif tok.startswith('*') and tok.endswith('*'):
                r = p.add_run(tok[1:-1])
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.italic = True
            else:
                r = p.add_run(tok)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)

        i += 1

    if in_table:
        flush_table(table_rows)

    doc.save(docx_path)
    print(f"Successfully generated DOCX: {docx_path} ({os.path.getsize(docx_path)} bytes)")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md = os.path.join(script_dir, "Draft_SRS_Medkreminfo.md")
    out_docx = os.path.join(script_dir, "Draft_SRS_Medkreminfo.docx")
    build_srs_docx(md, out_docx)
    out_rtm = os.path.join(script_dir, "Tugas_2_KelompokXX_DraftSRS.docx")
    build_srs_docx(md, out_rtm)
