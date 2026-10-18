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
    keyboard = [[
        InlineKeyboardButton(
            "✈️ AVIATOR O‘YININI OCHISH",
            url="https://db-bet-59066.pro/ru/my-casino?game=52358"
        )
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✈️ AVIATOR STATISTIKA BOT\n\n"
        "/add 1.25 — natija qo‘shish\n"
        "/stats — statistika\n"
        "/history — tarix\n"
        "/clear — tarixni tozalash\n\n"
        "Eslatma: keyingi raundni aniq bashorat qilib bo‘lmaydi.",
        reply_markup=reply_markup
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
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    values = data.get(str(update.effective_user.id), [])

    if len(values) < 10:
        await update.message.reply_text(
            "📊 Tahlil uchun kamida 10 ta natija kerak.\n"
            "Natijalarni /add 1.25 orqali kiriting."
        )
        return

    recent = values[-50:]
    avg = sum(recent) / len(recent)
    low = sum(x < 2 for x in recent)
    medium = sum(2 <= x < 5 for x in recent)
    high = sum(x >= 5 for x in recent)

    await update.message.reply_text(
        "✈️ AVIATOR — STATISTIK TAHLIL\n\n"
        f"Tahlil qilingan raundlar: {len(recent)}\n"
        f"O‘rtacha koeffitsiyent: {avg:.2f}x\n\n"
        f"1x–2x: {low} ta ({low / len(recent) * 100:.1f}%)\n"
        f"2x–5x: {medium} ta ({medium / len(recent) * 100:.1f}%)\n"
        f"5x va yuqori: {high} ta ({high / len(recent) * 100:.1f}%)\n\n"
        "⚠️ Bu tarixiy statistika, keyingi raund bashorati emas."
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
    app.add_handler(CommandHandler("stats", stats))app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("clear", clear))
    app.run_polling()

if __name__ == "__main__":
    main()
