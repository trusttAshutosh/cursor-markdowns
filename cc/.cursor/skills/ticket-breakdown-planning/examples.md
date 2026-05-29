# Reference Examples (Format Only)

## Data purging style reference

- Plan: `%USERPROFILE%\.cursor\plans\dsa_lead_lifecycle_tickets_02a51237.plan.md`
- Pattern highlights:
  - Product ticket with **Jira journey field - select / do not select**
  - **Journeys impacted** 3-column table
  - **Estimation** inside Product ticket for Ticket 1
  - Separate **Engineering reference** and **QA reference** with flow map, SQL, functional tests
  - Appendix with cross-ticket decisions

## Remarketing SMS style reference

- Plan: `%USERPROFILE%\.cursor\plans\cc_remarketing_subtickets_47faa95c.plan.md`
- Technical plan: `%USERPROFILE%\.cursor\plans\cc_remarketing_sms_batch_ddadc85b.plan.md`
- Pattern highlights:
  - **Product UD vs Locked Decisions** at top
  - Tickets CC-RMK-001..005
  - Per-ticket **Estimation** table with <=4h rows
  - **Estimation summary** + **Justification table** at end
  - Parallel dependency called out explicitly

## Jira journey quick reference (CC / platform)

| Ticket type | Select (examples) |
| --- | --- |
| CC batch/SMS/backend | Credit Card, Platform, Agent App (if UI impact), Admin Portal (if ops visibility) |
| Bulk/Kafka | Credit Card, Platform |
| Config/flyway only | Platform, Credit Card |
| QA/docs only | Credit Card, Platform, Admin Portal |

Always add **Do not select** for out-of-scope journeys (LOC, AOC, unrelated products).

## Estimation row examples (good vs bad)

| Subtask | Est (hrs) | Why (good) |
| --- | ---:| --- |
| Finalize eligibility predicate | 2.0 | Decision gate; blocks downstream tickets |
| Processor + orchestration wiring | 3.0 | Boilerplate + integration setup |
| Unit tests for include/exclude matrix | 4.0 | High-risk regression area |

| Subtask | Est (hrs) | Why (bad) |
| --- | ---:| --- |
| Coding | 8.0 | Too vague |
| Testing | 4.0 | No scope indicated |
