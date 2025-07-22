# 📘 DeepSeek LangChain RAG Engine

This project is a FastAPI-based LLM application that uses:
- 🧠 **DeepSeek V3 (via OpenRouter)**
- 🔗 **LangChain**
- 🗃️ **Chroma (local vector store)**
- 📄 **PDF document loader**
- 📚 **HuggingFace Embeddings**

## 💡 What It Does

- Upload a regulation PDF
- Extracts and chunks each regulation into vector DB using metadata
- Uses similarity search to retrieve relevant regulations
- Sends query + context to DeepSeek for smart answers

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
# Deepseek_Langchain_engine
A FastAPI-powered RAG (Retrieval-Augmented Generation) system that uses DeepSeek V3 via OpenRouter, LangChain, ChromaDB, and PDF document parsing to answer regulation-based queries.
