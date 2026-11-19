import os, random
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8532606474
SUDO_FILE = "sudo.txt"

def load_sudos():
    try:
        with open(SUDO_FILE) as f:
            return set(int(x.strip()) for x in f if x.strip())
    except:
        return set()

def save_sudos(s):
    with open(SUDO_FILE, "w") as f:
        for x in s:
            f.write(str(x)+"\n")

SUDOS = load_sudos()
SUDOS.add(OWNER_ID)

def is_allowed(uid):
    return uid in SUDOS or uid == OWNER_ID

async def send(update, text):
    try:
        await update.effective_chat.send_message(text)
    except Exception as e:
        print("Send fail:", e)

async def check(update):
    if not is_allowed(update.effective_user.id):
        await send(update, "SORRY BHAI! YE BOT SIRF OWNER AUR SUDO KE LIYE HAI 🔒")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "KASHYAP BOT ON HAI! 🔥 /HELP LIKH KE COMMANDS DEKH.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "/MYID - APNI ID DEKHO\n/PING - BOT SPEED CHECK\n/PAPA - PAPA WALA REPLY\n/SHAYARI - SHAYARI ❤️\n/JOKE - JOKE 😂\n/PAPABOL - TRUTH / DARE KHELO 🎲\n/TRUTH - SACH WALA SAWAL\n/DARE - DARE WALA TASK\n/ADDSUDO - REPLY KARKE SUDO BANAO (SIRF OWNER)\n/DELSUDO - REPLY KARKE SUDO HATAO\n/SUDOLIST - SUDO LIST DEKHO")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, f"TERI ID: {update.effective_user.id}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PING PONG! KASHYAP BOT LIVE 🔥")

async def papa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PAPA HU ME TERA 😈🔥")

SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Mohabbat me humne khud ko mita diya, tere liye duniya se ladna sikha diya ❤️","Teri aankhon me duniya dekh li, ab aur kisi ki zarurat nahi ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️"]
JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Girlfriend se breakup ho gaya tha. Teacher: To? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Santa: Meri biwi mujhse bahut pyar karti hai. Banta: Kaise pata? Santa: Jab bhi me ghar late aata hu, wo darwaza khol ke kehti hai - Aa gaya kutta 😂","Teacher: Beta, tum bade hoke kya banoge? Pappu: Dulha. Teacher: Matlab? Pappu: Shaadi karunga, aur kuch nahi 😂"]
TRUTHS = ["Tera sabse bada crush kaun hai? 😏","Kabhi kisi ka message chupke padha hai?","Sabse embarrassing moment kya tha tera?","Kis se sabse zyada jalte ho?","Apni life ka sabse bada jhooth batao."]
DARES = ["Apni DP 1 ghante ke liye badal de 😂","Group me 'PAPA HU ME TERA' likh ke bhej 😈","Apne crush ko Hi bhej ke screenshot bhej 😏","10 baar apna naam zor se bol ke voice bhej","Apni gallery ki last photo group me bhej"]

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, random.choice(SHAYARI))
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, random.choice(JOKES))
async def papabol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PAPA BOL RAHA HAI 🎲\n/TRUTH likh - Sach wala sawal\n/DARE likh - Dare wala task")
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "TRUTH ❓\n" + random.choice(TRUTHS))
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "DARE 🔥\n" + random.choice(DARES))

async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI")
        return
    if not update.message.reply_to_message:
        await send(update, "KISI KE MESSAGE PE REPLY KARKE /ADDSUDO LIKH")
        return
    uid = update.message.reply_to_message.from_user.id
    SUDOS.add(uid); save_sudos(SUDOS)
    await send(update, f"HO GAYA! {uid} AB SUDO HAI 🔥\nAb ye bhi bot chala payega.")
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI")
        return
    if not update.message.reply_to_message:
        await send(update, "KISI KE MESSAGE PE REPLY KARKE /DELSUDO LIKH")
        return
    uid = update.message.reply_to_message.from_user.id
    SUDOS.discard(uid); save_sudos(SUDOS)
    await send(update, f"HATA DIYA! {uid} AB SUDO NAHI HAI")
async def sudolist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "SUDO LIST:\n" + "\n".join(str(x) for x in SUDOS))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("papa", papa))
    app.add_handler(CommandHandler("shayari", shayari))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("papabol", papabol))
    app.add_handler(CommandHandler("truth", truth))
    app.add_handler(CommandHandler("dare", dare))
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("sudolist", sudolist))
    print("KASHYAP BOT STARTED")
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__":
    main()
