# 📡 Inter-Agent Communication Protocol v2.0 (Academic Standard)

## 1. Principles of Communication
All agents within the AI-EcoSystem must adhere to the following communication standards to ensure data integrity, traceability, and efficient collaboration.

### 1.1. Precision & Conciseness
- **No Fluff:** Eliminate conversational fillers. State facts, hypotheses, and requirements directly.
- **Structured Data:** Prefer structured formats (JSON, YAML, Markdown Tables) over unstructured text for data exchange.
- **Context Awareness:** Always reference the specific `Task ID` or `Project Phase` being addressed.

### 1.2. Hierarchical Reporting
- **Subordinate to Superior:** Report status updates, blockers, and final deliverables. Do not wait for polling; push updates upon milestone completion.
- **Superior to Subordinate:** Provide clear directives, constraints, and acceptance criteria.
- **Peer to Peer:** Exchange data artifacts only when explicitly authorized by the Orchestrator or defined in the workflow.

## 2. Output Artifact Specifications

### 2.1. Standard Deliverable Format
All textual deliverables must follow this structure:

```markdown
# [Artifact Name]
**Type:** [e.g., Code, Analysis, Plan, Report]
**Author:** [Agent Name]
**Date:** [ISO 8601]
**Status:** [Draft/Final/Review]

## Executive Summary
[Concise overview of the content < 50 words]

## Content
[Main body of the work]

## Metadata / Verification
- **Sources:** [List of sources]
- **Confidence Score:** [0.0 - 1.0]
- **Next Steps:** [Recommended actions]
```

### 2.2. Code Artifacts
- Must include comprehensive docstrings (Google or NumPy style).
- Must include type hinting (Python) or interfaces (TypeScript).
- Must be accompanied by a separate test plan or unit tests.

## 3. Operational States

Agents must explicitly signal their state in logs:
- `[IDLE]`: Awaiting instructions.
- `[ANALYZING]`: Processing input context.
- `[EXECUTING]`: Performing the core task.
- `[VALIDATING]`: Self-correction and quality assurance.
- `[COMPLETED]`: Task finished, awaiting acknowledgment.
- `[ERROR]`: Operational failure (requires traceback).

## 4. Error Handling Protocol
In case of failure:
1.  **Log:** Immediate detailed logging of the error context.
2.  **Isolate:** Do not propagate the error to the global scope if contained.
3.  **Retry:** Attempt self-correction (max 3 retries).
4.  **Escalate:** If unresolved, report to Prime Orchestrator with a `CRITICAL_FAILURE` report.
