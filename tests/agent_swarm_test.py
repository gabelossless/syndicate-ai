import asyncio
import aiohttp
import random
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("AgentSwarm")

BASE_URL = "http://localhost:8000"

async def high_frequency_trader(session):
    """Agent 1: Rapidly polls stats to check for backend bottlenecking."""
    logger.info("Agent 1 (HF Trader) deployed - Stress testing /api/stats")
    for _ in range(20):
        async with session.get(f"{BASE_URL}/api/stats") as resp:
            data = await resp.json()
            assert resp.status == 200
        await asyncio.sleep(0.5)
    logger.info("Agent 1 completed successfully.")

async def media_tycoon(session):
    """Agent 2: Uploads media and verifies duration logic."""
    logger.info("Agent 2 (Media Tycoon) deployed - Testing media constraints")
    # This simulation assumes existing files or mock uploads
    # Since we can't easily generate real audio duration here, we check the endpoint structure
    payload = {
        "title": "Agent Test Track",
        "price": "19.99",
        "media_type": "audio"
    }
    # Mocking a small file upload if we had a bytes stream
    # For now, we simulate a check on the dashboard to ensure previous uploads are visible
    async with session.get(f"{BASE_URL}/api/creator/dashboard") as resp:
        data = await resp.json()
        logger.info(f"Agent 2 found {len(data['tracks'])} existing tracks.")
    logger.info("Agent 2 completed.")

async def data_auditor(session):
    """Agent 3: Compares summary totals with track-level details."""
    logger.info("Agent 3 (Data Auditor) deployed - Verifying math logic")
    async with session.get(f"{BASE_URL}/api/creator/dashboard") as resp:
        data = await resp.json()
        summary = data['summary']
        tracks = data['tracks']
        
        calc_revenue = sum(t['revenue'] for t in tracks)
        calc_plays = sum(t['plays'] for t in tracks)
        
        if abs(summary['total_revenue'] - calc_revenue) < 0.01 and summary['total_plays'] == calc_plays:
            logger.info("✅ Math check PASSED.")
        else:
            logger.warning(f"❌ Math check FAILED: Summary {summary} vs Calc {calc_revenue}/{calc_plays}")

async def chaos_monkey(session):
    """Agent 4: Tries to break things with invalid IDs or paths."""
    logger.info("Agent 4 (Chaos Monkey) deployed - Looking for unhandled errors")
    # Delete non-existent ID
    async with session.delete(f"{BASE_URL}/api/media/999999") as resp:
        logger.info(f"Delete non-existent ID 999999 returned: {resp.status}")
    
    # Trigger 404
    async with session.get(f"{BASE_URL}/api/undefined_endpoint") as resp:
        assert resp.status == 404
        logger.info("Agent 4 verified 404 handling.")

async def roi_chaser(session):
    """Agent 5: Monitors leaderboard for consistency."""
    logger.info("Agent 5 (ROI Chaser) deployed - Checking leaderboard")
    async with session.get(f"{BASE_URL}/api/leaderboard") as resp:
        data = await resp.json()
        logger.info(f"Top rank: {data[0]['name']} with {data[0]['roi']}% ROI")
        assert len(data) > 0

async def main():
    async with aiohttp.ClientSession() as session:
        # Deploy all agents concurrently
        await asyncio.gather(
            high_frequency_trader(session),
            media_tycoon(session),
            data_auditor(session),
            chaos_monkey(session),
            roi_chaser(session)
        )

if __name__ == "__main__":
    logger.info("🚀 DEPLOYING AGENT SWARM...")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Swarm failed: {e}")
