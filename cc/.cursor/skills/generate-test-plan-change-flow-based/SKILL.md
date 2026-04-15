---
name: backend-test-plan-generation
description: Generate execution-driven backend test plans using DB + API validation by tracing full impacted flow from code changes. Use when user asks for test plans, QA validation steps, regression scenarios, or impact-based testing for backend services.
---

# Backend Test Plan Generation (Change + Flow Based)

## When To Use

Use this skill when:

- A PR / code change needs test coverage validation  
- Backend feature/API requires QA test plan  
- Regression scenarios need to be created  
- DB + API validation is required  
- Flow-level validation is important (not just unit-level)  
- Impact analysis of change is required  

---

## Inputs Required

If missing, ask:

Share:
1) PR / diff / changed files  
2) Feature / flow impacted  
3) Any known edge cases (optional)  

---

## Core Objective

Identify the COMPLETE FLOW impacted by the change and generate a test plan covering ALL involved components.

DO NOT rely on open/visible files  
DO NOT generate partial test plans  

Always derive from:
- Code change (PR/diff)
- Full flow traversal  

---

## Change Impact Analysis (MANDATORY)

Analyze the change and identify:

### Entry Points
- APIs / Controllers affected  

### Flow Traversal
- Service methods  
- Internal method calls  
- Utility classes  

### Data Layer
- Tables impacted (INSERT / UPDATE / SELECT)  
- Repositories used  
- Entity mappings  

### Dependencies
- External services  
- Queues / events  
- Cache / configs  

### Side Effects
- Audit/history tables  
- Logs  
- Status transitions  

### Indirect Impact
- Shared methods reused  
- Other flows impacted  

---

## Flow Trace (MANDATORY)

Controller → Service → Repository → DB → External Systems  

---

## Source of Truth

- Use entire repository  
- Follow method calls across files  
- Infer APIs, schema, logic from code  

If unclear → ASK  
DO NOT assume or invent  

---

## Strict Test Execution Format (NON-NEGOTIABLE)

For EVERY test scenario:

1. Insert minimal data in DB using SQL query  
2. Run the API  
3. Observe API response  
4. Run SELECT query to validate DB  
5. Expected output  
6. Conclusion from actual output  

---

## Test Scenario Template

### Scenario: <name>

#### Step 1: Insert Minimal Data

    -- SQL: exact insert query using real tables/columns

#### Step 2: Run API
- Endpoint:
- Method:
- Headers:
- Payload:

#### Step 3: Observe API Response

    {
      "expected": "response structure"
    }

#### Step 4: Validate DB

    -- SQL: select query verifying state

#### Step 5: Expected Output
- API:
- DB:
- Side effects (audit/events/logs):

#### Step 6: Conclusion
- Pass/Fail reasoning  

---

## Coverage (MANDATORY)

### Functional
- Happy path  
- Invalid input  
- Missing fields  
- Boundary values  

### Change Impact
- Existing flows affected  
- Backward compatibility  

### Data Integrity
- Correct DB operations  
- No unintended updates  
- Referential integrity  

### Reliability
- Idempotency / duplicate requests  
- Transaction rollback  
- Partial failures  

### System Behavior
- Concurrency  
- Retry / timeout  

### Dependencies
- Downstream failures  

### Observability
- Audit/history tables  
- Logs (if applicable)  

---

## Must-Have Practices

- Minimal test data  
- Test independence  
- Validate BOTH API + DB  
- Use real schema names  
- Verify:
  - status transitions  
  - rollback behavior  
  - no duplicate entries  

---

## Good-to-Have

- Tag scenarios (smoke / regression / critical)  
- Cleanup queries  
- Automation feasibility  
- Risk-based prioritization  
- Edge cases from code  

---

## Strict Rules

### DO NOT:
- Refer to open files  
- Miss indirect flows  
- Skip SQL or DB validation  
- Write generic test cases  
- Assume schema/APIs  

### DO:
- Trace from change  
- Cover full flow  
- Keep steps executable  
- Align with repository code  

---

## Output Format

Return:

1. Impacted flow summary  
2. Scenario list  
3. Detailed test scenarios (strict format)  
4. Coverage summary  
5. Gaps / risks  

---

## Final Expectation

Test plan must be:

- End-to-end  
- Change-impact driven  
- Fully executable  
- Zero fluff  