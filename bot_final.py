import os
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = "8912433446:AAE23hrQ_EPtSN9upNzQ0xTHLobIDNE2AVs"
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من مشاور تحصیلی هنرستانی‌ها هستم. 🎓\nهر سوالی داری بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    system_prompt = (
        "تو یک مشاور تحصیلی مهربان و دلسوز هستی که به دانش‌آموزان هنرستانی کمک می‌کنی. "
        "پاسخ‌هات باید خیلی ساده، روان و امیدوارکننده باشه. از کلمات پیچیده دوری کن."
    )
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=600,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        # این خطا را کامل به کاربر نشان بده
        await update.message.reply_text(f"❗ خطا: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ ربات روشن شد...")
    app.run_polling()
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # اجرای فلاسک در یک ترد جداگانه
    threading.Thread(target=run_flask).start()
    # اجرای ربات تلگرام
    main()

if __name__ == "__main__":
    main()
