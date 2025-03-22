"""
Models for VC Research Engine

This module defines the Pydantic models for the research output schema.
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

# Company Info Models
class CompanyInfo(BaseModel):
    name: str
    tagline: str
    description: str
    website: str
    founded_year: int
    headquarters: str
    company_stage: str
    employee_count: int
    business_model: str
    revenue_model: str
    industry: str

# Market Analysis Models
class MarketSize(BaseModel):
    size: str
    year: int
    cagr: str
    description: str
    sources: List[str]

class MarketTrend(BaseModel):
    trend: str
    description: str

class MarketAnalysis(BaseModel):
    tam: MarketSize
    sam: MarketSize
    som: MarketSize
    market_trends: List[MarketTrend]

# Financial Metrics Models
class FundingRound(BaseModel):
    date: str
    round_type: str
    amount: str
    valuation: Optional[str] = None
    lead_investors: List[str]

class LastRound(BaseModel):
    date: str
    amount: str
    round_type: str
    lead_investors: List[str]

class Revenue(BaseModel):
    current_arr: str
    growth_rate: str
    burn_rate: str
    runway: str

class Valuation(BaseModel):
    current: str
    date: str
    multiple: str

class UnitEconomics(BaseModel):
    cac: str
    ltv: str
    ltv_cac_ratio: str
    gross_margin: str
    payback_period: str

class Funding(BaseModel):
    total_raised: str
    last_round: LastRound
    funding_history: List[FundingRound]
    notable_investors: List[str]

class FinancialMetrics(BaseModel):
    funding: Funding
    revenue: Revenue
    valuation: Valuation
    unit_economics: UnitEconomics

# Growth Metrics Models
class QuarterlyData(BaseModel):
    quarter: str
    revenue: str

class UserGrowth(BaseModel):
    current_users: str
    growth_rate: str
    description: str

class RevenueGrowth(BaseModel):
    description: str
    quarterly_data: List[QuarterlyData]

class KeyMetric(BaseModel):
    metric: str
    value: str
    growth: str

class DataPoint(BaseModel):
    date: str
    value: float

class PieDataPoint(BaseModel):
    name: str
    value: int

class Chart(BaseModel):
    title: str
    type: str
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    data_points: List[Union[DataPoint, PieDataPoint]]

class ChartData(BaseModel):
    user_growth_chart: Chart
    revenue_growth_chart: Chart
    market_comparison_chart: Chart

class GrowthMetrics(BaseModel):
    user_growth: UserGrowth
    revenue_growth: RevenueGrowth
    key_metrics: List[KeyMetric]
    chart_data: ChartData

# Competitive Landscape Models
class Competitor(BaseModel):
    name: str
    description: str
    funding: str
    strengths: List[str]
    weaknesses: List[str]

class IndirectCompetitor(BaseModel):
    name: str
    description: str
    funding: str

class CompanyComparison(BaseModel):
    name: str
    values: List[str]

class ComparisonChart(BaseModel):
    title: str
    categories: List[str]
    companies: List[CompanyComparison]

class CompetitiveLandscape(BaseModel):
    direct_competitors: List[Competitor]
    indirect_competitors: List[IndirectCompetitor]
    competitive_advantage: str
    comparison_chart: ComparisonChart

# Team Analysis Models
class Person(BaseModel):
    name: str
    role: str
    background: str
    linkedin: Optional[str] = None

class BoardMember(BaseModel):
    name: str
    role: str
    organization: str
    background: str

class Advisor(BaseModel):
    name: str
    role: str
    background: str

class TeamAnalysis(BaseModel):
    key_people: List[Person]
    board_members: List[BoardMember]
    advisors: List[Advisor]
    team_strength: str

# Product Analysis Models
class Feature(BaseModel):
    feature: str
    description: str

class Screenshot(BaseModel):
    title: str
    url: str
    description: str

class ProductAnalysis(BaseModel):
    product_description: str
    key_features: List[Feature]
    technology_stack: List[str]
    product_roadmap: str
    intellectual_property: str
    product_screenshots: List[Screenshot]

# Customer Analysis Models
class Client(BaseModel):
    name: str
    industry: str
    description: str

class CaseStudy(BaseModel):
    title: str
    client: str
    description: str
    results: str

class CustomerAnalysis(BaseModel):
    target_customers: str
    customer_demographics: str
    major_clients: List[Client]
    case_studies: List[CaseStudy]
    customer_acquisition: str
    customer_retention: str

# Risk Assessment Models
class Risk(BaseModel):
    risk: str
    description: str
    mitigation: str

class RiskAssessment(BaseModel):
    market_risks: List[Risk]
    competitive_risks: List[Risk]
    financial_risks: List[Risk]
    regulatory_risks: List[Risk]

# Investment Analysis Models
class ExitStrategy(BaseModel):
    strategy: str
    description: str
    potential_acquirers: Optional[List[str]] = None
    timeline: Optional[str] = None

class ComparableExit(BaseModel):
    company: str
    exit_type: str
    date: str
    amount: str
    acquirer: str
    multiple: str

class InvestmentAnalysis(BaseModel):
    investment_thesis: str
    potential_exit_strategies: List[ExitStrategy]
    comparable_exits: List[ComparableExit]
    investment_recommendation: str
    investment_highlights: List[str]
    investment_concerns: List[str]

# Media and News Models
class News(BaseModel):
    title: str
    source: str
    date: str
    url: str
    summary: str

class PressRelease(BaseModel):
    title: str
    date: str
    url: str
    summary: str

class SocialMedia(BaseModel):
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None

class MediaAndNews(BaseModel):
    recent_news: List[News]
    social_media: SocialMedia
    press_releases: List[PressRelease]

# Research Metadata Models
class Source(BaseModel):
    name: str
    url: str

class ResearchMetadata(BaseModel):
    research_date: str
    analyst: str
    sources: List[Source]
    last_updated: str

# Complete Research Output Model
class ResearchOutput(BaseModel):
    company_info: CompanyInfo
    market_analysis: MarketAnalysis
    financial_metrics: FinancialMetrics
    growth_metrics: GrowthMetrics
    competitive_landscape: CompetitiveLandscape
    team_analysis: TeamAnalysis
    product_analysis: ProductAnalysis
    customer_analysis: CustomerAnalysis
    risk_assessment: RiskAssessment
    investment_analysis: InvestmentAnalysis
    media_and_news: MediaAndNews
    research_metadata: ResearchMetadata
