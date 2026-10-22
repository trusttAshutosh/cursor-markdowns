# 07 - Decision journal

Why, not how. Rejected alternatives matter more than the current design. If he cannot remember why, write **unknown - do not assume it was product lock**.

---

## BKYC assign (his)

| Decision | Why | Rejected | Product lock or engineering? |
| --- | --- | --- | --- |
| Auto cap 10 / manual cap 15 | [FILL confirm still current] | Unlimited / other numbers | [FILL] |
| Pin match uses office `address.pincode` | No separate agent-pincode column | Agent home pin | [FILL] |
| Visit owner = field-agent `corporate.id` | What Assign stores | `user.id`, `actor.id`, office id | Product + Actor model |
| Field agents cannot ADM3 reassign | Need `TASK-ALLOC-BKYC-ASSIGN`; they set `REASSIGNMENT_REQUESTED` | Agents reassign themselves | Product |
| Bank default grants: UPLOAD / UPLOAD-VIEW / REPORT-VIEW only | Flyway never seeds VIEW/ASSIGN to bank EMPL | Bank maker VIEW/ASSIGN | Product; QA drift is HDP-11535 |
| Entitled corporate **labels** are a static map | TaskAlloc does not live-call Actor for names | Live Actor lookup | **Engineering shortcut vs product lock** - successor must not treat as sacred |

## Agent OS (his)

| Decision | Why | Rejected |
| --- | --- | --- |
| Bob is proof engine, not the coder | Cursor agent plans/codes; Bob produces PASS/FAIL | Bob as the only workflow |
| `bob validate-ticket` explicit-only | Avoids burning boot time after every tiny edit | Auto-validate after every fix |
| Continual Learning stop-hook **off** | It rewrote AGENTS.md unasked | Auto-mine after every chat |
| One ticket per chat | Memory budget | Mega-chats |
| Unit tests: full suite only in CC repo | Other repos cannot afford preexisting suite on this machine | `gradle test` everywhere |
| Feature branches `ddp-fea-*` only | GitHub rejects other names | `ddp-fix-*` |
| Common-scripts Flyway before feature branch | Version collisions | Authoring Flyway on feature branch |

## CC / KYC Engine

| Decision | Why | Rejected |
| --- | --- | --- |
| KYC Engine: eKYC + cKYC only | Digilocker out of scope | [FILL] |
| Bank evidence = real applogs | Sample XML misleads the bank | Invented payloads |
| PAN: FE RSA-encrypts, CC forwards cipher, not stored on `kyc_detail` | [FILL] | Store PAN on kyc_detail |

## Add as they happen

Use `_template-entry.md`. One decision per heading.
