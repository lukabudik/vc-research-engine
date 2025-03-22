from typing import Dict, Any

class CrunchbaseService:
    """
    Service for interacting with Crunchbase data
    Currently uses mock data, but would be replaced with actual API calls in production
    """
    
    @staticmethod
    async def get_startup_data(company_name: str) -> Dict[str, Any]:
        """
        Retrieve startup data from Crunchbase (mock implementation)
        
        Args:
            company_name: Name of the company to retrieve data for
            
        Returns:
            Dictionary containing startup data
        """
        # Mock data for demonstration
        mock_data = {
            "openai": {
                "name": "OpenAI",
                "description": "OpenAI is an AI research and deployment company dedicated to ensuring that artificial general intelligence benefits all of humanity.",
                "funding_rounds": [
                    {"date": "2019-03-01", "amount": 1000000000, "series": "A", "investors": ["Microsoft"]},
                    {"date": "2021-01-15", "amount": 2000000000, "series": "B", "investors": ["Khosla Ventures", "Reid Hoffman"]}
                ],
                "founders": ["Sam Altman", "Elon Musk", "Greg Brockman", "Ilya Sutskever", "John Schulman", "Wojciech Zaremba"],
                "industry": "Artificial Intelligence",
                "founded_year": 2015,
                "total_funding": 3000000000,
                "website": "https://openai.com",
                "location": "San Francisco, CA",
                "status": "Operating"
            },
            "anthropic": {
                "name": "Anthropic",
                "description": "Anthropic is an AI safety company working to build reliable, interpretable, and steerable AI systems.",
                "funding_rounds": [
                    {"date": "2021-05-01", "amount": 124000000, "series": "A", "investors": ["Jaan Tallinn", "Dustin Moskovitz"]},
                    {"date": "2022-04-15", "amount": 580000000, "series": "B", "investors": ["Google", "Spark Capital"]}
                ],
                "founders": ["Dario Amodei", "Daniela Amodei", "Tom Brown"],
                "industry": "Artificial Intelligence",
                "founded_year": 2021,
                "total_funding": 704000000,
                "website": "https://www.anthropic.com",
                "location": "San Francisco, CA",
                "status": "Operating"
            }
        }
        
        # Check if the requested company exists in our mock data
        if company_name.lower() in mock_data:
            return mock_data[company_name.lower()]
        else:
            # Return a default mock entry if company not found
            return {
                "name": company_name,
                "description": f"Mock data for {company_name}",
                "funding_rounds": [
                    {"date": "2022-01-01", "amount": 5000000, "series": "Seed", "investors": ["Mock Ventures"]}
                ],
                "founders": ["Founder 1", "Founder 2"],
                "industry": "Technology",
                "founded_year": 2020,
                "total_funding": 5000000,
                "website": f"https://www.{company_name.lower()}.com",
                "location": "San Francisco, CA",
                "status": "Operating"
            }
