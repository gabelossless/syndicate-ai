import logging
from exchange_client import exchange_client
from solana_client import solana_client

logger = logging.getLogger("PortfolioTracker")

# Approximate USD prices for Solana balance conversion (fetched dynamically in production)
SOL_USD_ESTIMATE = 150.0

class PortfolioTracker:
    """
    Aggregates real-time P&L snapshots across CEX and Solana.
    """

    async def get_cex_snapshot(self) -> dict:
        """Fetches key asset balances from the centralized exchange."""
        try:
            usdt = await exchange_client.get_balance("USDT")
            btc = await exchange_client.get_balance("BTC")
            eth = await exchange_client.get_balance("ETH")
            return {
                "USDT": round(float(usdt), 2),
                "BTC": round(float(btc), 8),
                "ETH": round(float(eth), 6),
            }
        except Exception as e:
            logger.error(f"Failed to fetch CEX snapshot: {e}")
            return {"USDT": 0.0, "BTC": 0.0, "ETH": 0.0}

    async def get_solana_snapshot(self) -> dict:
        """Fetches Solana wallet balance."""
        try:
            sol_balance = await solana_client.get_balance()
            return {
                "SOL": round(float(sol_balance), 4),
                "SOL_USD": round(float(sol_balance) * SOL_USD_ESTIMATE, 2),
            }
        except Exception as e:
            logger.error(f"Failed to fetch Solana snapshot: {e}")
            return {"SOL": 0.0, "SOL_USD": 0.0}

    async def get_full_snapshot(self) -> dict:
        """Returns a unified portfolio snapshot with total estimated USD value."""
        cex = await self.get_cex_snapshot()
        solana = await self.get_solana_snapshot()

        # Estimate total USD (simplified: USDT is 1:1, BTC/ETH would need live price)
        total_usd = cex.get("USDT", 0.0) + solana.get("SOL_USD", 0.0)

        return {
            "cex": cex,
            "solana": solana,
            "total_usd_estimate": round(total_usd, 2),
        }

portfolio_tracker = PortfolioTracker()
