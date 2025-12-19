# 🔍 De Waarheidszoeker (The Truth Searcher)

**Zero-Hallucination Product Research MVP**

A production-grade Streamlit application that researches WHAT matters before scoring a product. Built on DMAIC (Define, Measure, Analyze, Improve, Control) and Lean efficiency principles.

## 🎯 The Problem

Standard review summaries fail because they guess what is important.

*Example:* A summary might praise a drill's color, while the buyer only cares about battery life and torque.

**We fix this.**

## 🧠 The Logic (1W5H & Research-First Approach)

The app executes two distinct phases for every user query:

### Phase 1: Market Research (The "What" & "Why")
- Identify the **Product Category** from the user query
- Search for buying guides and common complaints
- Extract the top 3-5 **Critical Decision Factors (CDFs)**
- *Example:* Drill → [Battery Life, Torque, Weight]
- *Example:* Hotel → [Hygiene, Noise Level, Bed Comfort]

### Phase 2: Product Analysis (The "How")
- Search for product-specific reviews
- Map review data AGAINST the Critical Decision Factors
- Score each factor (1-10) **only with evidence**
- **Poka Yoke:** If no evidence exists → Score = "N/A" (not a guess!)

### Phase 3: Output (The "Who" - Customer Centric)
- Simple Dutch language (CEFR A2 / "Jip en Janneke" style)
- Clean PDF report generation
- Source citations for transparency

## 🚀 Quick Start

### 1. Install dependencies

```bash
cd truth-searcher
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

Or set environment variables:
```bash
export OPENAI_API_KEY="sk-your-key"
export SERPAPI_KEY="your-serpapi-key"  # Optional
```

### 3. Run the application

```bash
streamlit run app.py
```

## 📁 Project Structure

```
truth-searcher/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── README.md                # This file
└── src/
    ├── __init__.py
    ├── config.py            # Configuration & system prompts
    ├── search_service.py    # Search abstraction (SerpAPI + DuckDuckGo)
    ├── market_research.py   # Phase 1: Category & CDF extraction
    ├── review_analyzer.py   # Phase 2: Evidence-based scoring
    └── pdf_generator.py     # Phase 3: Report generation
```

## 🔧 Architecture

### Key Design Principles

1. **Zero Hallucination**: Every score must have evidence. No guessing.
2. **Poka Yoke (Error-Proofing)**: If evidence is missing → "N/A"
3. **Source Citations**: Every claim links to its source URL
4. **Modular Design**: Separate classes for each phase
5. **Fallback Strategy**: DuckDuckGo when SerpAPI unavailable

### Classes

- `SearchService`: Unified search with automatic fallback and retry logic
- `MarketResearch`: Phase 1 engine - extracts Critical Decision Factors
- `ReviewAnalyzer`: Phase 2 engine - maps reviews to CDFs with scoring
- `generate_pdf_report()`: Creates professional PDF reports

## 🌐 API Requirements

### Required
- **OpenAI API** (GPT-4o recommended)

### Optional
- **SerpAPI** - For higher quality Google search results
  - Without it, DuckDuckGo is used as fallback

## 📊 Score Legend

| Score | Meaning |
|-------|---------|
| 8-10 ✅ | Excellent |
| 5-7 ⚠️ | Acceptable |
| 1-4 ❌ | Poor |
| N/A 🔍 | No data found |

## 🔒 Privacy & Security

- API keys are never logged or stored
- All processing happens in real-time
- No user data is retained between sessions

## 📝 License

MIT License - See LICENSE file for details.

---

*Built with ❤️ for honest product research*
