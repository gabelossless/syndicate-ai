import asyncio
import sys
import os

# Fix path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import ccxt
    print(f"CCXT Version: {ccxt.__version__}")
except ImportError:
    print("CCXT NOT FOUND")

from order_manager import OrderManager
from unittest.mock import MagicMock, AsyncMock

class MockExchange:
    async def get_balance(self, symbol):
        print("Mock get_balance called")
        return 1000.0
        
async def run():
    print("Starting Debug Run")
    mock_client = MockExchange()
    mock_client.execute_market_order = AsyncMock(return_value={'id': '123', 'status': 'filled'})
    
    manager = OrderManager(mock_client, user_id=1)
    print("Manager created")
    
    order = await manager.execute_safe_entry('ETH/USDT', 'BUY', 80)
    print(f"Order Result: {order}")
    
    # Verify call
    print(f"Mock called: {mock_client.execute_market_order.called}")
    print(f"Mock call args: {mock_client.execute_market_order.call_args}")

if __name__ == "__main__":
    asyncio.run(run())
