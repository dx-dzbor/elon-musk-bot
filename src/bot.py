import os
import logging
from typing import Optional
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
from pathlib import Path
from .config_manager import ConfigManager

class TelegramSchedulerBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("Telegram bot token not found in environment variables")
        
        self.bot = Bot(token=self.token)
        self.config_manager = ConfigManager()

    async def send_scheduled_message(self, chat_id: str):
        """Send scheduled message to specified chat."""
        try:
            message_content = self.config_manager.get_message_content()
            text = message_content.get('text', '')
            image_path = message_content.get('image_path')

            if image_path and Path(image_path).exists():
                with open(image_path, 'rb') as photo:
                    await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=text
                    )
            else:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=text
                )
            
            logging.info(f"Successfully sent scheduled message to chat {chat_id}")

        except TelegramError as e:
            error_message = f"Failed to send message to chat {chat_id}: {str(e)}"
            logging.error(error_message)
