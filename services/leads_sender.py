"""
Leads Sender Service for KingSpeech Bot
Sends lead data to another Telegram bot for processing
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from telegram import Bot
from config import LEADS_BOT_TOKEN, LEADS_BOT_CHAT_ID

logger = logging.getLogger(__name__)

class LeadsSenderService:
    """Service for sending leads to Telegram bot"""
    
    def __init__(self):
        self.bot_token = LEADS_BOT_TOKEN
        self.chat_id = LEADS_BOT_CHAT_ID
        self.bot = None
        
        if self.bot_token and self.chat_id:
            self.bot = Bot(token=self.bot_token)
            logger.info("LeadsSenderService initialized")
        else:
            logger.warning("LeadsSenderService not configured - missing token or chat_id")
    
    def format_lead_message(self, lead_data: Dict[str, Any]) -> str:
        """Format lead data into a structured message"""
        try:
            message = f"""🎯 **Новая заявка: KingSpeech**

👤 **Имя:** {lead_data.get('user_name', 'Не указано')}
📧 **Email:** {lead_data.get('email', 'Не указано')}
📱 **Телефон:** {lead_data.get('phone', 'Не указано')}
💬 **Мессенджер:** Telegram
🌐 **Страница:** https://t.me/kingspeechbot
🔗 **Реферер:** @kingspeechbot

📊 **Детали заявки:**
• **Уровень:** {lead_data.get('level', 'Не указано')}
• **Цель:** {lead_data.get('goals', 'Не указано')}
• **Формат:** {lead_data.get('format', 'Не указано')}
• **Ожидания:** {lead_data.get('expectations', 'Не указано')}
• **Дата начала:** {lead_data.get('start_date', 'Не указано')}

🆔 **Telegram ID:** {lead_data.get('telegram_id', 'Не указано')}
👤 **Username:** {lead_data.get('telegram_username', 'Не указано')}"""
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting lead message: {e}")
            return f"Ошибка форматирования заявки: {e}"
    
    async def send_lead(self, lead_data: Dict[str, Any]) -> bool:
        """Send lead data to the configured bot"""
        if not self.bot or not self.chat_id:
            logger.warning("Cannot send lead - bot not configured")
            return False
        
        try:
            message = self.format_lead_message(lead_data)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Lead sent successfully to {self.chat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending lead: {e}")
            return False
    
    def send_lead_sync(self, lead_data: Dict[str, Any]) -> bool:
        """Synchronous wrapper for send_lead"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, create a new task
                asyncio.create_task(self.send_lead(lead_data))
                return True
            else:
                # If no loop is running, run the async function
                return asyncio.run(self.send_lead(lead_data))
        except Exception as e:
            logger.error(f"Error in send_lead_sync: {e}")
            return False

# Global instance
leads_sender = LeadsSenderService()
