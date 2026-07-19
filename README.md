# Enterprise AI Assistant

> A production-oriented multi-source AI assistant for enterprise data intelligence, combining internal documents, structured databases, and live web information into a single conversational interface.

---

## Overview

The **Enterprise AI Assistant** is an intelligent business assistant designed to answer enterprise questions using multiple information sources.

Instead of relying on a single knowledge source, the system intelligently routes each user query to the most relevant source:

- 📄 **Company Documents** → Retrieval-Augmented Generation (RAG)
- 🗄️ **Structured Business Data** → Text-to-SQL
- 🌐 **Live Information** → Web Search
- 🧠 **LLM-based Synthesis** → Final grounded response

The system is built using a **LangGraph-based multi-agent architecture**, allowing specialized AI agents to work together in a controlled workflow.

---

## Key Features

### 🤖 Intelligent Query Routing

The Planner/Router Agent analyzes the user's query and determines the appropriate source:

- `RAG` → For internal documents and company policies
- `SQL` → For structured database questions and business metrics
- `WEB` → For current external information
- `MULTI-SOURCE` → When multiple sources are required

---

### 📄 Document Intelligence with RAG

The system can answer questions from uploaded enterprise documents.

#### Pipeline

```text
PDF Upload
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Embeddings
     ↓
FAISS Vector Store
     ↓
Semantic Retrieval
     ↓
LLM Response