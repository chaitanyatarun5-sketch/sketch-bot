from flask import Flask
import threading
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot chal raha hai..."
def run_web():
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
threading.Thread(target=run_web, daemon=True).start()
import json, random, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

FILE = "settings.json"

def load():
    if os.path.exists(FILE):
        with open(FILE) as f: return json.load(f)
    return {"reply": "Hello! Bot chal gaya", "pic": None, "react": True, "dm": True, "autoreply": True}

def save(data):
    with open(FILE, "w") as f: json.dump(data, f)

data = load()
EMOJIS = ["??", "??", "??", "??", "??", "??", "??", "??"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ON hai! /help likh ke command dekh")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/setreply <text> - Auto reply set karo\n"
        "/setpic - Kisi photo pe reply karke ye likho, wo pic set ho jayegi\n"
        "/autoreact on/off - GC me auto react on/off\n"
        "/setdm on/off - DM me auto reply on/off\n"
        "/autoreply on/off - Auto reply on/off\n"
        "/show - Kya set hai wo dekho\n"
        "/clearpic - Pic hatao"
    )

async def setreply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Aise likh: /setreply Hello bhai kya haal hai")
        return
    data["reply"] = " ".join(context.args)
    save(data)
    await update.message.reply_text(f"Ho gaya! Ab ye reply jayega:\n{data['reply']}")

async def setpic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        data["pic"] = update.message.reply_to_message.photo[-1].file_id
        save(data)
        await update.message.reply_text("Pic set ho gayi! Ab reply ke sath ye pic jayegi")
    else:
        await update.message.reply_text("Kisi photo pe reply karke /setpic likho")

async def autoreact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    data["react"] = context.args[0].lower() == "on"
    save(data)
    await update.message.reply_text(f"Auto React: {'ON' if data['react'] else 'OFF'}")

async def setdm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    data["dm"] = context.args[0].lower() == "on"
    save(data)
    await update.message.reply_text(f"DM Auto Reply: {'ON' if data['dm'] else 'OFF'}")

async def autoreply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    data["autoreply"] = context.args[0].lower() == "on"
    save(data)
    await update.message.reply_text(f"Auto Reply: {'ON' if data['autoreply'] else 'OFF'}")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Reply: {data['reply']}\nPic: {'Set hai' if data['pic'] else 'Nahi hai'}\nReact: {data['react']}\nDM: {data['dm']}\nAutoReply: {data['autoreply']}")

async def clearpic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data["pic"] = None
    save(data)
    await update.message.reply_text("Pic hata di")

async def auto_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    if update.message.text.startswith("/"): return
    if not data["autoreply"]: return

    chat_type = update.message.chat.type
    is_group = chat_type in ["group", "supergroup"]

    # GC me Auto React
    if is_group and data["react"]:
        try:
            await context.bot.set_message_reaction(update.message.chat_id, update.message.message_id, [random.choice(EMOJIS)])
        except: pass

    # DM check
    if chat_type == "private" and not data["dm"]:
        return

    # Auto Reply + Pic
    if data["pic"]:
        await update.message.reply_photo(photo=data["pic"], caption=data["reply"])
    else:
        await update.message.reply_text(data["reply"])

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("setreply", setreply))
app.add_handler(CommandHandler("setpic", setpic))
app.add_handler(CommandHandler("autoreact", autoreact))
app.add_handler(CommandHandler("setdm", setdm))
app.add_handler(CommandHandler("autoreply", autoreply_cmd))
app.add_handler(CommandHandler("show", show))
app.add_handler(CommandHandler("clearpic", clearpic))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_handle))

print("Bot chal raha hai...")
app.run_polling()
