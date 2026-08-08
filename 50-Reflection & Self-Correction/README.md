# Reflection & Self-Correction

**Phase:** 3 — AI Agents  
**Order:** 50  
**Status:** ✅ Completed  
**Focus:** Reflective Decision-Making

---

## Overview

This project demonstrates a manually orchestrated reflective AI agent capable of making informed decisions through multiple reasoning stages.

Rather than immediately generating an answer, the agent first plans what information is required, evaluates whether enough information exists to make a decision, and finally produces a verdict using the accumulated knowledge.

Every reasoning step is performed through explicit LLM API calls coordinated entirely in Python without relying on agent frameworks.

---

## Learning Objectives

- Understand reflection as a separate reasoning step
- Build a multi-stage AI workflow
- Separate planning from decision making
- Maintain shared working state across multiple LLM calls
- Validate structured outputs using Pydantic
- Manually orchestrate an AI agent without frameworks

---

## Architecture

```text
                    User Question
                          │
                          ▼
                API Call #1 (Planner)
                          │
                          ▼
             Generate Required Information
                          │
                          ▼
                 Update Shared State
                          │
                          ▼
      User + External Information Collection
                          │
                          ▼
          API Call #2 (Requirement Checker)
                          │
                          ▼
          Determine Missing Information
                          │
                          ▼
                 Update Shared State
                          │
                          ▼
             API Call #3 (Decision Maker)
                          │
                          ▼
                  Final Decision
```

---

## Reflection Workflow

### Stage 1 — Planning

The agent first analyzes the user's question and determines what information is necessary before a decision can be made.

Instead of answering immediately, it creates a structured plan consisting of five required pieces of information.

---

### Stage 2 — Requirement Evaluation

The user provides additional context.

The agent then evaluates whether every requirement can be satisfied using:

- User-provided information
- External knowledge

The result is stored as structured working state.

---

### Stage 3 — Final Decision

After all available information has been gathered, the agent performs a final reasoning step and produces a verdict based on the accumulated state.

---

## Shared State

Throughout execution, the agent maintains a shared working state containing:

- Original question
- Generated plan
- Requirement status
- Collected information
- Final verdict

The state acts as the agent's working memory throughout the reasoning process.

---

## Key Concepts

### Reflection Is Another Reasoning Step

Reflection is not automatic.

It requires another LLM call that asks questions such as:

- Do I have enough information?
- Can I answer confidently?
- What information is still missing?

---

### Planning and Decision Making Are Separate

Rather than immediately answering the user's question, the agent separates:

1. Planning
2. Information gathering
3. Final reasoning

This mirrors how production AI agents often decompose complex tasks.

---

### Shared State

The agent stores intermediate results inside a shared state object.

Each reasoning stage reads from and updates the same working memory, allowing information to flow throughout the workflow.

---

### Structured Outputs

Every reasoning stage returns structured JSON validated with Pydantic models.

This ensures deterministic communication between the LLM and the Python application.

---

## Technologies

- Python
- Google Gemini SDK
- Pydantic
- JSON
- python-dotenv

---

## Future Improvements

Potential production enhancements include:

- Iterative information acquisition loops
- Automatic external tool integration
- Memory persistence
- Human-in-the-loop approval
- Confidence estimation
- Better reflection prompts
- Evaluation metrics
- Retry and recovery policies

These improvements were intentionally omitted to focus on understanding the reflection architecture.

---

## Repository Philosophy

This project is part of a project-driven AI Engineering roadmap.

The objective is to understand reflection from first principles by manually orchestrating every reasoning step before introducing higher-level frameworks such as LangGraph or the OpenAI Agents SDK.