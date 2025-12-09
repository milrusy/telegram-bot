import os
import logging
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Помилка налаштування ключа: {e}")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MAIN_MENU_KEYBOARD = [
    [KeyboardButton("Student"), KeyboardButton("IT-technologies")],
    [KeyboardButton("Contacts"), KeyboardButton("ChatGPT")]
]
BACK_KEYBOARD = [[KeyboardButton("Назад")]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Вас вітає чат-бот! Виберіть відповідну команду",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Student":
        response = "Студент: Заіченко Мирослава, Група ІП-22"
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(BACK_KEYBOARD, resize_keyboard=True))
    elif text == "IT-technologies":
        response = "IT-технології:\n- Front-end\n- Back-end\n- WEB-технології"
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(BACK_KEYBOARD, resize_keyboard=True))
    elif text == "Contacts":
        response = "Контакти:\nтел. 050-55-55-55"
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(BACK_KEYBOARD, resize_keyboard=True))
    elif text == "ChatGPT":
        response = "Режим ШІ (Gemini) активовано. Пишіть запитання."
        context.user_data['chat_mode'] = True
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(BACK_KEYBOARD, resize_keyboard=True))
    elif text == "Назад":
        context.user_data['chat_mode'] = False
        await update.message.reply_text("Меню", reply_markup=ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True))
    else:
        if context.user_data.get('chat_mode'):
            await update.message.reply_text("Gemini думає...")
            try:
                response = model.generate_content(text)  # синхронний виклик
                if response.text:
                    await update.message.reply_text(response.text)
                else:
                    await update.message.reply_text("ШІ не зміг згенерувати текстову відповідь.")
            except Exception as e:
                await update.message.reply_text(f"Помилка: {e}")
        else:
            await update.message.reply_text("Будь ласка, скористайтеся меню.", reply_markup=ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот з Gemini запущений...")
    application.run_polling()

