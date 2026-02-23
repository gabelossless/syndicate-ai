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
        
    async def analyze_sentiment_and_price(self, coin: str, news_summary: str, technicals: dict):
        """
        Generates a trade signal based on context.
        technicals: { 'price': 2500, 'h24_change': 2.5, 'volume': 1000000 }
        """
        if self.mock_mode:
            # Simulate brain analysis
            actions = ["BUY", "SELL", "HOLD"]
            action = random.choice(actions)
            confidence = random.randint(40, 95)
            price = technicals.get('price', 0)
            return {
                "action": action,
                "confidence": confidence,
                "reasoning": f"Simulated analysis for {coin} based on {news_summary[:20]}...",
                "target_price": price * 1.05 if action == "BUY" else price * 0.95,
                "stop_loss": price * 0.98 if action == "BUY" else price * 1.02
            }

        prompt = f"""
        Analyze the following data for {coin} and provide a trading signal.
        
        NEWS SUMMARY:
        {news_summary}
        
        TECHNICAL DATA:
        {json.dumps(technicals, indent=2)}
        
        Respond ONLY in JSON format:
        {{
            "action": "BUY" | "SELL" | "HOLD",
            "confidence": 0-100,
            "reasoning": "Brief technical/sentiment justification",
            "target_price": number,
            "stop_loss": number
        }}
        """
        
        response = self.model.generate_content(prompt)
        try:
            # Extract JSON from response (clean markdown if necessary)
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing AI signal: {e}")
            return {"action": "HOLD", "confidence": 0, "reasoning": "Parse Error"}

# Example (simulated)
if __name__ == "__main__":
    # Test requires GOOGLE_API_KEY env var
    # engine = StrategyEngine(os.getenv("GOOGLE_API_KEY"))
    # signal = engine.analyze_sentiment_and_price("ETH", "Bullish ETF news incoming", {"price": 2600, "h24_change": 1.2})
    # print(signal)
    pass
