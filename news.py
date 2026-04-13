import os
import httpx
import hashlib
import logging

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def fetch_tech_news():
    # Fetch top technology headlines
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                logging.error(f"NewsAPI Error: {response.text}")
                return []
            
            data = response.json()
            articles = data.get("articles", [])
            
            processed_news = []
            for art in articles[:5]:  # Limit to top 5
                if not art.get("title") or not art.get("url"):
                    continue
                    
                processed_news.append({
                    "title": art["title"],
                    "summary": (art["description"][:150] + "...") if art.get("description") else "No summary available.",
                    "url": art["url"],
                    "hash": hashlib.md5(art["url"].encode()).hexdigest()
                })
            return processed_news
    except Exception as e:
        logging.error(f"Exception while fetching news: {e}")
        return []
