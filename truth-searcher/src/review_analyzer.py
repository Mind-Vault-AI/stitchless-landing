"""
Review Analyzer Module - Phase 2: The "How"
Maps product reviews against Critical Decision Factors with evidence-based scoring.
DMAIC Principle: Measure and Analyze with Poka Yoke (error-proofing).
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI

from .config import SEARCH_TEMPLATES, SYSTEM_PROMPTS
from .market_research import CriticalFactor
from .search_service import SearchResult, SearchService

logger = logging.getLogger(__name__)


@dataclass
class FactorAnalysis:
    """Analysis of a single Critical Decision Factor for a product."""

    factor: str
    score: str  # 1-10 or "N/A"
    evidence_count: int
    summary: str  # Jip en Janneke style
    sentiment: str  # positief/negatief/gemengd/onbekend
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "factor": self.factor,
            "score": self.score,
            "evidence_count": self.evidence_count,
            "summary": self.summary,
            "sentiment": self.sentiment,
            "sources": self.sources,
        }

    @property
    def has_evidence(self) -> bool:
        """Check if this factor has supporting evidence."""
        return self.score != "N/A" and self.evidence_count > 0

    @property
    def score_numeric(self) -> Optional[float]:
        """Get numeric score if available."""
        try:
            return float(self.score)
        except (ValueError, TypeError):
            return None

    @property
    def score_emoji(self) -> str:
        """Get emoji representation of score."""
        if self.score == "N/A":
            return "🔍"
        try:
            num = float(self.score)
            if num >= 8:
                return "✅"
            elif num >= 5:
                return "⚠️"
            else:
                return "❌"
        except ValueError:
            return "🔍"


@dataclass
class UnitEconomics:
    """Price-value analysis for the product."""

    price_value_ratio: str
    recommendation: str

    def to_dict(self) -> dict:
        return {
            "price_value_ratio": self.price_value_ratio,
            "recommendation": self.recommendation,
        }


@dataclass
class ProductAnalysisResult:
    """Complete result from Phase 2 product analysis."""

    product_name: str
    category: str
    analyses: list[FactorAnalysis]
    unit_economics: UnitEconomics
    confidence_level: str  # hoog/gemiddeld/laag
    total_reviews_analyzed: int
    raw_search_results: list[SearchResult] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "product_name": self.product_name,
            "category": self.category,
            "analysis": [a.to_dict() for a in self.analyses],
            "unit_economics": self.unit_economics.to_dict(),
            "confidence_level": self.confidence_level,
            "total_reviews_analyzed": self.total_reviews_analyzed,
            "error": self.error,
        }

    @property
    def average_score(self) -> Optional[float]:
        """Calculate average score across factors with evidence."""
        scores = [a.score_numeric for a in self.analyses if a.score_numeric is not None]
        return sum(scores) / len(scores) if scores else None

    @property
    def factors_with_data(self) -> int:
        """Count factors that have evidence."""
        return sum(1 for a in self.analyses if a.has_evidence)

    @property
    def factors_without_data(self) -> int:
        """Count factors without evidence (N/A)."""
        return sum(1 for a in self.analyses if not a.has_evidence)


class ReviewAnalyzer:
    """
    Phase 2 Engine: Analyzes product reviews against Critical Decision Factors.

    Workflow:
    1. Search for product-specific reviews
    2. Map review content to each Critical Decision Factor
    3. Assign evidence-based scores (1-10 or N/A)
    4. Generate simple Dutch summaries (Jip en Janneke style)

    Poka Yoke (Error-Proofing) Rules:
    - Score = "N/A" if no review mentions a factor
    - Score = "N/A" if evidence is unclear or contradictory
    - NEVER guess or invent scores
    - ALWAYS cite source URLs
    """

    def __init__(
        self,
        openai_api_key: str,
        search_service: SearchService,
        model: str = "gpt-4o",
        temperature: float = 0.1,
        min_evidence_threshold: int = 1,
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.search_service = search_service
        self.model = model
        self.temperature = temperature
        self.min_evidence_threshold = min_evidence_threshold

    def _build_review_queries(self, product_name: str) -> list[str]:
        """Build search queries for product reviews."""
        queries = []
        for template in SEARCH_TEMPLATES["reviews"]:
            queries.append(template.format(product=product_name))
        return queries

    def _format_search_results_for_llm(self, results: list[SearchResult]) -> str:
        """Format search results as context for LLM."""
        if not results:
            return "Geen reviews gevonden."

        formatted = []
        for r in results:
            formatted.append(f"""
---
Bron: {r.url}
Titel: {r.title}
Inhoud: {r.snippet}
---""")

        return "\n".join(formatted)

    def _analyze_with_llm(
        self,
        product_name: str,
        category: str,
        critical_factors: list[CriticalFactor],
        review_context: str,
    ) -> ProductAnalysisResult:
        """Use LLM to analyze reviews against Critical Decision Factors."""
        # Build factor list for prompt
        factor_list = "\n".join([f"- {cf.factor}" for cf in critical_factors])

        user_prompt = f"""
Product: {product_name}
Categorie: {category}

Critical Decision Factors om te analyseren:
{factor_list}

Review data:
{review_context}

Analyseer de reviews en geef voor ELKE factor:
1. Een score (1-10) OF "N/A" als er geen bewijs is
2. Het aantal keer dat de factor wordt genoemd
3. Een korte samenvatting (max 2 zinnen, Jip en Janneke stijl)
4. Het sentiment (positief/negatief/gemengd/onbekend)
5. De bron-URLs die het bewijs leveren

POKA YOKE REGELS (VERPLICHT):
- GEEN score geven zonder bewijs = "N/A"
- Tegenstrijdige meningen = "N/A" of sentiment "gemengd"
- Altijd bronnen citeren
- Simpele taal gebruiken (A2 niveau)

Geef ook een unit economics analyse:
- Is dit product zijn geld waard?
- Kort advies voor de koper
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS["review_analyzer"]},
                    {"role": "user", "content": user_prompt},
                ],
            )

            result_json = json.loads(response.choices[0].message.content)

            # Parse factor analyses
            analyses = []
            for analysis_data in result_json.get("analysis", []):
                # Validate score - must be N/A if no evidence
                score = analysis_data.get("score", "N/A")
                evidence_count = analysis_data.get("evidence_count", 0)
                
                # Poka Yoke: Force N/A if evidence is below threshold
                # and override summary to ensure consistency
                if isinstance(evidence_count, int) and evidence_count < self.min_evidence_threshold:
                    score = "N/A"
                    final_summary = "Niet genoeg bewijs gevonden om een score te geven."
                else:
                    final_summary = analysis_data.get("summary", "Geen informatie beschikbaar.")

                analyses.append(
                    FactorAnalysis(
                        factor=analysis_data.get("factor", "Onbekend"),
                        score=str(score),
                        evidence_count=evidence_count if isinstance(evidence_count, int) else 0,
                        summary=final_summary,
                        sentiment=analysis_data.get("sentiment", "onbekend"),
                        sources=analysis_data.get("sources", []),
                    )
                )

            # Ensure all critical factors are covered
            analyzed_factors = {a.factor.lower() for a in analyses}
            for cf in critical_factors:
                if cf.factor.lower() not in analyzed_factors:
                    analyses.append(
                        FactorAnalysis(
                            factor=cf.factor,
                            score="N/A",
                            evidence_count=0,
                            summary="Geen informatie gevonden in de reviews.",
                            sentiment="onbekend",
                            sources=[],
                        )
                    )

            # Parse unit economics
            ue_data = result_json.get("unit_economics", {})
            unit_economics = UnitEconomics(
                price_value_ratio=ue_data.get("price_value_ratio", "Onbekend"),
                recommendation=ue_data.get("recommendation", "Niet genoeg informatie voor advies."),
            )

            # Determine confidence level
            confidence = result_json.get("confidence_level", "gemiddeld")
            total_reviews = result_json.get("total_reviews_analyzed", 0)

            return ProductAnalysisResult(
                product_name=product_name,
                category=category,
                analyses=analyses,
                unit_economics=unit_economics,
                confidence_level=confidence,
                total_reviews_analyzed=total_reviews if isinstance(total_reviews, int) else 0,
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return self._create_error_result(
                product_name, category, critical_factors, "Analyse mislukt: ongeldige response"
            )
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return self._create_error_result(
                product_name, category, critical_factors, f"Analyse mislukt: {str(e)}"
            )

    def _create_error_result(
        self,
        product_name: str,
        category: str,
        critical_factors: list[CriticalFactor],
        error_message: str,
    ) -> ProductAnalysisResult:
        """Create a result with all N/A scores when analysis fails."""
        analyses = [
            FactorAnalysis(
                factor=cf.factor,
                score="N/A",
                evidence_count=0,
                summary="Analyse niet mogelijk.",
                sentiment="onbekend",
                sources=[],
            )
            for cf in critical_factors
        ]

        return ProductAnalysisResult(
            product_name=product_name,
            category=category,
            analyses=analyses,
            unit_economics=UnitEconomics(
                price_value_ratio="Onbekend",
                recommendation="Niet genoeg informatie beschikbaar.",
            ),
            confidence_level="laag",
            total_reviews_analyzed=0,
            error=error_message,
        )

    def analyze(
        self,
        product_name: str,
        category: str,
        critical_factors: list[CriticalFactor],
    ) -> ProductAnalysisResult:
        """
        Execute Phase 2: Product Analysis.

        Args:
            product_name: The specific product to analyze
            category: Product category from Phase 1
            critical_factors: List of CDFs from Phase 1

        Returns:
            ProductAnalysisResult with scores and evidence
        """
        logger.info("Starting Phase 2 product analysis")

        # Step 1: Build and execute review search queries
        queries = self._build_review_queries(product_name)
        logger.info(f"Executing {len(queries)} review search queries")

        all_results: list[SearchResult] = []
        for query in queries:
            results = self.search_service.search(query, num_results=5)
            all_results.extend(results)

        logger.info(f"Collected {len(all_results)} total review results")

        # Step 2: Handle no results case
        if not all_results:
            logger.warning("No review results found")
            return self._create_error_result(
                product_name,
                category,
                critical_factors,
                "Geen reviews gevonden. Probeer een andere productnaam.",
            )

        # Step 3: Format results and analyze with LLM
        review_context = self._format_search_results_for_llm(all_results)
        result = self._analyze_with_llm(product_name, category, critical_factors, review_context)
        result.raw_search_results = all_results

        logger.info(
            f"Phase 2 complete: Analyzed {len(result.analyses)} factors, "
            f"{result.factors_with_data} with data, {result.factors_without_data} N/A"
        )

        return result


def create_simplified_summary(
    client: OpenAI,
    analysis_result: ProductAnalysisResult,
    model: str = "gpt-4o",
) -> str:
    """
    Create an ultra-simple summary in Jip en Janneke style.
    CEFR A2 Dutch level.
    """
    # Build summary of scores
    score_summary = []
    for a in analysis_result.analyses:
        score_summary.append(f"- {a.factor}: {a.score} {a.score_emoji}")

    input_text = f"""
Product: {analysis_result.product_name}
Scores:
{chr(10).join(score_summary)}

Prijs-kwaliteit: {analysis_result.unit_economics.price_value_ratio}
Advies: {analysis_result.unit_economics.recommendation}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS["simplifier"]},
                {
                    "role": "user",
                    "content": f"Maak een heel simpele samenvatting (max 5 zinnen) van:\n{input_text}",
                },
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Simplification failed: {e}")
        return analysis_result.unit_economics.recommendation
