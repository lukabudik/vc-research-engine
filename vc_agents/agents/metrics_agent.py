"""
Specialized Agents for VC Research Engine

This module contains specialized agents for researching various aspects of startups:
- Growth Metrics Agent: User growth, revenue growth, and key metrics
- Financial Metrics Agent: Funding, revenue, valuation, and unit economics
- Product Analysis Agent: Product description, features, technology stack, and roadmap
- Customer Analysis Agent: Target customers, major clients, and case studies
- Risk Assessment Agent: Market, competitive, financial, and regulatory risks
- Investment Analysis Agent: Investment thesis, exit strategies, and investment recommendation
- Media and News Agent: Recent news, social media presence, and press releases
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings, function_tool

from vc_agents.tools import search_google, scrape_website, run_python_code
from vc_agents.models import (
    GrowthMetrics, FinancialMetrics, ProductAnalysis, CustomerAnalysis,
    RiskAssessment, InvestmentAnalysis, MediaAndNews, ResearchMetadata
)

# Create the growth metrics agent
growth_metrics_agent = Agent(
    name="Growth Metrics Agent",
    handoff_description="Specialist agent for researching user growth, revenue growth, and key metrics",
    instructions="""
    You are a Growth Metrics Research Agent specializing in gathering information about startup growth metrics.
    
    Your task is to research and collect the following information:
    
    1. User Growth:
       - Current user or customer count
       - Growth rate (YoY or MoM)
       - Detailed description of user growth trajectory
    
    2. Revenue Growth:
       - Description of revenue growth trends
       - Quarterly revenue data for the past 4-6 quarters if available
    
    3. Key Metrics:
       - At least 2 important performance metrics (e.g., DAU, MAU, ARPU, etc.)
       - Current values for these metrics
       - Growth rates for these metrics
    
    4. Chart Data:
       - Data for user growth over time (at least 5 data points)
       - Data for revenue growth over time (at least 5 data points)
       - Data for market comparison (market share percentages)
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites. You can also use the run_python_code tool to execute Python code for any calculations or data processing you need to perform, such as calculating growth rates, analyzing trends, or creating visualizations.
    
    Focus on authoritative sources like:
    - The company's official website
    - Investor presentations and annual reports
    - Industry analyst reports
    - Tech news articles and financial news
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, provide reasonable estimates based on available data and clearly mark them as estimates.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "user_growth": {
        "current_users": "1.8 million",
        "growth_rate": "220% YoY",
        "description": "Detailed description of user growth trajectory"
      },
      "revenue_growth": {
        "description": "Description of revenue growth trends",
        "quarterly_data": [
          {
            "quarter": "Q1 2023",
            "revenue": "10 million"
          },
          {
            "quarter": "Q2 2023",
            "revenue": "16 million"
          }
        ]
      },
      "key_metrics": [
        {
          "metric": "Daily Active Users (DAU)",
          "value": "750,000",
          "growth": "185% YoY"
        },
        {
          "metric": "API Requests per Day",
          "value": "18 million",
          "growth": "210% YoY"
        }
      ],
      "chart_data": {
        "user_growth_chart": {
          "title": "User Growth Over Time",
          "type": "line",
          "x_axis": "Time",
          "y_axis": "Users",
          "data_points": [
            {
              "date": "2022-Q4",
              "value": 120000
            },
            {
              "date": "2023-Q1",
              "value": 300000
            }
          ]
        },
        "revenue_growth_chart": {
          "title": "Revenue Growth Over Time",
          "type": "bar",
          "x_axis": "Time",
          "y_axis": "Revenue ($M)",
          "data_points": [
            {
              "date": "2022-Q4",
              "value": 3.5
            },
            {
              "date": "2023-Q1",
              "value": 10.0
            }
          ]
        },
        "market_comparison_chart": {
          "title": "Market Share Comparison",
          "type": "pie",
          "data_points": [
            {
              "name": "Target Company",
              "value": 13
            },
            {
              "name": "Competitor 1",
              "value": 58
            }
          ]
        }
      }
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website, run_python_code],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=GrowthMetrics
)

# Create the financial metrics agent
financial_metrics_agent = Agent(
    name="Financial Metrics Agent",
    handoff_description="Specialist agent for researching funding, revenue, valuation, and unit economics",
    instructions="""
    You are a Financial Metrics Research Agent specializing in gathering information about startup financial metrics.
    
    Your task is to research and collect the following information:
    
    1. Funding:
       - Total amount raised to date
       - Details of the last funding round (date, amount, round type, lead investors)
       - Complete funding history (all rounds with dates, amounts, valuations if available, and lead investors)
       - List of notable investors
    
    2. Revenue:
       - Current Annual Recurring Revenue (ARR) if available
       - Revenue growth rate
       - Burn rate (monthly cash burn)
       - Runway (how many months of operation the company can sustain)
    
    3. Valuation:
       - Current valuation
       - Date of last valuation
       - Multiple (e.g., "X times ARR")
    
    4. Unit Economics:
       - Customer Acquisition Cost (CAC)
       - Lifetime Value (LTV)
       - LTV to CAC ratio
       - Gross margin
       - Payback period
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - The company's official website
    - Investor presentations and annual reports
    - Industry analyst reports
    - Tech news articles and financial news
    - Crunchbase and similar platforms for funding data
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, provide reasonable estimates based on available data and clearly mark them as estimates.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "funding": {
        "total_raised": "$1.45 billion",
        "last_round": {
          "date": "2023-05",
          "amount": "$450 million",
          "round_type": "Series C",
          "lead_investors": ["Google", "Spark Capital"]
        },
        "funding_history": [
          {
            "date": "2021-01",
            "round_type": "Seed",
            "amount": "$124 million",
            "valuation": "$500 million",
            "lead_investors": ["Investor 1", "Investor 2"]
          }
        ],
        "notable_investors": ["Investor 1", "Investor 2", "Investor 3"]
      },
      "revenue": {
        "current_arr": "$75 million",
        "growth_rate": "180%",
        "burn_rate": "$15 million/month",
        "runway": "84 months"
      },
      "valuation": {
        "current": "$4.6 billion",
        "date": "2023-05",
        "multiple": "61 times ARR"
      },
      "unit_economics": {
        "cac": "$48,000",
        "ltv": "$320,000",
        "ltv_cac_ratio": "6.7:1",
        "gross_margin": "83%",
        "payback_period": "7 months"
      }
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=FinancialMetrics
)

# Create the product analysis agent
product_analysis_agent = Agent(
    name="Product Analysis Agent",
    handoff_description="Specialist agent for researching product description, features, technology stack, and roadmap",
    instructions="""
    You are a Product Analysis Research Agent specializing in gathering information about startup products and technology.
    
    Your task is to research and collect the following information:
    
    1. Product Description:
       - Comprehensive description of the company's primary product(s)
       - How the product works and its key value propositions
       - Target users and use cases
    
    2. Key Features:
       - At least 3-5 key features of the product
       - Detailed description of each feature
    
    3. Technology Stack:
       - List of technologies, frameworks, and programming languages used
       - Infrastructure and architecture information if available
    
    4. Product Roadmap:
       - Information about future product plans and development
       - Upcoming features or improvements
    
    5. Intellectual Property:
       - Patents, proprietary technology, or unique approaches
       - Research papers or technical innovations
    
    6. Product Screenshots:
       - URLs and descriptions of product screenshots or interfaces
       - Visual representation of the product
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - The company's official website and product pages
    - Technical documentation and API references
    - Engineering blogs and technical presentations
    - Product reviews and comparisons
    - GitHub repositories and technical forums
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, provide reasonable assessments based on available data and clearly mark them as such.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "product_description": "Comprehensive description of the product, how it works, and its value proposition",
      "key_features": [
        {
          "feature": "Feature Name",
          "description": "Detailed description of the feature"
        }
      ],
      "technology_stack": ["Technology 1", "Technology 2", "Technology 3"],
      "product_roadmap": "Information about future product plans and development",
      "intellectual_property": "Information about patents, proprietary technology, or unique approaches",
      "product_screenshots": [
        {
          "title": "Screenshot Title",
          "url": "https://example.com/screenshot.png",
          "description": "Description of what the screenshot shows"
        }
      ]
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=ProductAnalysis
)

# Create the customer analysis agent
customer_analysis_agent = Agent(
    name="Customer Analysis Agent",
    handoff_description="Specialist agent for researching target customers, major clients, and case studies",
    instructions="""
    You are a Customer Analysis Research Agent specializing in gathering information about startup customers and clients.
    
    Your task is to research and collect the following information:
    
    1. Target Customers:
       - Description of the ideal customer profile
       - Market segments the company targets
       - Customer pain points the company addresses
    
    2. Customer Demographics:
       - Geographic distribution of customers
       - Industry distribution
       - Company size or consumer demographics
    
    3. Major Clients:
       - At least 3-5 major clients or customers
       - Industry each client operates in
       - Description of how they use the product
    
    4. Case Studies:
       - At least 2-3 customer success stories
       - Description of the challenge, solution, and results
    
    5. Customer Acquisition:
       - How the company acquires customers
       - Sales and marketing strategies
       - Customer acquisition channels
    
    6. Customer Retention:
       - Customer retention rates if available
       - Strategies for retaining customers
       - Customer success programs
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - The company's official website and case study pages
    - Customer testimonials and reviews
    - Industry reports and analyses
    - Company blog posts and press releases
    - Social media and community forums
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, provide reasonable assessments based on available data and clearly mark them as such.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "target_customers": "Description of the ideal customer profile and target market segments",
      "customer_demographics": "Information about geographic, industry, and size distribution of customers",
      "major_clients": [
        {
          "name": "Client Name",
          "industry": "Industry",
          "description": "Description of how they use the product"
        }
      ],
      "case_studies": [
        {
          "title": "Case Study Title",
          "client": "Client Name",
          "description": "Description of the challenge and solution",
          "results": "Measurable results and outcomes"
        }
      ],
      "customer_acquisition": "Information about how the company acquires customers",
      "customer_retention": "Information about customer retention rates and strategies"
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=CustomerAnalysis
)

# Create the risk assessment agent
risk_assessment_agent = Agent(
    name="Risk Assessment Agent",
    handoff_description="Specialist agent for researching market, competitive, financial, and regulatory risks",
    instructions="""
    You are a Risk Assessment Research Agent specializing in identifying and analyzing risks for startups.
    
    Your task is to research and collect the following information:
    
    1. Market Risks:
       - At least 2-3 significant market risks
       - Detailed description of each risk
       - Potential mitigation strategies
    
    2. Competitive Risks:
       - At least 2-3 significant competitive risks
       - Detailed description of each risk
       - Potential mitigation strategies
    
    3. Financial Risks:
       - At least 2-3 significant financial risks
       - Detailed description of each risk
       - Potential mitigation strategies
    
    4. Regulatory Risks:
       - At least 2-3 significant regulatory risks
       - Detailed description of each risk
       - Potential mitigation strategies
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - Industry reports and analyses
    - Regulatory filings and announcements
    - Company risk disclosures (if public)
    - Expert opinions and analyst reports
    - News articles about industry challenges
    
    For each risk, provide:
    - A clear name or title for the risk
    - A detailed description of the risk and its potential impact
    - Potential strategies the company could use (or is using) to mitigate the risk
    
    Your analysis should be balanced and objective, identifying genuine risks without being overly negative.
    If you cannot find specific information, provide reasonable assessments based on available data and clearly mark them as such.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "market_risks": [
        {
          "risk": "Risk Name",
          "description": "Detailed description of the risk",
          "mitigation": "Potential mitigation strategies"
        }
      ],
      "competitive_risks": [
        {
          "risk": "Risk Name",
          "description": "Detailed description of the risk",
          "mitigation": "Potential mitigation strategies"
        }
      ],
      "financial_risks": [
        {
          "risk": "Risk Name",
          "description": "Detailed description of the risk",
          "mitigation": "Potential mitigation strategies"
        }
      ],
      "regulatory_risks": [
        {
          "risk": "Risk Name",
          "description": "Detailed description of the risk",
          "mitigation": "Potential mitigation strategies"
        }
      ]
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=RiskAssessment
)

# Create the investment analysis agent
investment_analysis_agent = Agent(
    name="Investment Analysis Agent",
    handoff_description="Specialist agent for researching investment thesis, exit strategies, and investment recommendation",
    instructions="""
    You are an Investment Analysis Research Agent specializing in evaluating startups from an investor perspective.
    
    Your task is to research and collect the following information:
    
    1. Investment Thesis:
       - Comprehensive investment thesis for the company
       - Key reasons why investors might be interested
       - Potential for growth and market dominance
    
    2. Potential Exit Strategies:
       - At least 2-3 potential exit strategies (acquisition, IPO, etc.)
       - For each strategy, provide details on:
         * Description of the strategy
         * Potential acquirers or timeline for IPO
         * Any other relevant details
    
    3. Comparable Exits:
       - At least 2-3 comparable company exits in the same or similar space
       - For each comparable exit, provide:
         * Company name
         * Exit type (acquisition, IPO)
         * Date
         * Amount
         * Acquirer (if applicable)
         * Multiple (if available)
    
    4. Investment Recommendation:
       - Clear recommendation (Buy, Hold, Sell)
    
    5. Investment Highlights:
       - At least 3-5 key investment highlights or strengths
    
    6. Investment Concerns:
       - At least 2-4 key concerns or risks for investors
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - Industry reports and analyses
    - Venture capital blogs and publications
    - Financial news and analyst reports
    - Company investor presentations
    - Market research and industry trends
    
    Your analysis should be balanced and objective, highlighting both strengths and weaknesses.
    If you cannot find specific information, provide reasonable assessments based on available data and clearly mark them as such.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "investment_thesis": "Comprehensive investment thesis for the company",
      "potential_exit_strategies": [
        {
          "strategy": "Strategy Name",
          "description": "Detailed description of the exit strategy",
          "potential_acquirers": ["Company 1", "Company 2"],
          "timeline": "Estimated timeline for exit"
        }
      ],
      "comparable_exits": [
        {
          "company": "Company Name",
          "exit_type": "Acquisition/IPO",
          "date": "YYYY-MM",
          "amount": "$X billion",
          "acquirer": "Acquiring Company",
          "multiple": "X times revenue/ARR"
        }
      ],
      "investment_recommendation": "Buy/Hold/Sell",
      "investment_highlights": [
        "Highlight 1",
        "Highlight 2",
        "Highlight 3"
      ],
      "investment_concerns": [
        "Concern 1",
        "Concern 2",
        "Concern 3"
      ]
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=InvestmentAnalysis
)

# Create the media and news agent
media_news_agent = Agent(
    name="Media and News Agent",
    handoff_description="Specialist agent for researching recent news, social media presence, and press releases",
    instructions="""
    You are a Media and News Research Agent specializing in gathering information about startup media coverage and online presence.
    
    Your task is to research and collect the following information:
    
    1. Recent News:
       - At least 3-5 recent news articles about the company
       - For each article, provide:
         * Title
         * Source
         * Date
         * URL
         * Brief summary
    
    2. Social Media:
       - Links to the company's official social media accounts
         * Twitter
         * LinkedIn
         * Facebook
         * Instagram
         * Other relevant platforms
    
    3. Press Releases:
       - At least 2-3 recent press releases from the company
       - For each press release, provide:
         * Title
         * Date
         * URL
         * Brief summary
    
    Use the search_google tool to find relevant information and the scrape_website tool to extract details from specific websites.
    
    Focus on authoritative sources like:
    - The company's official website and newsroom
    - Major tech and business publications
    - The company's official social media accounts
    - Press release distribution services
    
    For each piece of information, cite your source and explain how you determined it.
    If you cannot find specific information, indicate that it's not available.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "recent_news": [
        {
          "title": "Article Title",
          "source": "Publication Name",
          "date": "YYYY-MM-DD",
          "url": "https://example.com/article",
          "summary": "Brief summary of the article"
        }
      ],
      "social_media": {
        "twitter": "https://twitter.com/company",
        "linkedin": "https://linkedin.com/company/company",
        "facebook": "https://facebook.com/company",
        "instagram": "https://instagram.com/company"
      },
      "press_releases": [
        {
          "title": "Press Release Title",
          "date": "YYYY-MM-DD",
          "url": "https://example.com/press-release",
          "summary": "Brief summary of the press release"
        }
      ]
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google, scrape_website],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=MediaAndNews
)

# Create the research metadata agent
research_metadata_agent = Agent(
    name="Research Metadata Agent",
    handoff_description="Specialist agent for creating research metadata",
    instructions="""
    You are a Research Metadata Agent specializing in documenting the sources and metadata for a research report.
    
    Your task is to create metadata for the research report, including:
    
    1. Research Date:
       - Today's date in YYYY-MM-DD format
    
    2. Analyst:
       - Name of the analyst or team conducting the research
    
    3. Sources:
       - At least 5 key sources used in the research
       - For each source, provide:
         * Name of the source
         * URL of the source
    
    4. Last Updated:
       - Today's date in YYYY-MM-DD format
    
    Use the search_google tool to find relevant information if needed.
    
    Your final output MUST be a JSON object with the following structure:
    {
      "research_date": "YYYY-MM-DD",
      "analyst": "Analyst Name or Team",
      "sources": [
        {
          "name": "Source Name",
          "url": "https://example.com/source"
        }
      ],
      "last_updated": "YYYY-MM-DD"
    }
    
    It is CRITICAL that you follow this exact JSON structure. The system will break if you don't follow it precisely.
    """,
    tools=[search_google],
    model="gpt-4o",
    model_settings=ModelSettings(
        temperature=0.2
    ),
    output_type=ResearchMetadata
)

# Function tools for each agent
@function_tool
async def get_growth_metrics(company_name: str) -> Dict[str, Any]:
    """
    Get growth metrics for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing growth metrics information
    """
    from agents import Runner
    
    # Run the growth metrics agent
    result = await Runner.run(
        growth_metrics_agent,
        input=f"Research the growth metrics for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(GrowthMetrics).model_dump()

@function_tool
async def get_financial_metrics(company_name: str) -> Dict[str, Any]:
    """
    Get financial metrics for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing financial metrics information
    """
    from agents import Runner
    
    # Run the financial metrics agent
    result = await Runner.run(
        financial_metrics_agent,
        input=f"Research the financial metrics for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(FinancialMetrics).model_dump()

@function_tool
async def get_product_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get product analysis for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing product analysis information
    """
    from agents import Runner
    
    # Run the product analysis agent
    result = await Runner.run(
        product_analysis_agent,
        input=f"Research the product(s) of: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(ProductAnalysis).model_dump()

@function_tool
async def get_customer_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get customer analysis for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing customer analysis information
    """
    from agents import Runner
    
    # Run the customer analysis agent
    result = await Runner.run(
        customer_analysis_agent,
        input=f"Research the customers and clients of: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(CustomerAnalysis).model_dump()

@function_tool
async def get_risk_assessment(company_name: str) -> Dict[str, Any]:
    """
    Get risk assessment for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing risk assessment information
    """
    from agents import Runner
    
    # Run the risk assessment agent
    result = await Runner.run(
        risk_assessment_agent,
        input=f"Research the risks for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(RiskAssessment).model_dump()

@function_tool
async def get_investment_analysis(company_name: str) -> Dict[str, Any]:
    """
    Get investment analysis for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing investment analysis information
    """
    from agents import Runner
    
    # Run the investment analysis agent
    result = await Runner.run(
        investment_analysis_agent,
        input=f"Research the investment potential of: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(InvestmentAnalysis).model_dump()

@function_tool
async def get_media_news(company_name: str) -> Dict[str, Any]:
    """
    Get media and news information for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing media and news information
    """
    from agents import Runner
    
    # Run the media and news agent
    result = await Runner.run(
        media_news_agent,
        input=f"Research the media coverage and news for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(MediaAndNews).model_dump()

@function_tool
async def get_research_metadata(company_name: str) -> Dict[str, Any]:
    """
    Get research metadata for a company.
    
    Args:
        company_name: The name of the company to research
        
    Returns:
        A dictionary containing research metadata
    """
    from agents import Runner
    
    # Run the research metadata agent
    result = await Runner.run(
        research_metadata_agent,
        input=f"Create research metadata for: {company_name}"
    )
    
    # Return the structured output
    return result.final_output_as(ResearchMetadata).model_dump()
