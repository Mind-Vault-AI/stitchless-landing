"""
The Truth Searcher - Zero-Hallucination Product Research MVP
Main Streamlit Application

DMAIC Philosophy: Define, Measure, Analyze, Improve, Control
1W5H Approach: What, Why, Who, Where, When, How

Author: Truth Searcher Team
Version: 1.0.0
"""

import json
import logging
import os
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_check import get_health_status
from src.config import UI_MESSAGES, AppConfig
from src.market_research import MarketResearch
from src.pdf_generator import generate_pdf_report, generate_simple_text_report
from src.review_analyzer import ProductAnalysisResult, ReviewAnalyzer, create_simplified_summary
from src.search_service import SearchService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "research_result" not in st.session_state:
        st.session_state.research_result = None
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "simplified_summary" not in st.session_state:
        st.session_state.simplified_summary = None
    if "current_phase" not in st.session_state:
        st.session_state.current_phase = None


def check_api_keys() -> tuple[bool, str]:
    """Check if required API keys are configured."""
    openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_api_key")

    if not openai_key:
        return False, "OpenAI API sleutel ontbreekt"

    return True, ""


def create_services(config: AppConfig) -> tuple[SearchService, MarketResearch, ReviewAnalyzer]:
    """Initialize all services with configuration."""
    # Get API keys from environment or session state
    openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_api_key", "")
    serpapi_key = os.getenv("SERPAPI_KEY") or st.session_state.get("serpapi_key")

    # Initialize search service
    search_service = SearchService(
        serpapi_key=serpapi_key,
        country=config.search_country,
        language=config.search_language,
    )

    # Initialize market research
    market_research = MarketResearch(
        openai_api_key=openai_key,
        search_service=search_service,
        model=config.model_name,
        temperature=config.temperature,
    )

    # Initialize review analyzer
    review_analyzer = ReviewAnalyzer(
        openai_api_key=openai_key,
        search_service=search_service,
        model=config.model_name,
        temperature=config.temperature,
        min_evidence_threshold=config.min_evidence_threshold,
    )

    return search_service, market_research, review_analyzer


def render_sidebar():
    """Render the sidebar with settings and info."""
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/search--v1.png",
            width=64,
        )
        st.title("Instellingen")

        # API Key inputs (if not in environment)
        if not os.getenv("OPENAI_API_KEY"):
            st.text_input(
                "OpenAI API Key",
                type="password",
                key="openai_api_key",
                help="Vereist voor de analyse",
            )

        if not os.getenv("SERPAPI_KEY"):
            st.text_input(
                "SerpAPI Key (optioneel)",
                type="password",
                key="serpapi_key",
                help="Voor betere zoekresultaten. Zonder dit wordt DuckDuckGo gebruikt.",
            )

        st.divider()

        st.subheader("ℹ️ Hoe werkt het?")
        st.markdown("""
        1. **Fase 1**: We onderzoeken wat écht belangrijk is voor dit type product
        2. **Fase 2**: We zoeken reviews en scoren op die punten
        3. **Fase 3**: Je krijgt een helder rapport

        **Geen verzinsels!**
        Als we iets niet weten, zeggen we "N/A" (geen data).
        """)

        st.divider()

        st.caption("Gemaakt met ❤️ voor eerlijk onderzoek")


def render_results_table(analysis_result: ProductAnalysisResult):
    """Render the results as a styled dataframe."""
    # Build dataframe
    data = []
    for analysis in analysis_result.analyses:
        data.append({
            UI_MESSAGES["table_header_factor"]: analysis.factor,
            UI_MESSAGES["table_header_score"]: f"{analysis.score} {analysis.score_emoji}",
            UI_MESSAGES["table_header_explanation"]: analysis.summary,
            "Sentiment": analysis.sentiment,
            "Bronnen": len(analysis.sources),
        })

    df = pd.DataFrame(data)

    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            UI_MESSAGES["table_header_factor"]: st.column_config.TextColumn(
                UI_MESSAGES["table_header_factor"],
                width="medium",
            ),
            UI_MESSAGES["table_header_score"]: st.column_config.TextColumn(
                UI_MESSAGES["table_header_score"],
                width="small",
            ),
            UI_MESSAGES["table_header_explanation"]: st.column_config.TextColumn(
                UI_MESSAGES["table_header_explanation"],
                width="large",
            ),
            "Sentiment": st.column_config.TextColumn(
                "Gevoel",
                width="small",
            ),
            "Bronnen": st.column_config.NumberColumn(
                "# Bronnen",
                width="small",
            ),
        },
    )


def render_legend():
    """Render the score legend."""
    with st.expander(UI_MESSAGES["legend_title"], expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.success(UI_MESSAGES["legend_good"])
        with col2:
            st.warning(UI_MESSAGES["legend_ok"])
        with col3:
            st.error(UI_MESSAGES["legend_bad"])
        with col4:
            st.info(UI_MESSAGES["legend_na"])


def render_confidence_badge(confidence: str):
    """Render confidence level badge."""
    if confidence == "hoog":
        st.success(UI_MESSAGES["confidence_high"])
    elif confidence == "gemiddeld":
        st.warning(UI_MESSAGES["confidence_medium"])
    else:
        st.error(UI_MESSAGES["confidence_low"])


def render_unit_economics(analysis_result: ProductAnalysisResult):
    """Render the unit economics section."""
    st.subheader("💰 Prijs-Kwaliteit Analyse")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Verhouding",
            value=analysis_result.unit_economics.price_value_ratio,
        )
    with col2:
        st.info(f"💡 **Advies:** {analysis_result.unit_economics.recommendation}")


def render_sources(analysis_result: ProductAnalysisResult):
    """Render source URLs."""
    with st.expander("🔗 Bekijk bronnen", expanded=False):
        all_sources = set()
        for analysis in analysis_result.analyses:
            all_sources.update(analysis.sources)

        if all_sources:
            for source in all_sources:
                st.markdown(f"- [{source[:50]}...]({source})")
        else:
            st.info("Geen specifieke bronnen beschikbaar.")


def run_research(query: str, config: AppConfig):
    """Execute the full research pipeline."""
    try:
        # Initialize services
        search_service, market_research, review_analyzer = create_services(config)

        # Get OpenAI client for simplified summary
        from openai import OpenAI

        openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("openai_api_key", "")
        openai_client = OpenAI(api_key=openai_key)

        # === PHASE 1: Market Research ===
        st.session_state.current_phase = 1
        phase1_placeholder = st.empty()

        with phase1_placeholder.container():
            with st.spinner(UI_MESSAGES["phase1_status"].format(category="dit product")):
                research_result = market_research.research(query)
                st.session_state.research_result = research_result

        if research_result.error:
            st.error(f"⚠️ Fase 1 mislukt: {research_result.error}")
            return

        # Show Phase 1 results briefly
        phase1_placeholder.success(
            f"✅ Categorie gevonden: **{research_result.category}** | "
            f"Belangrijke factoren: {len(research_result.critical_factors)}"
        )

        # === PHASE 2: Product Analysis ===
        st.session_state.current_phase = 2
        phase2_placeholder = st.empty()

        with phase2_placeholder.container():
            with st.spinner(UI_MESSAGES["phase2_status"].format(product=query)):
                analysis_result = review_analyzer.analyze(
                    product_name=query,
                    category=research_result.category,
                    critical_factors=research_result.critical_factors,
                )
                st.session_state.analysis_result = analysis_result

        if analysis_result.error:
            st.warning(f"⚠️ Let op: {analysis_result.error}")

        phase2_placeholder.success(
            f"✅ Analyse compleet | "
            f"Reviews: {analysis_result.total_reviews_analyzed} | "
            f"Factoren met data: {analysis_result.factors_with_data}/{len(analysis_result.analyses)}"
        )

        # === PHASE 3: Generate Summary ===
        st.session_state.current_phase = 3

        with st.spinner(UI_MESSAGES["phase3_status"]):
            simplified_summary = create_simplified_summary(
                client=openai_client,
                analysis_result=analysis_result,
                model=config.model_name,
            )
            st.session_state.simplified_summary = simplified_summary

        st.session_state.current_phase = None

    except Exception as e:
        logger.exception("Research pipeline failed")
        st.error(f"❌ Er ging iets mis: {str(e)}")
        st.session_state.current_phase = None


def render_health_check():
    """Render health check page with JSON output."""
    st.set_page_config(
        page_title="Health Check",
        page_icon="🏥",
        layout="wide",
    )
    
    st.title("🏥 Health Check")
    st.markdown("*System health status and monitoring*")
    
    with st.spinner("Running health checks..."):
        health_status = get_health_status()
    
    # Display overall status
    status = health_status["status"]
    if status == "healthy":
        st.success(f"✅ System Status: **{status.upper()}**")
    elif status == "degraded":
        st.warning(f"⚠️ System Status: **{status.upper()}**")
    else:
        st.error(f"❌ System Status: **{status.upper()}**")
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Check Time", f"{health_status['total_check_time_ms']:.0f}ms")
    with col2:
        st.metric("Avg Response Time", f"{health_status['average_response_time_ms']:.0f}ms")
    with col3:
        target = health_status['sla_metrics']['target_response_time_ms']
        st.metric("Target Response Time", f"<{target}ms")
    
    st.divider()
    
    # Display individual service checks
    st.subheader("Service Health Checks")
    
    for check in health_status["checks"]:
        with st.expander(f"{check['service']} - {check['status'].upper()}", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                if check['status'] == "healthy":
                    st.success(check['message'])
                elif check['status'] == "degraded":
                    st.warning(check['message'])
                else:
                    st.error(check['message'])
            with col2:
                st.metric("Response Time", f"{check['response_time_ms']:.0f}ms")
            
            if check.get('details'):
                st.json(check['details'])
    
    st.divider()
    
    # Display SLA targets
    st.subheader("SLA Targets")
    sla = health_status['sla_metrics']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Target SLA:** {sla['target_sla']}")
    with col2:
        st.info(f"**Target Response:** <{sla['target_response_time_ms']}ms")
    with col3:
        st.info(f"**Target Error Rate:** <{sla['target_error_rate']}")
    
    st.divider()
    
    # Display raw JSON
    with st.expander("Raw JSON Output", expanded=False):
        st.json(health_status)
    
    st.caption(f"Last updated: {health_status['timestamp']}")


def main():
    """Main application entry point."""
    # Check if health check is requested via query params
    query_params = st.query_params
    if "health" in query_params or query_params.get("mode") == "health":
        render_health_check()
        return
    
    # Page config
    st.set_page_config(
        page_title="De Waarheidszoeker",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize
    init_session_state()
    config = AppConfig()

    # Render sidebar
    render_sidebar()

    # Main content
    st.title(UI_MESSAGES["title"])
    st.markdown(f"*{UI_MESSAGES['subtitle']}*")

    # Check API keys
    api_ok, api_error = check_api_keys()

    if not api_ok:
        st.warning(f"⚠️ {api_error}. Voer je API sleutel in via de zijbalk.")

    # Search input
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input(
            UI_MESSAGES["input_label"],
            placeholder=UI_MESSAGES["input_placeholder"],
            label_visibility="collapsed",
        )

    with col2:
        search_button = st.button(
            UI_MESSAGES["button_search"],
            type="primary",
            use_container_width=True,
            disabled=not api_ok,
        )

    # Execute research
    if search_button and query:
        # Clear previous results
        st.session_state.research_result = None
        st.session_state.analysis_result = None
        st.session_state.simplified_summary = None

        run_research(query, config)

    # Display results
    if st.session_state.analysis_result:
        analysis_result = st.session_state.analysis_result

        st.divider()

        # Header with product info
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.subheader(f"📊 Resultaten voor: {analysis_result.product_name}")
            st.caption(f"Categorie: {analysis_result.category}")

        with col2:
            render_confidence_badge(analysis_result.confidence_level)

        with col3:
            st.metric("Reviews", analysis_result.total_reviews_analyzed)

        # Simplified summary
        if st.session_state.simplified_summary:
            st.info(f"📝 **Samenvatting:** {st.session_state.simplified_summary}")

        # Results table
        st.subheader("📋 Scores")
        render_results_table(analysis_result)
        render_legend()

        # Unit economics
        render_unit_economics(analysis_result)

        # Sources
        render_sources(analysis_result)

        st.divider()

        # Download buttons
        col1, col2 = st.columns(2)

        with col1:
            try:
                pdf_bytes = generate_pdf_report(
                    analysis_result,
                    st.session_state.simplified_summary,
                )
                st.download_button(
                    label=UI_MESSAGES["download_pdf"],
                    data=pdf_bytes,
                    file_name=f"waarheidszoeker_{analysis_result.product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    type="primary",
                )
            except ImportError:
                st.warning("PDF generatie niet beschikbaar. Installeer: pip install reportlab")
            except Exception as e:
                st.error(f"PDF generatie mislukt: {e}")

        with col2:
            text_report = generate_simple_text_report(
                analysis_result,
                st.session_state.simplified_summary,
            )
            st.download_button(
                label="📄 Download Tekst Rapport",
                data=text_report,
                file_name=f"waarheidszoeker_{analysis_result.product_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
            )

    # Footer
    st.divider()
    st.caption(
        "⚠️ Dit onderzoek is gebaseerd op publiek beschikbare informatie. "
        "Controleer altijd meerdere bronnen voordat je een aankoopbeslissing neemt. "
        "Scores zijn 'N/A' als er niet genoeg bewijs is - we gissen nooit!"
    )


if __name__ == "__main__":
    main()
