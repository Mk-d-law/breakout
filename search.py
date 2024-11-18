import os
import logging
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def serp_search(query, num_results=10):
    """Performs a Google search and scrapes top results using SERP API."""
    try:
        search = GoogleSearch({
            "q": query,
            "num": num_results,
            "api_key": os.getenv("SERPAPI_KEY")
        })
        results = search.get_dict()
        
        if "error" in results:
            logger.error(f"SERP API Error: {results['error']}")
            raise Exception(f"SERP API Error: {results['error']}")
        
        organic_results = results.get("organic_results", [])
        if not organic_results:
            logger.warning(f"No organic results found for query: {query}")
        return organic_results

    except Exception as e:
        logger.exception("An error occurred while performing the search.")
        raise e
