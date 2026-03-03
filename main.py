import asyncio
import os
import logging
import shutil
from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from eth_account.messages import encode_defunct
from eth_account import Account
from mutagen import File as MutagenFile
from tortoise.functions import Sum
from tortoise.contrib.fastapi import register_tortoise

# Local Imports
from exchange_client import exchange_client
from strategy_engine import StrategyEngine
from bot_interface import SyndicateBot
from database.models import MediaAsset, Play, Sale, StatDaily, User, Trade
from audio_manager import media_manager
from storage_client import storage_client
from solana_tracker import whale_tracker
from indicators import generate_technical_score
from news_client import news_client
from portfolio_tracker import portfolio_tracker
from backtester import backtester

# --- CONFIGURATION ---
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://syndicate.db")
UPLOAD_DIR = "syndicate-ai/uploads"

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SyndicateMain")

# Initialization
app = FastAPI(title="Syndicate.ai API")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# --- SCHEMAS ---
class AuthRequest(BaseModel):
    address: str
    signature: str
    message: str

# --- ROUTES ---

@app.get("/")
async def root():
    return {"status": "online", "message": "Syndicate.ai API is running."}

@app.get("/api/stats")
async def get_stats():
    volume_record = await Trade.annotate(total=Sum("amount")).first()
    total_volume = volume_record.total if volume_record and volume_record.total else 0.0
    active_syndicates = 2 
    users_delegated = await User.all().count()
    top_roi = 45.2 if total_volume == 0 else 12.5 
    
    return {
        "total_volume": float(total_volume),
        "active_syndicates": active_syndicates,
        "top_roi": top_roi,
        "users_delegated": users_delegated
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    return [
        {"rank": 1, "name": "The Whale Hunter", "roi": 45.2, "win_rate": 78, "volume": 500000},
        {"rank": 2, "name": "Gemini Scalper", "roi": 32.1, "win_rate": 65, "volume": 320000},
        {"rank": 3, "name": "Trend Surfer", "roi": 18.5, "win_rate": 55, "volume": 120000},
    ]

@app.post("/api/auth/verify")
async def verify_signature(req: AuthRequest):
    try:
        message_encoded = encode_defunct(text=req.message)
        recovered_address = Account.recover_message(message_encoded, signature=req.signature)
        
        if recovered_address.lower() == req.address.lower():
            user, created = await User.get_or_create(username=req.address)
            return {"status": "success", "user_id": user.id, "address": recovered_address}
        else:
            raise HTTPException(status_code=401, detail="Signature verification failed")
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/media/upload")
async def upload_media(
    title: str = Form(...),
    price: float = Form(...),
    media_type: str = Form("audio"), 
    file: UploadFile = File(...)
):
    file_location = await storage_client.upload_file(file.file, file.filename)
    duration = 0.0
    
    try:
        if "http" not in file_location:
            local_path = os.path.join(UPLOAD_DIR, os.path.basename(file_location))
            media_info = MutagenFile(local_path)
            if media_info and hasattr(media_info, 'info'):
                duration = media_info.info.length
                
            if media_type == "reel" and duration > 15.0:
                os.remove(local_path)
                raise HTTPException(status_code=400, detail="Reels cannot exceed 15 seconds")
                
            if media_type == "video" and duration > 1200.0:
                os.remove(local_path)
                raise HTTPException(status_code=400, detail="Long form videos cannot exceed 20 minutes")
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Could not parse duration for {file.filename}: {e}")
        
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
        stats.append({**media, "plays": plays, "revenue": revenue})
        
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

@app.get("/api/portfolio")
async def get_portfolio():
    """Returns a real-time aggregated snapshot of CEX and Solana balances."""
    snapshot = await portfolio_tracker.get_full_snapshot()
    return snapshot

class BacktestRequest(BaseModel):
    symbol: str = "BTC/USDT"
    timeframe: str = "1h"
    limit: int = 300

@app.post("/api/backtest")
async def run_backtest(req: BacktestRequest):
    """Runs a strategy backtest and returns performance metrics + HTML report link."""
    result = await backtester.run(req.symbol, req.timeframe, req.limit)
    html = backtester.generate_html_report(result, req.symbol)
    report_path = "backtest_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    return {
        "symbol": req.symbol,
        "timeframe": req.timeframe,
        "total_return_pct": result.total_return_pct,
        "win_rate": result.win_rate,
        "max_drawdown": result.max_drawdown,
        "sharpe_ratio": result.sharpe_ratio,
        "total_trades": len(result.trades),
        "final_balance": result.final_balance,
        "report": f"/static/{report_path}",
    }

# --- APP CLASSES ---

class SyndicateApp:
    def __init__(self, ai_api_key: str, telegram_token: str):
        self.strategy = StrategyEngine(ai_api_key)
        self.bot = SyndicateBot(telegram_token, "master_secret_2030")

    async def poll_and_mirror(self):
        logger.info("Starting Syndicate Watcher Loop...")
        while True:
            try:
                for symbol in SYMBOLS:
                    ohlcv = await exchange_client.fetch_ohlcv(symbol, '1h', limit=100)
                    
                    if isinstance(ohlcv, list) and len(ohlcv) > 50:
                        prices = [float(candle[4]) for candle in ohlcv if len(candle) > 4]
                        if prices:
                            technicals = {
                                "price": prices[-1],
                                "h24_change": ((prices[-1] - prices[-min(24, len(prices))]) / prices[-min(24, len(prices))] * 100) if len(prices) >= 24 else 0,
                                "volume": sum([float(candle[5]) for candle in ohlcv[-min(24, len(ohlcv)):] if len(candle) > 5]) if len(ohlcv) >= 24 else 0
                            }
                            indicator_data = generate_technical_score(prices)
                        else:
                            technicals = {"price": 0.0, "h24_change": 0.0, "volume": 0.0}
                            indicator_data = None
                    else:
                        technicals = {"price": 65000.0 if "BTC" in symbol else 3500.0, "h24_change": 1.5, "volume": 50000000.0}
                        indicator_data = None

                    # Fetch LIVE news instead of a mock
                    live_news = await news_client.fetch_headlines(symbol)
                    signal = await self.strategy.analyze_sentiment_and_price(symbol, live_news, technicals, indicator_data)
                    
                    action = signal.get("action", "HOLD")
                    confidence = signal.get("confidence", 0)
                    if action != "HOLD" and confidence > 70:
                        logger.info(f"🚨 SIGNAL: {action} {symbol} | Conf: {confidence}% | Tech Score: {signal.get('technical_score')}")
                        
            except Exception as e:
                logger.error(f"Error in poll loop: {e}")
                
            await asyncio.sleep(300)

# --- INFRASTRUCTURE ---

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["database.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.on_event("startup")
async def startup_event():
    ai_key = os.getenv("GOOGLE_API_KEY", "mock_key_for_dev")
    tel_key = os.getenv("TELEGRAM_TOKEN", "mock_token_for_dev")
    app_instance = SyndicateApp(ai_key, tel_key)
    asyncio.create_task(app_instance.poll_and_mirror())
    media_manager.start_scheduler()
    asyncio.create_task(whale_tracker.connect_and_listen())

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


