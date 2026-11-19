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

# ===== AESTHETIC ENGINE =====
FANCY_MAP = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
def fancy(t: str):
    return t.translate(FANCY_MAP)
def box(text: str):
    return f"╭━━━━━━━━━━━━╮\n┃ {text} ┃\n╰━━━━━━━━━━━━╯"

async def send(update, text):
    try:
        await update.effective_chat.send_message(text)
    except Exception as e:
        print("Send fail:", e)

async def check(update):
    if not is_allowed(update.effective_user.id):
        await send(update, "╭━━━━━━━━━━━━╮\n┃ 🔒 𝐒𝐎𝐑𝐑𝐘 𝐆𝐔𝐑𝐔! 𝐎𝐍𝐋𝐘 𝐎𝐖𝐍𝐄𝐑 / 𝐒𝐔𝐃𝐎 ┃\n╰━━━━━━━━━━━━╯")
        return False
    return True

async def need_admin(update):
    if not await is_admin(update) and update.effective_user.id not in SUDOS:
        await send(update, box("🔒 𝐆𝐔𝐑𝐔 𝐘𝐄 𝐒𝐈𝐑𝐅 𝐀𝐃𝐌𝐈𝐍 𝐊𝐀𝐑 𝐒𝐀𝐊𝐓𝐀 𝐇𝐀𝐈"))
        return False
    return True

# ===== AUTO STORAGE =====
WATCHED = set()
AUTOPIN_CHATS = set()
DMAUTOPIN = set()
AUTOREACT_CHATS = set()
AUTOREACT_EMOJI = "❤️"
SMART_REACT_ON = True
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

# ===== TARUN DADA BUSY MODE - FINAL =====
TARUN_BUSY_ON = True
TARUN_BUSY_MSG = "╭━━━━━━━━━━━━━━━━━━━━━╮\n┃ 😈 TARUN DADA ABHI BUSY HAI BACCHO! ┃\n┃ BAAD ME AAYENGE VO, TAB BAAT KAR LENA! 🔥 ┃\n╰━━━━━━━━━━━━━━━━━━━━━╯"
TARUN_IDS_USERNAMES = ["sm302mp17", "u_r_not_type"]
TARUN_TRIGGERS = [
    "@sm302mp17", "@u_r_not_type",
    "sm302mp17", "u_r_not_type",
    "tarun", "tallu", "tarun kaha hai", "tarun kaha", "tarun kaha ho",
    "billa", "bhaii", "bebyy", "bebby", "bebyy bhaii", "bebby bhaii",
    "tarun bebby", "tarun bebby sun na", "tarun bebby sun na", "tarun dada", "dada"
]

# ===== BIO ROTATION - ALAG ALAG MAST BIO =====
AUTOBIO_ON = False
AUTOBIO_INDEX = 0
AUTOBIO_LIST = [
    "🔥 KASHYAP BOT 😈 | PAPA HU ME TERA",
    "💀 DEMON MODE ON | KASHYAP IS HERE",
    "👑 KING OF TELEGRAM | KASHYAP 👑",
    "❤️ PYAR MOHABBAT SAB DHOKA HAI",
    "😈 CHAOTIC ENERGY | DON'T MESS WITH ME",
    "⚡ TEJ HU ME | KASHYAP BOT LIVE 🔥",
    "🌙 RAAT KA RAJA | DIN KA BADSHAH",
    "🎭 DUNIA GOL HAI | ME USKA CENTRE HU",
    "💔 DIL TUTA HUA | PAR ATTITUDE FULL HAI",
    "🚀 ROCKET JAISE UDEGA | KASHYAP BOT",
    "🦁 SHER HU ME | JUNGLE KA RAJA",
    "😎 ATTITUDE KING | KASHYAP BOT 😎",
    "🔥 JALNE WALO JALO | ME TO CHAMKUNGA",
    "💯 100% REAL | NO FAKE | KASHYAP",
    "🎲 ZINDAGI EK GAME HAI | ME USKA PLAYER",
    "🖤 BLACK HEART | WHITE SOUL | KASHYAP",
    "⚔️ WARRIOR MODE ON | KASHYAP BOT",
    "🌟 STAR HU ME | AASMAN KA SABSE BRIGHT",
    "😂 HASI KE LIYE BANA HU | RULANE KE LIYE NAHI",
    "👊 DUSHMANO KE LIYE KHATRA | DOSTO KE LIYE JAAN",
    "😈 TARUN DADA ABHI BUSY HAI BACCHO! 🔥",
]

def get_smart_emoji(text: str):
    t = text.lower()
    if any(w in t for w in ["love","pyar","jaan","baby","miss you","miss u","dil","shayari","kiss","chumma","crush","mohabbat","ishq"]):
        return random.choice(["❤️","😍","🥰","💋","💖","😘"])
    if any(w in t for w in ["haha","hehe","lol","funny","joke","haso","majak","mazak","😂","🤣","pagal"]):
        return random.choice(["😂","🤣","😆","😹","🤪"])
    if any(w in t for w in ["sad","rona","dukhi","dil tut","breakup","tuta","akela","tanha","miss","yaad","udaas","tension","depress"]):
        return random.choice(["😢","😭","🥺","💔","🫂"])
    if any(w in t for w in ["gussa","bakwas","chup","bhad","gandu","madarchod","behenchod","kutte","saale","harami","mc","bc"]):
        return random.choice(["😡","🤬","😤","👿","😠"])
    if any(w in t for w in ["good morning","gm","subah","morning"]):
        return random.choice(["☀️","🌅","😊","👋"])
    if any(w in t for w in ["good night","gn","so raha","neend","sone ja"]):
        return random.choice(["🌙","😴","🌜","💤"])
    if any(w in t for w in ["birthday","bday","party","congrats","badhai","mubarak","jeet","win"]):
        return random.choice(["🎉","🎊","🥳","🎂","🔥"])
    if any(w in t for w in ["thank","thanks","shukriya","acha","mast","badiya","great","super","op","nice","awesome"]):
        return random.choice(["👍","🔥","👏","💯","❤️‍🔥","😎"])
    if any(w in t for w in ["hi","hello","hey","kaise ho"]):
        return random.choice(["👋","😊","🔥","😈","❤️"])
    return random.choice(["❤️","🔥","😂","😍","👍","😊","🥰","😎"])

GAALI_LIST = ["madarchod","behenchod","bhosdike","chutiya","gandu","randi","bhenchod","lund","gand"]
REPLY_MAP = {
    "hi": "╭━━━━━━━━━━━━╮\n┃ 𝐇𝐢 𝐆𝐔𝐑𝐔! 𝐊𝐚𝐢𝐬𝐞 𝐇𝐨? 🔥 ┃\n╰━━━━━━━━━━━━╯",
    "hello": "╭━━━━━━━━━━━━╮\n┃ 𝐇𝐞𝐥𝐥𝐨 𝐆𝐔𝐑𝐔! 😈 ┃\n╰━━━━━━━━━━━━╯",
    "hey": "╭━━━━━━━━━━━━╮\n┃ 𝐇𝐞𝐲 𝐆𝐔𝐑𝐔! 𝐁𝐨𝐥 𝐊𝐲𝐚 𝐊𝐚𝐚𝐦 𝐇𝐚𝐢? ┃\n╰━━━━━━━━━━━━╯",
    "good morning": "╭━━━━━━━━━━━━╮\n┃ ☀️ 𝐆𝐨𝐨𝐝 𝐌𝐨𝐫𝐧𝐢𝐧𝐠 𝐆𝐔𝐑𝐔! 𝐂𝐡𝐚𝐢 𝐏𝐢 𝐋𝐢? ┃\n╰━━━━━━━━━━━━╯",
    "good night": "╭━━━━━━━━━━━━╮\n┃ 🌙 𝐆𝐨𝐨𝐝 𝐍𝐢𝐠𝐡𝐭 𝐆𝐔𝐑𝐔! 😴 ┃\n╰━━━━━━━━━━━━╯",
    "kaise ho": "╭━━━━━━━━━━━━╮\n┃ 𝐄𝐤𝐝𝐚𝐦 𝐌𝐚𝐬𝐭 𝐆𝐔𝐑𝐔! 𝐓𝐮 𝐁𝐚𝐭𝐚? 🔥 ┃\n╰━━━━━━━━━━━━╯",
    "kaha ho": "╭━━━━━━━━━━━━╮\n┃ 𝐆𝐔𝐑𝐔 𝐘𝐚𝐡𝐢 𝐇𝐚𝐢, 𝐁𝐚𝐬 𝐓𝐡𝐨𝐝𝐚 𝐁𝐮𝐬𝐲 𝐇𝐚𝐢! 😈 ┃\n╰━━━━━━━━━━━━╯",
    "demon kaha hai": "╭━━━━━━━━━━━━╮\n┃ 𝐆𝐔𝐑𝐔 𝐀𝐚𝐭𝐚 𝐇𝐢 𝐇𝐨𝐠𝐚! 𝐓𝐡𝐨𝐝𝐚 𝐑𝐮𝐤 𝐉𝐚! 🔥 ┃\n╰━━━━━━━━━━━━╯",
    "kashyap kaha hai": "╭━━━━━━━━━━━━╮\n┃ 𝐆𝐔𝐑𝐔 𝐀𝐚𝐭𝐚 𝐇𝐢 𝐇𝐨𝐠𝐚! 𝐓𝐡𝐨𝐝𝐚 𝐑𝐮𝐤 𝐉𝐚! 🔥 ┃\n╰━━━━━━━━━━━━╯",
    "papa": "╭━━━━━━━━━━━━╮\n┃ 𝐏𝐀𝐏𝐀 𝐇𝐔 𝐌𝐄 𝐓𝐄𝐑𝐀 😈🔥 ┃\n╰━━━━━━━━━━━━╯",
    "love you": "╭━━━━━━━━━━━━╮\n┃ ❤️ 𝐋𝐨𝐯𝐞 𝐘𝐨𝐮 𝐓𝐨𝐨 𝐆𝐔𝐑𝐔! ┃\n╰━━━━━━━━━━━━╯",
    "bye": "╭━━━━━━━━━━━━╮\n┃ 👋 𝐁𝐲𝐞 𝐆𝐔𝐑𝐔! 𝐉𝐚𝐥𝐝𝐢 𝐀𝐚𝐧𝐚! ┃\n╰━━━━━━━━━━━━╯",
}

ALL_COMMANDS_TEXT = """╔════════════════════╗
║ 🔥 𝐊𝐀𝐒𝐇𝐘𝐀𝐏 𝐁𝐎𝐓 🔥 ║
╚════════════════════╝
━━━━━━━━━━━━━━━━━━
👤 𝐆𝐄𝐍𝐄𝐑𝐀𝐋
/MYID /PEHCHAN /JANKARI /GROUPID /PING /TEJ /CHALU /BAREME /UPTIME /TAG /MALIK /NIYAM /ANKDA /BOL
━━━━━━━━━━━━━━━━━━
😈 𝐏𝐀𝐏𝐀 𝐖𝐀𝐋𝐄
/PAPA /SHAYARI /JOKE /HASO /PAPABOL /TRUTH /SACH /DARE /HIMMAT
━━━━━━━━━━━━━━━━━━
🛡️ 𝐌𝐎𝐃𝐄𝐑𝐀𝐓𝐈𝐎𝐍
/NIKAL /WAPAS /DHAKKA /CHUP /BOLNEDE /CHETAVNI /MITAO /CHIPKAO /HATAO /TALA /KHOLO /LINKBAND
━━━━━━━━━━━━━━━━━━
👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄
/SWAGATSET /SWAGATOFF /SWAGATTEST
━━━━━━━━━━━━━━━━━━
🎲 𝐆𝐀𝐌𝐄𝐒
/PASA /SIKKA /GHUMAO /KAINCHI /JADU /CHUNO /SAWAL /ANK
━━━━━━━━━━━━━━━━━━
❤️ 𝐅𝐔𝐍
/GALE /THAPPAD /CHUMMA /THAPTHAPAO /PANJA /HATH /PYAR /TARIFF /JODI /VICHAR
━━━━━━━━━━━━━━━━━━
🧮 𝐓𝐎𝐎𝐋𝐒
/GIN /ULTA /BADA /CHOTA /GINO /SAMAY /TARIKH /BEHISAAB
━━━━━━━━━━━━━━━━━━
👀 𝐖𝐀𝐓𝐂𝐇
/WATCH /UNWATCH /WATCHLIST /AUTOPIN /DMAUTOPIN /ART
━━━━━━━━━━━━━━━━━━
🤖 𝐀𝐔𝐓𝐎 - 𝐒𝐌𝐀𝐑𝐓
/AUTOREACT /AUTOREACTSET /SMARTREACT /AUTODELETE /AUTOREPLY /AUTOBAN /AUTOWARN /AFK /BACK /AUTOTYPE /AUTOSAVE /AUTOPURGE /AUTOSHAYARI /AUTOGM /AUTOGN /GM /GN /AUTOBIO /AUTOANSWER /AUTOPROTECT /TARUNBUSY /TARUNFREE
━━━━━━━━━━━━━━━━━━
👑 𝐒𝐔𝐃𝐎
/ADDSUDO /DELSUDO /SUDOLIST
━━━━━━━━━━━━━━━━━━
📋 𝐇𝐄𝐋𝐏
/HELP /MADAD /COMMAND /COMMANDS /MENU /ALL
━━━━━━━━━━━━━━━━━━
𝐓𝐎𝐓𝐀𝐋 𝟗𝟓+ 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 🔥 𝐎𝐖𝐍𝐄𝐑: 𝐊𝐀𝐒𝐇𝐘𝐀𝐏 😈👑
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
    await send(update, box(fancy("KASHYAP BOT ON HAI!") + " 🔥\n" + fancy("/COMMAND LIKH KE SARE DEKH")))
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
    await send(update, f"╔══════════════╗\n║ 🔥 {fancy('GURU ID CARD')} 🔥 ║\n╚══════════════╝\n👤 {fancy('NAAM')}: {fancy(u.first_name)}\n🆔 {fancy('ID')}: `{u.id}`\n📎 {fancy('USERNAME')}: {username}\n🔗 {fancy('LINK')}: tg://user?id={u.id}\n━━━━━━━━━━━━━━\n{tag}")
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, box(fancy("PING PONG! BOT LIVE") + " 🔥"))
async def papa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, box(fancy("PAPA HU ME TERA") + " 😈🔥"))
async def shayari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"✦ ❤️ {fancy(random.choice(SHAYARI))} ❤️ ✦")
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"😂 {random.choice(JOKES)}")
async def haso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"😂 {random.choice(JOKES)}")
async def papabol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, box(fancy("PAPA BOL RAHA HAI") + " 🎲\n/TRUTH - Sach\n/DARE - Dare"))
async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"❓ {fancy('TRUTH')} ❓\n{random.choice(TRUTHS)}")
async def sach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"❓ {fancy('SACH')} ❓\n{random.choice(TRUTHS)}")
async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"🔥 {fancy('DARE')} 🔥\n{random.choice(DARES)}")
async def himmat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, f"🔥 {fancy('HIMMAT')} 🔥\n{random.choice(DARES)}")
async def chalu(update, context):
    if not await check(update): return
    await send(update, box(fancy("BOT ON HAI!") + " 🔥"))
async def bareme(update, context):
    if not await check(update): return
    await send(update, box(fancy("ME HU KASHYAP BOT") + " 😈🔥 Owner: Kashyap"))
async def tej(update, context):
    if not await check(update): return
    await send(update, box(fancy("TEJ HU ME") + " 🔥"))
async def pehchan(update, context):
    u = update.effective_user
    username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"╔══════════════╗\n║ 🔥 {fancy('PEHCHAN GURU')} 🔥 ║\n╚══════════════╝\n👤 {fancy(u.first_name)}\n🆔 `{u.id}`\n📎 {username}")
async def jankari(update, context):
    if not await check(update): return
    u = update.effective_user; c = update.effective_chat
    username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"╔══════════════╗\n║ 📋 {fancy('FULL JANKARI')} 📋 ║\n╚══════════════╝\n👤 {fancy(u.first_name)}\n🆔 `{u.id}`\n📎 {username}\n💬 {c.title if c.title else 'DM'}\n💬 CHAT ID: `{c.id}`")
async def groupid(update, context):
    if not await check(update): return
    await send(update, box(f"GROUP ID: {update.effective_chat.id}"))
async def tag(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("AISE: /TAG @username")); return
    await send(update, box(f"HEY {context.args[0]} PAPA BULA RAHE HAI 😈"))
async def malik(update, context):
    if not await check(update): return
    try:
        admins = await update.effective_chat.get_administrators()
        await send(update, box(fancy("MALIK LOG:") + "\n" + "\n".join([a.user.first_name for a in admins])))
    except: await send(update, box("Admin list nahi mili."))
async def niyam(update, context):
    if not await check(update): return
    await send(update, "╔══════════════╗\n║ 📜 " + fancy("NIYAM") + " ║\n╚══════════════╝\n1. Gaali nahi\n2. Link nahi\n3. Admin ki izzat karo")
async def ankda(update, context):
    if not await check(update): return
    await send(update, box(f"GROUP: {update.effective_chat.title} - Bot Live 🔥"))
async def uptime(update, context):
    if not await check(update): return
    await send(update, box(f"BOT ON HAI: {int(time.time()-START_TIME)//60} MIN SE 🔥"))
async def bol(update, context):
    if not await check(update): return
    if context.args: await send(update, box(fancy(" ".join(context.args))))
async def nikal(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: await send(update, box("Reply karke /NIKAL likh")); return
    try: await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id); await send(update, box("NIKAL DIYA! 👋"))
    except: await send(update, box("Nahi nikal paya, mujhe admin bana."))
async def wapas(update, context):
    if not await need_admin(update): return
    if not context.args: await send(update, box("/WAPAS 123456")); return
    try: await update.effective_chat.unban_member(int(context.args[0])); await send(update, box("WAPAS AA GAYA!"))
    except: await send(update, box("Nahi hua."))
async def dhakka(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)
        await update.effective_chat.unban_member(update.message.reply_to_message.from_user.id)
        await send(update, box("DHAKKA DE DIYA! 👋"))
    except: await send(update, box("Nahi hua."))
async def chup(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await send(update, box("CHUP KAR DIYA 🤫"))
    except: await send(update, box("Nahi hua."))
async def bolnede(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await send(update, box("AB BOL SAKTA HAI!"))
    except: await send(update, box("Nahi hua."))
async def chetavni(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message: await send(update, box(f"⚠️ CHETAVNI! {update.message.reply_to_message.from_user.first_name} Sudhar ja!"))
async def mitao(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.delete(); await update.message.delete()
        except: await send(update, box("Delete nahi hua."))
async def chipkao(update, context):
    if not await need_admin(update): return
    if update.message.reply_to_message:
        try: await update.message.reply_to_message.pin(); await send(update, box("CHIPKA DIYA 📌"))
        except: await send(update, box("Nahi hua."))
async def hatao(update, context):
    if not await need_admin(update): return
    try: await update.effective_chat.unpin_all_messages(); await send(update, box("PIN HATA DIYA"))
    except: pass
async def tala(update, context):
    if not await need_admin(update): return
    await send(update, box("TALA laga diya 🔒"))
async def kholo(update, context):
    if not await need_admin(update): return
    await send(update, box("KHOL DIYA 🔓"))
async def linkband(update, context):
    if not await need_admin(update): return
    await send(update, box("LINK BAND ON! /AUTOBAN ON likh"))
async def linkbandoff(update, context):
    if not await need_admin(update): return
    await send(update, box("LINK BAND OFF!"))
async def linkbandon(update, context): await linkband(update, context)
async def swagatset(update, context):
    if not await need_admin(update): return
    txt = " ".join(context.args) if context.args else "Welcome {name} 🔥"
    WELCOME[update.effective_chat.id] = txt; await send(update, box(f"SWAGAT SET: {txt}"))
async def swagatoff(update, context):
    if not await need_admin(update): return
    WELCOME.pop(update.effective_chat.id, None); await send(update, box("SWAGAT OFF!"))
async def swagattest(update, context):
    if not await check(update): return
    txt = WELCOME.get(update.effective_chat.id, "Welcome {name} 🔥")
    await send(update, box(txt.replace("{name}", update.effective_user.first_name)))
async def pasa(update, context):
    if not await check(update): return
    await send(update, box(f"🎲 PASA: {random.randint(1,6)}"))
async def sikka(update, context):
    if not await check(update): return
    await send(update, box(f"🪙 SIKKA: {random.choice(['HEAD','TAIL'])}"))
async def ghumao(update, context):
    if not await check(update): return
    await send(update, box(f"🎯 NUMBER: {random.randint(1,100)}"))
async def kainchi(update, context):
    if not await check(update): return
    await send(update, box(f"✂️ TUNE: {random.choice(['ROCK','PAPER','SCISSORS'])}"))
async def jadu(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/JADU kya hoga?")); return
    await send(update, box(random.choice(["Haan ✅","Nahi ❌","Pakka 🔥","Socho mat, kar de 😈"])))
async def chuno(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/CHUNO chai coffee")); return
    await send(update, box(f"ME CHUNTA HU: {random.choice(context.args)}"))
async def sawal(update, context):
    if not await check(update): return
    await send(update, box("SAWAL: Bharat ki rajdhani kya hai?\nA) Delhi B) Mumbai C) Goa"))
async def ank(update, context):
    if not await check(update): return
    await send(update, box(f"ANK: {random.randint(1,1000)}"))
async def fun_reply(update, txt):
    if not update.message.reply_to_message: await send(update, box("Kisi pe reply karke bhej!")); return
    await send(update, box(txt.format(name=update.message.reply_to_message.from_user.first_name)))
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
    await send(update, box(f"JODI: {update.effective_user.first_name} ❤️ {random.choice(['Kashyap','Demon','Angel','Cutie'])} - {random.randint(50,99)}% MATCH!"))
async def vichar(update, context):
    if not await check(update): return
    await send(update, f"✦ {random.choice(['Zindagi me aage badho 🔥','Mehnat karo, Kashyap jaisa bano 😈','Hasna sabse badi dawa hai ❤️'])} ✦")
async def gin(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/GIN 2+2")); return
    try: await send(update, box(f"JAWAB: {eval(' '.join(context.args))}"))
    except: await send(update, box("Galat hisaab."))
async def ulta(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args)[::-1]))
async def bada(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args).upper()))
async def chota(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args).lower()))
async def gino(update, context):
    if not await check(update): return
    if context.args: await send(update, box(f"LETTERS: {len(' '.join(context.args))}"))
async def samay(update, context):
    if not await check(update): return
    await send(update, box(f"SAMAY: {datetime.datetime.now().strftime('%H:%M:%S')}"))
async def tarikh(update, context):
    if not await check(update): return
    await send(update, box(f"TARIKH: {datetime.datetime.now().strftime('%d/%m/%Y')}"))
async def behisaab(update, context):
    if not await check(update): return
    await send(update, box(f"BEHISAAB: {random.randint(1,999)}"))
async def addsudo(update, context):
    if update.effective_user.id != OWNER_ID:
        await send(update, box("SIRF OWNER KAR SAKTA HAI")); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, box("AISE LIKH: /ADDSUDO 123456")); return
    SUDOS.add(uid); await send(update, box(f"HO GAYA! {uid} AB SUDO HAI 🔥"))
async def delsudo(update, context):
    if update.effective_user.id != OWNER_ID:
        await send(update, box("SIRF OWNER KAR SAKTA HAI")); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, box("AISE LIKH: /DELSUDO 123456")); return
    if uid == OWNER_ID:
        await send(update, box("OWNER KO NAHI HATA SAKTE")); return
    SUDOS.discard(uid); await send(update, box(f"HATA DIYA! {uid} AB SUDO NAHI HAI"))
async def sudolist(update, context):
    if not await check(update): return
    await send(update, box("SUDO LIST:\n" + "\n".join(str(x) for x in SUDOS)))
async def watch(update, context):
    if not await check(update): return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, box("AISE: /WATCH 123456")); return
    WATCHED.add(uid); await send(update, box(f"👀 WATCH ON! {uid} pe nazar hai GURU!"))
async def unwatch(update, context):
    if not await check(update): return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    if uid is None:
        await send(update, box("AISE: /UNWATCH 123456")); return
    WATCHED.discard(uid); await send(update, box(f"👀 WATCH OFF! {uid} se nazar hata di."))
async def watchlist(update, context):
    if not await check(update): return
    if not WATCHED: await send(update, box("WATCHLIST KHALI HAI GURU 👀")); return
    await send(update, box("👀 WATCHLIST:\n" + "\n".join(str(x) for x in WATCHED)))
async def autopin(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPIN_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOPIN OFF! 📌")); return
    AUTOPIN_CHATS.add(update.effective_chat.id); await send(update, box("AUTOPIN ON! 📌 Har msg auto pin hoga!"))
async def dmautopin(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        DMAUTOPIN.discard(update.effective_user.id); await send(update, box("DMAUTOPIN OFF")); return
    DMAUTOPIN.add(update.effective_user.id); await send(update, box("DMAUTOPIN ON 📌"))
async def art(update, context):
    if not await check(update): return
    if not context.args:
        txt = "BINDI ART LIST GURU:\n\n"
        for a in ARTS_LIST: txt += f"/ART {a}\n"
        txt += "\nYa /ART apna naam likh"; await send(update, box(txt)); return
    name = " ".join(context.args); art_text = bindi_art(name)
    await send(update, f"```\n{art_text}\n```")

async def autoreact(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREACT_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOREACT OFF! ❌")); return
    AUTOREACT_CHATS.add(update.effective_chat.id)
    await send(update, box("SMART AUTOREACT ON! 🧠❤️\nPyar pe ❤️, Funny pe 😂, Sad pe 😢, Gussa pe 😡"))
async def smartreact(update, context):
    global SMART_REACT_ON
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        SMART_REACT_ON = False; await send(update, box("SMART REACT OFF! Ab ek hi emoji aayega.")); return
    SMART_REACT_ON = True; await send(update, box("SMART REACT ON! 🧠 Mood ke hisab se react!"))
async def autoreactset(update, context):
    global AUTOREACT_EMOJI, SMART_REACT_ON
    if not await check(update): return
    if not context.args: await send(update, box(f"Abhi: {AUTOREACT_EMOJI}\n/AUTOREACTSET 🔥")); return
    AUTOREACT_EMOJI = context.args[0]; SMART_REACT_ON = False; await send(update, box(f"FIXED EMOJI SET! Ab {AUTOREACT_EMOJI} hi aayega. Smart ke liye /SMARTREACT ON"))
async def autodelete(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTODELETE_CHATS.pop(update.effective_chat.id, None); await send(update, box("AUTODELETE OFF! ❌")); return
    sec = 10
    if context.args:
        try: sec = int(context.args[0])
        except: pass
    AUTODELETE_CHATS[update.effective_chat.id] = sec
    await send(update, box(f"AUTODELETE ON! ⏳ Har msg {sec} sec baad delete hoga!"))
async def autoreply(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREPLY_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOREPLY OFF! ❌")); return
    AUTOREPLY_CHATS.add(update.effective_chat.id); await send(update, box("AUTOREPLY ON! 🤖 Ab 'hi' pe jawab dunga!"))
async def autoban(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOBAN_LINK.discard(update.effective_chat.id); AUTOBAN_GAALI.discard(update.effective_chat.id); await send(update, box("AUTOBAN OFF! ❌")); return
    AUTOBAN_LINK.add(update.effective_chat.id); AUTOBAN_GAALI.add(update.effective_chat.id); await send(update, box("AUTOBAN ON! 🔥 Link/Gaali pe delete + warn!"))
async def autowarn(update, context):
    if not await check(update): return
    if not WARN_COUNT: await send(update, box("Abhi kisi ko warn nahi mila GURU!")); return
    txt = "⚠️ WARN LIST:\n"
    for k,v in WARN_COUNT.items(): txt += f"{k} : {v}/3 warn\n"
    await send(update, box(txt))
async def afk(update, context):
    if not await check(update): return
    reason = " ".join(context.args) if context.args else "Busy hu GURU!"
    AFK_USERS[update.effective_user.id] = reason
    await send(update, box(f"AFK ON! 😴 {update.effective_user.first_name} ab AFK hai: {reason}"))
async def back(update, context):
    if update.effective_user.id in AFK_USERS:
        AFK_USERS.pop(update.effective_user.id); await send(update, box("WELCOME BACK GURU! 🔥 AFK khatam!"))
    else: await send(update, box("Tu AFK tha hi nahi GURU!"))
async def autotype(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOTYPE_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOTYPE OFF! ❌")); return
    AUTOTYPE_CHATS.add(update.effective_chat.id); await send(update, box("AUTOTYPE ON! ⌨️"))
async def autosave(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSAVE_ON.discard(update.effective_user.id); await send(update, box("AUTOSAVE OFF! ❌")); return
    AUTOSAVE_ON.add(update.effective_user.id); await send(update, box("AUTOSAVE ON! 💾"))
async def autopurge(update, context):
    if not await need_admin(update): return
    await send(update, box("AUTOPURGE ON! 🧹 /AUTODELETE 10 kar de!"))
async def purge(update, context):
    if not await need_admin(update): return
    await send(update, box("PURGE ke liye /AUTODELETE 10 likh de GURU!"))
async def autoshayari(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSHAYARI_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOSHAYARI OFF! ❌")); return
    AUTOSHAYARI_CHATS.add(update.effective_chat.id); await send(update, box("AUTOSHAYARI ON! ❤️"))
    await send(update, f"✦ ❤️ {fancy(random.choice(SHAYARI))} ❤️ ✦")
async def autogm(update, context):
    if not await need_admin(update): return
    AUTOGM_CHATS.add(update.effective_chat.id); await send(update, box("AUTOGM ON! ☀️ Ab /GM likh ke dekho!"))
async def autogn(update, context):
    if not await need_admin(update): return
    AUTOGN_CHATS.add(update.effective_chat.id); await send(update, box("AUTOGN ON! 🌙 Ab /GN likh ke dekho!"))
async def gm(update, context):
    if not await check(update): return
    await send(update, box("Good Morning GURU! ☀️🔥 Chai pi li?"))
async def gn(update, context):
    if not await check(update): return
    await send(update, box("Good Night GURU! 😴❤️ Kal milte hai!"))

# ===== TARUN BUSY COMMANDS =====
async def tarunbusy(update, context):
    global TARUN_BUSY_ON
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        TARUN_BUSY_ON = False
        await send(update, box("TARUN BUSY MODE OFF! ❌"))
        return
    TARUN_BUSY_ON = True
    await send(update, box("TARUN BUSY MODE ON! 😈🔥\n@SM302MP17 / @U_R_NOT_TYPE ko tag karne pe Bot bolega!"))
async def tarunfree(update, context):
    global TARUN_BUSY_ON
    if not await check(update): return
    TARUN_BUSY_ON = False
    await send(update, box("TARUN DADA FREE HAI AB! 🔥\nAb sab baat kar sakte hai!"))

# ===== ASLI AUTOBIO - HAR 1 MIN ME ALAG BIO =====
async def autobio(update, context):
    global AUTOBIO_ON, AUTOBIO_INDEX
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOBIO_ON = False
        await send(update, box("AUTOBIO OFF! ❌\nAb bio change nahi hogi!"))
        return
    if context.args and context.args[0].upper() == "ADD":
        if len(context.args) > 1:
            new_one = " ".join(context.args[1:])
            AUTOBIO_LIST.append(new_one)
            await send(update, box(f"NAYI BIO ADD HO GAYI! ✅\n{new_one}\nTotal Bio: {len(AUTOBIO_LIST)}"))
            return
        else:
            await send(update, box("AISE LIKH: /AUTOBIO ADD Meri nayi bio"))
            return
    if context.args and context.args[0].upper() == "LIST":
        txt = "📋 BIO LIST:\n\n" + "\n".join([f"{i+1}. {b}" for i,b in enumerate(AUTOBIO_LIST)])
        await send(update, box(txt[:3500]))
        return
    AUTOBIO_ON = True
    AUTOBIO_INDEX = 0
    try:
        now = datetime.datetime.now().strftime('%H:%M | %d/%m/%Y')
        first_bio = AUTOBIO_LIST[0]
        new_bio = f"{first_bio}\n⏰ {now} | OWNER: KASHYAP 🔥"
        await context.bot.set_my_description(new_bio)
        await context.bot.set_my_short_description(first_bio[:250])
        await send(update, box(f"AUTOBIO ON! ✅\nAb har 1 min me ALAG-ALAG Bio aayegi!\n\nAbhi wali Bio:\n{first_bio}\n\nTotal {len(AUTOBIO_LIST)} Bio hai!"))
    except Exception as e:
        await send(update, box(f"AUTOBIO FAIL: {e}"))

async def autobio_loop(app):
    global AUTOBIO_INDEX
    while True:
        await asyncio.sleep(60)
        if AUTOBIO_ON:
            try:
                AUTOBIO_INDEX = (AUTOBIO_INDEX + 1) % len(AUTOBIO_LIST)
                bio = AUTOBIO_LIST[AUTOBIO_INDEX]
                now = datetime.datetime.now().strftime('%H:%M | %d/%m/%Y')
                new_bio = f"{bio}\n⏰ {now} | OWNER: KASHYAP 🔥"
                await app.bot.set_my_description(new_bio)
                await app.bot.set_my_short_description(bio[:250])
                print(f"AUTOBIO ROTATED [{AUTOBIO_INDEX}]: {bio}")
            except Exception as e:
                print(f"AUTOBIO LOOP FAIL: {e}")

async def autoanswer(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOANSWER_ON.discard(update.effective_chat.id); await send(update, box("AUTOANSWER OFF! ❌")); return
    AUTOANSWER_ON.add(update.effective_chat.id); await send(update, box("AUTOANSWER ON! 🤖 'Demon kaha hai' pe jawab dunga!"))
async def autoprotect(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPROTECT_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOPROTECT OFF! ❌")); return
    AUTOPROTECT_CHATS.add(update.effective_chat.id); await send(update, box("AUTOPROTECT ON! 🛡️"))

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

        # ===== TARUN DADA - KOI BHI TAG / NAAM LIKHE TO - SABSE PEHLE =====
        if TARUN_BUSY_ON:
            low = orig_text.lower().strip()
            hit = False
            for w in TARUN_TRIGGERS:
                if w in low:
                    hit = True
                    break
            if msg.entities:
                for ent in msg.entities:
                    if ent.type == "mention":
                        m = orig_text[ent.offset:ent.offset+ent.length].lower().replace("@","")
                        if m in TARUN_IDS_USERNAMES:
                            hit = True
                    if ent.type == "text_mention" and ent.user and ent.user.username and ent.user.username.lower() in TARUN_IDS_USERNAMES:
                        hit = True
            if msg.reply_to_message and msg.reply_to_message.from_user.username and msg.reply_to_message.from_user.username.lower() in TARUN_IDS_USERNAMES:
                hit = True
            # Khud Tarun bole to Bot chup rahega
            if user.username and user.username.lower() in TARUN_IDS_USERNAMES:
                hit = False
            if hit:
                await send(update, TARUN_BUSY_MSG)
                return

        if orig_text.startswith("."):
            cmd = orig_text[1:].split()[0].lower()
            if cmd in ["command","commands","help","madad","menu","all"]:
                await send(update, ALL_COMMANDS_TEXT)
                return
        if user.id in WATCHED and user.id not in SUDOS:
            await send(update, box(f"👀 WATCH ALERT! {user.first_name} ({user.id}) ne bola: {orig_text[:100] if orig_text else 'Media bheja'}"))
        if msg.reply_to_message and msg.reply_to_message.from_user.id in AFK_USERS:
            await send(update, box(f"😴 {msg.reply_to_message.from_user.first_name} abhi AFK hai! Wajah: {AFK_USERS[msg.reply_to_message.from_user.id]}"))
        if chat_id in AUTOTYPE_CHATS:
            try: await context.bot.send_chat_action(chat_id, "typing")
            except: pass
        if chat_id in AUTOREACT_CHATS:
            try:
                emoji_to_use = get_smart_emoji(orig_text) if SMART_REACT_ON else AUTOREACT_EMOJI
                await context.bot.set_message_reaction(chat_id, msg.message_id, reaction=[ReactionTypeEmoji(emoji=emoji_to_use)])
            except Exception as e:
                print(f"REACT FAIL: {e}")
        if chat_id in AUTOPIN_CHATS or user.id in DMAUTOPIN:
            try: await msg.pin(disable_notification=True)
            except: pass
        if chat_id in AUTOBAN_LINK and ("http" in text or "t.me" in text or "www." in text) and user.id not in SUDOS:
            try: await msg.delete()
            except: pass
            await send(update, box(f"⚠️ {user.first_name} Link bhejna mana hai! Delete kar diya!"))
            return
        if chat_id in AUTOBAN_GAALI and user.id not in SUDOS:
            for g in GAALI_LIST:
                if g in text:
                    WARN_COUNT[user.id] = WARN_COUNT.get(user.id, 0) + 1
                    w = WARN_COUNT[user.id]
                    if w >= 3:
                        try: await update.effective_chat.ban_member(user.id); await send(update, box(f"🚫 {user.first_name} ko 3 warn pe BAN kar diya!"))
                        except: await send(update, box(f"⚠️ {user.first_name} 3 warn ho gaye! Admin banao!"))
                        WARN_COUNT[user.id] = 0
                    else:
                        try: await msg.delete()
                        except: pass
                        await send(update, box(f"⚠️ WARN {w}/3 {user.first_name}! Gaali mat de!"))
                    return
        if chat_id in AUTOREPLY_CHATS or chat_id in AUTOANSWER_ON:
            for k, v in REPLY_MAP.items():
                if k in text:
                    await send(update, v)
                    break
        if msg.photo or msg.video or msg.document:
            if OWNER_ID in AUTOSAVE_ON or user.id in AUTOSAVE_ON:
                try: await context.bot.send_message(OWNER_ID, f"💾 AUTOSAVE! {user.first_name} ne media bheja")
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
                await send(update, box(f"🛡️ AUTOPROTECT ALERT! Naya bot {m.first_name} add hua!"))
            if update.effective_chat.id in WELCOME:
                txt = WELCOME[update.effective_chat.id]
                await send(update, box(txt.replace("{name}", m.first_name)))
    except: pass

app_bot = None
def main():
    global app_bot
    app = ApplicationBuilder().token(TOKEN).build()
    app_bot = app.bot
    cmds = {"start": start, "help": help_cmd, "command": command_cmd, "commands": command_cmd, "madad": madad, "menu": menu_cmd, "all": all_cmd, "myid": myid, "ping": ping, "papa": papa, "shayari": shayari, "joke": joke, "haso": haso, "papabol": papabol, "truth": truth, "sach": sach, "dare": dare, "himmat": himmat, "chalu": chalu, "bareme": bareme, "tej": tej, "pehchan": pehchan, "jankari": jankari, "groupid": groupid, "tag": tag, "malik": malik, "niyam": niyam, "ankda": ankda, "uptime": uptime, "bol": bol, "nikal": nikal, "wapas": wapas, "dhakka": dhakka, "chup": chup, "bolnede": bolnede, "chetavni": chetavni, "mitao": mitao, "chipkao": chipkao, "hatao": hatao, "tala": tala, "kholo": kholo, "linkband": linkband, "linkbandoff": linkbandoff, "linkbandon": linkbandon, "swagatset": swagatset, "swagatoff": swagatoff, "swagattest": swagattest, "pasa": pasa, "sikka": sikka, "ghumao": ghumao, "kainchi": kainchi, "jadu": jadu, "chuno": chuno, "sawal": sawal, "ank": ank, "gale": gale, "thappad": thappad, "chumma": chumma, "thapthapao": thapthapao, "panja": panja, "hath": hath, "pyar": pyar, "tariff": tariff, "jodi": jodi, "vichar": vichar, "gin": gin, "ulta": ulta, "bada": bada, "chota": chota, "gino": gino, "samay": samay, "tarikh": tarikh, "behisaab": behisaab, "addsudo": addsudo, "delsudo": delsudo, "sudolist": sudolist, "watch": watch, "unwatch": unwatch, "watchlist": watchlist, "autopin": autopin, "dmautopin": dmautopin, "art": art, "autoreact": autoreact, "smartreact": smartreact, "autoreactset": autoreactset, "autodelete": autodelete, "autoreply": autoreply, "autoban": autoban, "autowarn": autowarn, "afk": afk, "back": back, "autotype": autotype, "autosave": autosave, "autopurge": autopurge, "purge": purge, "autoshayari": autoshayari, "autogm": autogm, "autogn": autogn, "gm": gm, "gn": gn, "autobio": autobio, "autoanswer": autoanswer, "autoprotect": autoprotect, "tarunbusy": tarunbusy, "tarunfree": tarunfree}
    for n, fn in cmds.items(): app.add_handler(CommandHandler(n, fn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_watcher), group=1)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    print("KASHYAP BOT STARTED - SUDOS:", SUDOS)
    try:
        asyncio.get_event_loop().create_task(autobio_loop(app))
    except:
        pass
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__":
    main()
