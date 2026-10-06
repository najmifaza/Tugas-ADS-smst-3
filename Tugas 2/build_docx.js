const fs = require('fs');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, AlignmentType,
  WidthType, BorderStyle, Footer, PageNumber, LevelFormat, HeadingLevel, TabStopType, Tab,
  TableLayoutType, VerticalAlign, LineRuleType } = D;

const SRC = '/mnt/user-data/uploads/';
const OUT = process.argv[2];
const pageMap = process.argv[3] ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : {};
const FONT = 'Times New Roman';
const TOTAL_W = 7937; // A4 11906 - 2268 (4cm) - 1701 (3cm)
let rawLines = fs.readFileSync(SRC + 'Draft_SRS_Medkreminfo.md', 'utf8').split('\n');
{ // place Referensi before Lampiran so body order matches the Daftar Isi
  const r = rawLines.findIndex(l => l.startsWith('## Referensi Acuan'));
  const a = rawLines.findIndex(l => l.startsWith('## Lampiran A'));
  if (r > a && a > 0) { const ref = rawLines.slice(r); rawLines = [...rawLines.slice(0, a), ...ref, '', '---', '', ...rawLines.slice(a, r)]; }
}
const lines = rawLines;

const tr = (text, o = {}) => new TextRun({ text, font: FONT, size: 24, ...o });
function runs(text, base = {}) {
  const out = []; const re = /(\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`)/g; let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(tr(text.slice(last, m.index), base));
    if (m[2] !== undefined) out.push(tr(m[2], { ...base, bold: true }));
    else if (m[3] !== undefined) out.push(tr(m[3], { ...base, italics: true }));
    else out.push(tr(m[4], base));
    last = re.lastIndex;
  }
  if (last < text.length) out.push(tr(text.slice(last), base));
  return out;
}
const plain = s => s.replace(/\*\*|\*|`/g, '');

const body = (text, opts = {}) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
  children: runs(text, opts.run || {}), ...(opts.p || {}),
});
const spacer = () => new Paragraph({ spacing: { line: 240, before: 0, after: 0 }, children: [tr('', { size: 12 })] });

// ---- numbering
const numConfigs = [];
const lvlIndent = l => ({ left: (l + 1) * 454, hanging: 340 });
numConfigs.push({
  reference: 'bul',
  levels: [0, 1, 2, 3].map(l => ({
    level: l, format: LevelFormat.BULLET, text: l % 2 ? '–' : '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: lvlIndent(l) }, run: { font: FONT } },
  })),
});
let numCount = 0;
function newNumRef(lvl) {
  const ref = 'num' + (++numCount);
  numConfigs.push({
    reference: ref,
    levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: lvlIndent(lvl) }, run: { font: FONT } } }],
  });
  return ref;
}

// ---- table
const B = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
const borders = { top: B, bottom: B, left: B, right: B };
function colWidths(rows) {
  const n = rows[0].length;
  const cw = ch => (/[A-Z0-9#]/.test(ch) ? 140 : /[ilftjr.,:;()\/\-]/.test(ch) ? 62 : 98);
  const mins = [], weights = [];
  for (let c = 0; c < n; c++) {
    let longest = 0, tot = 0;
    rows.forEach((r, ri) => {
      const t = plain(r[c] || '');
      tot += t.length;
      const f = (ri === 0 || /^\*\*/.test(r[c] || '')) ? 1.12 : 1;
      t.split(/\s+/).forEach(w => { longest = Math.max(longest, f * [...w].reduce((a, ch) => a + cw(ch), 0)); });
    });
    mins.push(Math.min(longest * 1.0 + 170, 2500));
    weights.push(Math.max(8, Math.min(tot / rows.length, 120)));
  }
  let sumMin = mins.reduce((a, b) => a + b, 0);
  let w;
  if (sumMin >= TOTAL_W) w = mins.map(m => Math.floor(m * TOTAL_W / sumMin));
  else {
    const extra = TOTAL_W - sumMin, sw = weights.reduce((a, b) => a + b, 0);
    w = mins.map((m, i) => Math.floor(m + extra * weights[i] / sw));
  }
  w[w.length - 1] += TOTAL_W - w.reduce((a, b) => a + b, 0);
  return w;
}
function makeTable(rows) {
  const widths = colWidths(rows);
  const trs = rows.map((r, ri) => new TableRow({
    tableHeader: ri === 0, cantSplit: true,
    children: r.map((cell, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA }, borders,
      margins: { top: 40, bottom: 40, left: 80, right: 80 }, verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        alignment: ri === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { line: 240, before: 0, after: 0 },
        children: runs(cell, ri === 0 ? { bold: true } : {}),
      })],
    })),
  }));
  return new Table({
    width: { size: TOTAL_W, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED,
    borders: { ...borders, insideHorizontal: B, insideVertical: B }, rows: trs,
  });
}

// ---- parse
const children = []; const tocEntries = [];
let cover = true; const runsByLvl = {};
const lvlOf = s => (s.length >= 6 ? 3 : s.length >= 4 ? 2 : s.length >= 2 ? 1 : 0);
let i = 0;
while (i < lines.length) {
  const line = lines[i];
  if (!line.trim()) { i++; continue; }
  if (/^---+\s*$/.test(line)) { i++; continue; }

  const h = line.match(/^(#{1,4})\s+(.*)$/);
  if (h) {
    const lvl = h[1].length, text = h[2].trim();
    Object.keys(runsByLvl).forEach(k => delete runsByLvl[k]);
    if (text === 'Daftar Isi') {
      cover = false;
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [tr(text, { bold: true })] }));
      i++;
      while (i < lines.length && !/^---+\s*$/.test(lines[i])) {
        const m = lines[i].match(/^(\s*)([*-]|\d+\.)\s+(.*)$/);
        if (m) {
          const num = /\d+\./.test(m[2]);
          tocEntries.push({ title: num ? `${m[2]} ${m[3]}` : m[3], level: (!num && m[1].length >= 2) ? 1 : 0 });
        }
        i++;
      }
      const tocParas = tocEntries.map(e => new Paragraph({
        spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 }, indent: { left: e.level ? 567 : 0 },
        tabStops: [{ type: TabStopType.RIGHT, position: TOTAL_W, leader: 'dot' }],
        children: [tr(e.title), new TextRun({ font: FONT, size: 24, children: [new Tab(), String(pageMap[e.title] || '00')] })],
      }));
      children.push(...tocParas);
      continue;
    }
    if (cover) {
      children.push(new Paragraph({
        alignment: AlignmentType.CENTER, spacing: { line: 360, before: lvl === 3 && text.startsWith('Tim') ? 360 : 0, after: 0 },
        keepNext: true, children: [tr(text, { bold: true })],
      }));
    } else {
      const heading = [null, null, HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][lvl];
      const pb = /^(1\. Pendahuluan|Referensi Acuan|Lampiran )/.test(text);
      children.push(new Paragraph({ heading, pageBreakBefore: pb, children: [tr(text, { bold: true })] }));
    }
    i++; continue;
  }

  if (line.startsWith('|')) {
    const rows = [];
    while (i < lines.length && lines[i].startsWith('|')) {
      const cells = lines[i].trim().replace(/^\||\|$/g, '').split('|').map(s => s.trim());
      if (!cells.every(c => /^:?-+:?$/.test(c))) rows.push(cells);
      i++;
    }
    children.push(spacer(), makeTable(rows), spacer());
    continue;
  }

  if (/^<\/?(details|summary)/.test(line.trim())) {
    i++;
    continue;
  }

  if (line.trim().startsWith('```')) {
    i++;
    while (i < lines.length && !lines[i].trim().startsWith('```')) {
      i++;
    }
    i++;
    continue;
  }

  const img = line.match(/^!\[(.*)\]\((.*)\)\s*$/);
  if (img) {
    const pngName = img[2].replace(/\.svg$/, '.png');
    const targetImg = fs.existsSync(SRC + img[2]) && img[2].endsWith('.png') ? img[2] : pngName;
    const dims = { 'diagram_system_context.png': [529, 280], 'diagram_traceability_chain.png': [529, 156] }[targetImg] || [529, 280];
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true, spacing: { line: 240, lineRule: LineRuleType.AUTO, before: 120, after: 60 },
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(SRC + targetImg),
        transformation: { width: dims[0], height: dims[1] },
        altText: { title: img[1], description: img[1], name: targetImg } })],
    }));
    Object.keys(runsByLvl).forEach(k => delete runsByLvl[k]);
    i++; continue;
  }

  const chk = line.match(/^(\s*)-\s+\[([ xX])\]\s+(.*)$/);
  if (chk) {
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 }, indent: { left: 567, hanging: 567 },
      children: [tr('[' + (chk[2] === ' ' ? ' ' : '√') + ']'), new TextRun({ font: FONT, size: 24, children: [new Tab()] }), ...runs(chk[3])],
    }));
    i++; continue;
  }

  const li = line.match(/^(\s*)([*-]|\d+\.)\s+(.*)$/);
  if (li) {
    const lvl = lvlOf(li[1]);
    Object.keys(runsByLvl).forEach(k => { if (+k > lvl) delete runsByLvl[k]; });
    if (/\d+\./.test(li[2])) {
      if (!runsByLvl[lvl]) runsByLvl[lvl] = newNumRef(lvl);
      children.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
        numbering: { reference: runsByLvl[lvl], level: 0 }, children: runs(li[3]),
      }));
    } else {
      delete runsByLvl[lvl];
      children.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
        numbering: { reference: 'bul', level: Math.min(lvl, 3) }, children: runs(li[3]),
      }));
    }
    i++; continue;
  }

  // paragraph
  Object.keys(runsByLvl).forEach(k => delete runsByLvl[k]);
  const t = line.trim();
  if (/^\*Gambar/.test(t)) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { line: 360, lineRule: LineRuleType.AUTO, before: 0, after: 0 }, children: runs(t) }));
  } else children.push(body(t));
  i++;
}

const hStyle = (id, name, outline) => ({
  id, name, basedOn: 'Normal', next: 'Normal', quickFormat: true,
  run: { font: FONT, size: 24, bold: true, color: '000000' },
  paragraph: { spacing: { line: 360, before: 120, after: 0 }, keepNext: true, keepLines: true, outlineLevel: outline },
});

const doc = new Document({
  creator: 'Tim Penyusun Medkreminfo', title: 'SRS Sistem Informasi Layanan Pemesanan Konten Medkreminfo',
  styles: {
    default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 360 } } } },
    paragraphStyles: [hStyle('Heading1', 'Heading 1', 0), hStyle('Heading2', 'Heading 2', 1), hStyle('Heading3', 'Heading 3', 2)],
  },
  numbering: { config: numConfigs },
  sections: [{
    properties: {
      titlePage: true,
      page: { size: { width: 11906, height: 16838 }, margin: { top: 2268, bottom: 1701, left: 2268, right: 1701, header: 709, footer: 709 } },
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ font: FONT, size: 24, children: [PageNumber.CURRENT] })] })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }),
    },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); fs.writeFileSync('toc.json', JSON.stringify(tocEntries)); console.log('ok', children.length); });