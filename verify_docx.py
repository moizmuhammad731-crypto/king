import re
from collections import Counter

from docx import Document
from docx.oxml.ns import qn

d = Document("docs/report/Pink_Wheels_CEP_Report.docx")

print("inline images:", len(d.inline_shapes))
print("tables:", len(d.tables))
hs = Counter(p.style.name for p in d.paragraphs if p.style.name.startswith("Heading"))
print("headings:", dict(hs))
print("words (paragraphs):", sum(len(p.text.split()) for p in d.paragraphs))
print("words (tables):", sum(len(c.text.split()) for t in d.tables for r in t.rows for c in r.cells))

# separator rows that leaked into a table
leaks = []
for ti, tb in enumerate(d.tables):
    for r in tb.rows:
        joined = " | ".join(c.text for c in r.cells)
        if re.fullmatch(r"[\s:|-]+", joined or "x"):
            leaks.append((ti, joined[:60]))
print("separator-row leaks:", len(leaks), leaks[:5])

# figure captions in order
figs = [p.text.split("—")[0].strip() for p in d.paragraphs if p.text.startswith("Figure ")]
print("figure captions:", len(figs), figs)

# chapter page breaks
chap = [p for p in d.paragraphs if p.style.name == "Heading 1" and p.text.startswith("Chapter")]
print("chapters:", len(chap), "with break:", sum(1 for p in chap if p.paragraph_format.page_break_before))

# code blocks (1x1 tables) line counts
code = [t for t in d.tables if len(t.columns) == 1 and len(t.rows) == 1]
print("code blocks:", len(code), "total code lines:", sum(len(t.cell(0, 0).paragraphs) for t in code))

# empty cells / single-column tables that are not code
odd = []
for ti, tb in enumerate(d.tables):
    if len(tb.columns) == 1 and len(tb.rows) == 1:
        continue
    for r in tb.rows:
        for c in r.cells:
            if not c.text.strip():
                odd.append((ti, r._tr.getprevious() is not None))
print("empty cells:", len(odd))

# fields present
xml = d.element.xml
print("TOC field:", "TOC \\o" in xml, "| PAGE field:", "PAGE" in d.sections[0].footer.paragraphs[0]._p.xml)
settings = d.settings.element.xml
print("updateFields:", "updateFields" in settings)

# first 12 paragraphs text
for p in d.paragraphs[:14]:
    t = p.text.strip()
    if t:
        print("  |", t[:90])
