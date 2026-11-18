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
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, InlineQueryHandler

TOKEN = os.getenv("TOKEN")

ALLOWED_USER_IDS = [8532606474, 9239452757] 
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
    if update.effective_user.id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Abbee baap ka bot nahi hai Tarun papa ko baap bol ke aa tab acces milega.")
        return
    await update.message.reply_text("Bot ON hai! /papa likh ke command dekh")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE ):   
        if update.effective_user.id not in ALLOWED_USER_IDS:
            await update.message.reply_text("Sorry, ye bot sirf owner aur uske VIP ke liye hai.")
            return
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
from telegram import InlineQueryResultArticle, InputTextMessageContent
import uuid, random

jokes_list = [
"Teacher: Kal kyu nahi aaye? Student: Girlfriend se milne gaya tha 😂",
"Zindagi me 2 hi sukh hai, ek neend, dusra fir se neend 😴",
"Wifi slow ho to lagta hai zindagi hi ruk gayi hai 📶",
"Papa: Beta result kaisa raha? Beta: Papa, 2 khushkhabri hai, ek fail ho gaya, dusri bhi fail ho gaya 😅",
"Girlfriend: Tum mujhe kabhi ghumane nahi le jate. Boyfriend: Le jata hu na, roz sapno me 😍",
"Exams aate hi dosti bhi topper se ho jati hai 📚",
"Mummy: Beta khana kha le. Beta: Pehle wifi ka password batao, khana to baad me bhi kha lunga 😋",
"Dost: Bhai breakup ho gaya. Main: Chal party karte hai, ek bojh kam hua 😂",
"Jab tak phone me charge hai, tab tak zindagi me sukh hai 🔋",
"Padhai karne baitho to neend aati hai, aur sone jao to padhai yaad aati hai 🤦",
"Single rehne ka ek fayda hai, koi puchega nahi 'kaha ho, khana khaya?' 😎",
"Teacher: Tum itne late kyu aaye? Student: Sir, sapne me school jaldi aa gaya tha, isliye late ho gaya 😂",
"Paise ho to log puchte hai 'kaise ho', na ho to puchte bhi nahi 🤑",
"Girlfriend ka gussa aur Mumbai ki baarish, kabhi bhi aa sakti hai 🌧️",
"Subah uthna sabse bada struggle hai, alarm se bada dushman koi nahi ⏰",
"Dost ke paise udhar lena aasan hai, wapas dena sabse mushkil 😭",
"Sharma ji ka beta to topper hai, humara beta to meme banane me topper hai 😂",
"Jab koi kahe '5 minute me aaya' to samajh jao 1 ghanta pakka hai ⌚",
"Love me padna aasan hai, usse bahar nikalna mushkil hai 💔",
"Phone girne pe dil se zyada screen tutne ka dard hota hai 📱"
]

shayari_list = [
"Teri yaad me humne chai bhi thandi pi li ☕",
"Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti 🌙",
"Tum mile to laga, zindagi me kuch kami nahi thi, bas tumhari kami thi ❤️",
"Door rehkar bhi tu dil ke paas hai, teri yaad hi meri har saans hai 🫶",
"Na chahiye daulat, na chahiye shoharat, bas ek tu chahiye, aur teri mohabbat ❤️",
"Teri muskaan pe fida hai ye dil, tu mile to lage duniya mil gayi 🌹",
"Raaton ko neend nahi aati, teri yaad bahut satati hai 😔",
"Tu jo mile to laga, khuda ne meri sun li, warna dua me to humne tujhe hi manga tha 🤲",
"Mohabbat me humne khud ko mita diya, tune kaha alvida aur humne maan liya 💔",
"Teri ek jhalak ke liye tarasta hai dil, tu na mile to udaas rehta hai dil 🥺",
"Zindagi guzar gayi tujhe chahte chahte, tu ek pal bhi na samajh paya hume chahte chahte 💭",
"Chai se zyada nasha teri yaado me hai, peeke bhi utarta nahi ☕❤️",
"Tu door hai to kya hua, teri yaadein to paas hai, dil me basi teri har baat hai 💌",
"Humne to bas tujhe chaha tha, tune to zamana hi badal diya 🥀",
"Khushboo ki tarah guzar gaya koi, yaadein chhod gaya, dil tod gaya 🌸",
"Tujhe dekh kar dil ne ye farmaya, tu hi hai meri duniya, tu hi hai meri dua ✨",
"Barish me teri yaad aur bhi badh jati hai, boondon me teri tasveer nazar aati hai 🌧️",
"Na din ko chain hai, na raat ko neend hai, bas teri yaad me dil ka ye haal hai 😢",
"Teri baatein sunne ko tarasta hu, teri ek awaaz pe marta hu 🎧❤️",
"Tu mile ya na mile, mohabbat to hum karte rahenge, tujhe yaad karke hum jeete rahenge 💖"
]

async def inline_query(update, context):
    q = update.inline_query.query.lower()
    if "shayari" in q or "syri" in q or "sayar" in q:
        text = random.choice(shayari_list)
    else:
        text = random.choice(jokes_list)
    results = [InlineQueryResultArticle(id=str(uuid.uuid4()), title="Bhejne ke liye click karo 👈", input_message_content=InputTextContent(text))]
    await update.inline_query.answer(results)

app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_handle))

print("Bot chal raha hai...")
app.run_polling()
