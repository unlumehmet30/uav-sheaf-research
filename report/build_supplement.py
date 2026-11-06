"""Builds report/supplementary.pdf (search log, literature matrix, gap analysis) from literature/*.md.
Usage: python report/build_supplement.py   (needs pandoc and Chrome, like build.py)"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIT = HERE.parent / "literature"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE = "Supplementary Material: Literature Search, Matrix and Gap Analysis"

head = f"""---
title: "{TITLE}"
lang: en
---

<p class="author">Mehmet Ünlü (040230253) · EHB 420E Artificial Neural Networks · HW1 – From Curiosity to Scientific Discovery ·
supplement to the report "Reliability-Aware Sheaf Consistency for Distinguishing UAV Position Anomalies from Communication Failures"</p>

Contents: S1 search protocol and log · S2 comparative literature matrix · S3 critical synthesis, gap verification and originality ledger.
"""


def section(label: str, path: Path, newpage: bool = True) -> str:
    md = path.read_text()
    lines = md.split("\n")
    # the file's own H1 becomes the numbered section title; its H2/H3 move one level down
    title = lines[0].lstrip("# ").strip()
    body = "\n".join(lines[1:])
    body = "\n".join(("#" + ln) if ln.startswith("#") else ln for ln in body.split("\n"))
    brk = '<div class="pagebreak"></div>\n\n' if newpage else ""
    return f"{brk}## {label}. {title}\n\n{body}"


md = "\n\n".join([head, section("S1", LIT / "search_log.md", newpage=False), section("S2", LIT / "literature_matrix.md"),
                  section("S3", LIT / "gap_analysis.md")])
md = md.replace("\n## Round 2 additions", "\n### Round 2 additions")   # second H1 inside the matrix file
(HERE / "supplementary.md").write_text(md)
subprocess.run(["pandoc", str(HERE / "supplementary.md"), "--from", "markdown+pipe_tables+smart", "--columns", "1000",
                "--standalone", "--css", "report.css", "--metadata", f"pagetitle={TITLE}",
                "-o", str(HERE / "supplementary.html")], check=True)
html = HERE / "supplementary.html"
html.write_text(html.read_text().replace("al.\u00a0", "al. "))   # see build.py
if Path(CHROME).exists():
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                    f"--print-to-pdf={HERE / 'supplementary.pdf'}", f"file://{HERE / 'supplementary.html'}"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from pypdf import PdfReader
    print(f"supplementary.pdf: {len(PdfReader(str(HERE / 'supplementary.pdf')).pages)} pages")
else:
    print("Chrome not found; PDF skipped")
