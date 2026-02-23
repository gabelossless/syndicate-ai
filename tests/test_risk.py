import pytest
import asyncio
import sys
import os

# Ensure the parent directory is in the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, AsyncMock
from order_manager import OrderManager

# Mock classes
class MockExchange:
    async def get_balance(self, symbol):
        return 1000.0 # $1000 balance
        
    async def execute_market_order(self, symbol, side, amount):
        return {
            'id': '123',
            'symbol': symbol,
            'side': side,
            'amount': amount / 100.0, # Approximate price of 100
            'average': 100.0,
            'status': 'filled'
        }
    
    # We need to explicitly define this so we can override it in tests easily if needed,
    # or let the AsyncMock overlay take precedence.
    pass

@pytest.mark.asyncio
async def test_safe_entry_sizing():
    # Setup
    mock_client = MockExchange()
    # Explicitly set execute_market_order as an AsyncMock to track calls.
    # The return value is the RESULT of the coroutine, not the coroutine itself.
    mock_client.execute_market_order = AsyncMock(return_value={
        'id': '123', 'price': 100.0, 'amount': 1.0, 'average': 100.0, 'status': 'filled'
    })
    
    manager = OrderManager(mock_client, user_id=1)
    
    # Execute with 80% confidence
    # Sizing rule: 0.1 * (80/100) = 0.08 (8%) of balance
    # Balance = 1000. Trade size should be $80.
    order = await manager.execute_safe_entry('ETH/USDT', 'BUY', 80)
    
    assert order is not None
    assert order['status'] == 'filled'
    
    # Verify the call to execute_market_order had the right value
    mock_client.execute_market_order.assert_called_with('ETH/USDT', 'BUY', 80.0)

@pytest.mark.asyncio
async def test_low_balance_reject():
    mock_client = MockExchange()
    mock_client.get_balance = AsyncMock(return_value=5.0) # $5 balance
    
    manager = OrderManager(mock_client, user_id=1)
    order = await manager.execute_safe_entry('ETH/USDT', 'BUY', 80)
    
    assert order is None
