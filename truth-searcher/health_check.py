"""
Health Check Module for Truth Searcher
Provides comprehensive health monitoring for SLA compliance

Target SLA: 99.9% (max 43.8 min downtime/month)
Response time target: <2s (95th percentile)
Error rate target: <0.1%
"""

import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    service: str
    status: str  # "healthy", "degraded", "unhealthy"
    response_time_ms: float
    message: str
    timestamp: str
    details: Optional[Dict] = None


class HealthChecker:
    """Performs health checks on all critical services."""

    def __init__(self):
        """Initialize health checker."""
        self.checks: List[HealthCheckResult] = []

    def check_openai_api(self) -> HealthCheckResult:
        """Check OpenAI API connectivity."""
        start_time = time.time()
        service = "OpenAI API"
        
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                return HealthCheckResult(
                    service=service,
                    status="unhealthy",
                    response_time_ms=0,
                    message="OpenAI API key not configured",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={"error": "Missing API key"}
                )
            
            # Try to import and initialize OpenAI client
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            # Make a minimal API call to verify connectivity
            # Using a very small completion to minimize cost
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.choices:
                return HealthCheckResult(
                    service=service,
                    status="healthy",
                    response_time_ms=response_time_ms,
                    message="OpenAI API is responding",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={"model": "gpt-3.5-turbo"}
                )
            else:
                return HealthCheckResult(
                    service=service,
                    status="degraded",
                    response_time_ms=response_time_ms,
                    message="OpenAI API returned empty response",
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                
        except ImportError as e:
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message="OpenAI library not available",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"error": str(e)}
            )
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"OpenAI API error: {str(e)[:100]}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"error": str(e)}
            )

    def check_serpapi(self) -> HealthCheckResult:
        """Check SerpAPI connectivity."""
        start_time = time.time()
        service = "SerpAPI"
        
        try:
            api_key = os.getenv("SERPAPI_KEY")
            
            if not api_key:
                # SerpAPI is optional, so this is degraded not unhealthy
                return HealthCheckResult(
                    service=service,
                    status="degraded",
                    response_time_ms=0,
                    message="SerpAPI key not configured (optional)",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={"note": "Will fallback to DuckDuckGo"}
                )
            
            # Try to import serpapi
            from serpapi import GoogleSearch
            
            # Make a minimal search query to verify connectivity
            search = GoogleSearch({
                "q": "test",
                "api_key": api_key,
                "num": 1
            })
            result = search.get_dict()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            if "error" in result:
                return HealthCheckResult(
                    service=service,
                    status="unhealthy",
                    response_time_ms=response_time_ms,
                    message=f"SerpAPI error: {result['error']}",
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={"error": result["error"]}
                )
            
            return HealthCheckResult(
                service=service,
                status="healthy",
                response_time_ms=response_time_ms,
                message="SerpAPI is responding",
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            
        except ImportError:
            return HealthCheckResult(
                service=service,
                status="degraded",
                response_time_ms=(time.time() - start_time) * 1000,
                message="SerpAPI library not available",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"note": "Will fallback to DuckDuckGo"}
            )
        except Exception as e:
            logger.error(f"SerpAPI health check failed: {e}")
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"SerpAPI error: {str(e)[:100]}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"error": str(e)}
            )

    def check_duckduckgo(self) -> HealthCheckResult:
        """Check DuckDuckGo search connectivity."""
        start_time = time.time()
        service = "DuckDuckGo"
        
        try:
            from duckduckgo_search import DDGS
            
            # Make a minimal search query
            with DDGS() as ddgs:
                results = list(ddgs.text("test", max_results=1))
            
            response_time_ms = (time.time() - start_time) * 1000
            
            if results:
                return HealthCheckResult(
                    service=service,
                    status="healthy",
                    response_time_ms=response_time_ms,
                    message="DuckDuckGo is responding",
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
            else:
                return HealthCheckResult(
                    service=service,
                    status="degraded",
                    response_time_ms=response_time_ms,
                    message="DuckDuckGo returned no results",
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                
        except ImportError:
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message="DuckDuckGo library not available",
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        except Exception as e:
            logger.error(f"DuckDuckGo health check failed: {e}")
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"DuckDuckGo error: {str(e)[:100]}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"error": str(e)}
            )

    def check_application(self) -> HealthCheckResult:
        """Check application basic functionality."""
        start_time = time.time()
        service = "Application"
        
        try:
            # Check if we can import core modules
            from src.config import AppConfig
            from src.search_service import SearchService
            from src.market_research import MarketResearch
            from src.review_analyzer import ReviewAnalyzer
            
            # Try to initialize config
            config = AppConfig()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            return HealthCheckResult(
                service=service,
                status="healthy",
                response_time_ms=response_time_ms,
                message="Application modules are operational",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"model": config.model_name}
            )
            
        except Exception as e:
            logger.error(f"Application health check failed: {e}")
            return HealthCheckResult(
                service=service,
                status="unhealthy",
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Application error: {str(e)[:100]}",
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={"error": str(e)}
            )

    def run_all_checks(self) -> Dict:
        """Run all health checks and return consolidated status."""
        start_time = time.time()
        
        self.checks = [
            self.check_application(),
            self.check_openai_api(),
            self.check_serpapi(),
            self.check_duckduckgo(),
        ]
        
        total_time_ms = (time.time() - start_time) * 1000
        
        # Determine overall status
        critical_services = ["Application", "OpenAI API"]
        critical_checks = [c for c in self.checks if c.service in critical_services]
        critical_unhealthy = any(c.status == "unhealthy" for c in critical_checks)
        
        if critical_unhealthy:
            # Critical services unhealthy
            overall_status = "unhealthy"
        elif any(c.status == "unhealthy" for c in self.checks):
            overall_status = "degraded"
        elif any(c.status == "degraded" for c in self.checks):
            overall_status = "degraded"
        else:
            overall_status = "healthy"
        
        # Calculate metrics
        avg_response_time = sum(c.response_time_ms for c in self.checks) / len(self.checks)
        
        return {
            "status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_check_time_ms": round(total_time_ms, 2),
            "average_response_time_ms": round(avg_response_time, 2),
            "checks": [
                {
                    "service": check.service,
                    "status": check.status,
                    "response_time_ms": round(check.response_time_ms, 2),
                    "message": check.message,
                    "details": check.details
                }
                for check in self.checks
            ],
            "sla_metrics": {
                "target_sla": "99.9%",
                "target_response_time_ms": 2000,
                "target_error_rate": "0.1%"
            }
        }


def get_health_status() -> Dict:
    """
    Get current health status of all services.
    
    Returns:
        Dict: Health status information including all service checks
    """
    checker = HealthChecker()
    return checker.run_all_checks()


if __name__ == "__main__":
    # For testing
    import json
    
    logging.basicConfig(level=logging.INFO)
    
    result = get_health_status()
    print(json.dumps(result, indent=2))
