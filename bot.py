import os, random
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8532606474

# SUDO AB FILE SE NAHI, RENDER KE ENVIRONMENT SE AAYEGA - RESTART PE NAHI UDEGA
SUDO_IDS = os.environ.get("SUDO_IDS", "")
SUDOS = set([OWNER_ID])
if SUDO_IDS:
    for x in SUDO_IDS.split(","):
        if x.strip():
            try:
                SUDOS.add(int(x.strip()))
            except:
                pass

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
    await send(update, "/MYID - APNI ID DEKHO\n/PING - BOT SPEED CHECK\n/PAPA - PAPA WALA REPLY\n/SHAYARI - SHAYARI ❤️\n/JOKE - JOKE 😂\n/PAPABOL - TRUTH / DARE KHELO 🎲\n/TRUTH - SACH WALA SAWAL\n/DARE - DARE WALA TASK\n/ADDSUDO - /ADDSUDO 123456 YA REPLY KARKE\n/DELSUDO - /DELSUDO 123456 YA REPLY KARKE\n/SUDOLIST - SUDO LIST DEKHO")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, f"TERI ID: {update.effective_user.id}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PING PONG! KASHYAP BOT LIVE 🔥")

async def papa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PAPA HU ME TERA 😈🔥")

SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Mohabbat me humne khud ko mita diya, tere liye duniya se ladna sikha diya ❤️","Teri aankhon me duniya dekh li, ab aur kisi ki zarurat nahi ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️","Teri baaton me jadoo hai, sunte hi dil kho jata hai ❤️","Chahte hai tujhe dil se, tu hi meri manzil hai ❤️","Tum bin jiya jaye kaise, ye dil tumhe hi chahe ❤️","Teri yaadon ka sahara hai, warna jeena mushkil tha ❤️","Tu jo hanse to phool khil jaye, tu jo roye to dil jal jaye ❤️"]

JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Girlfriend se breakup ho gaya tha. Teacher: To? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Santa: Meri biwi mujhse bahut pyar karti hai. Banta: Kaise pata? Santa: Jab bhi me ghar late aata hu, wo darwaza khol ke kehti hai - Aa gaya kutta 😂","Teacher: Beta, tum bade hoke kya banoge? Pappu: Dulha. Teacher: Matlab? Pappu: Shaadi karunga, aur kuch nahi 😂","Ladki: Tum mujhe kabhi chhod to nahi doge? Ladka: Pagal hai kya, Jio ka network hu kya jo chhod du 😂","Doctor: Tumhe kya problem hai? Patient: Mujhe bhoolne ki bimari hai. Doctor: Kab se hai? Patient: Kab se kya? 😂","Pappu: Papa, exam me fail ho gaya. Papa: Koi baat nahi beta, tu to waise bhi pass hone layak nahi tha 😂"]

TRUTHS = ["Tera sabse bada crush kaun hai? 😏","Kabhi kisi ka message chupke padha hai?","Sabse embarrassing moment kya tha tera?","Kis se sabse zyada jalte ho?","Apni life ka sabse bada jhooth batao.","Last baar kab roye the aur kyu?"]
DARES = ["Apni DP 1 ghante ke liye badal de 😂","Group me 'PAPA HU ME TERA' likh ke bhej 😈","Apne crush ko Hi bhej ke screenshot bhej 😏","10 baar apna naam zor se bol ke voice bhej","Apni gallery ki last photo group me bhej","Apne best friend ko call karke I Love You bol"]

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
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE LIKH: /addsudo 123456\nYa kisi ke message pe reply karke /addsudo")
        return
    SUDOS.add(uid)
    await send(update, f"HO GAYA! {uid} AB SUDO HAI 🔥\nNOTE: Permanent ke liye is ID ko Render ke SUDO_IDS me bhi daal de.")

async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI")
        return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE LIKH: /delsudo 123456")
        return
    SUDOS.discard(uid)
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
