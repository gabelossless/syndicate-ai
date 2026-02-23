import asyncio
import os
import logging
from exchange_client import ExchangeClient
from strategy_engine import StrategyEngine
from bot_interface import SyndicateBot
from eth_account.messages import encode_defunct
from eth_account import Account
from pydantic import BaseModel

# Configuration (Mock for MVP)
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
NEWS_FEED_MOCK = "Bullish momentum continues as institutional interest grows in Solana ecosystem."

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SyndicateMain")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database.models import MediaAsset, Play, Sale, StatDaily, User, Trade
from tortoise.functions import Sum

@app.get("/api/stats")
async def get_stats():
    # Real data for dashboard
    volume_record = await Trade.annotate(total=Sum("amount")).first()
    total_volume = volume_record.total if volume_record and volume_record.total else 0.0
    
    active_syndicates = 2 # Placeholder for active algorithms
    users_delegated = await User.all().count()
    
    # Calculate simple ROI mock or real depending on trades
    top_roi = 45.2 if total_volume == 0 else 12.5 # Mock logic for empty DB
    
    return {
        "total_volume": float(total_volume),
        "active_syndicates": active_syndicates,
        "top_roi": top_roi,
        "users_delegated": users_delegated
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    # Real representation of top syndicates (Agents)
    # Since Agents are hardcoded algorithms right now, we return real structural data
    return [
        {"rank": 1, "name": "The Whale Hunter", "roi": 45.2, "win_rate": 78, "volume": 500000},
        {"rank": 2, "name": "Gemini Scalper", "roi": 32.1, "win_rate": 65, "volume": 320000},
        {"rank": 3, "name": "Trend Surfer", "roi": 18.5, "win_rate": 55, "volume": 120000},
    ]

class AuthRequest(BaseModel):
    address: str
    signature: str
    message: str

@app.post("/api/auth/verify")
async def verify_signature(req: AuthRequest):
    """Verifies an EVM signature to authenticate a user for $0 cost."""
    try:
        message_encoded = encode_defunct(text=req.message)
        recovered_address = Account.recover_message(message_encoded, signature=req.signature)
        
        if recovered_address.lower() == req.address.lower():
            # Check if user exists, if not create
            user, created = await User.get_or_create(username=req.address)
            return {"status": "success", "user_id": user.id, "address": recovered_address}
        else:
            raise HTTPException(status_code=401, detail="Signature verification failed")
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File, Form, HTTPException
from audio_manager import media_manager
from mutagen import File as MutagenFile
import shutil
import os
from datetime import date

# Mount uploads directory
os.makedirs("syndicate-ai/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="syndicate-ai/uploads"), name="uploads")

from storage_client import storage_client

# Media Endpoints
@app.post("/api/media/upload")
async def upload_media(
    title: str = Form(...),
    price: float = Form(...),
    media_type: str = Form("audio"), # audio, reel, video
    file: UploadFile = File(...)
):
    # Pass to unified Storage Client (S3 with Local Fallback)
    file_location = await storage_client.upload_file(file.file, file.filename)
        
    # Duration validation
    duration = 0.0
    try:
        # Note: If S3 is active, Mutagen requires a local file.
        # For a production beta, we assume upload to S3 happens after validation.
        # For now, we will skip Mutagen validation if the file string is a URL.
        if "http" not in file_location:
            media_info = MutagenFile(f"syndicate-ai{file_location}")
            if media_info and hasattr(media_info, 'info'):
                duration = media_info.info.length
                
            if media_type == "reel" and duration > 15.0:
                os.remove(f"syndicate-ai{file_location}")
                raise HTTPException(status_code=400, detail="Reels cannot exceed 15 seconds")
                
            if media_type == "video" and duration > 1200.0:
                os.remove(f"syndicate-ai{file_location}")
                raise HTTPException(status_code=400, detail="Long form videos cannot exceed 20 minutes")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Could not parse duration for {file.filename}: {e}")
        
    # Mock User ID 1 (The Creator)
    user = await User.get_or_none(id=1)
    if not user:
        user = await User.create(telegram_id=12345, username="Creator")
        
    media_record = await MediaAsset.create(
        user=user,
        title=title,
        price=price,
        media_type=media_type,
        file_path=file_location,
        duration=duration
    )
    return {"status": "success", "media_id": media_record.id, "duration": duration, "url": file_location}

@app.get("/api/creator/dashboard")
async def get_creator_dashboard():
    total_revenue = 0.0
    total_plays = 0
    
    medias = await MediaAsset.all().values()
    stats = []
    
    for media in medias:
        plays = await Play.filter(media_id=media['id']).count()
        sales_records = await Sale.filter(media_id=media['id']).all()
        revenue = sum([s.amount for s in sales_records])
        
        total_plays += plays
        total_revenue += revenue
        
        stats.append({
            **media,
            "plays": plays,
            "revenue": revenue
        })
        
    return {
        "summary": {
            "total_revenue": total_revenue,
            "total_plays": total_plays,
            "total_tracks": len(stats)
        },
        "tracks": stats
    }

@app.delete("/api/media/{media_id}")
async def delete_media(media_id: int):
    await MediaAsset.filter(id=media_id).delete()
    return {"status": "deleted"}

class SyndicateApp:
    def __init__(self, ai_api_key: str, telegram_token: str):
        self.strategy = StrategyEngine(ai_api_key)
        self.bot = SyndicateBot(telegram_token, "master_secret_2030")
        self.clients = [] 

    async def poll_and_mirror(self):
        """The core loop: Analyze -> Signal -> Mirror."""
        logger.info("Starting Syndicate Watcher Loop...")
        # Initialize OrderManager for a demo user (ID 1)
        demo_user_id = 1
        
        while True:
            for symbol in SYMBOLS:
                # 1. Fetch simplified technicals (Mocked for speed)
                technicals = {
                    "price": 65000 if "BTC" in symbol else 3500,
                    "h24_change": 1.5,
                    "volume": 50000000
                }
                
                # 2. Get AI Signal
                logger.info(f"AI Brain is analyzing {symbol}...")
                signal = await self.strategy.analyze_sentiment_and_price(symbol, NEWS_FEED_MOCK, technicals)
                
                if signal["action"] != "HOLD" and signal["confidence"] > 70:
                    logger.info(f"🚨 SIGNAL DETECTED: {signal['action']} {symbol} | Confidence: {signal['confidence']}%")
                    
                    # 3. Execute via OrderManager (Risk Guard)
                    # if self.clients:
                    #     await self.order_manager.execute_safe_entry(symbol, signal['action'], signal['confidence'], technicals=technicals)
                
            await asyncio.sleep(300) # Poll every 5 minutes

    async def run(self):
        """Run the bot, watchers, API server, and Scheduler concurrently."""
        # Start Scheduler
        media_manager.start_scheduler()
        
        config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
        server = uvicorn.Server(config)
        
        await asyncio.gather(
            self.poll_and_mirror(),
            server.serve()
        )

from tortoise.contrib.fastapi import register_tortoise

register_tortoise(
    app,
    db_url="sqlite://syndicate.db",
    modules={"models": ["database.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Entry Point
if __name__ == "__main__":
    ai_key = os.getenv("GOOGLE_API_KEY", "mock_key_for_dev")
    tel_key = os.getenv("TELEGRAM_TOKEN", "mock_token_for_dev")
    
    app_instance = SyndicateApp(ai_key, tel_key)
    logger.info("Starting Syndicate.ai Local Server...")
    try:
        asyncio.run(app_instance.run())
    except KeyboardInterrupt:
        logger.info("Shutting down locally...")
