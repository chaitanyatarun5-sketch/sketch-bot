import os, random
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8532606474
SUDO_FILE = "sudo.txt"

# SUDO LOAD
def load_sudos():
    try:
        with open(SUDO_FILE) as f:
            return set(int(x.strip()) for x in f if x.strip())
    except:
        return set()

def save_sudos(s):
    with open(SUDO_FILE, "w") as f:
        for x in s: f.write(str(x)+"\n")

SUDOS = load_sudos()
SUDOS.add(OWNER_ID)

# WATCH WALA SYSTEM
watched_groups = set()

def is_allowed(update: Update):
    return update.effective_user.id in SUDOS or update.effective_user.id == OWNER_ID

# SAFE SEND - Kabhi crash nahi hoga, reply nahi karega
async def send(update, text):
    try:
        await update.effective_chat.send_message(text)
    except Exception as e:
        print("Send fail:", e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, "KASHYAP BOT ON HAI! 🔥 /HELP LIKH KE COMMANDS DEKH.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, "/MYID - APNI ID DEKHO\n/PING - BOT SPEED CHECK\n/PAPA - PAPA WALA REPLY\n/SHAYARI - SHAYARI ❤️\n/JOKE - JOKE 😂\n/RAID 10 - 10 BAAR ROAST 😈\n/SPAM 5 BYYEE - JO LIKHOGE WO 5 BAAR BHEJEGA 🔥\n/WATCH - GROUP KI BAAT OWNER TAK JAYEGI 👀\n/UNWATCH - WATCH BAND KARO\n/INBOX - OWNER KE LIYE\n/ADDSUDO - REPLY KARKE SUDO BANAO (SIRF OWNER)\n/DELSUDO - REPLY KARKE SUDO HATAO\n/SUDOLIST - SUDO LIST DEKHO")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, f"TERI ID: {update.effective_user.id}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, "PING PONG! KASHYAP BOT LIVE 🔥")

async def papa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, "PAPA HU ME TERA 😈🔥")

# --- WATCH SYSTEM START ---
async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        await send(update, "Ye command sirf group me chalegi bhai.")
        return
    keyboard = [[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{chat.id}")]]
    try:
        await chat.send_message(
            "👀 CHAT RELAY REQUEST\n\nIs group ki saari messages bot ke owner tak jayengi.\nKoi bhi member Approve dabaye to shuru ho jayega.\nBand karna: /unwatch",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print("Watch fail:", e)

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = int(query.data.split("_")[1])
    watched_groups.add(chat_id)
    try:
        await query.edit_message_text("✅ Relay ON ho gaya.\nAb is group ki saari baat Owner tak jayegi.\nBand karne ke liye /unwatch likho.")
    except:
        pass

async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in watched_groups:
        watched_groups.remove(chat_id)
        await send(update, "❌ Relay OFF ho gaya.\nAb koi baat Owner tak nahi jayegi.")
    else:
        await send(update, "Relay ON hi nahi tha.")

async def inbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await send(update, "Ye sirf Owner ke liye hai.")
        return
    await send(update, f"INBOX 📩\nWatched Groups: {len(watched_groups)}\nJab bhi watched group me koi bolega, message yaha aayega.")

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.id in watched_groups:
        user = update.effective_user
        text = update.message.text or "Photo/Sticker bheja"
        try:
            await context.bot.send_message(OWNER_ID, f"📩 {chat.title}\n👤 {user.first_name} (@{user.username}):\n{text}")
        except Exception as e:
            print("Relay fail:", e)
# --- WATCH SYSTEM END ---

SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Mohabbat me humne khud ko mita diya, tere liye duniya se ladna sikha diya ❤️","Teri aankhon me duniya dekh li, ab aur kisi ki zarurat nahi ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️","Teri baaton me jadoo hai, sunte hi dil kho jata hai ❤️","Chahte hai tujhe dil se, tu hi meri manzil hai ❤️","Tum bin jiya jaye kaise, ye dil tumhe hi chahe ❤️","Teri yaadon ka sahara hai, warna jeena mushkil tha ❤️","Tu jo hanse to phool khil jaye, tu jo roye to dil jal jaye ❤️","Ishq me humne sab kuch luta diya, bas teri ek muskan ke liye ❤️","Teri galiyon se guzre to laga, jannat yahi hai ❤️","Dil ka haal kya bataye, tujhe dekh ke dil dhadak jaye ❤️","Tum meri subah shaam ho, tum hi mera aaram ho ❤️","Teri ek jhalak ke liye, hum taraste rahe ❤️","Mohabbat ki galiyon me hum kho gaye, teri yaadon me so gaye ❤️","Tu mera chand hai, me tera tara ❤️","Teri khushi me meri khushi hai, tu hanse to me hanu ❤️","Dil ki kitaab me tera naam likha hai, har panne pe tu hi tu hai ❤️","Tujhe dekh ke dil ne ye kaha, tu hi meri duniya hai ❤️","Teri yaad me humne chai pi, aur raat guzar gayi ❤️","Tu jo mile to laga, dua kabool ho gayi ❤️","Teri aankhon ka nasha hai, utarta hi nahi ❤️","Dil me basa liya hai tujhe, ab nikalna mushkil hai ❤️","Tu meri zindagi ka sabse haseen pal hai ❤️"]

JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Girlfriend se breakup ho gaya tha. Teacher: To? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Ek ladki ne ladke se kaha: Tum bahut bure ho. Ladka: Thanks, tum bhi bahut buri lag rahi ho aaj 😂","Santa: Meri biwi mujhse bahut pyar karti hai. Banta: Kaise pata? Santa: Jab bhi me ghar late aata hu, wo darwaza khol ke kehti hai - Aa gaya kutta 😂","Teacher: Beta, tum bade hoke kya banoge? Pappu: Dulha. Teacher: Matlab? Pappu: Shaadi karunga, aur kuch nahi 😂","Ladki: Tum mujhe kabhi chhod to nahi doge? Ladka: Pagal hai kya, Jio ka network hu kya jo chhod du 😂","Doctor: Tumhe kya problem hai? Patient: Mujhe bhoolne ki bimari hai. Doctor: Kab se hai? Patient: Kab se kya? 😂","Pappu: Papa, exam me fail ho gaya. Papa: Koi baat nahi beta, tu to waise bhi pass hone layak nahi tha 😂","Girlfriend: Tum mujhe kitni izzat dete ho? Boyfriend: Jitni tu mujhe deti hai, matlab zero 😂","Ek baar ek chuha billi se bola: I love you. Billi: Pagal hai kya? Chuha: Pyar andha hota hai 😂","Teacher: Agar tumhe 100 rupaye mile to kya karoge? Pappu: Recharge karunga. Teacher: Padhai ka kya? Pappu: Free WiFi se ho jayegi 😂","Pati: Aaj khana kaisa bana hai? Patni: Acha hai. Pati: To fir ye jalne ki smell kaha se aa rahi hai? Patni: Meri jal rahi hai 😂","Ladka: Tumhari aankhen bahut sundar hai. Ladki: Thanks. Ladka: Aur chashma bhi 😂","Santa ne Banta ko phone kiya: Kaha ho? Banta: Ghar pe. Santa: Jhooth mat bol, me ghar pe hu, tu kaha hai? 😂","Mummy: Beta, padh le. Beta: Padh raha hu. Mummy: Phone me kya padh raha hai? Beta: Teri bahu ki photo dekh raha hu 😂","Teacher: Tumhara homework kaha hai? Pappu: Kutte ne kha liya. Teacher: Tumhare paas kutta kab se hai? Pappu: Abhi kharida, homework khane ke liye 😂","Boyfriend: Baby, tum bahut moti ho gayi ho. Girlfriend: To? Boyfriend: To ab tumhe koi uthake nahi le jayega, safe ho 😂","Ek aadmi: Bhai, ye rasta kaha jata hai? Dusra: Pata nahi, me yaha ka nahi hu. Pehla: To tu yaha kya kar raha hai? Dusra: Rasta dekh raha hu 😂","Pappu: Mummy, me shaadi karunga. Mummy: Kis se? Pappu: Jisse tum kaho. Mummy: Pados wali aunty se? Pappu: Mummy, mazak mat karo 😂","Girlfriend: Tum mere liye kya kar sakte ho? Boyfriend: Kuch bhi. Girlfriend: To mera phone recharge kar de 😂","Santa: Yaar, meri biwi bahut ladti hai. Banta: To chup raha kar. Santa: Me chup hi rehta hu, wo akele bhi lad leti hai 😂","Teacher: Sabse bada sach kya hai? Pappu: Sir, Sunday ko school nahi hota, yehi sabse bada sach hai 😂","Ladki: Tum cigarette pite ho? Ladka: Nahi. Ladki: Daru? Ladka: Nahi. Ladki: To fir tum mere layak nahi ho, boring ho 😂","Papa: Beta, result kaisa raha? Beta: Papa, 2 logo ne top kiya hai. Papa: Tu kitne number pe hai? Beta: Me teesra hu, pehle 2 ke baad me hi hu 😂","Ek ladka ladki ko propose kar raha tha: Will you marry me? Ladki: No. Ladka: To fir friendship to kar le, itna bhav kyu kha rahi hai 😂","Mummy: Beta, sabzi le aa. Beta: Konsi? Mummy: Jo tujhe pasand ho. Beta: Pizza le aau? 😂","Teacher: Tum late kyu aaye? Pappu: Sir, board pe likha tha - School 8 baje khulta hai, me 8 baje hi aaya, gate band tha 😂","Boyfriend: Tumhe sabse zyada kya pasand hai? Girlfriend: Shopping. Boyfriend: Aur sabse kam? Girlfriend: Tumhara bank balance 😂","Santa: Banta, tu itna khush kyu hai? Banta: Biwi mayke gayi hai. Santa: To? Banta: Ab ghar pe shanti hai 😂"]

ROASTS = ["Teri shakal dekh ke to WiFi bhi disconnect ho jaye 😂","Tu itna slow hai, Google bhi tujhe search karne se mana kar de 😂","Teri akal to itni hai jitni Jio ke network me speed 😂","Tu school me bhi itna fail hua ki teacher ne tujhe pass karne ke liye prarthna ki 😂","Teri harkate dekh ke to cartoon bhi sharma jaye 😂","Tu itna boring hai ki neend ki goli bhi tujhe dekh ke so jaye 😂","Teri DP dekh ke to phone bhi hang ho jaye 😂","Tu itna kala hai ki raat ko light band karke dhoondna padta hai 😂","Teri baatein sunke to kaan bhi chutti maang le 😂","Tu itna mota hai ki Google Map bhi tujhe load nahi kar pata 😂","Teri shakal dekh ke to bhoot bhi dar ke bhaag jaye 😂","Tu itna bewakoof hai ki exam me apna naam bhi galat likh de 😂","Teri English sunke to angrez bhi Hindi bolne lage 😂","Tu itna ganda hai ki saaf-safai wala bhi tujhe dekh ke bhaag jaye 😂","Teri hansi sunke to kutte bhi bhonkna band kar de 😂","Tu itna chipku hai ki Fevicol bhi tujhse haar jaye 😂","Teri photo dekh ke to camera bhi toot jaye 😂","Tu itna lazy hai ki sapne me bhi soya rehta hai 😂","Teri baat sunke to dimag bhi kehta hai - Bhai, rehne de 😂","Tu itna kadwa bolta hai ki karela bhi meetha lage 😂"]

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, random.choice(SHAYARI))
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, random.choice(JOKES))
async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update): return
    n = 5
    if context.args:
        try: n = int(context.args[0])
        except: pass
    n = max(1, min(n, 10))
    txt = "\n\n".join(random.sample(ROASTS, n))
    await send(update, txt)
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update): return
    if len(context.args) < 2:
        await send(update, "AISE LIKH BHAI: /spam 5 BYYEE")
        return
    try: count = int(context.args[0])
    except:
        await send(update, "PEHLE NUMBER DAAL: /spam 5 BYYEE")
        return
    count = max(1, min(count, 20))
    text = " ".join(context.args[1:])
    full = "\n".join([text]*count)
    await send(update, full)
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI")
        return
    if not update.message.reply_to_message:
        await send(update, "KISI KE MESSAGE PE REPLY KARKE /ADDSUDO LIKH")
        return
    uid = update.message.reply_to_message.from_user.id
    SUDOS.add(uid); save_sudos(SUDOS)
    await send(update, f"HO GAYA! {uid} AB SUDO HAI 🔥")
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
    app.add_handler(CommandHandler("raid", raid))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("unwatch", unwatch))
    app.add_handler(CommandHandler("inbox", inbox))
    app.add_handler(CommandHandler("addsudo", addsudo))
    app.add_handler(CommandHandler("delsudo", delsudo))
    app.add_handler(CommandHandler("sudolist", sudolist))
    app.add_handler(CallbackQueryHandler(approve))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))
    print("KASHYAP BOT STARTED")
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=10000), daemon=True).start()
if __name__ == "__main__":
    main()
