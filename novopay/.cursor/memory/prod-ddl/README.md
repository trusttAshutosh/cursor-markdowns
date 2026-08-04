# Prod DDL memory

Paste dumps from production here (or into chat - agent will save files).

Preferred artifacts:
- `columns.tsv` - from the column inventory query (best for query writing)
- `create-tables.sql` - from SHOW CREATE / mysqldump --no-data
- `README-schemas.txt` - which schemas were included and when

Agent rules: prefer these files over guessing `schema.table`; call out QA/UAT-only drift vs this baseline.
