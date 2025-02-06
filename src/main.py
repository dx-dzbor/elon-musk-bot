import logging
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from .bot import TelegramSchedulerBot
from .scheduler import Scheduler
from .config_manager import ConfigManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

async def send_message_wrapper(bot: TelegramSchedulerBot, chat_id: str):
    """Wrapper function to handle async send_scheduled_message."""
    await bot.send_scheduled_message(chat_id)

def main():
    # Load environment variables
    load_dotenv()

    # Initialize components
    bot = TelegramSchedulerBot()
    scheduler = Scheduler()
    config_manager = ConfigManager()

    logging.info("Telegram scheduler bot has been started successfully.")

    # Configure schedules for each chat
    for chat_config in config_manager.get_chats():
        scheduler.add_job(
            chat_config,
            lambda chat_id: asyncio.run(send_message_wrapper(bot, chat_id))
        )

    try:
        # Run the scheduler
        scheduler.run()
    except Exception as e:
        error_message = f"Bot crashed: {str(e)}"
        logging.error(error_message)
        raise

if __name__ == "__main__":
    main() 
