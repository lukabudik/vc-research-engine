"""
VC Research Engine Specialized Agents

This package contains specialized agents for different aspects of startup research.
"""

from vc_agents.agents.company_agent import company_overview_agent, get_company_overview
from vc_agents.agents.people_agent import key_people_agent, get_team_analysis
from vc_agents.agents.market_agent import market_analysis_agent, get_market_analysis
from vc_agents.agents.competitor_agent import competitor_analysis_agent, get_competitor_analysis
from vc_agents.agents.metrics_agent import (
    growth_metrics_agent, get_growth_metrics,
    financial_metrics_agent, get_financial_metrics,
    product_analysis_agent, get_product_analysis,
    customer_analysis_agent, get_customer_analysis,
    risk_assessment_agent, get_risk_assessment,
    investment_analysis_agent, get_investment_analysis,
    media_news_agent, get_media_news,
    research_metadata_agent, get_research_metadata
)

__all__ = [
    'company_overview_agent',
    'get_company_overview',
    'key_people_agent',
    'get_team_analysis',
    'market_analysis_agent',
    'get_market_analysis',
    'competitor_analysis_agent',
    'get_competitor_analysis',
    'growth_metrics_agent',
    'get_growth_metrics',
    'financial_metrics_agent',
    'get_financial_metrics',
    'product_analysis_agent',
    'get_product_analysis',
    'customer_analysis_agent',
    'get_customer_analysis',
    'risk_assessment_agent',
    'get_risk_assessment',
    'investment_analysis_agent',
    'get_investment_analysis',
    'media_news_agent',
    'get_media_news',
    'research_metadata_agent',
    'get_research_metadata'
]
