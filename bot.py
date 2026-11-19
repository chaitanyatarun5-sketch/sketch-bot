import os, random, time, datetime, asyncio
from flask import Flask
from threading import Thread
from telegram import Update
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
    uid = update.effective_user.id
    print(f"CHECK ID: {uid} | ALLOWED: {SUDOS}")
    if not is_allowed(uid):
        await send(update, "SORRY GURU! YE BOT SIRF OWNER AUR SUDO KE LIYE HAI 🔒")
        return False
    return True

async def need_admin(update):
    if not await is_admin(update) and update.effective_user.id not in SUDOS:
        await send(update, "GURU YE SIRF ADMIN KAR SAKTA HAI 🔒")
        return False
    return True

# ===== AUTO SYSTEMS =====
WATCHED = set()
AUTOPIN_CHATS = set()
DMAUTOPIN = set()
AUTOREACT_CHATS = set()
AUTOREACT_EMOJI = "❤️"
AUTODELETE_CHATS = {}
AUTODELETE_MEDIA = set()
AUTOREPLY_CHATS = set()
AUTOBAN_LINK = set()
AUTOBAN_GAALI = set()
WARN_COUNT = {}
AFK_USERS = {}
AUTOTYPE_CHATS = set()
AUTOSAVE_ON = set()
AUTOPURGE_CHATS = set()
AUTOSHAYARI_CHATS = set()
AUTOGM_CHATS = set()
AUTOGN_CHATS = set()
AUTOBIO_ON = False
AUTOANSWER_ON = set()
AUTOPROTECT_CHATS = set()
WELCOME = {}
LINK_OFF = set()

GAALI_LIST = ["madarchod","behenchod","bhosdike","chutiya","gandu","randi","bhenchod","mc","bc","chut","lund","gand"]
REPLY_MAP = {
    "hi": "Hi GURU! Kaise ho? 🔥",
    "hello": "Hello GURU! 😈",
    "hey": "Hey GURU! Bol kya kaam hai?",
    "good morning": "Good Morning GURU! ☀️ Chai pi li?",
    "good night": "Good Night GURU! 😴 Kal milte hai!",
    "good evening": "Good Evening GURU! 🌆",
    "kaise ho": "Ekdam mast GURU! Tu bata? 🔥",
    "kaha ho": "GURU yahi hai, bas thoda busy hai! 😈",
    "demon kaha hai": "GURU aata hi hoga! Thoda ruk ja! 🔥",
    "kashyap kaha hai": "GURU aata hi hoga! Thoda ruk ja! 🔥",
    "papa": "PAPA HU ME TERA 😈🔥",
    "love you": "Love you too GURU! ❤️",
    "bye": "Bye GURU! Jaldi aana! 👋",
    "kya kar rahe ho": "Teri yaad me shayari likh raha hu GURU! ❤️",
}

# ===== SARE COMMANDS KA FULL LIST - YAHI DIKHEGA =====
ALL_COMMANDS_TEXT = """🔥 KASHYAP BOT - SARE COMMANDS 🔥
━━━━━━━━━━━━━━━━━━
👤 ID / GENERAL (12)
━━━━━━━━━━━━━━━━━━
/MYID - Tera ID Card
/PEHCHAN - Pehchan Card
/JANKARI - Full Jankari
/GROUPID - Group Ki ID
/PING - Bot Speed Check
/TEJ - Bot Tej Hai?
/CHALU - Bot On Hai?
/BAREME - Bot Ke Bare Me
/UPTIME - Kitne Time Se On Hai
/TAG - Kisi Ko Tag Kar
/MALIK - Admin List
/NIYAM - Group Ke Niyam
/ANKDA - Group Ka Ankda
/BOL - Bot Se Bulwao

━━━━━━━━━━━━━━━━━━
😈 PAPA WALE (7)
━━━━━━━━━━━━━━━━━━
/PAPA - Papa Hu Me Tera
/SHAYARI - Shayari ❤️
/JOKE - Joke 😂
 /HASO - Haso Wala Joke
/PAPABOL - Truth / Dare Khelo
/TRUTH - Sach Wala Sawal
/SACH - Sach Wala Sawal
/DARE - Dare Wala Task
/HIMMAT - Himmat Wala Dare

━━━━━━━━━━━━━━━━━━
🛡️ MODERATION (13)
━━━━━━━━━━━━━━━━━━
/NIKAL - Reply Karke Ban
/WAPAS - Unban Kar
/DHAKKA - Kick Kar
/CHUP - Mute Kar
/BOLNEDE - Unmute Kar
/CHETAVNI - Warn De
/MITAO - Msg Delete Kar
/CHIPKAO - Msg Pin Kar
/HATAO - Pin Hatao
/TALA - Tala Laga
/KHOLO - Tala Khol
/LINKBAND - Link Band
/LINKBANDOFF - Link Band Off
/LINKBANDON - Link Band On

━━━━━━━━━━━━━━━━━━
👋 WELCOME (3)
━━━━━━━━━━━━━━━━━━
/SWAGATSET - Welcome Msg Set
/SWAGATOFF - Welcome Off
/SWAGATTEST - Welcome Test Kar

━━━━━━━━━━━━━━━━━━
🎲 GAMES (8)
━━━━━━━━━━━━━━━━━━
/PASA - Pasa Feko
/SIKKA - Head / Tail
/GHUMAO - Random Number
/KAINCHI - Rock Paper Scissors
/JADU - Haan / Nahi Batao
/CHUNO - Koi Ek Chuno
/SAWAL - Sawal Puchho
/ANK - Lucky Ank

━━━━━━━━━━━━━━━━━━
❤️ FUN (10)
━━━━━━━━━━━━━━━━━━
/GALE - Gale Lagao
/THAPPAD - Thappad Maro
/CHUMMA - Chumma Do
/THAPTHAPAO - Thapthapao
/PANJA - Panja Milao
/HATH - Hath Hilao
/PYAR - Pyar Karo
/TARIFF - Tariff Karo
/JODI - Jodi Banao
/VICHAR - Acha Vichar

━━━━━━━━━━━━━━━━━━
🧮 TOOLS (8)
━━━━━━━━━━━━━━━━━━
/GIN - Hisab Karo
/ULTA - Ulta Likho
/BADA - Bada Likho
/CHOTA - Chota Likho
/GINO - Letters Gino
/SAMAY - Abhi Ka Time
/TARIKH - Aaj Ki Tarikh
/BEHISAAB - Random Number

━━━━━━━━━━━━━━━━━━
👀 WATCH / PIN / ART (7)
━━━━━━━━━━━━━━━━━━
/WATCH - Kisi Pe Nazar Rakho
/UNWATCH - Nazar Hatao
/WATCHLIST - Watch List Dekho
/AUTOPIN - Auto Pin On
/DMAUTOPIN - DM Me Auto Pin
/ART - Bindi Art Banao
/ART RAM - Ram Wala Art

━━━━━━━━━━━━━━━━━━
🤖 AUTO WALE - SABSE MAST (22)
━━━━━━━━━━━━━━━━━━
/AUTOREACT - Har Msg Pe React ❤️
/AUTOREACTSET - React Emoji Badlo
/AUTODELETE - Msg Auto Delete ⏳
/AUTOREPLY - Hi/Hello Pe Auto Jawab
/AUTOBAN - Link/Gaali Pe Auto Ban
/AUTOWARN - Warn List Dekho
/AFK - AFK Lagao 😴
/BACK - AFK Se Wapas Aao
/AUTOTYPE - Typing Dikhayega ⌨️
/AUTOSAVE - Media Auto Save 💾
/AUTOPURGE - Purge On Karo
/PURGE - Chat Saaf Karo
/AUTOSHAYARI - Auto Shayari ❤️
/AUTOGM - Good Morning Auto
/GM - Good Morning Bhejo
/AUTOGN - Good Night Auto
/GN - Good Night Bhejo
/AUTOBIO - Auto Bio On
/AUTOANSWER - Demon Kaha Hai? Auto Jawab
/AUTOPROTECT - Naya Bot Aaye To Alert 🛡️

━━━━━━━━━━━━━━━━━━
👑 SUDO (3)
━━━━━━━━━━━━━━━━━━
/ADDSUDO - Naya Sudo Banao
/DELSUDO - Sudo Hatao
/SUDOLIST - Sudo List Dekho

━━━━━━━━━━━━━━━━━━
📋 HELP (5)
━━━━━━━━━━━━━━━━━━
/HELP - Ye List Dekho
/MADAD - Ye List Dekho
/COMMAND - Ye List Dekho
/COMMANDS - Ye List Dekho
/MENU - Ye List Dekho
/ALL - Ye List Dekho

━━━━━━━━━━━━━━━━━━
TOTAL = 95+ COMMANDS 🔥
OWNER: KASHYAP 😈👑
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
SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Mohabbat me humne khud ko mita diya, tere liye duniya se ladna sikha diya ❤️","Teri aankhon me duniya dekh li, ab aur kisi ki zarurat nahi ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️","Teri baaton me jadoo hai, sunte hi dil kho jata hai ❤️","Chahte hai tujhe dil se, tu hi meri manzil hai ❤️","Tum bin jiya jaye kaise, ye dil tumhe hi chahe ❤️","Teri yaadon ka sahara hai, warna jeena mushkil tha ❤️","Tu jo hanse to phool khil jaye, tu jo roye to dil jal jaye ❤️","Ishq me humne sab kuch luta diya, bas teri ek muskan ke liye ❤️","Teri galiyon se guzre to laga, jannat yahi hai ❤️","Dil ka haal kya bataye, tujhe dekh ke dil dhadak jaye ❤️","Tum meri subah shaam ho, tum hi mera aaram ho ❤️","Teri ek jhalak ke liye, hum taraste rahe ❤️","Mohabbat ki galiyon me hum kho gaye, teri yaadon me so gaye ❤️","Tu mera chand hai, me tera tara ❤️","Teri khushi me meri khushi hai, tu hanse to me hanu ❤️","Dil ki kitaab me tera naam likha hai, har panne pe tu hi tu hai ❤️","Tujhe dekh ke dil ne ye kaha, tu hi meri duniya hai ❤️","Teri yaad me humne chai pi, aur raat guzar gayi ❤️","Tu jo mile to laga, dua kabool ho gayi ❤️","Teri aankhon ka nasha hai, utarta hi nahi ❤️","Dil me basa liya hai tujhe, ab nikalna mushkil hai ❤️","Tu meri zindagi ka sabse haseen pal hai ❤️"]
JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Girlfriend se breakup ho gaya tha. Teacher: To? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Ek ladki ne ladke se kaha: Tum bahut bure ho. Ladka: Thanks, tum bhi bahut buri lag rahi ho aaj 😂","Santa: Meri biwi mujhse bahut pyar karti hai. Banta: Kaise pata? Santa: Jab bhi me ghar late aata hu, wo darwaza khol ke kehti hai - Aa gaya kutta 😂","Teacher: Beta, tum bade hoke kya banoge? Pappu: Dulha. Teacher: Matlab? Pappu: Shaadi karunga, aur kuch nahi 😂","Ladki: Tum mujhe kabhi chhod to nahi doge? Ladka: Pagal hai kya, Jio ka network hu kya jo chhod du 😂","Doctor: Tumhe kya problem hai? Patient: Mujhe bhoolne ki bimari hai. Doctor: Kab se hai? Patient: Kab se kya? 😂","Pappu: Papa, exam me fail ho gaya. Papa: Koi baat nahi beta, tu to waise bhi pass hone layak nahi tha 😂","Girlfriend: Tum mujhe kitni izzat dete ho? Boyfriend: Jitni tu mujhe deti hai, matlab zero 😂","Ek baar ek chuha billi se bola: I love you. Billi: Pagal hai kya? Chuha: Pyar andha hota hai 😂","Teacher: Agar tumhe 100 rupaye mile to kya karoge? Pappu: Recharge karunga. Teacher: Padhai ka kya? Pappu: Free WiFi se ho jayegi 😂","Pati: Aaj khana kaisa bana hai? Patni: Acha hai. Pati: To fir ye jalne ki smell kaha se aa rahi hai? Patni: Meri jal rahi hai 😂","Ladka: Tumhari aankhen bahut sundar hai. Ladki: Thanks. Ladka: Aur chashma bhi 😂","Santa ne Banta ko phone kiya: Kaha ho? Banta: Ghar pe. Santa: Jhooth mat bol, me ghar pe hu, tu kaha hai? 😂","Mummy: Beta, padh le. Beta: Padh raha hu. Mummy: Phone me kya padh raha hai? Beta: Teri bahu ki photo dekh raha hu 😂","Teacher: Tumhara homework kaha hai? Pappu: Kutte ne kha liya. Teacher: Tumhare paas kutta kab se hai? Pappu: Abhi kharida, homework khane ke liye 😂","Boyfriend: Baby, tum bahut moti ho gayi ho. Girlfriend: To? Boyfriend: To ab tumhe koi uthake nahi le jayega, safe ho 😂","Ek aadmi: Guru, ye rasta kaha jata hai? Dusra: Pata nahi, me yaha ka nahi hu. Pehla: To tu yaha kya kar raha hai? Dusra: Rasta dekh raha hu 😂","Pappu: Mummy, me shaadi karunga. Mummy: Kis se? Pappu: Jisse tum kaho. Mummy: Pados wali aunty se? Pappu: Mummy, mazak mat karo 😂","Girlfriend: Tum mere liye kya kar sakte ho? Boyfriend: Kuch bhi. Girlfriend: To mera phone recharge kar de 😂","Santa: Yaar, meri biwi bahut ladti hai. Banta: To chup raha kar. Santa: Me chup hi rehta hu, wo akele bhi lad leti hai 😂","Teacher: Sabse bada sach kya hai? Pappu: Sir, Sunday ko school nahi hota, yehi sabse bada sach hai 😂","Ladki: Tum cigarette pite ho? Ladka: Nahi. Ladki: Daru? Ladka: Nahi. Ladki: To fir tum mere layak nahi ho, boring ho 😂","Papa: Beta, result kaisa raha? Beta: Papa, 2 logo ne top kiya hai. Papa: Tu kitne number pe hai? Beta: Me teesra hu, pehle 2 ke baad me hi hu 😂","Ek ladka ladki ko propose kar raha tha: Will you marry me? Ladki: No. Ladka: To fir friendship to kar le, itna bhav kyu kha rahi hai 😂","Mummy: Beta, sabzi le aa. Beta: Konsi? Mummy: Jo tujhe pasand ho. Beta: Pizza le aau? 😂","Teacher: Tum late kyu aaye? Pappu: Sir, board pe likha tha - School 8 baje khulta hai, me 8 baje hi aaya, gate band tha 😂","Boyfriend: Tumhe sabse zyada kya pasand hai? Girlfriend: Shopping. Boyfriend: Aur sabse kam? Girlfriend: Tumhara bank balance 😂","Santa: Banta, tu itna khush kyu hai? Banta: Biwi mayke gayi hai. Santa: To? Banta: Ab ghar pe shanti hai 😂"]
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
    name = u.first_name
    username = f"@{u.username}" if u.username else "No Username"
    if u.id == OWNER_ID: tag = "Tu hi MALIK hai GURU! 😈👑"
    elif u.id in SUDOS: tag = "Tu SUDO hai GURU! 🔥"
    else: tag = "Tu Member hai GURU!"
    await send(update, f"━━━━━━━━━━━━━━\n🔥 GURU ID CARD 🔥\n━━━━━━━━━━━━━━\n👤 NAAM: {name}\n🆔 ID: `{u.id}`\n📎 USERNAME: {username}\n🔗 LINK: tg://user?id={u.id}\n━━━━━━━━━━━━━━\n{tag}")
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
        from telegram import ChatPermissions
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await send(update, "CHUP KAR DIYA 🤫")
    except: await send(update, "Nahi hua.")
async def bolnede(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try:
        from telegram import ChatPermissions
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
    LINK_OFF.add(update.effective_chat.id); await send(update, "LINK BAND ON!")
async def linkbandoff(update, context):
    if not await need_admin(update): return
    LINK_OFF.discard(update.effective_chat.id); await send(update, "LINK BAND OFF!")
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
    SUDOS.add(uid); await send(update, f"HO GAYA! {uid} AB SUDO HAI 🔥\nAb ye bhi bot chala payega.")
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
        DMAUTOPIN.discard(update.effective_user.id); await send(update, "DMAUTOPIN OFF - DM me auto pin band"); return
    DMAUTOPIN.add(update.effective_user.id); await send(update, "DMAUTOPIN ON - DM me auto pin ON 📌")
async def art(update, context):
    if not await check(update): return
    if not context.args:
        txt = "BINDI ART LIST GURU:\n\n"
        for a in ARTS_LIST: txt += f"/ART {a}\n"
        txt += "\nYa /ART apna naam likh"; await send(update, txt); return
    name = " ".join(context.args); art_text = bindi_art(name)
    await send(update, f"```\n{art_text}\n```")
async def autoreact(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREACT_CHATS.discard(update.effective_chat.id); await send(update, "AUTOREACT OFF! ❌"); return
    AUTOREACT_CHATS.add(update.effective_chat.id); await send(update, f"AUTOREACT ON! ❤️🔥 Ab har msg pe {AUTOREACT_EMOJI} react karunga GURU!")
async def autoreactset(update, context):
    global AUTOREACT_EMOJI
    if not await check(update): return
    if not context.args: await send(update, f"Abhi: {AUTOREACT_EMOJI}\n/AUTOREACTSET 🔥"); return
    AUTOREACT_EMOJI = context.args[0]; await send(update, f"AUTOREACT EMOJI SET! Ab {AUTOREACT_EMOJI} se react karunga! 🔥")
async def autodelete(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTODELETE_CHATS.pop(update.effective_chat.id, None); await send(update, "AUTODELETE OFF! ❌"); return
    sec = 60
    if context.args:
        try: sec = int(context.args[0])
        except: pass
    AUTODELETE_CHATS[update.effective_chat.id] = sec
    await send(update, f"AUTODELETE ON! ⏳ Har msg {sec} sec baad apne aap delete hoga GURU! 😈")
async def autoreply(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOREPLY_CHATS.discard(update.effective_chat.id); await send(update, "AUTOREPLY OFF! ❌"); return
    AUTOREPLY_CHATS.add(update.effective_chat.id); await send(update, "AUTOREPLY ON! 🤖 Ab hi/hello/good morning pe apne aap jawab dunga GURU!")
async def autoban(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOBAN_LINK.discard(update.effective_chat.id); AUTOBAN_GAALI.discard(update.effective_chat.id); await send(update, "AUTOBAN OFF! ❌"); return
    if context.args and context.args[0].upper() == "LINK":
        AUTOBAN_LINK.add(update.effective_chat.id); await send(update, "AUTOBAN LINK ON! 🔗 Link bhejte hi delete + warn!"); return
    if context.args and context.args[0].upper() == "GAALI":
        AUTOBAN_GAALI.add(update.effective_chat.id); await send(update, "AUTOBAN GAALI ON! 🤬 Gaali dete hi warn!"); return
    AUTOBAN_LINK.add(update.effective_chat.id); AUTOBAN_GAALI.add(update.effective_chat.id); await send(update, "AUTOBAN ON! 🔥 Link + Gaali dono pe action lunga GURU!")
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
    await send(update, f"AFK ON! 😴 {update.effective_user.first_name} ab AFK hai: {reason}\nWapas aane pe /BACK likhna!")
async def back(update, context):
    if update.effective_user.id in AFK_USERS:
        AFK_USERS.pop(update.effective_user.id); await send(update, "WELCOME BACK GURU! 🔥 AFK khatam!")
    else: await send(update, "Tu AFK tha hi nahi GURU!")
async def autotype(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOTYPE_CHATS.discard(update.effective_chat.id); await send(update, "AUTOTYPE OFF! ❌"); return
    AUTOTYPE_CHATS.add(update.effective_chat.id); await send(update, "AUTOTYPE ON! ⌨️ Ab har msg pe typing... dikhayega GURU!")
async def autosave(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSAVE_ON.discard(update.effective_user.id); await send(update, "AUTOSAVE OFF! ❌"); return
    AUTOSAVE_ON.add(update.effective_user.id); await send(update, "AUTOSAVE ON! 💾 Ab koi photo/video bheje to mujhe forward ho jayega GURU!")
async def autopurge(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPURGE_CHATS.discard(update.effective_chat.id); await send(update, "AUTOPURGE OFF! ❌"); return
    AUTOPURGE_CHATS.add(update.effective_chat.id); await send(update, "AUTOPURGE ON! 🧹 /PURGE likhte hi pura chat saaf kar dunga GURU!")
async def purge(update, context):
    if not await need_admin(update): return
    await send(update, "PURGE: Telegram Bot me purana chat delete nahi hota GURU, par AUTODELETE ON kar de - aage se sab auto delete hoga! /AUTODELETE 60 likh!")
async def autoshayari(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOSHAYARI_CHATS.discard(update.effective_chat.id); await send(update, "AUTOSHAYARI OFF! ❌"); return
    AUTOSHAYARI_CHATS.add(update.effective_chat.id); await send(update, "AUTOSHAYARI ON! ❤️ Ab /SHAYARI likhte hi to aayegi hi, aur tu chahe to me har baar nayi bhejunga!")
    await send(update, random.choice(SHAYARI))
async def autogm(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOGM_CHATS.discard(update.effective_chat.id); await send(update, "AUTOGM OFF! ❌"); return
    AUTOGM_CHATS.add(update.effective_chat.id); await send(update, "AUTOGM ON! ☀️ Good Morning GURU! Ab /GM likhte hi GM bhej dunga!")
async def autogn(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOGN_CHATS.discard(update.effective_chat.id); await send(update, "AUTOGN OFF! ❌"); return
    AUTOGN_CHATS.add(update.effective_chat.id); await send(update, "AUTOGN ON! 🌙 Good Night GURU! Ab /GN likhte hi GN bhej dunga!")
async def gm(update, context):
    if not await check(update): return
    await send(update, "Good Morning GURU! ☀️🔥 Chai pi li? Aaj ka din tera hai!")
async def gn(update, context):
    if not await check(update): return
    await send(update, "Good Night GURU! 😴❤️ Kal subah milte hai!")
async def autobio(update, context):
    global AUTOBIO_ON
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOBIO_ON = False; await send(update, "AUTOBIO OFF! ❌"); return
    AUTOBIO_ON = True; await send(update, f"AUTOBIO ON! 🔥 Ab har /MYID pe time ke hisab se bio dikhega!\nAbhi Time: {datetime.datetime.now().strftime('%H:%M')}")
async def autoanswer(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOANSWER_ON.discard(update.effective_chat.id); await send(update, "AUTOANSWER OFF! ❌"); return
    AUTOANSWER_ON.add(update.effective_chat.id); await send(update, "AUTOANSWER ON! 🤖 Ab koi 'Demon kaha hai' puche to me apne aap jawab dunga GURU!")
async def autoprotect(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPROTECT_CHATS.discard(update.effective_chat.id); await send(update, "AUTOPROTECT OFF! ❌"); return
    AUTOPROTECT_CHATS.add(update.effective_chat.id); await send(update, "AUTOPROTECT ON! 🛡️ Ab koi naya bot add kare to me alert dunga GURU!")

async def auto_watcher(update, context):
    try:
        chat_id = update.effective_chat.id
        user = update.effective_user
        msg = update.message
        text = (msg.text or "").lower() if msg.text else ""
        # DOT COMMAND - .command bhi kaam karega GURU!
        if msg.text and msg.text.startswith("."):
            cmd = msg.text[1:].split()[0].lower()
            if cmd in ["command","commands","help","madad","menu","all"]:
                await send(update, ALL_COMMANDS_TEXT)
                return
        if user.id in WATCHED and user.id not in SUDOS:
            await send(update, f"👀 WATCH ALERT! {user.first_name} ({user.id}) ne bola: {msg.text[:100] if msg.text else 'Media bheja'}")
        if msg.reply_to_message and msg.reply_to_message.from_user.id in AFK_USERS:
            await send(update, f"😴 {msg.reply_to_message.from_user.first_name} abhi AFK hai GURU! Wajah: {AFK_USERS[msg.reply_to_message.from_user.id]}")
        if chat_id in AUTOTYPE_CHATS:
            try: await context.bot.send_chat_action(chat_id, "typing")
            except: pass
        if chat_id in AUTOREACT_CHATS:
            try: await context.bot.set_message_reaction(chat_id, msg.message_id, reaction=[{"type": "emoji", "emoji": AUTOREACT_EMOJI}])
            except: pass
        if chat_id in AUTOPIN_CHATS or user.id in DMAUTOPIN:
            try: await msg.pin(disable_notification=True)
            except: pass
        if chat_id in AUTOBAN_LINK and ("http" in text or "t.me" in text or "www." in text) and user.id not in SUDOS:
            try: await msg.delete(); await send(update, f"⚠️ {user.first_name} Link bhejna mana hai GURU! Msg delete kar diya!")
            except: pass
            return
        if chat_id in AUTOBAN_GAALI and user.id not in SUDOS:
            for g in GAALI_LIST:
                if g in text:
                    WARN_COUNT[user.id] = WARN_COUNT.get(user.id, 0) + 1
                    w = WARN_COUNT[user.id]
                    if w >= 3:
                        try: await update.effective_chat.ban_member(user.id); await send(update, f"🚫 {user.first_name} ko 3 warn pe BAN kar diya! Gaali band GURU!")
                        except: await send(update, f"⚠️ {user.first_name} 3 warn ho gaye! Admin bana mujhe, ban kar dunga!")
                        WARN_COUNT[user.id] = 0
                    else:
                        try: await msg.delete()
                        except: pass
                        await send(update, f"⚠️ WARN {w}/3 {user.first_name}! Gaali mat de GURU! Agli baar ban!")
                    return
        if chat_id in AUTOREPLY_CHATS or chat_id in AUTOANSWER_ON:
            for k, v in REPLY_MAP.items():
                if k in text:
                    await send(update, v); break
        if user.id in AUTOSAVE_ON or OWNER_ID in AUTOSAVE_ON:
            if msg.photo or msg.video or msg.document:
                try: await context.bot.send_message(OWNER_ID, f"💾 AUTOSAVE! {user.first_name} ne media bheja - Chat: {update.effective_chat.title}")
                except: pass
        if chat_id in AUTODELETE_CHATS:
            sec = AUTODELETE_CHATS[chat_id]
            await asyncio.sleep(sec)
            try: await msg.delete()
            except: pass
            return
        if chat_id in AUTODELETE_MEDIA and (msg.photo or msg.video):
            await asyncio.sleep(300)
            try: await msg.delete()
            except: pass
    except Exception as e:
        print("Watcher error:", e)

async def new_member_handler(update, context):
    try:
        for m in update.message.new_chat_members:
            if m.is_bot and update.effective_chat.id in AUTOPROTECT_CHATS:
                await send(update, f"🛡️ AUTOPROTECT ALERT! Naya bot {m.first_name} add hua hai GURU! Dhyan rakhna!")
            if update.effective_chat.id in WELCOME:
                txt = WELCOME[update.effective_chat.id]
                await send(update, txt.replace("{name}", m.first_name))
    except: pass

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    cmds = {"start": start, "help": help_cmd, "command": command_cmd, "commands": command_cmd, "madad": madad, "menu": menu_cmd, "all": all_cmd, "myid": myid, "ping": ping, "papa": papa, "shayari": shayari, "joke": joke, "haso": haso, "papabol": papabol, "truth": truth, "sach": sach, "dare": dare, "himmat": himmat, "chalu": chalu, "bareme": bareme, "tej": tej, "pehchan": pehchan, "jankari": jankari, "groupid": groupid, "tag": tag, "malik": malik, "niyam": niyam, "ankda": ankda, "uptime": uptime, "bol": bol, "nikal": nikal, "wapas": wapas, "dhakka": dhakka, "chup": chup, "bolnede": bolnede, "chetavni": chetavni, "mitao": mitao, "chipkao": chipkao, "hatao": hatao, "tala": tala, "kholo": kholo, "linkband": linkband, "linkbandoff": linkbandoff, "linkbandon": linkbandon, "swagatset": swagatset, "swagatoff": swagatoff, "swagattest": swagattest, "pasa": pasa, "sikka": sikka, "ghumao": ghumao, "kainchi": kainchi, "jadu": jadu, "chuno": chuno, "sawal": sawal, "ank": ank, "gale": gale, "thappad": thappad, "chumma": chumma, "thapthapao": thapthapao, "panja": panja, "hath": hath, "pyar": pyar, "tariff": tariff, "jodi": jodi, "vichar": vichar, "gin": gin, "ulta": ulta, "bada": bada, "chota": chota, "gino": gino, "samay": samay, "tarikh": tarikh, "behisaab": behisaab, "addsudo": addsudo, "delsudo": delsudo, "sudolist": sudolist, "watch": watch, "unwatch": unwatch, "watchlist": watchlist, "autopin": autopin, "dmautopin": dmautopin, "art": art, "autoreact": autoreact, "autoreactset": autoreactset, "autodelete": autodelete, "autoreply": autoreply, "autoban": autoban, "autowarn": autowarn, "afk": afk, "back": back, "autotype": autotype, "autosave": autosave, "autopurge": autopurge, "purge": purge, "autoshayari": autoshayari, "autogm": autogm, "autogn": autogn, "gm": gm, "gn": gn, "autobio": autobio, "autoanswer": autoanswer, "autoprotect": autoprotect}
    for n, fn in cmds.items(): app.add_handler(CommandHandler(n, fn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_watcher))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    print("KASHYAP BOT STARTED - SUDOS:", SUDOS)
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__":
    main()
