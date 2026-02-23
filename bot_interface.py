import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from security_manager import SecurityManager
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class SyndicateBot:
    """The user interface for Syndicate.ai."""
    
    def __init__(self, token: str, master_password: str):
        self.app = ApplicationBuilder().token(token).build()
        self.security = SecurityManager(master_password)
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("add_key", self.add_key))
        self.app.add_handler(CommandHandler("status", self.status))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message and main menu."""
        user = update.effective_user
        welcome_text = (
            f"🚀 **Welcome to Syndicate.ai**, {user.first_name}!\n\n"
            "You are now part of the 2030 trading revolution. "
            "Delegate your assets to autonomous AI Syndicates and watch your alpha grow.\n\n"
            "**Commands:**\n"
            "/add_key - Connect an exchange (Binance/Bybit)\n"
            "/status - View your delegated syndicates and ROI\n"
            "/help - Get assistance"
        )
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    async def add_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Guidance for adding API keys securely."""
        instructions = (
            "🔐 **Secure API Key Integration**\n\n"
            "To connect your exchange, please use the following format:\n"
            "`/setup <exchange_id> <api_key> <api_secret>`\n\n"
            "*Note: We only support Read & Trade permissions. DO NOT ENABLE WITHDRAWALS.*"
        )
        await update.message.reply_text(instructions, parse_mode='Markdown')

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Display current syndicates."""
        # This would normally pull from the database
        demo_status = (
            "📊 **Your Syndicate Status**\n\n"
            "1. **The Gemini Scalper**: ✅ Active | ROI: +2.4%\n"
            "2. **Whale Hunter V1**: ⏳ Pending Delegation\n\n"
            "Balance Total: $1,240.50 (Mirroring)"
        )
        await update.message.reply_text(demo_status, parse_mode='Markdown')

    def run(self):
        """Starts the bot."""
        print("Syndicate Bot is alive and roaring...")
        self.app.run_polling()

if __name__ == "__main__":
    # Test requires TELEGRAM_TOKEN env var
    # bot = SyndicateBot(os.getenv("TELEGRAM_TOKEN"), "dev_master_pass")
    # bot.run()
    pass
