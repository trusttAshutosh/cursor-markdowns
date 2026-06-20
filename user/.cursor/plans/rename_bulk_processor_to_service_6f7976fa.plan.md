---
name: Rename bulk Processor to Service
overview: Rename the five v2 bulk classes from *Processor to *Service (class and file names) and update CreditCardBulkController references so naming is consistent with @Service and v2-only.
todos: []
isProject: false
---

# Rename bulk Processor classes to Service

## Scope

Rename the five v2-only bulk classes and their files; update [CreditCardBulkController](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/controller/CreditCardBulkController.java) to use the new names.

## Renames


| Current class (file)                  | New class (file)                    |
| ------------------------------------- | ----------------------------------- |
| `UploadCreditCardBulkFileProcessor`   | `UploadCreditCardBulkFileService`   |
| `GetCreditCardBulkLeadListProcessor`  | `GetCreditCardBulkLeadListService`  |
| `BulkSendCreditCardLinkProcessor`     | `BulkSendCreditCardLinkService`     |
| `UpdateCreditCardLeadStatusProcessor` | `UpdateCreditCardLeadStatusService` |
| `BulkResendCreditCardLinkProcessor`   | `BulkResendCreditCardLinkService`   |


## Steps

1. **Rename files and class names** (5 files)
  - [UploadCreditCardBulkFileProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/transaction/processor/UploadCreditCardBulkFileProcessor.java) → create `UploadCreditCardBulkFileService.java` with updated class name, delete old file.
  - [GetCreditCardBulkLeadListProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/transaction/processor/GetCreditCardBulkLeadListProcessor.java) → `GetCreditCardBulkLeadListService.java`.
  - [BulkSendCreditCardLinkProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/BulkSendCreditCardLinkProcessor.java) → `BulkSendCreditCardLinkService.java`.
  - [UpdateCreditCardLeadStatusProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/UpdateCreditCardLeadStatusProcessor.java) → `UpdateCreditCardLeadStatusService.java`.
  - [BulkResendCreditCardLinkProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/BulkResendCreditCardLinkProcessor.java) → `BulkResendCreditCardLinkService.java`.
  - Keep the same package for each (transaction.processor for the first two, common.processors for the last three). Internal implementation (extends AbstractProcessor, process/execute) unchanged.
2. **Update CreditCardBulkController**
  - Change imports to the new service classes.
  - Rename fields and constructor parameters (e.g. `uploadCreditCardBulkFileProcessor` → `uploadCreditCardBulkFileService`).
  - Update all five `.execute(ctx)` call sites to use the new field names.
3. **Verify**
  - Run `./gradlew compileJava` in `novopay-platform-creditcard-management`.

No other references to these class names exist in the repo (orchestration XMLs and templates were already removed).