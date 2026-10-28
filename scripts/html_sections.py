"""Section builders shared by the static plan page: markdown, calendar and report sections."""
import csv
import html
import json
from pathlib import Path
import markdown

CAL_COLS = ["week", "id", "segment", "theme", "language", "strategy", "intent", "gate"]


def md(text):
    out = markdown.markdown(text, extensions=["tables", "fenced_code"])
    return out.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")


def load(outdir, name):
    p = Path(outdir) / name
    return json.loads(p.read_text()) if p.exists() else {}


def section(sid, title, body):
    return f'<section id="{sid}"><h2>{html.escape(title)}</h2>{body}</section>'


def calendar_section(sdir):
    sdir = Path(sdir)
    parts = []
    if (sdir / "strategy.md").exists():
        parts.append(md((sdir / "strategy.md").read_text()))
    if (sdir / "calendar.csv").exists():
        rows = list(csv.DictReader(open(sdir / "calendar.csv")))
        head = "".join(f"<th>{c}</th>" for c in CAL_COLS)
        body = "".join("<tr>" + "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in CAL_COLS) + "</tr>" for r in rows)
        parts.append(f'<h3>Calendar (calendar.csv)</h3><div class="tbl"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    return section("strategy", "Content strategy", "".join(parts)) if parts else ""


def report_section(outdir):
    p = Path(outdir) / "report.md"
    body = md(p.read_text()) if p.exists() else "<p>No report.md found.</p>"
    body = body.replace("BLOCKED", '<span class="blocked">BLOCKED</span>').replace("<td>allow</td>", '<td class="allow">allow</td>')
    return section("report", "Full report (report.md)", body)
