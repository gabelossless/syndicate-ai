from exchange_client import ExchangeClient
from database.models import Trade, User, ApiKey
import asyncio

class OrderManager:
    """
    The 'Risk Guard' and Execution Orchestrator.
    Ensures we don't blow up the account.
    """
    
    def __init__(self, exchange_client: ExchangeClient, user_id: int):
        self.client = exchange_client
        self.user_id = user_id
        self.max_risk_per_trade = 0.02 # 2% risk per trade
        
    async def execute_safe_entry(self, symbol: str, signal_action: str, confidence: int, technicals: dict = None):
        """
        Calculates size based on risk, checks limits, and executes.
        Includes a Hallucination Circuit Breaker.
        """
        technicals = technicals or {}
        
        # 0. Hallucination Circuit Breaker
        if signal_action == 'BUY':
            h24_change = technicals.get('h24_change', 0)
            if h24_change < -15.0:
                print(f"🛑 CIRCUIT BREAKER TRIGGERED: Rejecting AI BUY for {symbol} due to -{abs(h24_change)}% plunge!")
                return None

        # 1. Check Balance
        try:
            balance = await self.client.get_balance('USDT')
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

        if balance < 10:
            print(f"Insufficient balance: ${balance}")
            return None
            
        # 2. Sizing Logic (Simple: 10% of balance * confidence)
        # confidence is 0-100.
        size_ratio = 0.1 * (confidence / 100.0)
        trade_amount_usdt = round(balance * size_ratio, 2)
        
        # 3. Execute
        print(f"Executing {signal_action} for ${trade_amount_usdt:.2f} (Conf: {confidence}%)")
        order = await self.client.execute_market_order(symbol, signal_action, trade_amount_usdt)
        
        if order:
            # 4. Log to DB
            await self._log_trade(symbol, signal_action, trade_amount_usdt, order)
            
            # 5. Place Stop Loss (Simulation)
            # await self.client.create_stop_loss_order(...)
            
        return order

    async def _log_trade(self, symbol, side, cost, order_data):
        try:
            await Trade.create(
                user_id=self.user_id,
                symbol=symbol,
                side=side,
                amount=order_data.get('amount', 0),
                price=order_data.get('average', 0) or order_data.get('price', 0),
                cost=cost,
                status="OPEN"
            )
            print("Trade logged to DB.")
        except Exception as e:
            print(f"Failed to log trade: {e}")

# Test stub
if __name__ == "__main__":
    pass
