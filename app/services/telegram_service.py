import os
import logging
from telegram import Bot


class TelegramService:
    """Service for handling Telegram notifications."""

    @staticmethod
    async def send_message(message: str) -> bool:
        """Send a message to the configured Telegram chat."""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            logging.debug("Telegram credentials missing - skipping notification")
            return False
        try:
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            logging.exception(f"Telegram notification failed: {e}")
            return False