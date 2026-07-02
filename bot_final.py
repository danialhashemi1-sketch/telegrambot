import os
import asyncio
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

TELEGRAM_TOKEN = "8912433446:AAE23hrQ_EPtSN9upNzQ0xTHLobIDNE2AVs"
OPENROUTER_API_KEY = "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"

# تنظیمات OpenAI
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! امیدوارم حالت خوب باشه، من مشاور تحصیلی هنرستانی‌ها هستم. 🎓\nهر سوالی داری بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    system_prompt = (
        "تو یک مشاور تحصیلی مهربان و دلسوز هستی که به دانش‌آموزان هنرستانی کمک می‌کنی. "
        "پاسخ‌هات باید خیلی ساده، روان و امیدوارکننده باشه. از کلمات پیچیده دوری کن."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=600,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"❗ خطا: {str(e)}")

# تنظیمات وب‌سرور فلاسک برای رندر
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    # فلاسک روی پورت 8080 اجرا می‌شود تا رندر سرویس را لایو نگه دارد
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

async def main():
    bot_app = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # راه‌اندازی ناهمگام ربات
    await bot_app.initialize()
    await bot_app.updater.start_polling()
    await bot_app.start()
    print("✅ ربات تلگرام با موفقیت بیدار و روشن شد...")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # ۱. ابتدا فلاسک را در یک ترد پس‌زمینه (Daemon) روشن می‌کنیم تا کد قفل نشود
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # ۲. حالا ربات تلگرام را در محیط اصلی اجرا می‌کنیم
    asyncio.run(main())
