"""Writes the 'Results at a glance' block of README.md from results/tables (no hand-typed numbers).
Usage: python -m experiments.update_readme"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "report"))
import fill  # noqa: E402

TEMPLATE = """<!-- RESULTS:START -->
## Results at a glance (5 seeds, simulation only)

{{tbl:main}}

*PR-AUC, mean ± 95% t-interval over seeds; chance = {{n:pos_rate}}. Full tables: `results/tables/results_summary.md`.*

* **Pre-specified hypothesis (RA-SCM beats the best capacity-matched conventional GNN under packet loss): not supported.**
  H1 met in {{n:h1_count}} of {{n:h1_total}} decision conditions (≥4 required); the interval contains 0 in {{n:ci_zero_count}} (≥3 falsifies).
  The practical margin (≥0.02) is reached only under 50% burst loss ({{dh:burst_50:best_conventional}}).
* RA-SCM beats the age-aware physics baseline in all decision conditions (e.g. 50% bursts: {{dh:burst_50:physics_aoi}}).
* A consistency test that ignores staleness collapses under bursty loss ({{m:physics_naive:burst_50:pr_auc}} PR-AUC at 50% bursts vs {{m:physics_naive:iid_0:pr_auc}} without loss).
* Ablations: the communication-reliability inputs carry the benefit ({{da:burst_50:rascm_no_rel}} when removed at 50% bursts); learned sheaf maps show no measurable benefit.
* Not validated on any real data; see Limitations.

{{tbl:cost}}
<!-- RESULTS:END -->"""

readme = (ROOT / "README.md").read_text()
block = fill.fill(TEMPLATE)
if "<!-- RESULTS:START -->" in readme:
    a, b = readme.index("<!-- RESULTS:START -->"), readme.index("<!-- RESULTS:END -->") + len("<!-- RESULTS:END -->")
    readme = readme[:a] + block + readme[b:]
else:
    marker = "## Status of every component"
    readme = readme.replace(marker, block + "\n\n" + marker)
(ROOT / "README.md").write_text(readme)
print("README results block updated")
