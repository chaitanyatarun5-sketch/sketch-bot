# ===== FULL BOT - BINDI ART + JOKE + SHAYARI + WATCH + SUDO + AUTOPIN =====
# pip install python-telegram-bot

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = "APNA_TOKEN_YAHA_DALO"

# ===== SUDO / OWNER =====
SUDO_USERS = [123456789]  # Yaha apni Telegram ID dalo

def is_sudo(user_id):
    return user_id in SUDO_USERS

# ===== BINDI FONT - Choti Choti Bindi Se Bada Akshar =====
FONT = {
'A': [" • ","• •","•••","• •","• •"],
'B': ["•• ","• •","•• ","• •","•• "],
'C': [" ••","•  ","•  ","•  "," ••"],
'D': ["•• ","• •","• •","• •","•• "],
'E': ["•••","•  ","•• ","•  ","•••"],
'F': ["•••","•  ","•• ","•  ","•  "],
'G': [" ••","•  ","• •","• •"," ••"],
'H': ["• •","• •","•••","• •","• •"],
'I': ["•••"," • "," • "," • ","•••"],
'J': ["•••"," • "," • ","• •"," • "],
'K': ["• •","• •","•• ","• •","• •"],
'L': ["•  ","•  ","•  ","•  ","•••"],
'M': ["• •","•••","• •","• •","• •"],
'N': ["• •","•••","• •","• •","• •"],
'O': [" • ","• •","• •","• •"," • "],
'P': ["•• ","• •","•• ","•  ","•  "],
'Q': [" • ","• •","• •"," ••","  •"],
'R': ["•• ","• •","•• ","• •","• •"],
'S': [" ••","•  "," • ","  •","•• "],
'T': ["•••"," • "," • "," • "," • "],
'U': ["• •","• •","• •","• •"," • "],
'V': ["• •","• •","• •","• •"," • "],
'W': ["• •","• •","• •","•••","• •"],
'X': ["• •","• •"," • ","• •","• •"],
'Y': ["• •","• •"," • "," • "," • "],
'Z': ["•••","  •"," • ","•  ","•••"],
' ': ["   ","   ","   ","   ","   "],
}

def bindi_art(text):
    text = text.upper()[:14]
    lines = [""]*5
    for ch in text:
        f = FONT.get(ch, FONT[' '])
        for i in range(5):
            lines[i] += f[i] + "  "
    return "\n".join(lines)

ARTS_LIST = [
"RAM", "JAISHREERAM", "HANUMAN", "MAHAKAL", "SHIV", "OM", "RADHE", "KRISHNA",
"ILOVEYOU", "LOVE", "HUG", "JAAN", "JAANU", "BABY", "CRUSH", "CUTE", "PYAR", "MISSYOU",
"HELLO", "BYEE", "PAPA", "MUMMY", "BRO", "BHAI", "DOSTI", "FRIEND", "BESTIE",
"KING", "QUEEN", "KASHYAP", "INDIA", "BHARAT",
"SORRY", "THANKYOU", "GOODMORNING", "GOODNIGHT", "HAPPYBIRTHDAY", "SINGLE", "HELICOPTER", "MERA"
]

def pretty_name(key):
    m = {"JAISHREERAM":"JAI SHREE RAM","ILOVEYOU":"I LOVE YOU","MISSYOU":"MISS YOU","GOODMORNING":"GOOD MORNING","GOODNIGHT":"GOOD NIGHT","HAPPYBIRTHDAY":"HAPPY BIRTHDAY","THANKYOU":"THANK YOU"}
    return m.get(key, key)

# ===== JOKE LIST =====
JOKES = [
"Teacher: Tum itne late kyu aaye?\nStudent: Sir, board pe likha tha 'School Ahead, Go Slow' 😂",
"Pappu: Mummy, aaj school me mujhe 100 me se 90 mile!\nMummy: Wah! Kis me?\nPappu: 50 Hindi me, 40 English me 😂",
"Boy: Tumhari smile bahut pyari hai\nGirl: Thanks\nBoy: Main to apni wali ki baat kar raha tha jab tumhe dekhta hu to aa jati hai 😍",
"Ek baar ek aadmi ne Google se pucha - Meri biwi kaha hai?\nGoogle bola - Teri himmat kaise hui mujhse puchne ki, main khud usi se darta hu 😂",
"Pati: Aaj khana kaisa bana hai?\nPatni: Acha hai\nPati: To fir roz aisa hi bana diya kar, jaisa aaj hotel se mangwaya hai 😂",
"Dost: Bhai, teri GF kaisi hai?\nDusra: Bilkul WiFi jaisi, sabke saath connect ho jati hai 😂",
"Girlfriend: Baby, tum mujhe kitna pyar karte ho?\nBoyfriend: Jitna Jio ka net, kabhi khatam nahi hota 😂",
"Teacher: Agar tumhe 100 rupaye mile to kya karoge?\nPappu: Udhari chuka dunga\nTeacher: Aur 1000 mile to?\nPappu: Udhari badha dunga 😂",
"Ek ladki ne ladke se kaha - Tum bahut bure ho\nLadka bola - To fir tum mere peeche kyu padi ho\nLadki - Kyunki bure logo se hi to pyar hota hai 😍",
"Bhai ne pucha - Exam kaisa gaya?\nMaine bola - Bilkul mere future jaisa, andhera hi andhera 😂",
"Biwi: Suno ji, agar main kho gayi to kya karoge?\nPati: Main newspaper me add dunga\nBiwi: Kis page pe?\nPati: Us page pe jise tum kabhi nahi padhti - Sports page 😂",
"Doctor: Tumhe kya problem hai?\nPatient: Sir, mujhe sab kuch bhool jata hai\nDoctor: Kab se?\nPatient: Kab se kya sir? 😂",
"Ek baar Santa ne 100 rupaye ka note jala diya\nKyu? Kyunki uspe likha tha - I Promise To Pay 😂",
"GF: Tum mujhe kabhi surprise nahi dete\nBF: Surprise! Main tumhara BF nahi hu, tumhara dost hu 😂",
"Teacher: Batao, duniya gol kyu hai?\nStudent: Taaki koi kone me jaake chup na sake 😂",
]

# ===== SHAYARI LIST =====
SHAYARI = [
"Teri yaad me humne jamana bhoola diya,\nTere pyar me humne khud ko bhoola diya,\nTu jo mili to laga zindagi mil gayi,\nPar tu jo gayi to laga zindagi hi chali gayi 💔",
"Mohabbat me humne kya kuch nahi kiya,\nDin raat teri yaad me guzara kiya,\nTu jo mile to laga sab kuch mil gaya,\nTu jo na mile to laga sab kuch lut gaya 😔",
"Tere chehre pe muskan humesha rahe,\nTeri zindagi me kabhi gam na aaye,\nTu jaha bhi rahe khush rahe,\nBas yehi dua hai meri rab se ❤️",
"Dosti me duri to aati rehti hai,\nFir bhi dosti dilo ko mila deti hai,\nJo dost dil se sacche hote hai,\nUnki yaad har pal tadpati hai 🤝",
"Raat bhar chandni me teri yaad aayi,\nDil ne kaha aaj fir teri kami mehsoos hui,\nTu jo paas hota to ye raat kitni haseen hoti,\nTu jo dur hai to ye raat kitni lambi lagti hai 🌙",
"Zindagi me har koi pyar karta hai,\nKoi dil se karta hai, koi matlab se,\nJo dil se karta hai wo kabhi bhoolta nahi,\nJo matlab se karta hai wo kabhi yaad nahi karta 💔",
"Tumse milke dil ko sukoon mila,\nTumse bichad ke dil ko dard mila,\nTum jo mile to laga jannat mil gayi,\nTum jo gaye to laga sab kuch lut gaya 😢",
"Chand ko dekh ke yaad teri aayi,\nTaro ko dekh ke yaad teri aayi,\nHar cheez me bas tu hi tu nazar aayi,\nAb to saanso me bhi bas tu hi tu samayi ❤️",
"Pyar me humne dil laga liya,\nDil laga ke humne dil gawa diya,\nAb to bas teri yaad hi reh gayi,\nJisme humne khud ko mita diya 💔",
"Jab se tu mili hai, zindagi badal gayi,\nHar khushi ab teri muskan se jud gayi,\nTu jo hanse to duniya hasin lage,\nTu jo roye to duniya veeran lage 😍",
"Dost wo jo har pal saath de,\nMuskil me bhi haath thaam le,\nKhushi me bhi saath hasse,\nGum me bhi saath roye 🤝",
"Teri muskan pe hum fida ho gaye,\nTeri adao pe hum kurban ho gaye,\nTu jo mili to laga sab kuch mil gaya,\nTu jo gayi to hum barbad ho gaye 💔",
"Waqt guzar jayega, yaadein reh jayengi,\nLog bhool jayenge, baatein reh jayengi,\nBas tu hi tu yaad aayegi,\nAur teri yaad me ye aankhein nam ho jayengi 😔",
"Zindagi ek safar hai, isme sab milte hai,\nKoi dil me bas jata hai, koi dil tod jata hai,\nJo dil me bas jata hai wo kabhi bhoolta nahi,\nJo dil tod jata hai wo kabhi yaad nahi aata 💔",
"Meri har dua me bas tu hi tu hai,\nMeri har khushi me bas tu hi tu hai,\nTu jo mile to laga rab mil gaya,\nTu jo na mile to laga sab kuch lut gaya ❤️",
]

# ===== WATCH + AUTOPIN STORAGE =====
WATCH_LIST = {}
AUTOPIN_GROUPS = {}
AUTOPIN_DM = set()

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 FULL BOT ON HAI BHAI 🔥\n\n"
        "• • • BINDI ART • • •\n"
        "/ART RAM - Bindi se RAM\n"
        "/ART ILOVEYOU - Bindi se I LOVE YOU\n"
        "/ART HUG - Bindi se HUG\n"
        "/ART - 40 ki list\n\n"
        "😂 JOKE / SHAYARI\n"
        "/JOKE - Naya Joke\n"
        "/SHAYARI - Nayi Shayari\n\n"
        "👀 WATCH\n"
        "/WATCH - Reply karke watch lagao\n"
        "/UNWATCH - Watch hatayo\n"
        "/WATCHLIST - List dekho\n\n"
        "👑 SUDO / ADMIN\n"
        "/ADD - Sudo add karo\n"
        "/SUDO - Sudo list\n\n"
        "📌 AUTO-PIN\n"
        "/AUTOPIN ON <id> - Group me auto pin\n"
        "/AUTOPIN OFF <id> - Band karo\n"
        "/DMAUTOPIN ON <id> - DM me auto pin\n"
        "/DMAUTOPIN OFF <id> - DM band\n\n"
        "Sab kuch ek hi bot me hai!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        txt = "• • • BINDI ART - 40 LIST • • •\n\n"
        for a in ARTS_LIST:
            txt += f"/ART {a}\n"
        txt += "\nYa khud ka bhi likh - /ART TERA NAAM"
        await update.message.reply_text(txt)
        return
    key = "".join(context.args).upper()
    show = pretty_name(key)
    art_text = bindi_art(show)
    await update.message.reply_text(f"```\n{art_text}\n```", parse_mode="Markdown")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"😂 JOKE:\n\n{random.choice(JOKES)}")

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"❤️ SHAYARI:\n\n{random.choice(SHAYARI)}")

async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe reply karke /WATCH likho bhai!")
        return
    target = update.message.reply_to_message.from_user
    WATCH_LIST[target.id] = target.first_name
    await update.message.reply_text(f"👀 {target.first_name} ko WATCH pe laga diya!")

async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe reply karke /UNWATCH likho!")
        return
    target = update.message.reply_to_message.from_user
    if target.id in WATCH_LIST:
        del WATCH_LIST[target.id]
        await update.message.reply_text(f"✅ {target.first_name} ko watch se hata diya!")
    else:
        await update.message.reply_text("Ye to watch pe tha hi nahi!")

async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not WATCH_LIST:
        await update.message.reply_text("Koi watch pe nahi hai!")
        return
    txt = "👀 WATCH LIST:\n\n"
    for name in WATCH_LIST.values():
        txt += f"• {name}\n"
    await update.message.reply_text(txt)

async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id):
        await update.message.reply_text("Tu sudo nahi hai bhai! Sirf sudo hi add kar sakta hai!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe reply karke /ADD likho!")
        return
    target = update.message.reply_to_message.from_user
    if target.id not in SUDO_USERS:
        SUDO_USERS.append(target.id)
        await update.message.reply_text(f"👑 {target.first_name} ko SUDO bana diya!")
    else:
        await update.message.reply_text("Ye pehle se hi sudo hai!")

async def sudo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "👑 SUDO LIST:\n\n"
    for uid in SUDO_USERS:
        txt += f"• {uid}\n"
    await update.message.reply_text(txt)

# ===== AUTO-PIN =====
async def autopin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "⌬  ᴀᴜᴛᴏ-ᴘɪɴ\n"
            "──────────────────────────────────\n"
            "▸ ɢʀᴏᴜᴘ ᴄʜᴀᴛ\n"
            "  .ᴀᴜᴛᴏᴘɪɴ ᴏɴ <ɪᴅ>       ᴘɪɴ ɴᴇᴡ ᴍsɢs\n"
            "  .ᴀᴜᴛᴏᴘɪɴ ᴏꜰꜰ <ɪᴅ>      sᴛᴏᴘ ᴘɪɴɴɪɴɢ\n"
            "▸ ᴅɪʀᴇᴄᴛ ᴍᴇssᴀɢᴇs\n"
            "  .ᴅᴍᴀᴜᴛᴏᴘɪɴ ᴏɴ <ᴛ>      ᴘɪɴ ɪɴ ᴅᴍ\n"
            "  .ᴅᴍᴀᴜᴛᴏᴘɪɴ ᴏꜰꜰ <ᴛ>     sᴛᴏᴘ ᴅᴍ ᴘɪɴ\n"
            "▸ ɴᴏᴛᴇ\n"
            "  <ɪᴅ> ᴀᴄᴄᴇᴘᴛs ᴜsᴇʀ ɪᴅ, @ᴜsᴇʀɴᴀᴍᴇ\n"
            "  ᴏʀ ɢʀᴏᴜᴘ ɪᴅ (ᴇ.ɢ. -100…)\n"
            "──────────────────────────────────\n"
            "  ᴛᴄs • ᴜsᴇʀʙᴏᴛ • ᴘʀɪᴍᴇ\n"
            "\nUse: /AUTOPIN ON 123456 ya reply karke /AUTOPIN ON"
        )
        return
    action = context.args[0].lower()
    target = context.args[1]
    try:
        if target.startswith("@"):
            if update.message.reply_to_message:
                target_id = update.message.reply_to_message.from_user.id
            else:
                await update.message.reply_text("Bhai @username ke liye uske message pe reply karke likh, ya ID de de!")
                return
        else:
            target_id = int(target)
    except:
        await update.message.reply_text("ID sahi se de bhai! Jaise -100123456 ya 123456789")
        return
    chat_id = update.effective_chat.id
    if chat_id not in AUTOPIN_GROUPS:
        AUTOPIN_GROUPS[chat_id] = set()
    if action == "on":
        AUTOPIN_GROUPS[chat_id].add(target_id)
        await update.message.reply_text(f"✅ AUTO-PIN ON ho gaya!\nAb {target} ka har naya message auto PIN hoga 📌")
    elif action == "off":
        AUTOPIN_GROUPS[chat_id].discard(target_id)
        await update.message.reply_text(f"❌ AUTO-PIN OFF ho gaya!\nAb {target} ka message PIN nahi hoga.")
    else:
        await update.message.reply_text("Sirf ON ya OFF likh bhai! /AUTOPIN ON <id>")

async def dmautopin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("DM ke liye - /DMAUTOPIN ON @username ya /DMAUTOPIN OFF @username")
        return
    action = context.args[0].lower()
    target = context.args[1]
    if update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
    else:
        try:
            target_id = int(target.replace("@",""))
        except:
            await update.message.reply_text("DM ke liye uske message pe reply karke likh!")
            return
    if action == "on":
        AUTOPIN_DM.add(target_id)
        await update.message.reply_text(f"✅ DM AUTO-PIN ON!\nAb {target} ka DM aate hi PIN ho jayega 📌")
    else:
        AUTOPIN_DM.discard(target_id)
        await update.message.reply_text(f"❌ DM AUTO-PIN OFF!")

async def auto_pin_watcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    chat_id = update.effective_chat.id
    user_id = msg.from_user.id
    if chat_id in AUTOPIN_GROUPS and user_id in AUTOPIN_GROUPS[chat_id]:
        try:
            await context.bot.pin_chat_message(chat_id, msg.message_id)
        except Exception as e:
            print(f"Pin nahi hua: {e}")
    if update.effective_chat.type == "private" and user_id in AUTOPIN_DM:
        try:
            await context.bot.pin_chat_message(chat_id, msg.message_id)
        except:
            pass

# ===== MAIN =====
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("art", art))
    app.add_handler(CommandHandler("bindi", art))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("shayari", shayari))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("unwatch", unwatch))
    app.add_handler(CommandHandler("watchlist", watchlist))
    app.add_handler(CommandHandler("add", add_sudo))
    app.add_handler(CommandHandler("sudo", sudo_list))
    app.add_handler(CommandHandler("autopin", autopin_cmd))
    app.add_handler(CommandHandler("dmautopin", dmautopin_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_pin_watcher))
    print("FULL BOT CHALU HO GAYA...")
    app.run_polling()

if __name__ == "__main__":
    main()
