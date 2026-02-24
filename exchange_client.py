import ccxt.async_support as ccxt
import asyncio

class ExchangeClient:
    """Wrapper for CCXT to interact with various exchanges."""
    
    def __init__(self, exchange_id: str, api_key: str, secret: str, demo=False):
        self.exchange_class = getattr(ccxt, exchange_id)
        config = {
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'} # Default to futures for advanced trading
        }
        self.exchange = self.exchange_class(config)
        if demo:
            self.exchange.set_sandbox_mode(True)
            
    async def get_balance(self, symbol: str = 'USDT'):
        """Fetches the balance for a specific symbol."""
        try:
            balance = await self.exchange.fetch_balance()
            return balance.get(symbol, {}).get('free', 0)
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0

    async def fetch_positions(self):
        """Fetches current open positions."""
        try:
            positions = await self.exchange.fetch_positions()
            # Filter for non-zero positions
            return [p for p in positions if float(p['contracts']) > 0]
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return []

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100):
        """Fetches historical candlestick data to calculate technical indicators."""
        try:
            # OHLCV: [Timestamp, Open, High, Low, Close, Volume]
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return []
            
    async def execute_market_order(self, symbol: str, side: str, amount_usdt: float):
        """Executes a market order (BUY/SELL) by value."""
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            price = ticker['last']
            quantity = amount_usdt / price
            # Adjust quantity needed here based on exchange rules (precision), skipping for MVP
            
            if side.upper() == 'BUY':
                return await self.exchange.create_market_buy_order(symbol, quantity)
            else:
                return await self.exchange.create_market_sell_order(symbol, quantity)
        except Exception as e:
            print(f"Error executing market {side}: {e}")
            return None

    async def create_limit_order(self, symbol: str, side: str, amount: float, price: float):
        """Executes a limit order."""
        try:
            if side.upper() == 'BUY':
                return await self.exchange.create_limit_buy_order(symbol, amount, price)
            else:
                return await self.exchange.create_limit_sell_order(symbol, amount, price)
        except Exception as e:
            print(f"Error executing limit {side}: {e}")
            return None

    async def create_stop_loss_order(self, symbol: str, side: str, amount: float, stop_price: float):
        """Executes a stop loss order."""
        try:
            # Note: CCXT mapping for params varies by exchange. This is a generic implementation.
            params = {'stopPrice': stop_price}
            return await self.exchange.create_order(symbol, 'stop', side, amount, None, params)
        except Exception as e:
            print(f"Error executing stop loss: {e}")
            return None
            
    async def close(self):
        await self.exchange.close()

# Singleton for sharing across modules
exchange_client = ExchangeClient(
    exchange_id='binance', 
    api_key='mock', 
    secret='mock', 
    demo=True
)

if __name__ == "__main__":
    pass
