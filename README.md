# RAG SQL Agent

A production-grade, end-to-end RAG SQL Agent that accepts data files,
generates SQL from natural language, self-corrects errors, and interprets results.
Powered by OpenRouter (any LLM) + DuckDB + ChromaDB + Streamlit.

## Quick Start

### 1. Clone and Install
\```bash
git clone <your-repo-url>
cd rag_sql_agent
pip install -r requirements.txt
\```

### 2. Configure API Key
\```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
# Get a key at: https://openrouter.ai/keys
\```

### 3. Run
\```bash
streamlit run app.py
\```

Open http://localhost:8501 in your browser.

## Supported File Formats
- CSV (auto-detects separator and encoding)
- TSV (tab-separated)
- Excel (.xlsx and .xls — all sheets loaded as separate tables)
- JSON (array or nested object format)
- JSON Lines (.jsonl)
- Parquet

## How It Works
1. Upload your data file in the sidebar
2. The agent extracts schema intelligence and embeds it in ChromaDB (vector store)
3. Ask a question in plain English
4. The agent retrieves relevant schema context via semantic search (RAG)
5. Generates DuckDB SQL using your chosen LLM via OpenRouter
6. Executes SQL against DuckDB (in-memory, no server)
7. Self-corrects if SQL fails (up to 3 attempts)
8. Interprets results in natural language

## Architecture
- **OpenRouter**: LLM provider (supports GPT-4o, Claude, Gemini, Llama, etc.)
- **DuckDB**: In-memory SQL engine — no database setup needed
- **ChromaDB**: Vector store for schema RAG
- **sentence-transformers**: Local embeddings (all-MiniLM-L6-v2, runs on CPU)
- **Streamlit**: Web UI

## Environment Variables
See `.env.example` for all configuration options.

## Sample Data

The `sample_data/` folder ships with four ready-to-use datasets so you can
demo the agent immediately — just upload one in the sidebar:

| File | Domain | Shape | Try asking |
|------|--------|-------|-----------|
| `DELTA_SaaS_Financial_Intelligence.csv` | SaaS finance | 720 rows × 37 cols | "Which companies clear the Rule of 40?" |
| `NEXUS_HEOR_CardiozemX_ClinicalTrial.csv` | Clinical / HEOR | 2,500 rows × 58 cols | "Compare HbA1c reduction across treatment arms" |
| `PHARMA_GLP1_Market_Rx_Intelligence.csv` | Rx market | Rx intelligence | "What is the prescription trend by region?" |
| `PRISM_CompetitiveIntelligence_AI_Market.csv` | Market intel | Competitive set | "Rank companies by market share" |

## Deployment — Streamlit Community Cloud

This is a **Python / Streamlit application**, so it cannot be hosted on GitHub
Pages (which only serves static files). Deploy it free on **Streamlit Community
Cloud**, which runs directly from your GitHub repository:

1. **Push this folder to a public GitHub repo**
   ```bash
   git init
   git add .
   git commit -m "RAG SQL Agent"
   git branch -M main
   git remote add origin https://github.com/<your-username>/rag-sql-agent.git
   git push -u origin main
   ```
   The included `.gitignore` keeps your `.env` (and your API key) out of the repo.

2. **Create the app**
   - Go to https://share.streamlit.io and sign in with GitHub.
   - Click **New app** -> select your repo, branch `main`, main file `app.py`.

3. **Add your secret** (do NOT commit the key)
   - In the app's **Settings -> Secrets**, paste:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-real-key"
     DEFAULT_MODEL = "openai/gpt-4o-mini"
     ```
   - Streamlit injects these as environment variables at runtime.

4. **Deploy** — the app builds from `requirements.txt` and goes live at
   `https://<your-app>.streamlit.app`.

> First boot downloads the `all-MiniLM-L6-v2` embedding model (~90 MB), so the
> initial load takes a minute. Subsequent loads are cached.

### Alternative hosts
Any platform that runs a Python web process works: **Hugging Face Spaces**
(choose the *Streamlit* SDK), **Render**, **Railway**, or a container via the
standard `streamlit run app.py` start command. Set `OPENROUTER_API_KEY` as an
environment variable / secret on whichever host you choose.

## Project Structure
```
rag_sql_agent/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Pinned dependencies
├── .env.example            # Copy to .env and add your key
├── .gitignore
├── sample_data/            # 4 demo datasets
├── config/                 # Settings (pydantic-settings)
├── utils/                  # SQL validation, formatting, session state
├── data/                   # File loader (CSV/TSV/Excel/JSON/Parquet)
├── rag/                    # Schema extraction, vector store, context builder
└── agent/                  # Intent -> SQL -> execute -> repair -> interpret
```
