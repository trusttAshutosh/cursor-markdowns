---
name: Optimize TransactionListReportRowMapper Query
overview: Refactor the SQL query construction in TransactionListReportRowMapper to push down filtering conditions into the large derived tables (tal and tas), preventing full table scans while preserving exact result equivalence.
todos:
  - id: extract-filter
    content: Modify Java code to extract filter building into a separate StringBuilder
    status: completed
  - id: create-subquery-strings
    content: Construct baseSubquery and IN conditions string variables
    status: completed
  - id: inject-conditions
    content: Modify the massive query text block to use .formatted() and inject the conditions into tal, tas, and the main WHERE clause
    status: completed
isProject: false
---

# Optimize TransactionListReportRowMapper Query

## Overview

The current query in `TransactionListReportRowMapper.java` performs extremely poorly because the derived tables `tal` and `tas` perform `GROUP BY` and `MAX` operations over the **entire** `transaction_audit_logs` table (which contains millions of rows) without any filtering. The date and hierarchy filters are only applied at the very end of the main query. 

To fix this with minimal change and maximal impact, we will extract the dynamically built `WHERE` clause in Java and inject it directly into the `tal` and `tas` subqueries. This forces MySQL to only scan and group the log records for the specific transactions matching the requested date range and filters.

## Implementation Steps

1. **Extract Filter Logic in Java:**
  Instead of appending the dynamic filter directly to the main `queryBuilder`, create a separate `StringBuilder` for the filter condition. This includes `ta.transaction_sub_type = 'CC'`, `applyDataFilter(...)`, and the date range.
2. **Construct a Base Subquery:**
  Using the extracted filter, construct an `IN` subquery that fetches the IDs of the filtered transactions:

```java
   String filterCondition = filterBuilder.toString();
   String baseSubquery = "SELECT ta.id FROM dsa_credit_card_mgmt.transaction_audit ta " +
       "LEFT JOIN dsa_credit_card_mgmt.transaction_hierarchy_log thl on ta.hierarchy_log_id = thl.id " +
       "WHERE " + filterCondition;
   String inCondition = "WHERE transaction_audit_id IN (" + baseSubquery + ")";
   String andInCondition = "AND transaction_audit_id IN (" + baseSubquery + ")";
   

```

1. **Inject Subquery into the SQL Text Block:**
  Update the massive `""" ... """` text block to use Java's `.formatted(...)` method to inject these filters.
  - Inside the `tal` derived table:

```sql
     FROM dsa_credit_card_mgmt.transaction_audit_logs
     %s  <-- Replaced by inCondition
     GROUP BY transaction_audit_id
     

```

- Inside the `tas` derived table (specifically the `t2` subquery):

```sql
     WHERE state <> 'updateCreditCardStatusBatch'
     %s  <-- Replaced by andInCondition
     GROUP BY transaction_audit_id
     

```

- At the end of the main query:

```sql
     WHERE %s <-- Replaced by filterCondition
     

```

1. **Verify Correctness:**
  Ensure the `applyDataFilter` now operates on the new `filterBuilder`. Since the base tables and join relationships remain exactly the same, the outputs will be identical in every scenario, but execution time will drastically drop by eliminating unbounded group operations.

