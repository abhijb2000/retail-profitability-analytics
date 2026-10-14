# Validation record

Validated in the preparation environment on 14 October 2026.

| Check | Result |
|---|---|
| Seeded dataset generation | 16,193 raw rows |
| Pipeline execution | Passed; 16,093 accepted lines |
| Python unittest suite | 8 passed |
| SQL queries executed | 10, exported as CSV (including header-only empty results) |
| SQL/Python KPI reconciliation | Passed |
| Accounting identities and resalable-return reversal | Passed |
| Monthly coverage | 24 months |
| Dashboard initial totals, combined filters, empty state, reset | Passed in Node DOM simulation |
| Dashboard CSV export | Passed in Node DOM simulation |
| Full browser rendering / responsive visual QA | Not executed; local browser executable unavailable |
| Power BI Desktop / DAX execution | Not executed; Desktop not available in this environment |

The dashboard uses standard HTML/CSS/JavaScript and embeds the accepted data. Open it in your browser to review layout and interaction. No dashboard screenshot or PBIX is asserted as verified. The Power BI guide includes expected totals for your Desktop validation. GitHub Actions will execute the Python and JavaScript checks once you upload the project with the workflow included.
