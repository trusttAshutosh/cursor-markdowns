# 05 - People and access

AI has no org chart of who actually answers. Transfer access **before** last day. Never paste secrets into this folder.

---

## People (successor pings)

| Need | Name | Channel | Notes |
| --- | --- | --- | --- |
| Platform / BKYC service spine | Deepankar Sarkar (`deepankar-np`) | [FILL] | Coding voice clone source |
| BKYC ingest / ADM7 / close file / Superset MIS | Abhishek Puranik (`trustt-abhishek`) | [FILL] | **Leaving** - get his KT first |
| Agent APIs / bio / submit | Harini (`Harini-Trustt`) | [FILL] | |
| Admin PWA | Anshu / Salini | [FILL] | |
| APK | Shailendra / Vinay | [FILL] | |
| Jenkins / TaskAlloc CI | Arnold | [FILL] | |
| Product (BKYC / CC) | [FILL] | | |
| QA who knows his cases | [FILL] | | |
| Bank - BKYC ingest/assign CSV | [FILL] | | |
| Bank - KYC Engine / DAP | [FILL] | | |
| HDFC Salesforce | [FILL] | | |
| Ops / DBA for Flyway when appuser lacks CREATE | [FILL] | | |

---

## Access that dies with the laptop

Point at the file. Do not copy values here.

| Access | Where it lives | Who must receive it |
| --- | --- | --- |
| QA / UAT / preprod MySQL + SSH + Superset | `%USERPROFILE%\.cursor\novopay-remote-db.env` | Successor + confirm ops rotated |
| Jira / GChat BKYC webhook | `%USERPROFILE%\.cursor\bkyc-jira.env` | Only if tracker resumes |
| GitHub `trusttAshutosh` | GitHub account | Org membership, not password sharing |
| cursor-markdowns | `Desktop/cursor-markdowns` remote `trusttAshutosh/cursor-markdowns` | Successor who will keep agent OS |
| mdshare (onboarding + BKYC tracker) | mdshare.trustt.com | Publishing rights |
| Cursor | his user settings + MCP | New owner of agent OS |
| Superset QA/UAT login | same remote-db.env keys `*_SUPERSET_*` | Read-only unless leadership says write |
| SFTP / DMS for BKYC files | [FILL] | Likely Abhishek's, not Ashutosh's - confirm |

## Do not

- Commit `.env` into this folder or into novopay git
- Put webhook URLs or DB passwords in CHANGELOG
- Leave his SSH key as the only way onto the QA box
