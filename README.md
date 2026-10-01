# 🏏 Cricket RAG Assistant

An LLM-powered Cricket Question Answering system that combines **Retrieval-Augmented Generation (RAG)** with a cricket knowledge base to provide grounded answers to cricket-related questions.

The application uses **FastAPI** for the backend API, **ChromaDB** for vector retrieval, **Hugging Face embeddings** for semantic search, **Ollama with Llama 3.2:1b** for language generation, and **Streamlit** for the user interface. The complete application can also be deployed using **Docker and Docker Compose**.

---

## 📌 Project Overview

Large Language Models can sometimes generate incorrect or hallucinated answers when asked factual questions.

This project addresses that problem by retrieving relevant information from a curated cricket knowledge base before generating an answer.

### Workflow

```text
User
  ↓
Streamlit UI
  ↓
FastAPI API
  ↓
Cricket RAG Engine
  ↓
ChromaDB Vector Search
  ↓
Relevant Cricket Documents
  ↓
Llama 3.2:1b / Hybrid Extraction
  ↓
Grounded Answer