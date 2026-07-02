import os
import asyncio
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI  # استفاده از ساختار استاندارد جدید

TELEGRAM_TOKEN = "8912433446:AAE23hrQ_EPtSN9upNzQ0xTHLobIDNE2AVs"
OPENROUTER_API_KEY = "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"

# تعریف کلاینت با ساختار نوین و کاملاً سازگار با پایتون‌های جدید
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! امیدوارم حالت خوب باشه، من مشاور تحصیلی هنرستانی‌ها هستم. 🎓\nهر سوالی داری بپرس!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    system_prompt = (
        "تو یک مشاور تحصیلی مهربان و دلسوز هستی که به دانش‌آموزان هنرستانی کمک می‌کنی. "
        "پاسخ‌هات باید خیلی ساده، روان و امیدوارکننده باشه. از کلمات پیچیده دوری کن و فارسی بنویس."
    )
    
    try:
        # ارسال درخواست به مدل پایدار هوش مصنوعی
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash-official:free", # مدل رایگان و بسیار دقیق‌تر برای زبان فارسی
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=600,
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"❗ خطا در ارتباط با هوش مصنوعی: {str(e)}")

# تنظیمات وب‌سرور فلاسک
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    # اجرای فلاسک روی پورت 10000 هماهنگ با رندر
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

async def main():
    # ساخت اپلیکیشن تلگرام بدون نیاز به updater مستقیم کلاسیک برای رفع ارور پایتون 3.14
    bot_app = Application.builder().token(TELEGRAM_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # شروع به کار ناهمگام و پایدار
    await bot_app.initialize()
    await bot_app.start()
    
    # استفاده از ساختar تایید شده بدون باگ انحصاری پایتون 3.14
    print("✅ ربات تلگرام با موفقیت بیدار و روشن شد...")
    
    # راه‌اندازی پولینگ امین
    updater = bot_app.updater
    await updater.start_polling()
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # ۱. اجرای فلاسک در بک‌گراند
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # ۲. اجرای حلقه اصلی ربات
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
