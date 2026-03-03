import httpx
import logging
from typing import Optional

logger = logging.getLogger("NewsClient")

CRYPTOPANIC_BASE = "https://cryptopanic.com/api/v1/posts/"

COIN_MAP = {
    "BTC/USDT": "BTC",
    "ETH/USDT": "ETH",
    "SOL/USDT": "SOL",
}

class NewsClient:
    """Fetches live crypto news from CryptoPanic public API (no API key required)."""
    
    _cache: dict = {}  # Simple in-memory cache: {coin: (timestamp, summary)}
    CACHE_TTL = 300  # 5 minutes
    
    async def fetch_headlines(self, symbol: str) -> str:
        """
        Fetches the latest news headlines for a given trading symbol.
        Returns a single concatenated string for AI analysis.
        """
        import time
        coin = COIN_MAP.get(symbol, symbol.split("/")[0])
        
        # Check cache first to avoid hammering the API
        cached = self._cache.get(coin)
        if cached:
            ts, summary = cached
            if time.time() - ts < self.CACHE_TTL:
                logger.info(f"Cache hit for {coin} news.")
                return summary
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    CRYPTOPANIC_BASE,
                    params={
                        "public": "true",
                        "currencies": coin,
                        "filter": "hot",
                        "kind": "news",
                    }
                )
                resp.raise_for_status()
                data = resp.json()
                
                results = data.get("results", [])
                if not results:
                    return f"No breaking news found for {coin}."
                
                headlines = []
                for post in results[:8]:  # Top 8 most recent/hot articles
                    title = post.get("title", "")
                    votes = post.get("votes", {})
                    sentiment = "positive" if votes.get("positive", 0) > votes.get("negative", 0) else "negative"
                    if title:
                        headlines.append(f"[{sentiment.upper()}] {title}")
                
                summary = "\n".join(headlines)
                self._cache[coin] = (time.time(), summary)
                logger.info(f"Fetched {len(headlines)} headlines for {coin}.")
                return summary
                
        except Exception as e:
            logger.warning(f"CryptoPanic fetch failed for {coin}: {e}. Using fallback.")
            return f"Live news unavailable for {coin}. Rely on technical indicators."

news_client = NewsClient()
