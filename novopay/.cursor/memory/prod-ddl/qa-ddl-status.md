# QA schema memory status

Updated: 2026-07-14

| Artifact | Status |
|----------|--------|
| `qa-show-create-stmts.csv` | SHOW CREATE generator stmts |
| `qa-schema-table-catalog.tsv` | schema.table list |
| `qa-columns.csv` | **full column inventory (canonical for SQL)** |
| `qa-columns-index.md` | priority schema column index |

Totals: 91 schemas, 2209 tables, 25922 columns.

Note: this dump is from **QA**, not prod. Before sharing SQL for UAT/prod, call out env drift vs Flyway / this baseline.
