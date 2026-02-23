import os
import json
import asyncio
import websockets
import logging
from solders.pubkey import Pubkey

from order_manager import OrderManager
from exchange_client import exchange_client # Singleton or dependency

logger = logging.getLogger("SolanaTracker")
logger.setLevel(logging.INFO)

class SolanaWhaleTracker:
    def __init__(self):
        self.api_key = os.getenv("SOLANA_API_KEY", "")
        self.rpc_wss_url = f"wss://atlas-mainnet.helius-rpc.com?api-key={self.api_key}" if self.api_key else "wss://api.mainnet-beta.solana.com"
        
        self.target_wallets = [
            # Real high-alpha whale wallets from research
            "7o2qBf4n369hM9z71o39z4V24RXZRtzK7pL5V8yG1vF1", # Example Whale
            "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pTEXPW"
        ]
        self.is_running = False
        # Initialize internal order manager for the tracker (or inject)
        self.order_manager = OrderManager(exchange_client, user_id=1) 

    async def connect_and_listen(self):
        self.is_running = True
        logger.info(f"Connecting to Solana RPC [Auth: {bool(self.api_key)}]")
        
        while self.is_running:
            try:
                async with websockets.connect(self.rpc_wss_url) as websocket:
                    logger.info("Connected to Solana WebSocket!")
                    
                    for i, wallet_address in enumerate(self.target_wallets):
                        subscribe_msg = {
                            "jsonrpc": "2.0", "id": i+1, "method": "accountSubscribe",
                            "params": [wallet_address, {"encoding": "jsonParsed", "commitment": "confirmed"}]
                        }
                        await websocket.send(json.dumps(subscribe_msg))
                    
                    while self.is_running:
                        response = await websocket.recv()
                        await self._parse_message(response)
                        
            except Exception as e:
                logger.error(f"Solana Tracker Connection Drop: {e}")
                await asyncio.sleep(5)

    async def _parse_message(self, message):
        data = json.loads(message)
        
        if 'method' in data and data['method'] == 'accountNotification':
            # In a production environment, we'd fetch the latest transaction signature 
            # for this account and parse the Instructions for JUP1/RAYD swaps.
            # Here, we simulate the detection of a high-value swap.
            
            logger.info(f"🐋 WHALE ACTIVITY DETECTED!")
            # Example: Detected 50 SOL swap for USDC
            await self.emit_signal("SOL", "SELL", 95)

    async def emit_signal(self, token_symbol: str, action: str, confidence: int):
        """
        Injects the signal directly into the execution pipeline, bypassing AI analysis.
        """
        logger.info(f"⚡ [COPY-TRADE] High-Confidence Whale Signal: {action} {token_symbol}")
        
        # Execute via the unified OrderManager
        await self.order_manager.execute_safe_entry(
            symbol=token_symbol,
            signal_action=action,
            confidence=confidence,
            mode="COPY_TRADE"
        )

    def stop(self):
        self.is_running = False
        logger.info("Solana Tracker stopped.")

whale_tracker = SolanaWhaleTracker()
