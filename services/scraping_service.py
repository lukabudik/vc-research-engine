from playwright.async_api import async_playwright
from typing import Dict, Any, Optional
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrapingService:
    """Service for scraping websites using Playwright"""
    
    @staticmethod
    async def scrape_website(url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Scrape content from a website
        
        Args:
            url: URL to scrape
            selectors: Optional CSS selectors to extract specific content
            
        Returns:
            Dictionary containing scraped content
        """
        logger.info(f"Scraping website: {url}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    logger.info(f"Navigating to {url}")
                    # Increase timeout to 60 seconds and use domcontentloaded instead of networkidle
                    # This helps with sites that have long-running scripts or many resources
                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    
                    # Get page title
                    title = await page.title()
                    logger.info(f"Page title: {title}")
                    
                    # Get meta description
                    description = await page.evaluate("""
                        () => {
                            const meta = document.querySelector('meta[name="description"]');
                            return meta ? meta.getAttribute('content') : '';
                        }
                    """)
                    
                    # Get main content (simplified approach)
                    content = await page.evaluate("""
                        () => {
                            // Remove script tags, style tags, and comments
                            const bodyClone = document.body.cloneNode(true);
                            const scripts = bodyClone.querySelectorAll('script, style, noscript, iframe');
                            scripts.forEach(s => s.remove());
                            
                            // Get text from main content areas
                            const contentSelectors = ['main', 'article', '.content', '#content', '.main'];
                            for (const selector of contentSelectors) {
                                const element = bodyClone.querySelector(selector);
                                if (element) {
                                    return element.innerText;
                                }
                            }
                            
                            // Fallback to body text
                            return bodyClone.innerText;
                        }
                    """)
                    
                    # Clean up content
                    content = re.sub(r'\s+', ' ', content).strip()
                    logger.info(f"Extracted {len(content)} characters of content")
                    
                    # Extract specific content if selectors provided
                    specific_content = {}
                    if selectors:
                        logger.info(f"Extracting specific content with selectors: {selectors}")
                        for key, selector in selectors.items():
                            try:
                                elements = await page.query_selector_all(selector)
                                if elements:
                                    texts = []
                                    for element in elements:
                                        text = await element.inner_text()
                                        if text.strip():
                                            texts.append(text.strip())
                                    specific_content[key] = texts
                                    logger.info(f"Found {len(texts)} elements for selector '{key}'")
                                else:
                                    logger.warning(f"No elements found for selector '{key}'")
                            except Exception as e:
                                logger.error(f"Error extracting {key}: {str(e)}")
                                specific_content[key] = f"Error extracting {key}: {str(e)}"
                    
                    result = {
                        "url": url,
                        "title": title,
                        "description": description,
                        "content": content[:5000],  # Limit content length
                        "specific_content": specific_content
                    }
                    
                    logger.info(f"Successfully scraped {url}")
                    return result
                    
                except Exception as e:
                    logger.exception(f"Error scraping {url}: {str(e)}")
                    return {
                        "url": url,
                        "error": str(e)
                    }
                finally:
                    await browser.close()
        except Exception as e:
            logger.exception(f"Error initializing Playwright for {url}: {str(e)}")
            return {
                "url": url,
                "error": f"Failed to initialize scraper: {str(e)}"
            }
