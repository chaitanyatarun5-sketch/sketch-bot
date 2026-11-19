# FULL BOT - NAYA CLEAN WALA
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import random
import os

TOKEN = os.getenv("BOT_TOKEN", "APNA_TOKEN_YAHA_DALO")

SUDO_USERS = [123456789]

def is_sudo(user_id):
    return user_id in SUDO_USERS

FONT = {
'A': [" . ",". .","...",". .",". ."],
'B': [".. ",". .",".. ",". .",".. "],
'C': [" ..",".  ",".  ",".  "," .."],
'D': [".. ",". .",". .",". .",".. "],
'E': ["...",".  ",".. ",".  ","..."],
'F': ["...",".  ",".. ",".  ",".  "],
'G': [" ..",".  ",". .",". ."," .."],
'H': [". .",". .","...",". .",". ."],
'I': ["..."," . "," . "," . ","..."],
'J': ["..."," . "," . ",". ."," . "],
'K': [". .",". .",".. ",". .",". ."],
'L': [".  ",".  ",".  ",".  ","..."],
'M': [". .","...",". .",". .",". ."],
'N': [". .","...",". .",". .",". ."],
'O': [" . ",". .",". .",". ."," . "],
'P': [".. ",". .",".. ",".  ",".  "],
'Q': [" . ",". .",". ."," ..","  ."],
'R': [".. ",". .",".. ",". .",". ."],
'S': [" ..",".  "," . ","  .",".. "],
'T': ["..."," . "," . "," . "," . "],
'U': [". .",". .",". .",". ."," . "],
'V': [". .",". .",". .",". ."," . "],
'W': [". .",". .",". .","...",". ."],
'X': [". .",". ."," . ",". .",". ."],
'Y': [". .",". ."," . "," . "," . "],
'Z': ["...","  ."," . ",".  ","..."],
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

JOKES = [
"Teacher: Tum itne late kyu aaye? Student: Sir, board pe likha tha School Ahead, Go Slow",
"Pappu: Mummy, aaj school me mujhe 100 me se 90 mile! Mummy: Wah! Kis me? Pappu: 50 Hindi me, 40 English me",
"Boy: Tumhari smile bahut pyari hai. Girl: Thanks. Boy: Main to apni wali ki baat kar raha tha jab tumhe dekhta hu to aa jati hai",
"Ek baar ek aadmi ne Google se pucha - Meri biwi kaha hai? Google bola - Teri himmat kaise hui mujhse puchne ki, main khud usi se darta hu",
"Pati: Aaj khana kaisa bana hai? Patni: Acha hai. Pati: To fir roz aisa hi bana diya kar, jaisa aaj hotel se mangwaya hai",
"Dost: Bhai, teri GF kaisi hai? Dusra: Bilkul WiFi jaisi, sabke saath connect ho jati hai",
"Girlfriend: Baby, tum mujhe kitna pyar karte ho? Boyfriend: Jitna Jio ka net, kabhi khatam nahi hota",
"Teacher: Agar tumhe 100 rupaye mile to kya karoge? Pappu: Udhari chuka dunga. Teacher: Aur 1000 mile to? Pappu: Udhari badha dunga",
"Ek ladki ne ladke se kaha - Tum bahut bure ho. Ladka bola - To fir tum mere peeche kyu padi ho. Ladki - Kyunki bure logo se hi to pyar hota hai",
"Bhai ne pucha - Exam kaisa gaya? Maine bola - Bilkul mere future jaisa, andhera hi andhera",
"Biwi: Suno ji, agar main kho gayi to kya karoge? Pati: Main newspaper me add dunga. Biwi: Kis page pe? Pati: Us page pe jise tum kabhi nahi padhti - Sports page",
"Doctor: Tumhe kya problem hai? Patient: Sir, mujhe sab kuch bhool jata hai. Doctor: Kab se? Patient: Kab se kya sir?",
"Ek baar Santa ne 100 rupaye ka note jala diya. Kyu? Kyunki uspe likha tha - I Promise To Pay",
"GF: Tum mujhe kabhi surprise nahi dete. BF: Surprise! Main tumhara BF nahi hu, tumhara dost hu",
"Teacher: Batao, duniya gol kyu hai? Student: Taaki koi kone me jaake chup na sake",
]

SHAYARI = [
"Teri yaad me humne jamana bhoola diya, Tere pyar me humne khud ko bhoola diya, Tu jo mili to laga zindagi mil gayi, Par tu jo gayi to laga zindagi hi chali gayi",
"Mohabbat me humne kya kuch nahi kiya, Din raat teri yaad me guzara kiya, Tu jo mile to laga sab kuch mil gaya, Tu jo na mile to laga sab kuch lut gaya",
"Tere chehre pe muskan humesha rahe, Teri zindagi me kabhi gam na aaye, Tu jaha bhi rahe khush rahe, Bas yehi dua hai meri rab se",
"Dosti me duri to aati rehti hai, Fir bhi dosti dilo ko mila deti hai, Jo dost dil se sacche hote hai, Unki yaad har pal tadpati hai",
"Raat bhar chandni me teri yaad aayi, Dil ne kaha aaj fir teri kami mehsoos hui, Tu jo paas hota to ye raat kitni haseen hoti, Tu jo dur hai to ye raat kitni lambi lagti hai",
"Zindagi me har koi pyar karta hai, Koi dil se karta hai, koi matlab se, Jo dil se karta hai wo kabhi bhoolta nahi, Jo matlab se karta hai wo kabhi yaad nahi karta",
"Tumse milke dil ko sukoon mila, Tumse bichad ke dil ko dard mila, Tum jo mile to laga jannat mil gayi, Tum jo gaye to laga sab kuch lut gaya",
"Chand ko dekh ke yaad teri aayi, Taro ko dekh ke yaad teri aayi, Har cheez me bas tu hi tu nazar aayi, Ab to saanso me bhi bas tu hi tu samayi",
"Pyar me humne dil laga liya, Dil laga ke humne dil gawa diya, Ab to bas teri yaad hi reh gayi, Jisme humne khud ko mita diya",
"Jab se tu mili hai, zindagi badal gayi, Har khushi ab teri muskan se jud gayi, Tu jo hanse to duniya hasin lage, Tu jo roye to duniya veeran lage",
"Dost wo jo har pal saath de, Muskil me bhi haath thaam le, Khushi me bhi saath hasse, Gum me bhi saath roye",
"Teri muskan pe hum fida ho gaye, Teri adao pe hum kurban ho gaye, Tu jo mili to laga sab kuch mil gaya, Tu jo gayi to hum barbad ho gaye",
"Waqt guzar jayega, yaadein reh jayengi, Log bhool jayenge, baatein reh jayengi, Bas tu hi tu yaad aayegi, Aur teri yaad me ye aankhein nam ho jayengi",
"Zindagi ek safar hai, isme sab milte hai, Koi dil me bas jata hai, koi dil tod jata hai, Jo dil me bas jata hai wo kabhi bhoolta nahi, Jo dil tod jata hai wo kabhi yaad nahi aata",
"Meri har dua me bas tu hi tu hai, Meri har khushi me bas tu hi tu hai, Tu jo mile to laga rab mil gaya, Tu jo na mile to laga sab kuch lut gaya",
]

WATCH_LIST = {}
AUTOPIN_GROUPS = {}
AUTOPIN_DM = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "FULL BOT ON HAI BHAI\n\n"
        "BINDI ART\n"
        "/ART RAM - Bindi se RAM\n"
        "/ART ILOVEYOU - Bindi se I LOVE YOU\n"
        "/ART - 40 ki list\n\n"
        "JOKE / SHAYARI\n"
        "/JOKE - Naya Joke\n"
        "/SHAYARI - Nayi Shayari\n\n"
        "WATCH\n"
        "/WATCH - Reply karke watch lagao\n"
        "/UNWATCH - Watch hatayo\n"
        "/WATCHLIST - List dekho\n\n"
        "SUDO / ADMIN\n"
        "/ADD - Sudo add karo\n"
        "/SUDO - Sudo list\n\n"
        "AUTO-PIN\n"
        "/AUTOPIN ON - Reply karke ON karo\n"
        "/AUTOPIN OFF - Reply karke OFF karo\n"
        "/DMAUTOPIN ON - DM me auto pin\n"
        "/DMAUTOPIN OFF - DM band\n\n"
        "Sab kuch ek hi bot me hai!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        txt = "BINDI ART - 40 LIST\n\n"
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
    await update.message.reply_text(f"JOKE:\n\n{random.choice(JOKES)}")

async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"SHAYARI:\n\n{random.choice(SHAYARI)}")

async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe reply karke /WATCH likho bhai!")
        return
    target = update.message.reply_to_message.from_user
    WATCH_LIST[target.id] = target.first_name
    await update.message.reply_text(f"{target.first_name} ko WATCH pe laga diya!")

async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi ke message pe reply karke /UNWATCH likho!")
        return
    target = update.message.reply_to_message.from_user
    if target.id in WATCH_LIST:
        del WATCH_LIST[target.id]
        await update.message.reply_text(f"{target.first_name} ko watch se hata diya!")
    else:
        await update.message.reply_text("Ye to watch pe tha hi nahi!")

async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not WATCH_LIST:
        await update.message.reply_text("Koi watch pe nahi hai!")
        return
    txt = "WATCH LIST:\n\n"
    for name in WATCH_LIST.values():
        txt += f"- {name}\n"
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
        await update.message.reply_text(f"{target.first_name} ko SUDO bana diya!")
    else:
        await update.message.reply_text("Ye pehle se hi sudo hai!")

async def sudo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "SUDO LIST:\n\n"
    for uid in SUDO_USERS:
        txt += f"- {uid}\n"
    await update.message.reply_text(txt)

async def autopin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("AUTO-PIN\nGroup: Reply karke /AUTOPIN ON likho\nDM: Reply karke /DMAUTOPIN ON likho")
        return
    action = context.args[0].lower()
    target_id = None
    if len(context.args) >= 2:
        try:
            target_id = int(context.args[1])
        except:
            if update.message.reply_to_message:
                target_id = update.message.reply_to_message.from_user.id
            else:
                await update.message.reply_text("Reply karke likho bhai!")
                return
    else:
        if update.message.reply_to_message:
            target_id = update.message.reply_to_message.from_user.id
        else:
            await update.message.reply_text("Bhai kisi ke message pe REPLY karke /AUTOPIN ON likho, ya ID do - /AUTOPIN ON 123456")
            return
    chat_id = update.effective_chat.id
    if chat_id not in AUTOPIN_GROUPS:
        AUTOPIN_GROUPS[chat_id] = set()
    if action == "on":
        AUTOPIN_GROUPS[chat_id].add(target_id)
        await update.message.reply_text("AUTO-PIN ON ho gaya! Ab iska har naya message auto PIN hoga")
    elif action == "off":
        AUTOPIN_GROUPS[chat_id].discard(target_id)
        await update.message.reply_text("AUTO-PIN OFF ho gaya!")
    else:
        await update.message.reply_text("Sirf ON ya OFF likh bhai! /AUTOPIN ON")

async def dmautopin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Reply karke /DMAUTOPIN ON likho")
        return
    action = context.args[0].lower()
    if update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
    elif len(context.args) >= 2:
        try:
            target_id = int(context.args[1].replace("@",""))
        except:
            await update.message.reply_text("Reply karke likho!")
            return
    else:
        await update.message.reply_text("Reply karke /DMAUTOPIN ON likho!")
        return
    if action == "on":
        AUTOPIN_DM.add(target_id)
        await update.message.reply_text("DM AUTO-PIN ON ho gaya!")
    else:
        AUTOPIN_DM.discard(target_id)
        await update.message.reply_text("DM AUTO-PIN OFF!")

async def auto_pin_watcher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.from_user:
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
