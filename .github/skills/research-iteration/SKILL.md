# Research Iteration Orchestrator

## Description
Orchestrate a full research iteration cycle: DO → CRITIQUE → LOG → COMPILE → COMMIT → PLAN NEXT.

## Workflow

### 1. DO WORK (parallel subagents)
Launch multiple background agents for independent work items:
- **Analysis agents**: Run analytical models, parameter studies, new physics
- **Paper agents**: Write/improve specific sections
- **Figure agents**: Generate publication-quality figures
- **FEA agents**: Mesh generation, modal analysis, validation

### 2. CRITIQUE (Reviewer B)
After work completes, invoke the `reviewer-b` agent on ALL new results:
- Check physics correctness, dimensional consistency, novelty claims
- Rate severity: FATAL / MAJOR / MODERATE / MINOR

### 3. LOG
Create timestamped research log entry in `docs/research-logs/`:
- Filename: `YYYY-MM-DDTHHMM-<topic>.md`
- Content: What was done, found, critical analysis, plan changes

### 4. COMPILE PAPER
Build current LaTeX draft and preserve timestamped PDF in `paper/drafts/`.

### 5. GIT CHECKPOINT
Commit all changes with descriptive message.

### 6. PLAN NEXT
Update SQL todos and identify the next parallel work batch.

## Parallelism Strategy
Always maintain 3-5 concurrent background agents:
- At least 1 analysis agent (new physics or refinement)
- At least 1 paper-writing agent (section content)
- At least 1 review/QA agent (critique, verification)
- Optional: FEA, figures, literature
