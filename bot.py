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
    await update.message.reply_text("Bot ON hai! /papa likh ke command dekh")

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

async def fun(update, context):
    await update.message.reply_text("✨ FUN MENU ✨\n\n/joke - Joke\n/shayari - Shayari\n/ping - Bot live hai?")

async def joke(update, context):
    import random
    jokes = [
    "Teacher: Kal kyu nahi aaye? Student: Girlfriend se milne gaya tha 😂",
    "Zindagi me 2 hi sukh hai, ek neend, dusra fir se neend 😴",
    "Pati: Tum pehle jaisi nahi rahi. Patni: Pehle tum bhi Ameer nahi the 😜",
    "Exam me fail hone ka dukh nahi, dost ke pass hone ka zyada dukh hai 😭",
    "Wifi slow ho to lagta hai zindagi hi ruk gayi hai 📶",
    "Mummy: Beta padh le. Main: Haan mummy, phone me hi padh raha hu 😎",
    "Dost ke paise wapas mangna matlab dosti khatam karna 💸",
    "Subah uthna mushkil nahi, bistar chhodna mushkil hai 🛏️",
    "Pyar me dhoka khane ke baad ladke shayar ban jate hai 😅",
    "Aaj kal log photo me gore dikhne ke liye filter lagate hai, pehle haldi lagate the 😂",
    "Bhai ka birthday bhool jao, par uska udhaar mat bhoolna 😜",
    "School me jo topper tha, aaj wo mere yaha job karta hai 😎",
    "Girlfriend ka reply late aaye to lagta hai breakup ho gaya 💔",
    "Petrol itna mehenga hai, ab cycle hi best hai 🚲",
    "Raat ko neend nahi aati, din me aankh nahi khulti 😴"
    ]
    await update.message.reply_text(random.choice(jokes))

async def shayari(update, context):
    import random
    shayari_list = [
    "Teri yaad me humne chai bhi thandi pi li ☕",
    "Tum mile to laga, zindagi me kuch kami nahi thi, bas tumhari kami thi ❤️",
    "Mohabbat me humne dil haar diya, ab kehte hai hum hi bewafa hai 💔",
    "Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti 🌙",
    "Teri muskan pe fida hai ye dil, tu hanse to jahan has jaye 😊",
    "Dil tod ke jaane wale, kabhi to yaad karoge hume 💔",
    "Teri galiyon me aana jaana, ab aadat si ho gayi hai ❤️",
    "Zindagi ki har khushi ek taraf, tera saath ek taraf ✨",
    "Teri bina jeena mushkil hai, ye dil ab kehta hai 🥺",
    "Raat bhar teri yaad me jagte hai, subah tujhe yaad karke sote hai 🌙",
    "Tu mile ya na mile, mohabbat to tujhse hi rahegi ❤️",
    "Teri ek jhalak ke liye, hum zamana bhool jate hai 😍",
    "Dil me basi hai teri yaadein, kaise bhulaye tujhe 💭",
    "Mohabbat ka koi mol nahi, ye dil se hoti hai ❤️",
    "Teri yaad aaye to dil ro deta hai, tu paas ho to dil has deta hai 😢"
    ]
    await update.message.reply_text(random.choice(shayari_list))

async def ping(update, context):
    await update.message.reply_text("⚡ Bot LIVE hai bhai!")

async def tagall(update, context):
    await update.message.reply_text("🔥 @all Sab aa jao! Photo bhejo, sketch bana dunga!")
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
app.add_handler(CommandHandler("fun", fun))
app.add_handler(CommandHandler("joke", joke))
app.add_handler(CommandHandler("shayari", shayari))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("tagall", tagall)) 
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_handle))

print("Bot chal raha hai...")
app.run_polling()
