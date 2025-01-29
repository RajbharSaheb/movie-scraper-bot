import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

async def search_movie(query):
    try:
        # Replace with actual movie website URL
        url = f"https://hdmaal.tw/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Replace with actual HTML parsing logic
        for item in soup.select('.movie-item'):
            title = item.select_one('.title').text.strip()
            link = item.select_one('a.download-link')['href']
            
            # Verify direct download link
            if any(link.endswith(ext) for ext in ['.mp4', '.mkv', '.avi']):
                results.append({
                    'title': title,
                    'link': link
                })
        
        return results
    
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return []
