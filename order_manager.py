from exchange_client import ExchangeClient
from solana_client import solana_client
from database.models import Trade, User, ApiKey
import asyncio
import logging

logger = logging.getLogger("OrderManager")

class OrderManager:
    """
    The 'Risk Guard' and Execution Orchestrator.
    Supports CEX (via CCXT) and Solana (via Jupiter).
    """
    
    def __init__(self, exchange_client: ExchangeClient, user_id: int):
        self.client = exchange_client
        self.user_id = user_id
        self.max_risk_per_trade = 0.02 # 2% risk per trade
        
    async def execute_safe_entry(self, symbol: str, signal_action: str, confidence: int, technicals: dict = None, mode: str = "AI"):
        """
        Calculates size based on risk, checks limits, and executes.
        """
        technicals = technicals or {}
        is_copy_trade = mode == "COPY_TRADE"
        
        # 0. Hallucination Circuit Breaker (ONLY for AI mode)
        if signal_action == 'BUY' and not is_copy_trade:
            h24_change = technicals.get('h24_change', 0)
            if h24_change < -15.0:
                logger.warning(f"🛑 CIRCUIT BREAKER: Rejecting AI BUY for {symbol} due to -{abs(h24_change)}% plunge!")
                return None

        # 1. Determine Backend (CEX or SOL)
        is_solana = "SOL" in symbol or len(symbol) > 30 
        
        try:
            if is_solana:
                balance = await solana_client.get_balance()
                logger.info(f"Solana Balance: {balance} SOL")
            else:
                balance = await self.client.get_balance('USDT')
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            return None

        min_balance = 0.05 if is_solana else 10.0
        if balance < min_balance:
            logger.warning(f"Insufficient balance: {balance} (Min: {min_balance})")
            return None
            
        # 2. Sizing Logic
        size_ratio = 0.1 * (confidence / 100.0)
        trade_amount = round(balance * size_ratio, 4)
        
        # 3. Execute
        logger.info(f"🚀 EXECUTING {signal_action} [{mode}] | Symbol: {symbol} | Vol: {trade_amount}")
        
        try:
            if is_solana:
                # Target Token Mint (Default to USDC if not specified)
                usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
                order = await solana_client.execute_jupiter_swap(
                    input_mint="So11111111111111111111111111111111111111112", # WSOL
                    output_mint=symbol if len(symbol) > 30 else usdc_mint,
                    amount_lamports=int(trade_amount * 1e9)
                )
            else:
                order = await self.client.execute_market_order(symbol, signal_action, trade_amount)
            
            if order:
                await self._log_trade(symbol, signal_action, trade_amount, order)
            return order
        except Exception as e:
            logger.error(f"Execution failed for {symbol}: {e}")
            return None

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
            logger.info(f"Trade for {symbol} logged to DB.")
        except Exception as e:
            logger.error(f"Failed to log trade to DB: {e}")


# Test stub
if __name__ == "__main__":
    pass
