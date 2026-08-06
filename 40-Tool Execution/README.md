# Tool Execution

**Phase:** 3 — AI Agents  
**Order:** 40  
**Status:** ✅ Completed  
**Focus:** Manual Tool Execution

---

## Overview

This project demonstrates the complete manual tool execution lifecycle of an AI agent.

Rather than relying on agent frameworks such as LangGraph or the OpenAI Agents SDK, every step is orchestrated manually using Python and the Google Gemini SDK.

The objective is to understand how modern LLMs request tool execution, how applications dispatch tool calls, and how observations are returned to the model for continued reasoning.

---

## Learning Objectives

- Understand the complete tool execution lifecycle
- Execute tools manually using Python
- Dispatch multiple tools
- Return structured observations to the LLM
- Continue reasoning after tool execution
- Build the orchestration layer without agent frameworks

---

## Architecture

```text
                User
                  │
                  ▼
          Initial LLM Request
                  │
                  ▼
      Does the model require a tool?
             │              │
          No │              │ Yes
             ▼              ▼
     Return Response     Function Call
                               │
                               ▼
                   Python Tool Dispatcher
                               │
                               ▼
                        Execute Tool
                               │
                               ▼
                  Structured Observation
                               │
                               ▼
                    Second LLM API Call
                               │
                               ▼
                     Final AI Response
```

---

## Project Features

- Manual tool declarations
- Multiple available tools
- Manual function dispatch
- Structured tool outputs
- Multiple LLM API calls
- Framework-free orchestration

---

## Implemented Tools

### Weather Tool

Returns mock weather information for a requested city.

### Light Temperature Tool

Adjusts the color temperature of a room's lighting using Kelvin values.

---

## Tool Execution Lifecycle

1. The user submits a request.
2. The LLM determines whether a tool is required.
3. If a tool is needed, the model returns a function call.
4. Python receives the function call and dispatches the appropriate tool.
5. The tool executes and produces a structured observation.
6. Python sends the observation back to the LLM.
7. The LLM continues reasoning using the observation and generates the final response.

---

## Key Concepts

### Tool Calls Are Not Answers

Tools produce observations—not responses to the user.

Example:

```json
{
    "city": "Orlando",
    "weather": "85.2°F"
}
```

The LLM reasons over this observation before generating the final answer.

---

### Python Executes the Tools

The LLM never executes Python code directly.

Instead, the workflow is:

1. LLM requests a tool.
2. Python executes the tool.
3. Python returns the observation.
4. The LLM continues reasoning.

---

### Multiple API Calls

Tool execution is not completed in a single interaction.

This project manually implements the complete workflow:

1. Initial reasoning
2. Tool execution
3. Final reasoning

---

## Technologies

- Python
- Google Gemini SDK
- JSON
- python-dotenv

---

## Future Improvements

Potential production enhancements include:

- Generic tool registry
- Structured error handling
- Retry policies
- Logging and observability
- Asynchronous tool execution
- Dynamic tool loading
- Unit and integration testing

These improvements were intentionally omitted to focus on understanding the underlying tool execution architecture.

---

## Repository Philosophy

This project is part of a project-driven AI Engineering roadmap.

The emphasis is on understanding AI systems from first principles by manually implementing core concepts before introducing higher-level abstractions such as LangGraph or the OpenAI Agents SDK.