---
name: Fix transaction_audit table missing
overview: "The error occurs because the app uses the database `platform_master` (via spring.datasource) but the table `transaction_audit` was never created there: Flyway is disabled at startup, so migrations in this project do not run automatically. The fix is to apply the existing Flyway migrations to the database that the app uses."
todos: []
isProject: false
---

# Fix: Table 'platform_master.transaction_audit' doesn't exist

## Root cause

- **Datasource**: [application.properties](novopay-platform-creditcard-management/src/main/resources/application.properties) sets `spring.datasource.url=jdbc:mysql://localhost:3306/platform_master`. All JPA entities (including [TransactionAudit](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/entity/TransactionAudit.java)) use this default datasource, so the app expects `transaction_audit` in the `platform_master` database.
- **Flyway disabled**: [Application.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/Application.java) excludes `FlywayAutoConfiguration.class`, so Flyway never runs at startup and the schema is never created in `platform_master`.
- **Migrations exist**: The table is defined in [V000001__transaction_audit_initial_tables.sql](novopay-platform-creditcard-management/src/main/resources/sql/migrations/product/V000001__transaction_audit_initial_tables.sql), with many later migrations (e.g. V000008, V000011, V000019, V000029, V000048, V000058, V000061, V000063) altering `transaction_audit`. The native report queries in [TransactionListReportRowMapper](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/TransactionListReportRowMapper.java) use the schema `dsa_credit_card_mgmt` in raw SQL—that is a different (e.g. deployed) schema name; for local dev the same tables live in whatever DB `spring.datasource.url` points to (here, `platform_master`).

So: **the database `platform_master` must contain the credit-card schema (transaction_audit, transaction_audit_attributes, etc.). Today it does not because migrations were never applied.**

## Recommended fix: Run Flyway migrations once against platform_master

Apply the project’s Flyway migrations to `platform_master` so that `transaction_audit` and related tables exist. Two ways to do that:

### Option A – Run Flyway from command line (recommended for local)

1. Ensure MySQL is running and the database `platform_master` exists:
   - `CREATE DATABASE IF NOT EXISTS platform_master;`
2. Run Flyway against the same URL/user/password as in `application.properties` (e.g. `root` / your password), with migrations location `src/main/resources/sql/migrations/product` (or the path that your Flyway config uses if you add one). Example (from project root):
   - **Flyway CLI**: If you have [Flyway CLI](https://flywaydb.org/documentation/usage/commandline/) installed, run something like:
     - `flyway -url=jdbc:mysql://localhost:3306/platform_master -user=root -password=... -locations=filesystem:src/main/resources/sql/migrations/product migrate`
   - **Gradle**: If the project (or lib) has a Flyway Gradle task that points to the product migrations and the same DB URL, run that task instead.
3. Restart the credit-card-management app and call the submit application API again; the `transaction_audit` query should succeed (assuming a row exists for the `client_reference_code` you use, or you first create one via the add-on card flow).

### Option B – Enable Flyway at application startup

1. Remove `FlywayAutoConfiguration.class` from the `exclude` list in [Application.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/Application.java) so Flyway runs on boot.
2. Ensure Flyway uses the same datasource as JPA. The app also excludes `DataSourceAutoConfiguration`; the datasource may be provided by the lib. If Flyway picks up `spring.datasource.*` automatically, it will run against `platform_master`. If the app uses a custom datasource bean, you may need a `FlywayConfiguration` that injects that bean and sets it on `Flyway`.
3. Set Flyway locations to the product migrations, e.g. in `application.properties`:  
   `spring.flyway.locations=classpath:sql/migrations/product`  
   (adjust to the actual classpath path used in the project).
4. On first startup after the change, Flyway will create the schema in `platform_master`; subsequent starts will only run new migrations.

**Caveat**: The project currently excludes Flyway deliberately (e.g. schema may be managed elsewhere in some environments). Enabling it is a behavioral change; prefer Option A for local dev if you want to avoid that.

## After the schema exists

- **Submit application**: The endpoint that loads `TransactionAudit` by `client_reference_code` will work only if there is a row for that code. For end-to-end testing you typically:
  1. Create an add-on card request (so that a `transaction_audit` row is inserted), or
  2. Insert a test row in `transaction_audit` with the desired `client_reference_code` and any required attributes (e.g. AAN) for submit application.
- **Report queries**: [TransactionListReportRowMapper](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/TransactionListReportRowMapper.java) uses the schema name `dsa_credit_card_mgmt` in raw SQL. If you keep using `platform_master` for local dev, those queries will fail unless you either:
  - Change the schema in those SQL strings to `platform_master` for local, or
  - Use a separate profile (e.g. `application-dev.properties`) that points `spring.datasource.url` to a DB named `dsa_credit_card_mgmt` and run migrations there so the same schema name works.

## Summary

| Action | Purpose |
|--------|--------|
| Run Flyway migrations against `platform_master` (Option A or B) | Create `transaction_audit` and related tables so the JDBC error goes away |
| Ensure a row exists for your test `client_reference_code` | So submit application can load `TransactionAudit` and proceed |
| (Optional) Align report SQL schema with local DB or use `dsa_credit_card_mgmt` DB | So report queries work locally if you use them |

No code change is strictly required to fix the “table doesn’t exist” error—only applying the existing migrations to the database. Code changes are needed only if you enable Flyway at startup (Option B) or adjust report SQL for local schema names.
