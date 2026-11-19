import os, random, time, datetime, asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReactionTypeEmoji, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatMemberStatus

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8532606474
SUDOS = {8532606474}
START_TIME = time.time()

SUDO_IDS = os.environ.get("SUDO_IDS", "")
if SUDO_IDS:
    for x in SUDO_IDS.split(","):
        if x.strip():
            try: SUDOS.add(int(x.strip()))
            except: pass

def is_allowed(uid: int):
    return uid in SUDOS

async def is_admin(update):
    try:
        m = await update.effective_chat.get_member(update.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False

async def send(update, text):
    try:
        await update.effective_chat.send_message(text)
    except Exception as e:
        print("Send fail:", e)

async def check(update):
    if not is_allowed(update.effective_user.id):
        await send(update, "SORRY GURU! YE BOT SIRF OWNER AUR SUDO KE LIYE HAI 🔒")
        return False
    return True

async def need_admin(update):
    if not await is_admin(update) and update.effective_user.id not in SUDOS:
        await send(update, "GURU YE SIRF ADMIN KAR SAKTA HAI 🔒")
        return False
    return True

# ===== AUTO STORAGE =====
WATCHED = set()
AUTOPIN_CHATS = set()
DMAUTOPIN = set()
AUTOREACT_CHATS = set()
AUTOREACT_EMOJI = "❤️"
SMART_REACT_ON = True  # SMART REACT BY DEFAULT ON HAI GURU!
AUTODELETE_CHATS = {}
AUTOREPLY_CHATS = set()
AUTOBAN_LINK = set()
AUTOBAN_GAALI = set()
WARN_COUNT = {}
AFK_USERS = {}
AUTOTYPE_CHATS = set()
AUTOSAVE_ON = set()
AUTOSHAYARI_CHATS = set()
AUTOGM_CHATS = set()
AUTOGN_CHATS = set()
AUTOANSWER_ON = set()
AUTOPROTECT_CHATS = set()
WELCOME = {}

# ===== SMART REACT - MOOD KE HISAB SE =====
def get_smart_emoji(text: str):
    t = text.lower()
    # PYAR / LOVE
    if any(w in t for w in ["love","pyar","jaan","baby","jaan","miss you","miss u","dil","shayari","kiss","chumma","crush","mohabbat","ishq","jaaneman"]):
        return random.choice(["❤️","😍","🥰","💋","💖","😘"])
    # FUNNY / HASI
    if any(w in t for w in ["haha","hehe","lol","funny","joke","haso","majak","mazak","bakchod","bhai","😂","🤣","chutiya","pagal","bewakoof"]):
        return random.choice(["😂","🤣","😆","😹","🤪"])
    # SAD / RONA
    if any(w in t for w in ["sad","rona","ro raha","dukhi","dil tut","breakup","tuta","akela","tanha","miss","yaad","mar gaya","rona","😢","😭","udaas","tension","depress"]):
        return random.choice(["😢","😭","🥺","💔","🫂"])
    # GUSSA / ANGRY
    if any(w in t for w in ["gussa","bakwas","chup","bhad","gandu","madarchod","behenchod","kutte","saale","harami","chud","bhosd","lund","mc","bc","pagal","hat","nikal"]):
        return random.choice(["😡","🤬","😤","👿","😠"])
    # GOOD MORNING / MORNING
    if any(w in t for w in ["good morning","gm","subah","morning","uth gaya"]):
        return random.choice(["☀️","🌅","😊","👋"])
    # GOOD NIGHT
    if any(w in t for w in ["good night","gn","so raha","neend","sone ja","night"]):
        return random.choice(["🌙","😴","🌜","💤"])
    # BIRTHDAY / PARTY
    if any(w in t for w in ["birthday","bday","party","congrats","badhai","mubarak","jeet","win","top"]):
        return random.choice(["🎉","🎊","🥳","🎂","🔥"])
    # SHOCK / HAIRAN
    if any(w in t for w in ["kya","sach","really","omg","wow","seriously","acha","kya bol","wtf","?"]):
        return random.choice(["😲","😮","😳","🤯","😱"])
    # THANK YOU / ACHA
    if any(w in t for w in ["thank","thanks","shukriya","acha","mast","badiya","great","super","op","nice","awesome","kya baat"]):
        return random.choice(["👍","🔥","👏","💯","❤️‍🔥","😎"])
    # HI / HELLO
    if any(w in t for w in ["hi","hello","hey","hii","heyy","kaise ho","kya haal"]):
        return random.choice(["👋","😊","🔥","😈","❤️"])
    # KHAANA / BHUKH
    if any(w in t for w in ["khana","bhukh","bhook","pizza","chai","coffee","maggi"]):
        return random.choice(["😋","🍕","🍔","☕","🤤"])
    # MUSIC / GAANA
    if any(w in t for w in ["gaana","song","music","gana","sun","suno"]):
        return random.choice(["🎵","🎶","🎧","🎤"])
    # DEFAULT - RANDOM MOOD
    return random.choice(["❤️","🔥","😂","😍","👍","😊","🥰","😎"])

GAALI_LIST = ["madarchod","behenchod","bhosdike","chutiya","gandu","randi","bhenchod","lund","gand"]
REPLY_MAP = {
    "hi": "Hi GURU! Kaise ho? 🔥",
    "hello": "Hello GURU! 😈",
    "hey": "Hey GURU! Bol kya kaam hai?",
    "good morning": "Good Morning GURU! ☀️ Chai pi li?",
    "good night": "Good Night GURU! 😴 Kal milte hai!",
    "kaise ho": "Ekdam mast GURU! Tu bata? 🔥",
    "kaha ho": "GURU yahi hai, bas thoda busy hai! 😈",
    "demon kaha hai": "GURU aata hi hoga! Thoda ruk ja! 🔥",
    "kashyap kaha hai": "GURU aata hi hoga! Thoda ruk ja! 🔥",
    "papa": "PAPA HU ME TERA 😈🔥",
    "love you": "Love you too GURU! ❤️",
    "bye": "Bye GURU! Jaldi aana! 👋",
}

ALL_COMMANDS_TEXT = """🔥 KASHYAP BOT - SARE COMMANDS 🔥
👤 GENERAL: /MYID /PEHCHAN /JANKARI /GROUPID /PING /TEJ /CHALU /BAREME /UPTIME /TAG /MALIK /NIYAM /ANKDA /BOL
😈 PAPA: /PAPA /SHAYARI /JOKE /HASO /PAPABOL /TRUTH /SACH /DARE /HIMMAT
🛡️ MOD: /NIKAL /WAPAS /DHAKKA /CHUP /BOLNEDE /CHETAVNI /MITAO /CHIPKAO /HATAO /TALA /KHOLO /LINKBAND
👋 WELCOME: /SWAGATSET /SWAGATOFF /SWAGATTEST
🎲 GAMES: /PASA /SIKKA /GHUMAO /KAINCHI /JADU /CHUNO /SAWAL /ANK
❤️ FUN: /GALE /THAPPAD /CHUMMA /THAPTHAPAO /PANJA /HATH /PYAR /TARIFF /JODI /VICHAR
🧮 TOOLS: /GIN /ULTA /BADA /CHOTA /GINO /SAMAY /TARIKH /BEHISAAB
👀 WATCH: /WATCH /UNWATCH /WATCHLIST /AUTOPIN /DMAUTOPIN /ART
🤖 AUTO: /AUTOREACT /AUTOREACTSET /SMARTREACT /AUTODELETE /AUTOREPLY /AUTOBAN /AUTOWARN /AFK /BACK /AUTOTYPE /AUTOSAVE /AUTOPURGE /AUTOSHAYARI /AUTOGM /AUTOGN /GM /GN /AUTOBIO /AUTOANSWER /AUTOPROTECT
👑 SUDO: /ADDSUDO /DELSUDO /SUDOLIST
📋 HELP: /HELP /MADAD /COMMAND /COMMANDS /MENU /ALL
TOTAL 95+ 🔥 OWNER: KASHYAP 😈👑
"""

FONT = {
'A': [" . ",". .","...",". .",". ."],'B': [".. ",". .",".. ",". .",".. "],'C': [" ..",".  ",".  ",".  "," .."],'D': [".. ",". .",". .",". .",".. "],'E': ["...",".  ",".. ",".  ","..."],'F': ["...",".  ",".. ",".  ",".  "],'G': [" ..",".  ",". .",". ."," .."],'H': [". .",". .","...",". .",". ."],'I': ["..."," . "," . "," . ","..."],'J': ["..."," . "," . ",". ."," . "],'K': [". .",". .",".. ",". .",". ."],'L': [".  ",".  ",".  ",".  ","..."],'M': [". .","...",". .",". .",". ."],'N': [". .","...",". .",". .",". ."],'O': [" . ",". .",". .",". ."," . "],'P': [".. ",". .",".. ",".  ",".  "],'Q': [" . ",". .",". ."," ..","  ."],'R': [".. ",". .",".. ",". .",". ."],'S': [" ..",".  "," . ","  .",".. "],'T': ["..."," . "," . "," . "," . "],'U': [". .",". .",". .",". ."," . "],'V': [". .",". .",". .",". ."," . "],'W': [". .",". .",". .","...",". ."],'X': [". .",". ."," . ",". .",". ."],'Y': [". .",". ."," . "," . "," . "],'Z': ["...","  ."," . ",".  ","..."],' ': ["   ","   ","   ","   ","   "],
}
def bindi_art(text):
    text = text.upper()[:14]
    lines = [""]*5
    for ch in text:
        f = FONT.get(ch, FONT[' '])
        for i in range(5):
            lines[i] += f[i] + "  "
    return "\n".join(lines)

ARTS_LIST = ["RAM","JAISHREERAM","HANUMAN","MAHAKAL","SHIV","OM","RADHE","KRISHNA","ILOVEYOU","LOVE","HUG","JAAN","BABY","CRUSH","CUTE","PYAR","MISSYOU","HELLO","BYEE","KING","QUEEN","KASHYAP","INDIA","BHARAT","SORRY","THANKYOU","GOODMORNING","GOODNIGHT","HAPPYBIRTHDAY"]
SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Mohabbat me humne khud ko mita diya, tere liye duniya se ladna sikha diya ❤️","Teri aankhon me duniya dekh li, ab aur kisi ki zarurat nahi ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️"]
JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Girlfriend se breakup ho gaya tha. Teacher: To? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Ek ladki ne ladke se kaha: Tum bahut bure ho. Ladka: Thanks, tum bhi bahut buri lag rahi ho aaj 😂","Santa: Meri biwi mujhse bahut pyar karti hai. Banta: Kaise pata? Santa: Jab bhi me ghar late aata hu, wo darwaza khol ke kehti hai - Aa gaya kutta 😂"]
TRUTHS = ["Tera sabse bada crush kaun hai? 😏","Kabhi kisi ka message chupke padha hai?","Sabse embarrassing moment kya tha tera?","Kis se sabse zyada jalte ho?","Apni life ka sabse bada jhooth batao.","Last baar kab roye the aur kyu?"]
DARES = ["Apni DP 1 ghante ke liye badal de 😂","Group me 'PAPA HU ME TERA' likh ke bhej 😈","Apne crush ko Hi bhej ke screenshot bhej 😏","10 baar apna naam zor se bol ke voice bhej","Apni gallery ki last photo group me bhej","Apne best friend ko call karke I Love You bol"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "KASHYAP BOT ON HAI! 🔥 /COMMAND LIKH KE SARE COMMANDS DEKH.")
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def command_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def madad(update, context):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def menu_cmd(update, context):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def all_cmd(update, context):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    username = f"@{u.username}" if u.username else "No Username"
    if u.id == OWNER_ID: tag = "Tu hi MALIK hai GURU! 😈👑"
    elif u.id in SUDOS: tag = "Tu SUDO hai GURU! 🔥"
    else: tag = "Tu Member hai GURU!"
    await send(update, f"━━━━━━━━━━━━━━\n🔥 GURU ID CARD 🔥\n━━━━━━━━━━━━━━\n👤 NAAM: {u.first_name}\n🆔 ID: `{u.id}`\n📎 USERNAME: {username}\n🔗 LINK: tg://user?id={u.id}\n━━━━━━━━━━━━━━\n{tag}")
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PING PONG! KASHYAP BOT LIVE 🔥")
async def papa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PAPA HU ME TERA 😈🔥")
async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, random.choice(SHAYARI))
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, random.choice(JOKES))
async def haso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, random.choice(JOKES))
async def papabol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "PAPA BOL RAHA HAI 🎲\n/TRUTH likh - Sach wala sawal\n/DARE likh - Dare wala task")
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "TRUTH ❓\n" + random.choice(TRUTHS))
async def sach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "SACH ❓\n" + random.choice(TRUTHS))
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "DARE 🔥\n" + random.choice(DARES))
async def himmat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "HIMMAT 🔥\n" + random.choice(DARES))
async def chalu(update, context):
    if not await check(update): return
    await send(update, "KASHYAP BOT ON HAI! 🔥 /COMMAND LIKH KE DEKH.")
async def bareme(update, context):
    if not await check(update): return
    await send(update, "ME HU KASHYAP BOT 😈🔥 Owner: Kashyap")
async def tej(update, context):
    if not await check(update): return
    await send(update, "TEJ HU ME 🔥 PING PONG LIVE!")
async def pehchan(update, context):
    u = update.effective_user
    username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"━━━━━━━━━━━━━━\n🔥 PEHCHAN GURU 🔥\n━━━━━━━━━━━━━━\n👤 NAAM: {u.first_name}\n🆔 ID: `{u.id}`\n📎 USERNAME: {username}\n🔗 LINK: tg://user?id={u.id}\n━━━━━━━━━━━━━━")
async def jankari(update, context):
    if not await check(update): return
    u = update.effective_user; c = update.effective_chat
    username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"━━━━━━━━━━━━━━\n📋 FULL JANKARI GURU 📋\n━━━━━━━━━━━━━━\n👤 NAAM: {u.first_name}\n🆔 ID: `{u.id}`\n📎 USERNAME: {username}\n💬 CHAT: {c.title if c.title else 'DM'}\n💬 CHAT ID: `{c.id}`\n🔗 LINK: tg://user?id={u.id}\n━━━━━━━━━━━━━━")
async def groupid(update, context):
    if not await check(update): return
    await send(update, f"GROUP ID: {update.effective_chat.id}")
async def tag(update, context):
    if not await check(update): return
    if not context.args: await send(update, "AISE: /TAG @username"); return
    await send(update, f"HEY {context.args[0]} PAPA BULA RAHE HAI 😈")
async def malik(update, context):
    if not await check(update): return
    try:
        admins = await update.effective_chat.get_administrators()
        await send(update, "MALIK LOG:\n" + "\n".join([a.user.first_name for a in admins]))
    except: await send(update, "Admin list nahi mili.")
async def niyam(update, context):
    if not await check(update): return
    await send(update, "NIYAM:\n1. Gaali nahi\n2. Link nahi\n3. Admin ki izzat karo")
async def ankda(update, context):
    if not await check(update): return
    await send(update, f"GROUP: {update.effective_chat.title}\nBot Live Hai 🔥")
async def uptime(update, context):
    if not await check(update): return
    await send(update, f"BOT ON HAI: {int(time.time()-START_TIME)//60} MIN SE 🔥")
async def bol(update, context):
    if not await check(update): return
    if context.args: await send(update, " ".join(context.args))
async def nikal(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: await send(update, "Reply karke /NIKAL likh"); return
    try: await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id); await send(update, "NIKAL DIYA! 👋")
    except: await send(update, "Nahi nikal paya, mujhe admin bana.")
async def wapas(update, context):
    if not await need_admin(update): return
    if not context.args: await send(update, "/WAPAS 123456"); return
    try: await update.effective_chat.unban_member(int(context.args[0])); await send(update, "WAPAS AA GAYA!")
    except: await send(update, "Nahi hua.")
async def dhakka(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)
        await update.effective_chat.unban_member(update.message.reply_to_message.from_user.id)
        await send(update, "DHAKKA DE DIYA! 👋")
    except: await send(update, "Nahi hua.")
async def chup(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await send(update, "CHUP KAR DIYA 🤫")
    except: await send(update, "Nahi hua.")
async def bolnede(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await send(update, "AB BOL SAKTA HAI!")
    except: await send(update, "Nahi hua.")
async def chetavni(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message: await send(update, f"⚠️ CHETAVNI! {update.message.reply_to_message.from_user.first_name} Sudhar ja!")
async def mitao(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.delete(); await update.message.delete()
        except: await send(update, "Delete nahi hua.")
async def chipkao(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.pin(); await send(update, "CHIPKA DIYA 📌")
        except: await send(update, "Nahi hua.")
async def hatao(update, context):
    if not await need_admin(update): return
    try: await update.effective_chat.unpin_all_messages(); await send(update, "PIN HATA DIYA")
    except: pass
async def tala(update, context):
    if not await need_admin(update): return
    await send(update, "TALA laga diya 🔒")
async def kholo(update, context):
    if not await need_admin(update): return
    await send(update, "KHOL DIYA 🔓")
async def linkband(update, context):
    if not await need_admin(update): return
    await send(update, "LINK BAND ON! /AUTOBAN ON likh - wo asli wala hai!")
async def linkbandoff(update, context):
    if not await need_admin(update): return
    await send(update, "LINK BAND OFF!")
async def linkbandon(update, context): await linkband(update, context)
async def swagatset(update, context):
    if not await need_admin(update): return
    txt = " ".join(context.args) if context.args else "Welcome {name} 🔥"
    WELCOME[update.effective_chat.id] = txt; await send(update, f"SWAGAT SET: {txt}")
async def swagatoff(update, context):
    if not await need_admin(update): return
    WELCOME.pop(update.effective_chat.id, None); await send(update, "SWAGAT OFF!")
async def swagattest(update, context):
    if not await check(update): return
    txt = WELCOME.get(update.effective_chat.id, "Welcome {name} 🔥")
    await send(update, txt.replace("{name}", update.effective_user.first_name))
async def pasa(update, context):
    if not await check(update): return
    await send(update, f"🎲 PASA: {random.randint(1,6)}")
async def sikka(update, context):
    if not await check(update): return
    await send(update, f"🪙 SIKKA: {random.choice(['HEAD','TAIL'])}")
async def ghumao(update, context):
    if not await check(update): return
    await send(update, f"🎯 NUMBER: {random.randint(1,100)}")
async def kainchi(update, context):
    if not await check(update): return
    await send(update, f"✂️ TUNE: {random.choice(['ROCK','PAPER','SCISSORS'])}")
async def jadu(update, context):
    if not await check(update): return
    if not context.args: await send(update, "/JADU kya hoga?"); return
    await send(update, random.choice(["Haan ✅","Nahi ❌","Pakka 🔥","Socho mat, kar de 😈"]))
async def chuno(update, context):
    if not await check(update): return
    if not context.args: await send(update, "/CHUNO chai coffee"); return
    await send(update, f"ME CHUNTA HU: {random.choice(context.args)}")
async def sawal(update, context):
    if not await check(update): return
    await send(update, "SAWAL: Bharat ki rajdhani kya hai?\nA) Delhi B) Mumbai C) Goa")
async def ank(update, context):
    if not await check(update): return
    await send(update, f"ANK: {random.randint(1,1000)}")
async def fun_reply(update, txt):
    if not update.message.reply_to_message: await send(update, "Kisi pe reply karke bhej!"); return
    await send(update, txt.format(name=update.message.reply_to_message.from_user.first_name))
async def gale(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko GALE laga liya 🤗")
async def thappad(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko THAPPAD mara 😂👋")
async def chumma(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko CHUMMA diya 😘")
async def thapthapao(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko THAPTHAPAYA 👏")
async def panja(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} se PANJA milaya 🤝")
async def hath(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko HATH hilaya 👋")
async def pyar(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} se PYAR hai ❤️")
async def tariff(update, context):
    if not await check(update): return
    await fun_reply(update, random.choice(['Tu bahut smart hai 🔥','Teri smile best hai ❤️','Tu group ki jaan hai 😈']) + " {name}")
async def jodi(update, context):
    if not await check(update): return
    await send(update, f"JODI: {update.effective_user.first_name} ❤️ {random.choice(['Kashyap','Demon','Angel','Cutie'])} - {random.randint(50,99)}% MATCH!")
async def vichar(update, context):
    if not await check(update): return
    await send(update, random.choice(["Zindagi me aage badho 🔥","Mehnat karo, Kashyap jaisa bano 😈","Hasna sabse badi dawa hai ❤️"]))
async def gin(update, context):
    if not await check(update): return
    if not context.args: await send(update, "/GIN 2+2"); return
    try: await send(update, f"JAWAB: {eval(' '.join(context.args))}")
    except: await send(update, "Galat hisaab.")
async def ulta(update, context):
    if not await check(update): return
    if context.args: await send(update, " ".join(context.args)[::-1])
async def bada(update, context):
    if not await check(update): return
    if context.args: await send(update, " ".join(context.args).upper())
async def chota(update, context):
    if not await check(update): return
    if context.args: await send(update, " ".join(context.args).lower())
async def gino(update, context):
    if not await check(update): return
    if context.args: await send(update, f"LETTERS: {len(' '.join(context.args))}")
async def samay(update, context):
    if not await check(update): return
    await send(update, f"SAMAY: {datetime.datetime.now().strftime('%H:%M:%S')}")
async def tarikh(update, context):
    if not await check(update): return
    await send(update, f"TARIKH: {datetime.datetime.now().strftime('%d/%m/%Y')}")
async def behisaab(update, context):
    if not await check(update): return
    await send(update, f"BEHISAAB: {random.randint(1,999)}")
async def addsudo(update, context):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI"); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE LIKH: /ADDSUDO 123456\nYa reply karke /ADDSUDO"); return
    SUDOS.add(uid); await send(update, f"HO GAYA! {uid} AB SUDO HAI 🔥")
async def delsudo(update, context):
    if update.effective_user.id != OWNER_ID:
        await send(update, "SIRF OWNER KAR SAKTA HAI"); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE LIKH: /DELSUDO 123456"); return
    if uid == OWNER_ID:
        await send(update, "OWNER KO NAHI HATA SAKTE"); return
    SUDOS.discard(uid); await send(update, f"HATA DIYA! {uid} AB SUDO NAHI HAI")
async def sudolist(update, context):
    if not await check(update): return
    await send(update, "SUDO LIST:\n" + "\n".join(str(x) for x in SUDOS))
async def watch(update, context):
    if not await check(update): return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE: /WATCH 123456\nYa reply karke /WATCH"); return
    WATCHED.add(uid); await send(update, f"👀 WATCH ON! {uid} pe nazar hai GURU!")
async def unwatch(update, context):
    if not await check(update): return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, "AISE: /UNWATCH 123456"); return
    WATCHED.discard(uid); await send(update, f"👀 WATCH OFF! {uid} se nazar hata di.")
async def watchlist(update, context):
    if not await check(update): return
    if not WATCHED: await send(update, "WATCHLIST KHALI HAI GURU 👀"); return
    await send(update, "👀 WATCHLIST:\n" + "\n".join(str(x) for x in WATCHED))
async def autopin(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPIN_CHATS.discard(update.effective_chat.id); await send(update, "AUTOPIN OFF! 📌"); return
    AUTOPIN_CHATS.add(update.effective_chat.id); await send(update, "AUTOPIN ON! 📌 Ab is chat me har msg auto pin hoga GURU!")
async def dmautopin(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        DMAUTOPIN.discard(update.effective_user.id); await send(update, "DMAUTOPIN OFF"); return
    DMAUTOPIN.add(update.effective_user.id); await send(update, "DMAUTOPIN ON 📌")
async def art(update, context):
    if not await check(update): return
    if not context.args:
        txt = "BINDI ART LIST GURU:\n\n"
        for a in ARTS_LIST: txt += f"/ART {a}\n"
        txt += "\nYa /ART apna naam likh"; await send(update, txt); return
    name = " ".join(context.args); art_text = bindi_art(name)
    await send(update, f"```\n{art_text}\n```")

# ===== SMART AUTO COMMANDS =====
async def autoreact(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREACT_CHATS.discard(update.effective_chat.id); await send(update, "AUTOREACT OFF! ❌"); return
    AUTOREACT_CHATS.add(update.effective_chat.id)
    await send(update, f"SMART AUTOREACT ON! 🧠❤️ Ab mood ke hisab se react karunga!\nPyar pe ❤️, Funny pe 😂, Sad pe 😢, Gussa pe 😡, GM pe ☀️\nAb koi msg likh ke dekho!")
async def smartreact(update, context):
    global SMART_REACT_ON
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        SMART_REACT_ON = False; await send(update, "SMART REACT OFF! Ab sirf ek hi emoji se react karunga. /AUTOREACTSET se emoji badal lo."); return
    SMART_REACT_ON = True; await send(update, "SMART REACT ON! 🧠 Ab mood ke hisab se alag-alag react karunga GURU!")
async def autoreactset(update, context):
    global AUTOREACT_EMOJI, SMART_REACT_ON
    if not await check(update): return
    if not context.args: await send(update, f"Abhi: {AUTOREACT_EMOJI}\n/AUTOREACTSET 🔥 likh - Smart OFF ho jayega aur yahi emoji aayega."); return
    AUTOREACT_EMOJI = context.args[0]; SMART_REACT_ON = False; await send(update, f"FIXED EMOJI SET! Ab har baar {AUTOREACT_EMOJI} hi aayega. Smart wapas chahiye to /SMARTREACT ON likh!")
async def autodelete(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTODELETE_CHATS.pop(update.effective_chat.id, None); await send(update, "AUTODELETE OFF! ❌"); return
    sec = 10
    if context.args:
        try: sec = int(context.args[0])
        except: pass
    AUTODELETE_CHATS[update.effective_chat.id] = sec
    await send(update, f"AUTODELETE ON! ⏳ Har msg {sec} sec baad delete hoga!")
async def autoreply(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREPLY_CHATS.discard(update.effective_chat.id); await send(update, "AUTOREPLY OFF! ❌"); return
    AUTOREPLY_CHATS.add(update.effective_chat.id); await send(update, "AUTOREPLY ON! 🤖 Ab koi 'hi' likhega to jawab dunga!")
async def autoban(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOBAN_LINK.discard(update.effective_chat.id); AUTOBAN_GAALI.discard(update.effective_chat.id); await send(update, "AUTOBAN OFF! ❌"); return
    AUTOBAN_LINK.add(update.effective_chat.id); AUTOBAN_GAALI.add(update.effective_chat.id); await send(update, "AUTOBAN ON! 🔥 Link/Gaali pe delete + warn!")
async def autowarn(update, context):
    if not await check(update): return
    if not WARN_COUNT: await send(update, "Abhi kisi ko warn nahi mila GURU!"); return
    txt = "⚠️ WARN LIST:\n"
    for k,v in WARN_COUNT.items(): txt += f"{k} : {v}/3 warn\n"
    await send(update, txt)
async def afk(update, context):
    if not await check(update): return
    reason = " ".join(context.args) if context.args else "Busy hu GURU!"
    AFK_USERS[update.effective_user.id] = reason
    await send(update, f"AFK ON! 😴 {update.effective_user.first_name} ab AFK hai: {reason}")
async def back(update, context):
    if update.effective_user.id in AFK_USERS:
        AFK_USERS.pop(update.effective_user.id); await send(update, "WELCOME BACK GURU! 🔥 AFK khatam!")
    else: await send(update, "Tu AFK tha hi nahi GURU!")
async def autotype(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOTYPE_CHATS.discard(update.effective_chat.id); await send(update, "AUTOTYPE OFF! ❌"); return
    AUTOTYPE_CHATS.add(update.effective_chat.id); await send(update, "AUTOTYPE ON! ⌨️")
async def autosave(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSAVE_ON.discard(update.effective_user.id); await send(update, "AUTOSAVE OFF! ❌"); return
    AUTOSAVE_ON.add(update.effective_user.id); await send(update, "AUTOSAVE ON! 💾")
async def autopurge(update, context):
    if not await need_admin(update): return
    await send(update, "AUTOPURGE ON! 🧹 /AUTODELETE 10 kar de - sab auto delete hoga!")
async def purge(update, context):
    if not await need_admin(update): return
    await send(update, "PURGE ke liye /AUTODELETE 10 likh de GURU!")
async def autoshayari(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSHAYARI_CHATS.discard(update.effective_chat.id); await send(update, "AUTOSHAYARI OFF! ❌"); return
    AUTOSHAYARI_CHATS.add(update.effective_chat.id); await send(update, "AUTOSHAYARI ON! ❤️")
    await send(update, random.choice(SHAYARI))
async def autogm(update, context):
    if not await need_admin(update): return
    AUTOGM_CHATS.add(update.effective_chat.id); await send(update, "AUTOGM ON! ☀️ Ab /GM likh ke dekho!")
async def autogn(update, context):
    if not await need_admin(update): return
    AUTOGN_CHATS.add(update.effective_chat.id); await send(update, "AUTOGN ON! 🌙 Ab /GN likh ke dekho!")
async def gm(update, context):
    if not await check(update): return
    await send(update, "Good Morning GURU! ☀️🔥 Chai pi li? Aaj ka din tera hai!")
async def gn(update, context):
    if not await check(update): return
    await send(update, "Good Night GURU! 😴❤️ Kal subah milte hai!")
async def autobio(update, context):
    if not await check(update): return
    await send(update, f"AUTOBIO: Bot bio nahi badal sakta GURU! Telegram ka rule hai. Time: {datetime.datetime.now().strftime('%H:%M')}")
async def autoanswer(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOANSWER_ON.discard(update.effective_chat.id); await send(update, "AUTOANSWER OFF! ❌"); return
    AUTOANSWER_ON.add(update.effective_chat.id); await send(update, "AUTOANSWER ON! 🤖 Ab koi 'Demon kaha hai' likhega to jawab dunga!")
async def autoprotect(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPROTECT_CHATS.discard(update.effective_chat.id); await send(update, "AUTOPROTECT OFF! ❌"); return
    AUTOPROTECT_CHATS.add(update.effective_chat.id); await send(update, "AUTOPROTECT ON! 🛡️")

async def delete_later(chat_id, msg_id, sec):
    await asyncio.sleep(sec)
    try:
        await app_bot.delete_message(chat_id, msg_id)
    except: pass

async def auto_watcher(update, context):
    try:
        msg = update.message
        if not msg: return
        if msg.from_user and msg.from_user.is_bot: return
        chat_id = update.effective_chat.id
        user = update.effective_user
        text = (msg.text or "").lower() if msg.text else ""
        orig_text = msg.text or ""
        print(f"AUTO WATCH: Chat {chat_id} User {user.id} Text: {orig_text[:50]} | REACT:{chat_id in AUTOREACT_CHATS} SMART:{SMART_REACT_ON}")
        if orig_text.startswith("."):
            cmd = orig_text[1:].split()[0].lower()
            if cmd in ["command","commands","help","madad","menu","all"]:
                await send(update, ALL_COMMANDS_TEXT)
                return
        if user.id in WATCHED and user.id not in SUDOS:
            await send(update, f"👀 WATCH ALERT! {user.first_name} ({user.id}) ne bola: {orig_text[:100] if orig_text else 'Media bheja'}")
        if msg.reply_to_message and msg.reply_to_message.from_user.id in AFK_USERS:
            await send(update, f"😴 {msg.reply_to_message.from_user.first_name} abhi AFK hai GURU! Wajah: {AFK_USERS[msg.reply_to_message.from_user.id]}")
        if chat_id in AUTOTYPE_CHATS:
            try: await context.bot.send_chat_action(chat_id, "typing")
            except: pass
        # ===== SMART REACT - YAHI MAIN HAI =====
        if chat_id in AUTOREACT_CHATS:
            try:
                if SMART_REACT_ON:
                    emoji_to_use = get_smart_emoji(orig_text)
                else:
                    emoji_to_use = AUTOREACT_EMOJI
                await context.bot.set_message_reaction(chat_id, msg.message_id, reaction=[ReactionTypeEmoji(emoji=emoji_to_use)])
                print(f"REACT DONE: {emoji_to_use} for text: {orig_text[:30]}")
            except Exception as e:
                print(f"REACT FAIL: {e}")
        if chat_id in AUTOPIN_CHATS or user.id in DMAUTOPIN:
            try: await msg.pin(disable_notification=True)
            except Exception as e: print(f"PIN FAIL: {e}")
        if chat_id in AUTOBAN_LINK and ("http" in text or "t.me" in text or "www." in text) and user.id not in SUDOS:
            try: await msg.delete()
            except: pass
            await send(update, f"⚠️ {user.first_name} Link bhejna mana hai GURU! Msg delete kar diya!")
            return
        if chat_id in AUTOBAN_GAALI and user.id not in SUDOS:
            for g in GAALI_LIST:
                if g in text:
                    WARN_COUNT[user.id] = WARN_COUNT.get(user.id, 0) + 1
                    w = WARN_COUNT[user.id]
                    if w >= 3:
                        try: await update.effective_chat.ban_member(user.id); await send(update, f"🚫 {user.first_name} ko 3 warn pe BAN kar diya!")
                        except: await send(update, f"⚠️ {user.first_name} 3 warn ho gaye! Mujhe admin banao!")
                        WARN_COUNT[user.id] = 0
                    else:
                        try: await msg.delete()
                        except: pass
                        await send(update, f"⚠️ WARN {w}/3 {user.first_name}! Gaali mat de GURU!")
                    return
        if chat_id in AUTOREPLY_CHATS or chat_id in AUTOANSWER_ON:
            for k, v in REPLY_MAP.items():
                if k in text:
                    await send(update, v)
                    break
        if msg.photo or msg.video or msg.document:
            if OWNER_ID in AUTOSAVE_ON or user.id in AUTOSAVE_ON:
                try: await context.bot.send_message(OWNER_ID, f"💾 AUTOSAVE! {user.first_name} ne media bheja - Chat: {update.effective_chat.title}")
                except: pass
        if chat_id in AUTODELETE_CHATS:
            sec = AUTODELETE_CHATS[chat_id]
            asyncio.create_task(delete_later(chat_id, msg.message_id, sec))
    except Exception as e:
        print("Watcher error:", e)

async def new_member_handler(update, context):
    try:
        for m in update.message.new_chat_members:
            if m.is_bot and update.effective_chat.id in AUTOPROTECT_CHATS:
                await send(update, f"🛡️ AUTOPROTECT ALERT! Naya bot {m.first_name} add hua hai GURU!")
            if update.effective_chat.id in WELCOME:
                txt = WELCOME[update.effective_chat.id]
                await send(update, txt.replace("{name}", m.first_name))
    except: pass

app_bot = None
def main():
    global app_bot
    app = ApplicationBuilder().token(TOKEN).build()
    app_bot = app.bot
    cmds = {"start": start, "help": help_cmd, "command": command_cmd, "commands": command_cmd, "madad": madad, "menu": menu_cmd, "all": all_cmd, "myid": myid, "ping": ping, "papa": papa, "shayari": shayari, "joke": joke, "haso": haso, "papabol": papabol, "truth": truth, "sach": sach, "dare": dare, "himmat": himmat, "chalu": chalu, "bareme": bareme, "tej": tej, "pehchan": pehchan, "jankari": jankari, "groupid": groupid, "tag": tag, "malik": malik, "niyam": niyam, "ankda": ankda, "uptime": uptime, "bol": bol, "nikal": nikal, "wapas": wapas, "dhakka": dhakka, "chup": chup, "bolnede": bolnede, "chetavni": chetavni, "mitao": mitao, "chipkao": chipkao, "hatao": hatao, "tala": tala, "kholo": kholo, "linkband": linkband, "linkbandoff": linkbandoff, "linkbandon": linkbandon, "swagatset": swagatset, "swagatoff": swagatoff, "swagattest": swagattest, "pasa": pasa, "sikka": sikka, "ghumao": ghumao, "kainchi": kainchi, "jadu": jadu, "chuno": chuno, "sawal": sawal, "ank": ank, "gale": gale, "thappad": thappad, "chumma": chumma, "thapthapao": thapthapao, "panja": panja, "hath": hath, "pyar": pyar, "tariff": tariff, "jodi": jodi, "vichar": vichar, "gin": gin, "ulta": ulta, "bada": bada, "chota": chota, "gino": gino, "samay": samay, "tarikh": tarikh, "behisaab": behisaab, "addsudo": addsudo, "delsudo": delsudo, "sudolist": sudolist, "watch": watch, "unwatch": unwatch, "watchlist": watchlist, "autopin": autopin, "dmautopin": dmautopin, "art": art, "autoreact": autoreact, "smartreact": smartreact, "autoreactset": autoreactset, "autodelete": autodelete, "autoreply": autoreply, "autoban": autoban, "autowarn": autowarn, "afk": afk, "back": back, "autotype": autotype, "autosave": autosave, "autopurge": autopurge, "purge": purge, "autoshayari": autoshayari, "autogm": autogm, "autogn": autogn, "gm": gm, "gn": gn, "autobio": autobio, "autoanswer": autoanswer, "autoprotect": autoprotect}
    for n, fn in cmds.items(): app.add_handler(CommandHandler(n, fn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_watcher), group=1)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    print("KASHYAP BOT STARTED - SUDOS:", SUDOS)
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__":
    main()
