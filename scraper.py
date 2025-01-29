import requests
from bs4 import BeautifulSoup

def scrape_movies(query):
    # Base URL of the website to scrape
    base_url = "https://hdmaal.tw/search?q="  # Replace with a legal website
    search_url = base_url + query.replace(" ", "+")
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse results (update selectors based on the website structure)
        results = soup.find_all('a', class_='movie-link')  # Replace with actual class name

        movies = []
        for result in results[:5]:  # Limit to top 5 results
            title = result.text.strip()
            link = result['href']
            movies.append({"title": title, "link": link})

        return movies

    except Exception as e:
        print(f"Error: {e}")
        return []
