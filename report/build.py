"""Builds report/report.{html,pdf,docx} from the markdown parts.  Usage: python report/build.py"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = ["report_head.md", "report_part1.md", "report_part2.md", "report_part3.md", "report_tail.md"]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

md = "\n\n".join((HERE / p).read_text() for p in PARTS if (HERE / p).exists())
sys.path.insert(0, str(HERE))
import fill  # noqa: E402  (numbers come from results/tables, never typed by hand)
md = fill.fill(md)
(HERE / "report.md").write_text(md)
# --columns 1000: no fixed <colgroup> widths, so the browser sizes table columns to their content
common = ["pandoc", str(HERE / "report.md"), "--from", "markdown+tex_math_dollars+pipe_tables+smart", "--columns", "1000", "--citeproc",
          "--bibliography", str(HERE / "references.bib"), "--resource-path", str(HERE)]
TITLE = "Reliability-Aware Sheaf Consistency for Distinguishing UAV Position Anomalies from Communication Failures"
# MathJax (pinned) instead of MathML: Chrome's MathML ignores upright operator names and misplaces accents
subprocess.run(common + ["--standalone", "--mathjax=https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml-full.js",
                         "--css", "report.css", "--metadata", f"pagetitle={TITLE}",
                         "-o", str(HERE / "report.html")], check=True)
# pandoc joins "et al." to the year with a no-break space, which Charter prints at double width
html = HERE / "report.html"
html.write_text(html.read_text().replace("al.\u00a0", "al. "))
subprocess.run(common + ["-o", str(HERE / "report.docx")], check=True)
if Path(CHROME).exists():
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={HERE / 'report.pdf'}", f"file://{HERE / 'report.html'}"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from pypdf import PdfReader
    r = PdfReader(str(HERE / "report.pdf"))
    first_ref = next((i for i, pg in enumerate(r.pages) if re.search(r"^\s*(\d+\.\s*)?References\s*$", pg.extract_text() or "", re.M)), None)
    print(f"PDF pages total: {len(r.pages)}; 'References' heading on page {None if first_ref is None else first_ref + 1}")
else:
    print("Chrome not found; PDF skipped")
