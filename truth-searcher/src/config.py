"""
Configuration module for Truth Searcher.
Contains all system prompts, constants, and settings.
DMAIC Principle: Define clear boundaries and controls.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AppConfig:
    """Application configuration with sensible defaults."""

    # API Keys (loaded from environment)
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    serpapi_key: Optional[str] = field(default_factory=lambda: os.getenv("SERPAPI_KEY"))

    # Model settings
    model_name: str = "gpt-4o"
    temperature: float = 0.1  # Low temperature for factual responses
    max_tokens: int = 2000

    # Search settings
    max_search_results: int = 10
    search_language: str = "nl"  # Dutch
    search_country: str = "nl"

    # Scoring settings
    min_evidence_threshold: int = 1  # Minimum mentions to assign a score
    score_range: tuple = (1, 10)

    # UI Language (Dutch - A2 Level)
    lang: str = "nl"


# System prompts - Engineering for zero hallucination
SYSTEM_PROMPTS = {
    "category_researcher": """Je bent een ervaren marktonderzoeker. Je taak is om:

1. IDENTIFICEER de productcategorie van de gebruikersvraag
2. ZOEK naar koopgidsen en klachten voor deze categorie
3. EXTRAHEER de 3-5 belangrijkste beslissingsfactoren (Critical Decision Factors)

STRIKTE REGELS:
- Baseer ALLEEN op zoekresultaten, NOOIT op eigen kennis
- Als je iets niet kunt vinden, zeg "Onbekend"
- Citeer ALTIJD de bron-URL voor elke claim
- Geen aannames, geen gissingen, alleen feiten

Output format (JSON):
{
    "category": "string",
    "critical_factors": [
        {"factor": "string", "why_important": "string", "source_url": "string"}
    ],
    "search_queries_used": ["string"]
}""",

    "review_analyzer": """Je bent een objectieve productanalist. Je taak is om:

1. ANALYSEER reviews over het specifieke product
2. MAP elk review-punt naar de gegeven Critical Decision Factors
3. SCORE alleen als er bewijs is (1-10 schaal)

STRIKTE REGELS - POKA YOKE (Foutpreventie):
- Score = "N/A" als er GEEN reviews over een factor zijn
- Score = "N/A" als bewijs onduidelijk of tegenstrijdig is
- NOOIT een score gissen of invullen zonder bewijs
- Citeer ALTIJD de bron-URL voor elke score
- Gebruik "Jip en Janneke" taal (heel simpel Nederlands, CEFR A2)

Output format (JSON):
{
    "product_name": "string",
    "category": "string",
    "analysis": [
        {
            "factor": "string",
            "score": "number of 'N/A'",
            "evidence_count": "number",
            "summary": "string (max 2 zinnen, heel simpel)",
            "sentiment": "positief/negatief/gemengd/onbekend",
            "sources": ["url1", "url2"]
        }
    ],
    "unit_economics": {
        "price_value_ratio": "string",
        "recommendation": "string (1 zin)"
    },
    "confidence_level": "hoog/gemiddeld/laag",
    "total_reviews_analyzed": "number"
}""",

    "simplifier": """Je bent een communicatie-expert. Herschrijf de tekst in "Jip en Janneke" stijl:
- Korte zinnen (max 10 woorden)
- Geen moeilijke woorden
- Concreet en duidelijk
- CEFR A2 niveau Nederlands
- Gebruik voorbeelden uit het dagelijks leven"""
}

# Dutch UI Messages
UI_MESSAGES = {
    "title": "🔍 De Waarheidszoeker",
    "subtitle": "Eerlijk product onderzoek zonder verzinsels",
    "input_label": "Wat wil je onderzoeken?",
    "input_placeholder": "Bijv: Bosch Accu-boormachine 18V of Hotel Zeezicht Zandvoort",
    "button_search": "🔎 Onderzoek starten",
    "phase1_status": "⏳ Even geduld, ik onderzoek eerst wat belangrijk is bij {category}...",
    "phase2_status": "📊 Nu kijk ik hoe {product} scoort op deze punten...",
    "phase3_status": "📝 Ik maak het rapport voor je klaar...",
    "error_no_api": "⚠️ API sleutel ontbreekt. Stel OPENAI_API_KEY in.",
    "error_search": "⚠️ Zoeken mislukt. Probeer het opnieuw.",
    "error_analysis": "⚠️ Analyse mislukt. Probeer het opnieuw.",
    "download_pdf": "📥 Download PDF Rapport",
    "table_header_factor": "Wat is belangrijk?",
    "table_header_score": "Score",
    "table_header_explanation": "Uitleg",
    "table_header_sources": "Bronnen",
    "na_explanation": "Geen informatie gevonden",
    "legend_title": "Wat betekenen de scores?",
    "legend_good": "8-10: Uitstekend ✅",
    "legend_ok": "5-7: Redelijk ⚠️",
    "legend_bad": "1-4: Matig ❌",
    "legend_na": "N/A: Geen data 🔍",
    "confidence_high": "🟢 Hoge betrouwbaarheid",
    "confidence_medium": "🟡 Gemiddelde betrouwbaarheid",
    "confidence_low": "🔴 Lage betrouwbaarheid",
}

# Category templates for search queries
SEARCH_TEMPLATES = {
    "buying_guide": [
        "koopgids {category}",
        "buying guide {category}",
        "waar op letten bij kopen {category}",
        "{category} kopen tips",
    ],
    "complaints": [
        "meest voorkomende klachten {category}",
        "problemen met {category}",
        "{category} nadelen",
        "common complaints {category}",
    ],
    "reviews": [
        "{product} review",
        "{product} ervaringen",
        "{product} test",
        "{product} beoordeling",
    ]
}
