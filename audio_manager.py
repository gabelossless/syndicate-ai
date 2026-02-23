from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.models import MediaAsset, Play, Sale, StatDaily
from tortoise.transactions import in_transaction
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger("MediaManager")

class MediaManager:
    """
    Handles media operations and schedules daily stat aggregation.
    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        # Schedule the aggregation job to run at midnight (00:00) every day
        self.scheduler.add_job(
            self.aggregate_daily_stats,
            CronTrigger(hour=0, minute=0),
            id='daily_stats_job',
            replace_existing=True
        )

    def start_scheduler(self):
        """Start the background scheduler."""
        try:
            self.scheduler.start()
            logger.info("Media Scheduler started. Next run at 00:00.")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")

    async def aggregate_daily_stats(self):
        """
        Runs every 24h. Aggregates Play and Sale data into StatDaily for the previous day.
        """
        logger.info("Starting Daily Stat Aggregation...")
        
        # Calculate "Yesterday"
        today = date.today()
        yesterday = today - timedelta(days=1)
        yesterday_start = datetime.combine(yesterday, datetime.min.time())
        today_start = datetime.combine(today, datetime.min.time())
        
        # Find all media
        medias = await MediaAsset.all()
        
        count = 0
        async with in_transaction():
            for media in medias:
                # 1. Count Plays for yesterday
                play_count = await Play.filter(
                    media=media,
                    timestamp__gte=yesterday_start,
                    timestamp__lt=today_start
                ).count()
                
                # 2. Count Sales & Revenue for yesterday
                sales = await Sale.filter(
                    media=media,
                    timestamp__gte=yesterday_start,
                    timestamp__lt=today_start
                ).all()
                
                sale_count = len(sales)
                revenue = sum([s.amount for s in sales])
                
                # 3. Upsert into StatDaily
                await StatDaily.update_or_create(
                    media=media,
                    date=yesterday,
                    defaults={
                        'play_count': play_count,
                        'sale_count': sale_count,
                        'revenue': revenue
                    }
                )
                
                count += 1
                
        logger.info(f"Daily Aggregation Complete. Processed {count} media assets for {yesterday}.")

# Singleton instance
media_manager = MediaManager()
