# Order #60 – Agent Memory

## Overview

This project implements an AI agent capable of maintaining both **short-term** and **long-term memory**. Unlike a traditional chatbot that forgets everything after each interaction, this agent can remember important user information across conversations and use that information to provide more personalized responses.

The system uses **Google Gemini**, **ChromaDB**, and **vector embeddings** to store and retrieve semantic memories.

---

## Features

- Maintains short-term conversation history during a session.
- Stores long-term user memories inside a vector database.
- Retrieves semantically relevant memories for future conversations.
- Uses cosine similarity for semantic memory retrieval.
- Automatically determines whether new information is worth remembering.
- Extracts persistent user facts from conversations.
- Uses structured JSON outputs with Pydantic validation.

---

## Technologies

- Python
- Google Gemini API
- ChromaDB
- Vector Embeddings
- Pydantic

---

## Architecture

```text
                    User Question
                          │
                          ▼
               Retrieve Relevant Memories
                 (Chroma Vector Database)
                          │
                          ▼
             Load Conversation History
                          │
                          ▼
                     Gemini API
          ┌────────────────────────────┐
          │                            │
          │  Answer User's Question    │
          │                            │
          │ Determine Whether Current  │
          │ Interaction Contains       │
          │ Long-Term Memory           │
          └────────────────────────────┘
                          │
                          ▼
          If Memory Exists → Extract Memory
                          │
                          ▼
               Store in ChromaDB
```

---

## Short-Term Memory

Short-term memory is maintained using conversation history.

It contains:

- Previous user messages
- Previous AI responses

This memory only exists while the application is running.

---

## Long-Term Memory

Long-term memories are stored inside ChromaDB as vector embeddings.

Examples of stored memories include:

- User preferences
- Favorite programming language
- Occupation
- Long-term goals
- Recurring interests

Each memory is embedded and stored individually, allowing future retrieval based on semantic similarity rather than exact keyword matching.

---

## Memory Retrieval

Whenever a new question is asked:

1. The user's question is embedded.
2. ChromaDB performs semantic similarity search.
3. Relevant memories are returned.
4. The retrieved memories are injected into the LLM prompt.
5. Gemini determines whether those memories are useful for answering the current question.

This prevents unrelated memories from unnecessarily influencing responses.

---

## Memory Storage

After answering the user's question, the agent determines whether the current interaction contains information valuable for future conversations.

If so:

1. Gemini extracts one or more long-term memories.
2. Each memory is stored as an independent document.
3. ChromaDB automatically generates embeddings for future retrieval.

---

## State Management

The application maintains a centralized state object containing:

- Current user question
- Retrieved long-term memories
- Conversation history
- Whether a memory was detected
- Current LLM response

This state serves as the source of truth throughout the interaction pipeline.

---

## What I Learned

Through this project I learned:

- The difference between short-term and long-term memory in AI agents.
- How vector databases enable semantic memory retrieval.
- How embeddings allow retrieval based on meaning rather than exact wording.
- How to integrate ChromaDB with an LLM.
- How to validate structured LLM outputs using Pydantic.
- How to build multi-stage LLM pipelines.
- The importance of prompt engineering for memory extraction.
- The challenges of determining which information is worth remembering for future conversations.

---

## Example Workflow

```text
User:
I'm a computer science student.

↓

Long-term memory stored:
"The user is a computer science student."

↓

User:
I love Python.

↓

Long-term memory stored:
"The user's favorite programming language is Python."

↓

User:
What backend framework should I learn?

↓

Retrieve relevant memories

↓

Gemini answers:

"Since you enjoy Python, FastAPI and Django would be excellent frameworks to learn..."
```