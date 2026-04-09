import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token and Group Chat ID
BOT_TOKEN = "8681121379:AAH8vQizK2z2Yd4hk9Tj3elfNKBQ8_s4xQg"
GROUP_CHAT_ID = -1003888594814  # Ensure this is an integer

# OpenAI Client
client = OpenAI()

async def get_ai_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that replies in Burmese language."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error getting AI response: {e}")
        return "AI တုံ့ပြန်မှု ရယူရာတွင် အမှားအယွင်း ဖြစ်ပေါ်ခဲ့ပါသည်။ (An error occurred while fetching AI response.)"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id == GROUP_CHAT_ID:
        user_message = update.message.text
        logger.info(f"Received message from {update.effective_user.first_name} in group {chat_id}: {user_message}")

        if user_message:
            ai_response = await get_ai_response(user_message)
            await update.message.reply_text(ai_response)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started. Listening for messages...")
    application.run_polling(allowed_updates=Update.MESSAGE)

if __name__ == "__main__":
    main()
