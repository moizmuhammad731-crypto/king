"""Build the NED-structure Pink Wheels CEP report (DOCX) from the Markdown master."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401  (kept for clarity)
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

HERE = Path(__file__).resolve().parent
MD = HERE / "Pink_Wheels_CEP_Report_NED.md"
OUT = HERE / "Pink_Wheels_NED_Report.docx"
LOGO = HERE / "ref" / "logo-0.png"

BODY_PT = 11.0
SERIF = "Times New Roman"
MONO = "Courier New"
SANS = "Calibri"
TEXT_W_CM = 16.2
HEADER_FILL = "D9D9D9"
CODE_FILL = "F2F2F2"
INK = "000000"
CAPTION_INK = RGBColor(0x1F, 0x38, 0x64)


# ------------------------------------------------------------------ xml utils
def shade(element, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    element.append(shd)


def cell_shade(cell, fill):
    shade(cell._tc.get_or_add_tcPr(), fill)


def para_shade(paragraph, fill):
    shade(paragraph._p.get_or_add_pPr(), fill)


def table_borders(table, color="000000", size=6, inside=True):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    edges = ["top", "left", "bottom", "right"]
    if inside:
        edges += ["insideH", "insideV"]
    for edge in edges:
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def no_borders(table):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        borders.append(el)
    tblPr.append(borders)


def cell_margins(table, top=50, bottom=50, left=90, right=90):
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblCellMar")):
        tblPr.remove(old)
    mar = OxmlElement("w:tblCellMar")
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def table_indent(table, cm):
    tblPr = table._tbl.tblPr
    ind = OxmlElement("w:tblInd")
    ind.set(qn("w:w"), str(Cm(cm).twips))
    ind.set(qn("w:type"), "dxa")
    tblPr.append(ind)


def table_width_pct(table, pct=100):
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "pct")
    tblW.set(qn("w:w"), str(pct * 50))


def fixed_layout(table):
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(layout)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.insert(0, OxmlElement("w:cantSplit"))


def add_field(paragraph, instr, placeholder="", size=None):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for el in (begin, instr_el, sep, text, end):
        run._r.append(el)
    if size:
        run.font.size = Pt(size)
        run.font.name = SERIF
    return run


def set_font(run, name=SERIF, size=BODY_PT, bold=None, italic=None, caps=False):
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if caps:
        run.font.all_caps = True


# --------------------------------------------------------------------- inline
INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def add_inline(paragraph, text, size=BODY_PT, bold=False, italic=False, name=SERIF):
    text = text.strip()
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            run = paragraph.add_run(text[pos:m.start()])
            set_font(run, name=name, size=size, bold=bold, italic=italic)
        token = m.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            set_font(run, name=name, size=size, bold=True, italic=italic)
        else:
            run = paragraph.add_run(token[1:-1])
            set_font(run, name=MONO, size=size - 1.0, bold=bold, italic=italic)
        pos = m.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_font(run, name=name, size=size, bold=bold, italic=italic)


# ------------------------------------------------------------------- document
def setup_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.4)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.4)
    section.right_margin = Cm(2.4)
    section.header_distance = Cm(1.2)
    section.footer_distance = Cm(1.1)
    section.different_first_page_header_footer = True

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    f = add_field(fp, " PAGE ", "1", size=11)
    set_font(f, size=11)

    settings = doc.settings.element
    for old in settings.findall(qn("w:updateFields")):
        settings.remove(old)

    normal = doc.styles["Normal"]
    normal.font.name = SERIF
    normal.font.size = Pt(BODY_PT)
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), SERIF)
    pf = normal.paragraph_format
    pf.line_spacing = 1.12
    pf.space_before = Pt(0)
    pf.space_after = Pt(8)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1 = doc.styles["Heading 1"]
    h1.font.name = SERIF
    h1.font.size = Pt(13.5)
    h1.font.bold = True
    h1.font.color.rgb = None
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(14)
    h1.paragraph_format.line_spacing = 1.0
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    h2.font.name = SERIF
    h2.font.size = Pt(12)
    h2.font.bold = True
    h2.font.italic = False
    h2.font.color.rgb = None
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(3)
    h2.paragraph_format.line_spacing = 1.0
    h2.paragraph_format.keep_with_next = True
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h3 = doc.styles["Heading 3"]
    h3.font.name = SERIF
    h3.font.size = Pt(11)
    h3.font.bold = True
    h3.font.italic = True
    h3.font.color.rgb = None
    h3.paragraph_format.space_before = Pt(9)
    h3.paragraph_format.space_after = Pt(3)
    h3.paragraph_format.line_spacing = 1.0
    h3.paragraph_format.keep_with_next = True
    h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for name, size, bold, indent in (("TOC 1", 11.5, True, 0.0),
                                     ("TOC 2", 10.5, False, 0.7)):
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = doc.styles["Normal"]
        st.font.name = SERIF
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.italic = False
        pf = st.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.left_indent = Cm(indent)
        pf.space_before = Pt(6 if bold else 1.5)
        pf.space_after = Pt(2 if bold else 1.5)
        pf.line_spacing = 1.0
        pf.tab_stops.add_tab_stop(Cm(TEXT_W_CM), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)


# ---------------------------------------------------------------------- cover
def spacer(doc, pts):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(pts)
    p.add_run(" ").font.size = Pt(1)
    return p


def cover_line(doc, text, size, bold=False, after=0, before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.0
    run = p.add_run(text)
    set_font(run, size=size, bold=bold)
    return p


def cover(doc):
    spacer(doc, 34)
    cover_line(doc, "PINK WHEELS", 15, bold=True, after=11)
    cover_line(doc, "REPORT", 15, bold=True, after=32)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(48)
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(str(LOGO), width=Cm(5.2))

    members = [("S. No.", "Name", "Seat No."),
               ("1", "MUHAMMAD MOIZ BROHI", "SE-25027"),
               ("2", "MUHAMMAD RAHIM ALI", "SE-25036"),
               ("3", "MUHAMMAD SAAD", "SE-25040")]

    table = doc.add_table(rows=len(members) + 1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table)
    table_borders(table, size=6)
    cell_margins(table, top=52, bottom=52, left=90, right=90)
    table_indent(table, 0.75)
    widths = (Cm(2.3), Cm(7.9), Cm(4.5))
    for c, w in enumerate(widths):
        table.columns[c].width = w

    merged = table.cell(0, 0).merge(table.cell(0, 2))
    merged.width = Cm(14.7)
    tcPr = merged._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for edge, val in (("top", 30), ("left", 90), ("bottom", 30), ("right", 90)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tcPr.append(mar)
    merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    cell_shade(merged, "D9D9D9")
    mp = merged.paragraphs[0]
    mp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mp.paragraph_format.space_before = Pt(1)
    mp.paragraph_format.space_after = Pt(1)
    set_font(mp.add_run("GROUP MEMBERS"), size=11.5, bold=True)

    for r, row in enumerate(members, start=1):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.width = widths[c]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.space_before = Pt(1)
            para.paragraph_format.space_after = Pt(1)
            para.paragraph_format.line_spacing = 1.0
            set_font(para.add_run(value), size=11.5, bold=(r == 1))

    for row in table.rows:
        cant_split(row)

    spacer(doc, 8)

    box = doc.add_table(rows=1, cols=1)
    box.alignment = WD_TABLE_ALIGNMENT.CENTER
    box.autofit = False
    fixed_layout(box)
    table_borders(box, size=8, inside=False)
    cell_margins(box, top=80, bottom=80, left=120, right=120)
    table_indent(box, 0.75)
    box.columns[0].width = Cm(14.7)
    cell = box.cell(0, 0)
    cell.width = Cm(14.7)
    first = True
    for label in ("Batch:", "Semester:", "Year:"):
        para = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        pf = para.paragraph_format
        pf.space_before = Pt(2)
        pf.space_after = Pt(2)
        pf.line_spacing = 1.0
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.tab_stops.add_tab_stop(Cm(14.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.LINES)
        set_font(para.add_run(label), size=11)
        set_font(para.add_run("\t"), size=11)
    cant_split(box.rows[0])


# ---------------------------------------------------------------------- index
def index_page(doc):
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    set_font(p.add_run("INDEX"), size=13.5, bold=True)

    fp = doc.add_paragraph()
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    add_field(fp, ' TOC \\o "1-2" \\h \\z \\u ', "", size=11)


# ------------------------------------------------------------- block writers
def h1(doc, title):
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.page_break_before = True
    run = p.add_run(title)
    set_font(run, size=13.5, bold=True)


def h2(doc, title, heading=True):
    if heading:
        p = doc.add_paragraph(style="Heading 2")
        run = p.add_run(title)
        set_font(run, size=12, bold=True)
    else:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        set_font(p.add_run(title), size=11.5, bold=True)


def h3(doc, title):
    p = doc.add_paragraph(style="Heading 3")
    run = p.add_run(title)
    set_font(run, size=11, bold=True, italic=True)


def body(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    lead = re.match(r"(Keywords:)\s*(.*)", text)
    if lead:
        set_font(p.add_run(lead.group(1) + " "), bold=True)
        add_inline(p, lead.group(2))
    else:
        add_inline(p, text)
    return p


def bold_line(doc, text, keep=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(3)
    pf.keep_with_next = keep
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_inline(p, text, bold=True)
    for run in p.runs:
        run.bold = True


def table_caption(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(10)
    pf.space_after = Pt(3)
    pf.keep_with_next = True
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_inline(p, text, size=10.5, bold=True)
    for run in p.runs:
        run.bold = True


def bullet(doc, text, level, marker):
    indent = 0.75 + 0.72 * level
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(-0.55)
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.1
    pf.tab_stops.add_tab_stop(Cm(indent - 0.05), WD_TAB_ALIGNMENT.LEFT)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_font(p.add_run(f"{marker}\t"), size=BODY_PT)
    add_inline(p, text)


def numbered(doc, number, text, level=0):
    indent = 0.85 + 0.72 * level
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(-0.7)
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.1
    pf.tab_stops.add_tab_stop(Cm(indent), WD_TAB_ALIGNMENT.LEFT)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_font(p.add_run(f"{number}.\t"), size=BODY_PT)
    add_inline(p, text)


def figure(doc, rel_path, caption):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(4)
    pf.keep_with_next = True
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p, caption, size=11, name=SANS)
    for run in p.runs:
        run.font.color.rgb = CAPTION_INK

    path = (HERE / rel_path).resolve()
    with Image.open(path) as img:
        w, h = img.size

    width_cm = TEXT_W_CM
    height_cm = width_cm * h / w
    if height_cm > 18.5:
        height_cm = 18.5
        width_cm = height_cm * w / h

    ip = doc.add_paragraph()
    ip.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ipf = ip.paragraph_format
    ipf.space_before = Pt(2)
    ipf.space_after = Pt(14)
    ipf.line_spacing = 1.0
    ip.add_run().add_picture(str(path), width=Cm(width_cm))


def grey_box(doc, lines, numbered_lines=False, size=None, after=10):
    if size is None:
        longest = max((len(l) for l in lines), default=1)
        avail = 425 if numbered_lines else 455
        size = max(7.4, min(9.2, avail / (0.6 * max(1, longest))))

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table)
    no_borders(table)
    cell_margins(table, top=90, bottom=90, left=120, right=100)
    cell = table.cell(0, 0)
    cell.width = Cm(TEXT_W_CM)
    cell_shade(cell, CODE_FILL)
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)

    line_pts = size * 1.24
    for idx, raw in enumerate(lines, start=1):
        p = cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(line_pts)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        text = f"{idx:>3}   {raw}" if numbered_lines else (raw if raw else "")
        run = p.add_run(text)
        set_font(run, name=MONO, size=size)

    cant_split(table.rows[0])
    spacer(doc, after)


def code_listing(doc, lines):
    longest = max((len(l) for l in lines), default=1)
    size = max(7.2, min(9.0, 765 / (0.6 * max(1, longest))))
    for raw in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(size * 1.3)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(raw if raw else "")
        set_font(run, name=MONO, size=size, bold=False, italic=False)
    spacer(doc, 10)


def source_line(doc, source, after=3):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(after)
    pf.keep_with_next = True
    pf.line_spacing = 1.0
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_font(p.add_run(f"Source: {source}"), size=9.5, italic=True)


def algo_heading(doc, title, complexity):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(9)
    pf.space_after = Pt(2)
    pf.keep_with_next = True
    pf.line_spacing = 1.0
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_font(p.add_run(title), size=10.5, bold=True)
    set_font(p.add_run("    " + complexity), size=10, italic=True)


def pseudo_heading(doc, title):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(10)
    pf.space_after = Pt(2)
    pf.keep_with_next = True
    pf.line_spacing = 1.0
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_font(p.add_run(title), size=10.5, bold=True, italic=True)


def grid_table(doc, rows, size=9.5):
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table)
    table.style = doc.styles["Table Grid"]
    table_borders(table, size=6)
    cell_margins(table, top=40, bottom=40, left=80, right=80)
    table_width_pct(table, 100)

    weights = []
    for c in range(ncols):
        longest = max((len(r[c]) if c < len(r) else 0) for r in rows)
        weights.append(min(max(longest, 7), 42))
    total = sum(weights)
    widths = [Cm(TEXT_W_CM * w / total) for w in weights]

    for r, row in enumerate(rows):
        for c in range(ncols):
            value = row[c] if c < len(row) else ""
            cell = table.cell(r, c)
            cell.width = widths[c]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p = cell.paragraphs[0]
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.line_spacing = 1.05
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if r == 0:
                add_inline(p, value, size=size, bold=True)
                for run in p.runs:
                    run.bold = True
                cell_shade(cell, HEADER_FILL)
            else:
                add_inline(p, value, size=size)

    repeat_header(table.rows[0])
    for row in table.rows:
        cant_split(row)
    spacer(doc, 10)


# ---------------------------------------------------------------------- parse
def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_separator(line):
    return bool(re.fullmatch(r"\|?[\s:\-|]+\|?", line.strip())) and "-" in line


SNIP = re.compile(r"^\[\[(FIG|PSEUDO|ALG|CODETITLE):([^\]|]+)\|?([^\]]*)\]\]$")


def main():
    text = MD.read_text(encoding="utf-8")
    lines = text.split("\n")

    doc = Document()
    setup_document(doc)
    doc.core_properties.title = "Pink Wheels — Complex Engineering Problem Report"
    doc.core_properties.author = "Muhammad Moiz Brohi, Muhammad Rahim Ali, Muhammad Saad"
    doc.core_properties.subject = "Women-focused ride-hailing platform with data structures and algorithms"

    cover(doc)
    index_page(doc)

    i = 0
    current_h1 = None
    pending = None  # ("pseudo"|"algo"|"code", payload)

    def next_fence(start):
        j = start
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and lines[j].startswith("```"):
            lang = lines[j][3:].strip()
            j += 1
            block = []
            while j < len(lines) and not lines[j].startswith("```"):
                block.append(lines[j].rstrip())
                j += 1
            return lang, block, j + 1
        return None, None, start

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        if not s:
            i += 1
            continue

        m = SNIP.match(s)
        if m:
            kind, first, second = m.group(1), m.group(2).strip(), m.group(3).strip()
            if kind == "FIG":
                figure(doc, first, second)
                i += 1
                continue
            if kind == "PSEUDO":
                pseudo_heading(doc, first)
                if second:
                    source_line(doc, second)
                pending = "pseudo"
                i += 1
                continue
            if kind == "ALG":
                algo_heading(doc, first, second)
                pending = "algo"
                i += 1
                continue
            if kind == "CODETITLE":
                source_line(doc, f"{second} — {first}" if second else first)
                pending = "code"
                i += 1
                continue

        if s.startswith("```"):
            lang, block, nxt = next_fence(i)
            if lang is None:
                i += 1
                continue
            if lang == "pseudo":
                grey_box(doc, block, numbered_lines=True)
            elif lang == "output":
                grey_box(doc, block, numbered_lines=False, size=9.2)
            else:
                code_listing(doc, block)
            pending = None
            i = nxt
            continue

        if s.startswith("#### "):
            i += 1
            continue

        if s.startswith("# "):
            title = s[2:].strip()
            h1(doc, title)
            current_h1 = title
            pending = None
            i += 1
            continue

        if s.startswith("## "):
            title = s[3:].strip()
            in_demo = current_h1 == "DEMONSTRATION"
            h2(doc, title, heading=not in_demo)
            pending = None
            i += 1
            continue

        if s.startswith("### "):
            h3(doc, s[4:].strip())
            pending = None
            i += 1
            continue

        if s.startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            rows = [split_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            grid_table(doc, rows)
            continue

        if re.fullmatch(r"-{3,}", s):
            i += 1
            continue

        bm = re.match(r"^( *)[-*] +(.*)$", raw)
        if bm:
            level = min(len(bm.group(1)) // 2, 2)
            marker = ("•", "o", "–")[level]
            bullet(doc, bm.group(2), level, marker)
            i += 1
            continue

        nm = re.match(r"^( *)(\d+)\. +(.*)$", raw)
        if nm:
            level = min(len(nm.group(1)) // 2, 2)
            numbered(doc, nm.group(2), nm.group(3), level)
            i += 1
            continue

        if re.fullmatch(r"\*\*[^*]+\*\*", s):
            if s.startswith("**Table"):
                table_caption(doc, s)
            else:
                bold_line(doc, s)
            i += 1
            continue

        # paragraph: merge following plain lines until a block boundary
        buf = [s]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            t = nxt.strip()
            if (not t or t.startswith("#") or t.startswith("```") or t.startswith("|")
                    or t.startswith("[[") or re.match(r"^[-*] +", t)
                    or re.match(r"^\d+\. +", t) or re.fullmatch(r"\*\*[^*]+\*\*", t)
                    or re.fullmatch(r"-{3,}", t)):
                break
            buf.append(t)
            i += 1
        body(doc, " ".join(buf))

    doc.save(OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
