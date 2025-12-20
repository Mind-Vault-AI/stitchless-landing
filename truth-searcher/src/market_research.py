"""
Market Research Module - Phase 1: The "What" & "Why"
Identifies product category and Critical Decision Factors (CDFs).
DMAIC Principle: Define what matters BEFORE measuring.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from .config import SEARCH_TEMPLATES, SYSTEM_PROMPTS
from .search_service import SearchResult, SearchService

logger = logging.getLogger(__name__)


@dataclass
class CriticalFactor:
    """A Critical Decision Factor for a product category."""

    factor: str
    why_important: str
    source_url: str

    def to_dict(self) -> dict:
        return {
            "factor": self.factor,
            "why_important": self.why_important,
            "source_url": self.source_url,
        }


@dataclass
class MarketResearchResult:
    """Complete result from Phase 1 market research."""

    category: str
    critical_factors: list[CriticalFactor]
    search_queries_used: list[str]
    raw_search_results: list[SearchResult] = field(default_factory=list)
    confidence: str = "gemiddeld"  # hoog/gemiddeld/laag
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "critical_factors": [cf.to_dict() for cf in self.critical_factors],
            "search_queries_used": self.search_queries_used,
            "confidence": self.confidence,
            "error": self.error,
        }

    def get_factor_names(self) -> list[str]:
        """Return list of factor names for Phase 2."""
        return [cf.factor for cf in self.critical_factors]


class MarketResearch:
    """
    Phase 1 Engine: Researches what matters for a product category.

    Workflow:
    1. Extract potential category from user query
    2. Search for buying guides and common complaints
    3. Use LLM to identify top 3-5 Critical Decision Factors
    4. Return structured result with sources

    Zero-Hallucination Guarantee:
    - All factors must have source URLs
    - Unknown = "Onbekend", never guessed
    """

    def __init__(
        self,
        openai_api_key: str,
        search_service: SearchService,
        model: str = "gpt-4o",
        temperature: float = 0.1,
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.search_service = search_service
        self.model = model
        self.temperature = temperature

    def _build_search_queries(self, query: str, category: Optional[str] = None) -> list[str]:
        """Build search queries for market research."""
        # Use category if known, otherwise use query as-is
        target = category if category else query

        queries = []

        # Buying guide queries
        for template in SEARCH_TEMPLATES["buying_guide"]:
            queries.append(template.format(category=target))

        # Complaint queries
        for template in SEARCH_TEMPLATES["complaints"]:
            queries.append(template.format(category=target))

        return queries[:6]  # Limit to 6 queries for efficiency

    def _extract_category_from_query(self, user_query: str) -> str:
        """Use LLM to extract the product category from user query."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": """Je bent een productcategorie-expert.
Gegeven een productnaam of zoekopdracht, identificeer de algemene productcategorie.
Antwoord ALLEEN met de categorie, niets anders.
Voorbeelden:
- "Bosch Accu-boormachine 18V" -> "accuboormachine"
- "Hotel Zeezicht Zandvoort" -> "hotel"
- "Samsung Galaxy S24" -> "smartphone"
- "Nike Air Max 90" -> "sneakers"
""",
                    },
                    {"role": "user", "content": user_query},
                ],
            )
            category = response.choices[0].message.content.strip().lower()
            logger.info(f"Extracted category from user query")
            return category
        except Exception as e:
            logger.error(f"Category extraction failed: {e}")
            # Fallback: use the full query as category (more reliable than first word)
            logger.warning("Falling back to using full query as category")
            return user_query.lower()

    def _format_search_results_for_llm(self, results: list[SearchResult]) -> str:
        """Format search results as context for LLM."""
        if not results:
            return "Geen zoekresultaten gevonden."

        formatted = []
        for r in results:
            formatted.append(f"""
---
Bron: {r.url}
Titel: {r.title}
Samenvatting: {r.snippet}
---""")

        return "\n".join(formatted)

    def _analyze_with_llm(
        self, category: str, search_context: str, queries_used: list[str]
    ) -> MarketResearchResult:
        """Use LLM to extract Critical Decision Factors from search results."""
        try:
            user_prompt = f"""
Productcategorie: {category}

Zoekresultaten (koopgidsen en klachten):
{search_context}

Gebruikte zoekopdrachten: {', '.join(queries_used)}

Analyseer bovenstaande informatie en identificeer de 3-5 belangrijkste
Critical Decision Factors (CDFs) voor deze productcategorie.

BELANGRIJK:
- Elke factor MOET een bron-URL hebben uit de zoekresultaten
- Als je geen bewijs vindt voor een factor, neem het NIET op
- Liever 3 goed onderbouwde factoren dan 5 zwakke
"""

            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS["category_researcher"]},
                    {"role": "user", "content": user_prompt},
                ],
            )

            result_json = json.loads(response.choices[0].message.content)

            # Parse critical factors
            factors = []
            for cf_data in result_json.get("critical_factors", []):
                factors.append(
                    CriticalFactor(
                        factor=cf_data.get("factor", "Onbekend"),
                        why_important=cf_data.get("why_important", "Geen uitleg beschikbaar"),
                        source_url=cf_data.get("source_url", ""),
                    )
                )

            # Determine confidence based on number of factors and sources
            confidence = "laag"
            valid_sources = sum(1 for f in factors if f.source_url)
            if len(factors) >= 3 and valid_sources >= 2:
                confidence = "hoog"
            elif len(factors) >= 2 and valid_sources >= 1:
                confidence = "gemiddeld"

            return MarketResearchResult(
                category=result_json.get("category", category),
                critical_factors=factors,
                search_queries_used=result_json.get("search_queries_used", queries_used),
                confidence=confidence,
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return MarketResearchResult(
                category=category,
                critical_factors=[],
                search_queries_used=queries_used,
                error="Analyse mislukt: ongeldige response",
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return MarketResearchResult(
                category=category,
                critical_factors=[],
                search_queries_used=queries_used,
                error=f"Analyse mislukt: {str(e)}",
            )

    def research(self, user_query: str) -> MarketResearchResult:
        """
        Execute Phase 1: Market Research.

        Args:
            user_query: The product or service to research (e.g., "Bosch Drill 3000")

        Returns:
            MarketResearchResult with category and Critical Decision Factors
        """
        logger.info("Starting Phase 1 market research")

        # Step 1: Extract category
        category = self._extract_category_from_query(user_query)
        logger.info(f"Identified category: {category}")

        # Step 2: Build and execute search queries
        queries = self._build_search_queries(user_query, category)
        logger.info(f"Executing {len(queries)} search queries")

        all_results: list[SearchResult] = []
        for query in queries:
            results = self.search_service.search(query, num_results=5)
            all_results.extend(results)

        logger.info(f"Collected {len(all_results)} total search results")

        # Step 3: Handle no results case
        if not all_results:
            logger.warning("No search results found for market research")
            return MarketResearchResult(
                category=category,
                critical_factors=[],
                search_queries_used=queries,
                error="Geen zoekresultaten gevonden. Probeer een andere zoekopdracht.",
            )

        # Step 4: Format results and analyze with LLM
        search_context = self._format_search_results_for_llm(all_results)
        result = self._analyze_with_llm(category, search_context, queries)
        result.raw_search_results = all_results

        logger.info(
            f"Phase 1 complete: Found {len(result.critical_factors)} Critical Decision Factors"
        )

        return result

    def get_default_factors(self, category: str) -> list[CriticalFactor]:
        """
        Fallback: Return generic factors if research fails.
        Marked as 'Onbekend' to indicate lack of evidence.
        """
        return [
            CriticalFactor(
                factor="Prijs-kwaliteitverhouding",
                why_important="Geen specifieke informatie gevonden",
                source_url="",
            ),
            CriticalFactor(
                factor="Gebruiksgemak",
                why_important="Geen specifieke informatie gevonden",
                source_url="",
            ),
            CriticalFactor(
                factor="Duurzaamheid",
                why_important="Geen specifieke informatie gevonden",
                source_url="",
            ),
        ]
