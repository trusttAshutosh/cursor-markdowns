---
name: feedback-flyway-manual-history-insert
description: "Manual flyway_schema_history insert must be ONE guarded INSERT ... SELECT line (COALESCE MAX rank, WHERE NOT EXISTS, backticks, manual-ops), plus a checksum reminder"
metadata:
  type: feedback
---

When the user needs a Flyway migration marked as applied by hand, give exactly ONE one-line statement in this shape. Never use the two-step `SET @rank` + `INSERT ... VALUES` form:

```sql
INSERT INTO `schema`.`flyway_schema_history` (`installed_rank`,`version`,`description`,`type`,`script`,`checksum`,`installed_by`,`installed_on`,`execution_time`,`success`) SELECT COALESCE(MAX(`installed_rank`),0)+1,'<version>','<description>','SQL','<script>',<checksum>,'manual-ops',NOW(),0,1 FROM `schema`.`flyway_schema_history` WHERE NOT EXISTS (SELECT 1 FROM `schema`.`flyway_schema_history` WHERE `version`='<version>');
```

**Why:**
- One statement computes the rank and the row together, so no session variable can be lost between statements.
- The `WHERE NOT EXISTS` guard is mandatory. Only `installed_rank` is the primary key and `version` is not unique, so a re-run would silently add a duplicate row.
- Backtick every table and column name (CodeAnt quote_identifiers).
- `installed_by` = 'manual-ops' so the audit trail shows the row was added by hand.

**How to apply:** Every time, remind the user to confirm that the checksum matches the Flyway checksum of the built script. A wrong checksum fails validation at boot. Related: [[ref-flyway-infra-versioning]], [[proj-task-allocation]].
