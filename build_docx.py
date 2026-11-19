"""Build the Pink Wheels CEP report DOCX from the Markdown master copy."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT,
                            WD_TAB_LEADER)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu
from PIL import Image

HERE = Path(__file__).resolve().parent
MD = HERE / "Pink_Wheels_CEP_Report.md"
OUT = HERE / "Pink_Wheels_CEP_Report.docx"
IMAGES = HERE / "images"

PINK = RGBColor(0xB0, 0x1A, 0x53)
DEEP_PINK = "B01A53"
INK = RGBColor(0x1F, 0x23, 0x29)
BODY_INK = RGBColor(0x21, 0x23, 0x27)
MUTED = RGBColor(0x5C, 0x5E, 0x66)
CODE_INK = RGBColor(0x7A, 0x12, 0x36)

BODY_PT = 11.5
TABLE_PT = 9.0
TEXT_W_CM = 16.6


# ---------------------------------------------------------------- xml helpers
def shade(element, fill):
    """Apply a solid fill to a cell or paragraph properties element."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    element.append(shd)


def cell_shade(cell, fill):
    shade(cell._tc.get_or_add_tcPr(), fill)


def para_shade(paragraph, fill):
    shade(paragraph._p.get_or_add_pPr(), fill)


def para_border(paragraph, edge="bottom", color=DEEP_PINK, size=12, space=4):
    pPr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    borders.append(el)
    pPr.append(borders)


def table_borders(table, color="D9CFDA", size=4):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def cell_margins(table, top=60, bottom=60, left=100, right=100):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for edge, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.insert(0, OxmlElement("w:cantSplit"))


def table_width_pct(table, pct=100):
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:type"), "pct")
    tblW.set(qn("w:w"), str(pct * 50))


def add_field(paragraph, instr, placeholder="1"):
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
    return run


def set_run_font(run, name=None, size=None, bold=None, italic=None, color=None):
    if name:
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
    if color is not None:
        run.font.color.rgb = color


# ------------------------------------------------------------ latex->unicode
GREEK = {
    "Delta": "Δ", "delta": "δ", "lambda": "λ", "Lambda": "Λ", "phi": "φ", "Phi": "Φ",
    "pi": "π", "mu": "μ", "sigma": "σ", "Sigma": "Σ", "Theta": "Θ", "theta": "θ",
    "Omega": "Ω", "omega": "ω", "alpha": "α", "beta": "β", "gamma": "γ", "tau": "τ",
}

SYMBOLS = {
    "cdot": "·", "times": "×", "div": "÷", "pm": "±", "mp": "∓",
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠",
    "approx": "≈", "equiv": "≡", "in": "∈", "notin": "∉",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "Rightarrow": "⇒",
    "infty": "∞", "sum": "Σ", "prod": "Π", "partial": "∂", "nabla": "∇",
    "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉",
    "qquad": "\u2003\u2003", "quad": "\u2003", "ldots": "…", "dots": "…",
    "therefore": "∴", "because": "∵", "emptyset": "∅", "subset": "⊂",
    "cap": "∩", "cup": "∪", "forall": "∀", "exists": "∃", "perp": "⊥",
}

FUNCS = ("log", "ln", "lg", "sin", "cos", "tan", "arctan2", "arctan", "arcsin",
         "arccos", "exp", "max", "min", "lim", "det")

SUP = str.maketrans("0123456789+-=()n*'", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ*'")
SUB = str.maketrans("0123456789+-=()aeiox", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢₒₓ")


def _frac(text):
    """Rewrite \\frac{a}{b} (one nesting level) as (a)/(b) or a/b."""
    out = []
    i = 0
    while i < len(text):
        if text.startswith("\\frac", i):
            i += 5
            nums = []
            for _ in range(2):
                while i < len(text) and text[i] == " ":
                    i += 1
                if i < len(text) and text[i] == "{":
                    depth, j = 0, i
                    while j < len(text):
                        if text[j] == "{":
                            depth += 1
                        elif text[j] == "}":
                            depth -= 1
                            if depth == 0:
                                break
                        j += 1
                    nums.append(text[i + 1:j])
                    i = j + 1
                else:
                    nums.append(text[i])
                    i += 1
            if len(nums) == 2:
                num, den = _frac(nums[0]), _frac(nums[1])
                wrap = (lambda s: s if re.fullmatch(r"[\w.]+|\\[a-zA-Z]+", s) else f"({s})")
                out.append(f"{wrap(num)}/{wrap(den)}")
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def latex_to_text(src: str) -> str:
    s = src.strip()
    if s.startswith("$$") and s.endswith("$$"):
        s = s[2:-2]
    elif s.startswith("$") and s.endswith("$"):
        s = s[1:-1]
    s = s.replace("{,}", ",")
    s = s.replace("\\left", "").replace("\\right", "")
    s = s.replace("\\!", "").replace("\\,", " ").replace("\\;", " ").replace("\\:", " ")
    s = _frac(s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", lambda m: "√" + (m.group(1) if len(m.group(1)) == 1 else f"({m.group(1)})"), s)
    s = s.replace("\\sqrt", "√")
    for name, char in SYMBOLS.items():
        s = s.replace("\\" + name, char)
    for name, char in GREEK.items():
        s = s.replace("\\" + name, char)
    for fn in FUNCS:
        s = s.replace("\\" + fn, fn)
    s = s.replace("\\text", "").replace("\\mathrm", "")
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"\^(\w)", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"_\{([^{}]*)\}", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"_(\w)", lambda m: m.group(1).translate(SUB), s)
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\\", "")
    s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()


DISPLAY_MATH = {
    "\\phi_1 = \\frac{\\pi}{180}\\,lat_1,\\qquad \\phi_2 = \\frac{\\pi}{180}\\,lat_2":
        "φ₁ = (π/180)·lat₁        φ₂ = (π/180)·lat₂",
    "\\Delta\\phi = \\frac{\\pi}{180}(lat_2-lat_1),\\qquad \\Delta\\lambda = \\frac{\\pi}{180}(lon_2-lon_1)":
        "Δφ = (π/180)·(lat₂ − lat₁)        Δλ = (π/180)·(lon₂ − lon₁)",
    "a = \\sin^2\\!\\left(\\frac{\\Delta\\phi}{2}\\right) + \\cos\\phi_1\\cos\\phi_2\\sin^2\\!\\left(\\frac{\\Delta\\lambda}{2}\\right)":
        "a = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)",
    "c = 2\\arctan2\\!\\left(\\sqrt{a},\\sqrt{1-a}\\right),\\qquad d = 6371.0 \\times c":
        "c = 2·arctan2(√a, √(1−a))        d = 6371.0 × c",
}


# ------------------------------------------------------------- inline markup
INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\$[^$]+\$|\*[^*\s][^*]*\*)")


def add_inline(paragraph, text, size=BODY_PT, color=BODY_INK, bold=False, italic=False):
    text = text.strip()
    pos = 0
    for match in INLINE.finditer(text):
        if match.start() > pos:
            run = paragraph.add_run(text[pos:match.start()])
            set_run_font(run, size=size, bold=bold, italic=italic, color=color)
        token = match.group(0)
        if token.startswith("**"):
            inner = token[2:-2].replace("`", "")
            run = paragraph.add_run(inner)
            set_run_font(run, size=size, bold=True, italic=italic, color=color)
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            set_run_font(run, name="Consolas", size=size - 1.2, color=CODE_INK)
        elif token.startswith("$"):
            rendered = latex_to_text(token)
            run = paragraph.add_run(rendered)
            set_run_font(run, size=size, italic=True, color=color)
        else:
            inner = token[1:-1]
            run = paragraph.add_run(inner)
            set_run_font(run, size=size, bold=bold, italic=True, color=color)
        pos = match.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_run_font(run, size=size, bold=bold, italic=italic, color=color)


# ------------------------------------------------------------------- document
def setup_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(BODY_PT)
    normal.font.color.rgb = BODY_INK
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), "Times New Roman")
    pf = normal.paragraph_format
    pf.line_spacing = 1.28
    pf.space_after = Pt(7)
    pf.space_before = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h1 = doc.styles["Heading 1"]
    h1.font.name = "Arial"
    h1.font.size = Pt(18)
    h1.font.bold = True
    h1.font.color.rgb = PINK
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(14)
    h1.paragraph_format.keep_with_next = True
    h1.paragraph_format.line_spacing = 1.1
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h2 = doc.styles["Heading 2"]
    h2.font.name = "Arial"
    h2.font.size = Pt(13.5)
    h2.font.bold = True
    h2.font.color.rgb = INK
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True
    h2.paragraph_format.line_spacing = 1.1
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h3 = doc.styles["Heading 3"]
    h3.font.name = "Arial"
    h3.font.size = Pt(11.5)
    h3.font.bold = True
    h3.font.color.rgb = RGBColor(0x43, 0x33, 0x3A)
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    h3.paragraph_format.keep_with_next = True
    h3.paragraph_format.line_spacing = 1.1
    h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for idx, (name, size, indent) in enumerate(
        (("TOC 1", 10.2, 0.0), ("TOC 2", 9.8, 0.42), ("TOC 3", 9.4, 0.85)),
        start=1,
    ):
        st = doc.styles.add_style(name, 1)
        st.base_style = doc.styles["Normal"]
        st.font.name = "Arial"
        st.font.size = Pt(size)
        st.font.color.rgb = INK
        pf = st.paragraph_format
        pf.space_before = Pt(3 if idx == 1 else 1.5)
        pf.space_after = Pt(3 if idx == 1 else 1.5)
        pf.line_spacing = 1.12
        pf.left_indent = Cm(indent)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.tab_stops.add_tab_stop(Cm(16.55), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

    cap = doc.styles["Caption"]
    cap.font.name = "Arial"
    cap.font.size = Pt(8.8)
    cap.font.italic = True
    cap.font.bold = False
    cap.font.color.rgb = MUTED
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(3)
    cap.paragraph_format.space_after = Pt(10)
    cap.paragraph_format.line_spacing = 1.05


def setup_section(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.1)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    section.header_distance = Cm(1.1)
    section.footer_distance = Cm(1.0)
    section.different_first_page_header_footer = True

    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.paragraph_format.space_after = Pt(2)
    run = hp.add_run("Pink Wheels  ·  SE-213 Data Structures and Algorithms  ·  CEP Report")
    set_run_font(run, name="Arial", size=8, color=MUTED)
    para_border(hp, "bottom", color=DEEP_PINK, size=6, space=4)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run("Page ")
    set_run_font(r, name="Arial", size=8.5, color=MUTED)
    f1 = add_field(fp, " PAGE ", "1")
    set_run_font(f1, name="Arial", size=8.5, color=MUTED)
    r = fp.add_run(" of ")
    set_run_font(r, name="Arial", size=8.5, color=MUTED)
    f2 = add_field(fp, " NUMPAGES ", "1")
    set_run_font(f2, name="Arial", size=8.5, color=MUTED)

    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)


def cover(doc):
    def spacer(pts):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = Pt(pts)
        p.add_run(" ").font.size = Pt(2)
        return p

    bar = doc.add_paragraph()
    bar.paragraph_format.space_before = Pt(0)
    bar.paragraph_format.space_after = Pt(26)
    bar.paragraph_format.line_spacing = Pt(7)
    run = bar.add_run(" ")
    run.font.size = Pt(2)
    para_shade(bar, DEEP_PINK)

    def line(text, size, color, bold=False, italic=False, before=0, after=0, caps=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.12
        run = p.add_run(text)
        set_run_font(run, name="Arial", size=size, bold=bold, italic=italic, color=color)
        if caps:
            run.font.all_caps = True
        return p

    line("NED UNIVERSITY OF ENGINEERING & TECHNOLOGY", 15.5, INK, bold=True)
    line("Department of Software Engineering", 11.5, MUTED, after=6)
    line("SE-213  ·  Data Structures and Algorithms", 10.5, PINK, bold=True, after=34)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run("PINK WHEELS")
    set_run_font(run, name="Arial", size=46, bold=True, color=PINK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("A Women-Focused Ride-Hailing Platform for Karachi")
    set_run_font(run, name="Arial", size=15, color=INK)
    run.add_break()
    run2 = p.add_run("with DSA-Based Matchmaking")
    set_run_font(run2, name="Arial", size=15, color=INK)

    rule = doc.add_paragraph()
    rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rule.paragraph_format.space_before = Pt(0)
    rule.paragraph_format.space_after = Pt(16)
    rule.paragraph_format.line_spacing = Pt(2)
    rule.add_run(" ").font.size = Pt(1)
    para_border(rule, "bottom", color="E7B3C8", size=12, space=1)
    rule.paragraph_format.left_indent = Cm(4.2)
    rule.paragraph_format.right_indent = Cm(4.2)

    line("Complex Engineering Problem (CEP) Report", 13.5, INK, bold=True, after=6)
    line("CLO 2 — Problem Analysis   |   CLO 3 — Individual and Teamwork", 10, MUTED, italic=True, after=40)

    members = [
        ("Group Member", "Seat Number", "Primary Contribution"),
        ("[Member 1 Full Name]", "[SE-XX-XXX]",
         "Linked list and priority-queue design; Chapters 1–2"),
        ("[Member 2 Full Name]", "[SE-XX-XXX]",
         "Matchmaking workflows, complexity analysis; Chapters 4–5"),
        ("[Member 3 Full Name]", "[SE-XX-XXX]",
         "Frontend integration, testing, walkthrough; Chapters 3 and 6"),
    ]
    table = doc.add_table(rows=len(members), cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_borders(table, color="E3CBD6", size=4)
    cell_margins(table, top=70, bottom=70, left=110, right=110)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(layout)
    widths = (Cm(7.4), Cm(3.2), Cm(5.2))
    for r, row in enumerate(members):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.width = widths[c]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(0)
            para.paragraph_format.space_before = Pt(0)
            para.paragraph_format.line_spacing = 1.05
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if c == 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = para.add_run(value)
            if r == 0:
                set_run_font(run, name="Arial", size=8.6, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
                cell_shade(cell, DEEP_PINK)
            else:
                set_run_font(run, name="Arial", size=8.6, color=BODY_INK)
        if r == 0:
            repeat_header(table.rows[r])

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(46)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("Semester: Fall 2026     Section: [Section]     Date: 19 November 2026")
    set_run_font(run, name="Arial", size=9.6, color=INK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("Course Instructor: [Instructor Name]")
    set_run_font(run, name="Arial", size=9.6, bold=True, color=INK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(30)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(
        "Submitted in partial fulfilment of the Complex Engineering Problem requirement for SE-213."
    )
    set_run_font(run, name="Arial", size=8.4, italic=True, color=MUTED)


def add_toc(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    add_field(p, ' TOC \\o "1-3" \\h \\z \\u ', "Right-click and choose Update Field to build the contents.")

    note = doc.add_paragraph()
    note.paragraph_format.space_before = Pt(10)
    run = note.add_run(
        "Contents entries are generated from the report headings. If they are not populated on opening, "
        "select all (Ctrl+A) and press F9 to update fields."
    )
    set_run_font(run, name="Arial", size=8, italic=True, color=MUTED)


def caption(doc, text, kind):
    p = doc.add_paragraph(style="Caption")
    prefix = "Figure" if kind == "figure" else "Table"
    body = text.strip().strip("*")
    p.paragraph_format.keep_with_next = kind == "table"
    add_inline(p, body, size=8.8, color=MUTED, italic=False)
    for run in p.runs:
        run.italic = True
        run.font.name = "Arial"
    return p


def add_picture(doc, rel_path, alt):
    path = (HERE / rel_path).resolve()
    with Image.open(path) as img:
        w, h = img.size
    width_cm = 15.9
    height_cm = width_cm * h / w
    if height_cm > 12.0:
        height_cm = 12.0
        width_cm = height_cm * w / h
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    if alt:
        doc.core_properties.subject = doc.core_properties.subject or alt


def code_block(doc, code_lines, lang=""):
    lines = code_lines if code_lines else [""]
    max_len = max((len(l) for l in lines), default=0)
    if max_len <= 88:
        size = 8.2
    elif max_len <= 94:
        size = 7.8
    elif max_len <= 99:
        size = 7.4
    elif max_len <= 110:
        size = 7.1
    else:
        size = 6.8
    line_pts = size * 1.22

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_borders(table, color="DFD3E0", size=4)
    cell_margins(table, top=90, bottom=90, left=120, right=120)
    cell = table.cell(0, 0)
    cell.width = Cm(TEXT_W_CM - 0.3)
    cell_shade(cell, "F7F4F8")
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)

    for raw in lines:
        p = cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(line_pts)
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(raw if raw else "")
        set_run_font(run, name="Consolas", size=size, color=RGBColor(0x2B, 0x2B, 0x33))
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = Pt(8)
    spacer.add_run(" ").font.size = Pt(2)


def markdown_table(doc, rows):
    header = rows[0]
    body = rows[1:]
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    table.style = doc.styles["Table Grid"]
    table_borders(table, color="D9CFDA", size=4)
    cell_margins(table, top=45, bottom=45, left=80, right=80)
    table_width_pct(table, 100)

    for r, row in enumerate(rows):
        for c in range(ncols):
            value = row[c] if c < len(row) else ""
            cell = table.cell(r, c)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.06
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if r else WD_ALIGN_PARAGRAPH.LEFT
            if r == 0:
                add_inline(p, value, size=TABLE_PT - 0.4, color=RGBColor(0xFF, 0xFF, 0xFF), bold=True)
                for run in p.runs:
                    run.bold = True
                cell_shade(cell, DEEP_PINK)
            else:
                add_inline(p, value, size=TABLE_PT, color=BODY_INK)
                if r % 2 == 0:
                    cell_shade(cell, "FBF6F9")
    repeat_header(table.rows[0])
    for row in table.rows:
        cant_split(row)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = Pt(9)
    spacer.add_run(" ").font.size = Pt(2)


def list_item(doc, marker, text, indent=0.72):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(indent)
    pf.first_line_indent = Cm(-indent)
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.24
    pf.tab_stops.add_tab_stop(Cm(indent), WD_TAB_ALIGNMENT.LEFT)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"{marker}\t")
    set_run_font(run, name="Times New Roman", size=BODY_PT, color=BODY_INK)
    add_inline(p, text, size=BODY_PT)


def quote_block(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.9)
    pf.right_indent = Cm(0.6)
    pf.space_before = Pt(6)
    pf.space_after = Pt(10)
    pf.line_spacing = 1.25
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para_border(p, "left", color="D06A93", size=18, space=8)
    para_shade(p, "FCF3F7")
    add_inline(p, text, size=BODY_PT, color=RGBColor(0x33, 0x2C, 0x30), italic=True)


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


def main():
    text = MD.read_text(encoding="utf-8")
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.strip() == "## Abstract")

    doc = Document()
    setup_styles(doc)
    setup_section(doc)
    doc.core_properties.title = "Pink Wheels — SE-213 Complex Engineering Problem Report"
    doc.core_properties.author = "SE-213 Project Team"
    doc.core_properties.subject = "Women-focused ride-hailing platform with DSA-based matchmaking"

    cover(doc)

    i = start
    pending_list_kind = None
    in_contents = False
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i].rstrip("\n"))
                i += 1
            i += 1
            code_block(doc, block, lang)
            continue

        if not stripped.strip():
            i += 1
            continue

        if re.fullmatch(r"-{3,}", stripped.strip()):
            i += 1
            continue

        # display math
        if stripped.strip().startswith("$$"):
            expr = stripped.strip()
            inner = expr[2:-2].strip() if expr.endswith("$$") else expr[2:]
            rendered = DISPLAY_MATH.get(inner) or latex_to_text(expr)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(10)
            run = p.add_run(rendered)
            set_run_font(run, name="Cambria Math", size=12, italic=True, color=INK)
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            if title == "Contents":
                h = doc.add_paragraph(style="TOC Heading")
                h.paragraph_format.page_break_before = True
                h.paragraph_format.space_before = Pt(0)
                h.paragraph_format.space_after = Pt(14)
                add_inline(h, "Contents", size=18, color=PINK, bold=True)
                add_toc(doc)
                in_contents = True
                i += 1
                continue
            in_contents = False
            front = title in {"Abstract", "Acknowledgement", "List of Figures", "List of Tables"}
            if level == 1 or front:
                h = doc.add_heading("", level=1)
                h.paragraph_format.page_break_before = True
                add_inline(h, title, size=18, color=PINK, bold=True)
                if not front:
                    para_border(h, "bottom", color="E7B3C8", size=8, space=6)
            elif level == 2:
                h = doc.add_heading("", level=2)
                add_inline(h, title, size=13.5, color=INK, bold=True)
            else:
                h = doc.add_heading("", level=3)
                add_inline(h, title, size=11.5, color=RGBColor(0x43, 0x33, 0x3A), bold=True)
            i += 1
            continue

        if in_contents and re.match(r"^\d+\.\s", stripped.strip()):
            i += 1
            continue

        # table
        if stripped.strip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            markdown_table(doc, rows)
            continue

        # image
        img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped.strip())
        if img:
            add_picture(doc, img.group(2), img.group(1))
            i += 1
            continue

        # figure/table captions
        cap = re.match(r"^\*(Figure|Table)\s[\d.]+\s*[—-].*\*$", stripped.strip())
        if cap:
            caption(doc, stripped, "figure" if cap.group(1) == "Figure" else "table")
            i += 1
            continue

        # blockquote
        if stripped.lstrip().startswith("> "):
            quote_block(doc, stripped.lstrip()[2:])
            i += 1
            continue

        # lists
        li = re.match(r"^(\s*)[-*]\s+(.*)$", stripped)
        if li:
            list_item(doc, "•", li.group(2))
            i += 1
            continue
        li = re.match(r"^(\s*)(\d+)\.\s+(.*)$", stripped)
        if li:
            list_item(doc, f"{li.group(2)}.", li.group(3))
            i += 1
            continue

        # bold lead-in lines (listing headers)
        if re.fullmatch(r"\*\*[^*]+\*\*", stripped.strip()):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            add_inline(p, stripped)
            i += 1
            continue

        # paragraph (merge wrapped source lines)
        buf = [stripped.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            s = nxt.strip()
            if (not s or s.startswith("#") or s.startswith("```") or s.startswith("|")
                    or s.startswith("!") or s.startswith(">") or s.startswith("$$")
                    or re.fullmatch(r"-{3,}", s) or re.match(r"^[-*]\s+", s)
                    or re.match(r"^\d+\.\s+", s) or re.fullmatch(r"\*\*[^*]+\*\*", s)
                    or re.match(r"^\*(Figure|Table)\s[\d.]+\s*[—-].*\*$", s)):
                break
            buf.append(s)
            i += 1
        p = doc.add_paragraph()
        joined = " ".join(buf)
        p.alignment = (WD_ALIGN_PARAGRAPH.LEFT if re.match(r"^\[\d+\]\s", joined)
                       else WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_inline(p, joined)

    doc.save(OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
