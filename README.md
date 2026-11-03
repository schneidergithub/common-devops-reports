# Common DevOps Reports

Public reports and monthly AI & cybersecurity reviews from Common DevOps.

## Source of truth

Permanent report URLs under `/reports/YYYY-MM/` are the authoritative published editions.

### October 2026 — Cybersecurity Must Keep Pace with AI

**Canonical publication:**
https://www.aaronschneider.org/common-devops-reports/reports/2026-10/

- PDF edition: [reports/2026-10/common-devops-october-2026.pdf](reports/2026-10/common-devops-october-2026.pdf)
- Markdown source: [reports/2026-10/newsletter.md](reports/2026-10/newsletter.md)
- Reporting period: October 1 to November 1, 2026.

### September 2026 — AI Got Cheaper. Control Got Harder.

**Canonical publication:**
https://www.aaronschneider.org/common-devops-reports/reports/2026-09/

- Reports archive: https://www.aaronschneider.org/common-devops-reports/
- Markdown source: [reports/2026-09/newsletter.md](reports/2026-09/newsletter.md)

## Publishing structure

```
index.html
.nojekyll
reports/
  index.html
  2026-09/
    index.html
    newsletter.md
  2026-10/
    index.html
    newsletter.md
    common-devops-october-2026.pdf
```

Each monthly issue receives a permanent `reports/YYYY-MM/` URL. The repository root is an archive/index rather than a duplicate copy of the latest report.

## Rebuilding the October edition

Edit `reports/2026-10/newsletter.md`, then run `python3 scripts/build_october_report.py` with ReportLab installed. This updates the HTML and two-page PDF from the same text. Review both editions before publishing. Update the two archive listings when the issue title or summary changes.
