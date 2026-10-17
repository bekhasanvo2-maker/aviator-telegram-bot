import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

DATA_FILE = "history.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ AVIATOR STATISTIKA BOT\n\n"
        "/add 1.25 — natija qo‘shish\n"
        "/stats — statistika\n"
        "/history — tarix\n"
        "/clear — tarixni tozalash\n\n"
        "Eslatma: keyingi raundni aniq bashorat qilib bo‘lmaydi."
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Masalan: /add 1.25")
        return
    try:
        value = float(context.args[0].replace(",", "."))
        if value < 1:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Natijani to‘g‘ri kiriting. Masalan: /add 1.25")
        return

    data = load_data()
    user = str(update.effective_user.id)
    data.setdefault(user, []).append(value)
    save_data(data)
    await update.message.reply_text(f"✅ {value:.2f}x saqlandi.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    values = data.get(str(update.effective_user.id), [])
    if not values:
        await update.message.reply_text("Hali natijalar yo‘q. /add 1.25")
        return
    avg = sum(values) / len(values)
    low = sum(x < 2 for x in values)
    await update.message.reply_text(
        f"📊 STATISTIKA\n"
        f"Raundlar: {len(values)}\n"
        f"O‘rtacha ko‘paytirgich: {avg:.2f}x\n"
        f"2x dan past: {low} ({low/len(values)*100:.1f}%)\n"
        f"2x va yuqori: {len(values)-low}\n\n"
        "Bu ma’lumotlar keyingi raundni bashorat qilmaydi."
    )

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    values = data.get(str(update.effective_user.id), [])
    if not values:
        await update.message.reply_text("Tarix bo‘sh.")
        return
    text = "\n".join(f"{i}. {v:.2f}x" for i, v in enumerate(values[-20:], 1))
    await update.message.reply_text("📜 Oxirgi natijalar:\n" + text)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    data[str(update.effective_user.id)] = []
    save_data(data)
    await update.message.reply_text("🗑 Sizning tarixingiz tozalandi.")

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN sozlanmagan!")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("clear", clear))
    app.run_polling()

if __name__ == "__main__":
    main()
