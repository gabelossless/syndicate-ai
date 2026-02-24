import google.generativeai as genai
import os
import json
import random

class StrategyEngine:
    """The 'Brain' of the Syndicate. Uses LLM to analyze and generate signals."""
    
    def __init__(self, api_key: str):
        self.mock_mode = api_key == "mock_key_for_dev"
        if not self.mock_mode:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("🚀 StrategyEngine: Running in MOCK MODE (No real AI calls)")
        
    async def analyze_sentiment_and_price(self, coin: str, news_summary: str, technicals: dict, indicator_data: dict = None):
        """
        Generates a trade signal based on context.
        technicals: { 'price': 2500, 'h24_change': 2.5, 'volume': 1000000 }
        indicator_data: { 'score': 40, 'rsi': 35, 'macd_hist': 1.5, 'trend': 'bullish' }
        """
        indicator_data = indicator_data or {"score": 0, "rsi": 50, "macd_hist": 0, "trend": "neutral"}
        
        if self.mock_mode:
            # Simulate brain analysis + technicals
            actions = ["BUY", "SELL", "HOLD"]
            if indicator_data["score"] > 30:
                action = "BUY"
            elif indicator_data["score"] < -30:
                action = "SELL"
            else:
                action = random.choice(actions)
                
            confidence = min(100, max(0, 50 + abs(indicator_data["score"]) // 2 + random.randint(-10, 10)))
            price = technicals.get('price', 0)
            return {
                "action": action,
                "confidence": confidence,
                "reasoning": f"Simulated multi-factor for {coin} (Score: {indicator_data['score']})",
                "target_price": price * 1.05 if action == "BUY" else price * 0.95,
                "stop_loss": price * 0.98 if action == "BUY" else price * 1.02,
                "technical_score": indicator_data["score"]
            }

        prompt = f"""
        Analyze the following data for {coin} and provide a trading signal.
        
        NEWS SUMMARY:
        {news_summary}
        
        TECHNICAL DATA:
        {json.dumps(technicals, indent=2)}
        
        INDICATOR DATA (Score from -100 to +100):
        {json.dumps(indicator_data, indent=2)}
        
        Combine the AI sentiment of the news with the mathematical INDICATOR DATA.
        If the Indicator Score contradicts the News Sentiment heavily, reduce confidence or HOLD.
        
        Respond ONLY in JSON format:
        {{
            "action": "BUY" | "SELL" | "HOLD",
            "confidence": 0-100,
            "reasoning": "Brief technical/sentiment justification",
            "target_price": number,
            "stop_loss": number
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            signal = json.loads(content)
            signal["technical_score"] = indicator_data["score"]
            return signal
        except Exception as e:
            print(f"Error parsing AI signal: {e}")
            return {"action": "HOLD", "confidence": 0, "reasoning": "Parse Error", "technical_score": indicator_data["score"]}

# Example (simulated)
if __name__ == "__main__":
    # Test requires GOOGLE_API_KEY env var
    # engine = StrategyEngine(os.getenv("GOOGLE_API_KEY"))
    # signal = engine.analyze_sentiment_and_price("ETH", "Bullish ETF news incoming", {"price": 2600, "h24_change": 1.2})
    # print(signal)
    pass
