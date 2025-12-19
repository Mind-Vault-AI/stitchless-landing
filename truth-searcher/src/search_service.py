"""
Search Service Module - Abstraction layer for web search.
Supports SerpAPI and DuckDuckGo as fallback.
DMAIC Principle: Measure with multiple data sources for reliability.
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Standardized search result format."""

    title: str
    url: str
    snippet: str
    position: int
    source: str  # 'serpapi' or 'duckduckgo'

    def __repr__(self) -> str:
        return f"SearchResult(title='{self.title[:30]}...', url='{self.url}')"


class SearchProvider(ABC):
    """Abstract base class for search providers."""

    @abstractmethod
    def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        """Execute a search query and return results."""
        pass


class SerpAPIProvider(SearchProvider):
    """SerpAPI search provider - Primary source."""

    def __init__(self, api_key: str, country: str = "nl", language: str = "nl"):
        self.api_key = api_key
        self.country = country
        self.language = language
        self._client = None

    def _get_client(self):
        """Lazy load SerpAPI client."""
        if self._client is None:
            try:
                from serpapi import GoogleSearch

                self._client = GoogleSearch
            except ImportError:
                raise ImportError(
                    "serpapi package not installed. Run: pip install google-search-results"
                )
        return self._client

    def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        """Execute search via SerpAPI."""
        results = []

        try:
            GoogleSearch = self._get_client()
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "gl": self.country,
                "hl": self.language,
            }

            search = GoogleSearch(params)
            response = search.get_dict()

            organic_results = response.get("organic_results", [])

            for idx, item in enumerate(organic_results[:num_results]):
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        position=idx + 1,
                        source="serpapi",
                    )
                )

            logger.info(f"SerpAPI returned {len(results)} results for: {query}")

        except Exception as e:
            logger.error(f"SerpAPI search failed: {e}")
            raise

        return results


class DuckDuckGoProvider(SearchProvider):
    """DuckDuckGo search provider - Fallback source."""

    def __init__(self, region: str = "nl-nl"):
        self.region = region
        self._client = None

    def _get_client(self):
        """Lazy load DuckDuckGo client."""
        if self._client is None:
            try:
                from duckduckgo_search import DDGS

                self._client = DDGS
            except ImportError:
                raise ImportError(
                    "duckduckgo-search package not installed. Run: pip install duckduckgo-search"
                )
        return self._client

    def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        """Execute search via DuckDuckGo."""
        results = []

        try:
            DDGS = self._get_client()

            with DDGS() as ddgs:
                search_results = list(
                    ddgs.text(query, region=self.region, max_results=num_results)
                )

            for idx, item in enumerate(search_results):
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("href", ""),
                        snippet=item.get("body", ""),
                        position=idx + 1,
                        source="duckduckgo",
                    )
                )

            logger.info(f"DuckDuckGo returned {len(results)} results for: {query}")

        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            raise

        return results


class SearchService:
    """
    Unified search service with automatic fallback.
    Implements retry logic with exponential backoff.
    DMAIC Principle: Control through redundancy and error handling.
    """

    def __init__(
        self,
        serpapi_key: Optional[str] = None,
        country: str = "nl",
        language: str = "nl",
        max_retries: int = 3,
        base_delay: float = 1.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay

        # Initialize providers
        self.providers: list[SearchProvider] = []

        if serpapi_key:
            self.providers.append(SerpAPIProvider(serpapi_key, country, language))
            logger.info("SerpAPI provider initialized")

        # DuckDuckGo as fallback (always available, no API key needed)
        self.providers.append(DuckDuckGoProvider(region=f"{language}-{country}"))
        logger.info("DuckDuckGo provider initialized as fallback")

    def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        """
        Execute search with automatic fallback and retry logic.
        Returns empty list if all providers fail.
        """
        last_exception = None

        for provider in self.providers:
            for attempt in range(self.max_retries):
                try:
                    results = provider.search(query, num_results)
                    if results:
                        return results
                except Exception as e:
                    last_exception = e
                    delay = self.base_delay * (2**attempt)
                    logger.warning(
                        f"Search attempt {attempt + 1} failed for {provider.__class__.__name__}: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)

            logger.error(
                f"All retries exhausted for {provider.__class__.__name__}, trying next provider..."
            )

        logger.error(f"All search providers failed. Last exception: {last_exception}")
        return []

    def multi_search(
        self, queries: list[str], num_results_per_query: int = 5
    ) -> dict[str, list[SearchResult]]:
        """
        Execute multiple searches and aggregate results.
        Returns a dictionary mapping query -> results.
        """
        all_results = {}

        for query in queries:
            results = self.search(query, num_results_per_query)
            all_results[query] = results
            # Small delay between queries to avoid rate limiting
            time.sleep(0.5)

        return all_results

    def get_unique_urls(self, results: list[SearchResult]) -> list[str]:
        """Extract unique URLs from search results."""
        seen = set()
        unique = []
        for r in results:
            if r.url not in seen:
                seen.add(r.url)
                unique.append(r.url)
        return unique
