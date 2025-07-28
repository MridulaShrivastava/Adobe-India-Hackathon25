# 🇮🇳 Adobe India Hackathon 2025 — Data Dynamo 🚀

> 🏆 Submitted by **Team: Data Dynamo**  
> 👩‍💻 Members:  
> - Mridula Shrivastava  
> - Kumari Sonam  
> 🎓 College: **Banasthali Vidyapith**

---

## 💡 Challenge Overview

We built a **Persona-Driven Document Intelligence System** that smartly analyzes PDFs and extracts the most relevant content based on a given user persona and task — such as planning, reviewing, or summarizing information.

This project was developed for **Round 1a** and **Round 1b** of the **Adobe India Hackathon 2025**.

---

## 🔷 Round 1A — PDF Outline Extractor

### ✅ Key Features:
- Extracts **document title** and **headings (H1, H2, H3)** with **page numbers**
- Detects headings using **font size and layout heuristics**
- Outputs clean **JSON structure** for easy integration
- Works on complex multi-page PDFs with nested sections

---

## 🔷 Round 1B — Persona-Driven Document Intelligence

### ✅ Key Features:
- Analyzes documents based on **user persona** and **task/job**
- Supports **multi-lingual documents** (e.g., English, Hindi, French)
- Ranks and selects **most relevant sections** from PDFs
- Input via simple **JSON config** (documents + persona + job)
- Fully **Dockerized** — easy to run without local setup
- Outputs insights in structured **JSON** with metadata

---

## 🌐 Multilingual Support

Our system is designed to **analyze and extract meaningful insights from PDFs in different languages**, using Unicode-aware extraction and tokenization techniques. It helps cater to users who work with documents in:

- English  
- Hindi  
- French  
- German  
- And many more (as long as text is extractable)

This allows global use for researchers, HR professionals, planners, and analysts working in different linguistic environments.

---

## ⚙️ Tech Stack

- 🐳 Docker
- 🐍 Python 3.11
- 📄 PDFMiner / PyMuPDF
- 🔍 NLP-based relevance scoring
- 📦 JSON-based configuration

---




## 🧠 Key Features

✅ Automatically identifies and ranks the most relevant sections in PDFs  
✅ Supports multiple personas and task-specific filtering  
✅ Clean JSON-based input and output  
✅ Headless and dockerized for easy cross-platform execution

---
