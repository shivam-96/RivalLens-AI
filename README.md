# Universal Competitive Intelligence Platform

Welcome to the **Universal Competitive Intelligence Platform**! 

This project is an advanced, automated pipeline designed to deliver **"Zero-Research Competitor Analysis."** By simply inputting a competitor's name and product, the system performs a multi-dimensional analysis and outputs a comprehensive **Intelligence Report** — arming your team with actionable tactics, sentiment analysis, product data, and comparison metrics within seconds.

## ✨ Key Features (What it does)

- **One-Click Intelligence Reports:** Generate a comprehensive, multi-tab competitive dashboard from just a competitor URL and product name.
- **RAG-Powered Head-to-Head Scorecards:** Directly compare your product's strengths against competitors. The system reads your internal product documentation and automatically generates "Where We Win" and "Where They Outperform" profiles.
- **"Questions They Might Ask" (Flashcards):** Automatically generates interactive 3D flashcards identifying potential buyer objections alongside tactical rebuttals and supporting data points.
- **Voice of Customer (Masonry Quotes):** Scrapes the web (G2, Reddit, YouTube) to calculate brand sentiment and organizes raw verbatim quotes into an aesthetically pleasing grid of 'Positive Resonance' and 'Critical Pain Points'.
- **Executive Quick Facts:** Aggregates corporate intel instantly, including recent funding rounds, accurate pricing tiers, and hidden product frictions (e.g., forced annual billing).
- **Distraction-Free UI:** A premium, "Clean Enterprise" Tailwind Dashboard. The input forms cleanly disappear once data is generated so you can focus entirely on the intelligence.

---

## 🎯 Who is this for?

- **Sales Representatives:** Gain instant, deep knowledge about a competitor right before a pitch. You get tailor-made objection handlers, elevator pitches, and precise comparison points.
- **Product Marketing Managers (PMMs):** Automate the tedious process of tracking competitor pricing, feature updates, and customer sentiment across disparate platforms.
- **Competitive Intelligence Analysts:** Easily aggregate corporate info, recent news, funding rounds, and raw review data into a single, standardized pipeline.

## 🧠 How it Works: The 6-Agent Architecture

The application operates using a powerful **Agentic Pipeline** built on **LangGraph** and deployed via **FastAPI** on the backend. When a request is submitted, these agents execute in order, accumulating data in a shared LangGraph state:

1. **Agent 0 | Classifier:** Normalizes the user input and formulates targeted search queries for the subsequent agents.
2. **Agent 1 | Corporate Profiler:** Gathers high-level corporate intelligence: employee count, total funding, rounds, and recent news.
3. **Agent 2 | Product Specialist:** Dives deep into the competitor's product offering. Extracts pricing tiers and critical "hidden frictions."
4. **Agent 3 | Reviewer:** Aggregates customer feedback to calculate sentiment scores and pull verbatim quotes.
5. **Agent 4 | RAG Strategist:** Contrasts competitor features against your own using **ChromaDB** as a vector database.
6. **Agent 5 | Compiler:** Synthesizes the intelligence into actionable field tactics.

## 💻 Tech Stack

### Backend
- **Python / FastAPI:** High-performance REST API.
- **LangGraph:** Framework for building stateful, multi-actor applications with LLMs.
- **Pydantic:** Robust data validation and schema definitions for the complex outputs.
- **ChromaDB:** Local vector database used to store and retrieve "our product" documentation.

### Frontend
- **React 19 & Vite:** Modern UI component composition and lightning-fast compilation.
- **Tailwind CSS v4:** Highly structural utility-first styling ensuring a spacious, readable, enterprise-grade aesthetic.

