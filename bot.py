import os, random, time, datetime, asyncio, ast, operator, string
from flask import Flask
from threading import Thread
from telegram import Update, ChatPermissions, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatMemberStatus

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 8532606474
SUDOS = {8532606474}
START_TIME = time.time()
SUDO_IDS = os.environ.get("SUDO_IDS", "")
if SUDO_IDS:
    for x in SUDO_IDS.split(","):
        if x.strip().isdigit():
            SUDOS.add(int(x.strip()))

def is_allowed(uid: int): return uid in SUDOS
async def is_admin(update):
    try:
        m = await update.effective_chat.get_member(update.effective_user.id)
        return m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except: return False

FANCY_MAP = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
def fancy(t: str): return t.translate(FANCY_MAP)
def box(text: str): return f"╭━━━━━━━━━━━━╮\n┃ {text} ┃\n╰━━━━━━━━━━━━╯"
async def send(update, text):
    try: await update.effective_chat.send_message(text)
    except Exception as e: print("Send fail:", e)
async def check(update):
    if not is_allowed(update.effective_user.id):
        await send(update, box("🔒 YE BOT SIRF OWNER / SUDO KE LIYE HAI"))
        return False
    return True
async def need_admin(update):
    if not await is_admin(update) and update.effective_user.id not in SUDOS:
        await send(update, box("🔒 YE SIRF ADMIN KAR SAKTA HAI"))
        return False
    return True

# ===== STORAGE =====
WELCOME = {}; AFK_USERS = {}; MSG_COUNT = {}; WARN_COUNT = {}
AUTOREACT_CHATS = set(); AUTOREPLY_CHATS = set(); AUTOPIN_CHATS = set(); AUTOSHAYARI_CHATS = set(); AUTOGM_CHATS = set(); AUTOGN_CHATS = set()
AUTO_TAGALL = set(); AUTO_STICKER = set(); AUTO_MOTIVATE = set(); AUTO_THANK = set(); AUTO_HELLO = set(); AUTO_BYE = set(); AUTO_MEME = set(); AUTO_GAME = set(); AUTO_SHOUT = set(); AUTO_REPEAT = set(); AUTO_TRUTH_AUTO = set(); AUTO_POLL = set(); AUTO_QUIZ = set(); AUTO_BIRTHDAY = set(); AUTO_STATS = set(); AUTO_JOIN = set(); AUTO_LEAVE = set(); AUTO_SHOUTOUT = set(); AUTO_COMPLIMENT = set(); AUTO_EMOJI = set(); AUTO_PHOTO = set(); AUTO_VOICE = set()

# ===== DATA =====
SHAYARI = ["Teri yaad me dil ne ye farmaya hai, tu jo mili to laga khuda ne bulaya hai ❤️","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ❤️","Tumse milke laga zindagi mil gayi, ab to har khushi tumse hi judi ❤️","Dil ki dhadkan ban gayi ho tum, meri har dua me aati ho tum ❤️","Teri muskan pe fida hu me, tu jo hanse to jahan hanse ❤️","Raaton ko neend nahi aati, teri yaad bahut satati ❤️","Tu mile to laga sab mil gaya, ab koi gham nahi ❤️","Dil ne tujhe itna chaha, ki khud ko bhool gaya ❤️"]
JOKES = ["Ek aadmi doctor ke paas gaya: Doctor, mujhe sab kuch do-do dikhta hai. Doctor: Baith jao, tum char log ek saath mat baitho 😂","Teacher: Kal school kyu nahi aaye? Pappu: Dil tuta to pair bhi tut gaya samjho 😂","Pati: Tum mujhe kitna pyar karti ho? Patni: Jitna tum phone ko karte ho, usse thoda kam 😂","Dost: Bhai exam me kya likha? Me: Jo aata tha wo likha, jo nahi aata tha wo bhi likha 😂"]
TRUTHS = ["Tera sabse bada crush kaun hai? 😏","Kabhi kisi ka message chupke padha hai?","Sabse embarrassing moment kya tha tera?","Apni life ka sabse bada jhooth batao.","Last baar kab roye the aur kyu?","Kis cheez se sabse zyada dar lagta hai?"]
DARES = ["Apni DP 1 ghante ke liye badal de 😂","Group me apni favourite shayari likh ke bhej ❤️","10 baar apna naam zor se bol ke voice bhej","Apne dost ki tareef me 3 line likh","Kal subah sabko Good Morning bolna"]
MEMES = ["Meme 1: Jab teacher bole kal test hai aur tune kuch padha nahi 😂","Meme 2: Jab mummy bole phone rakh de aur tu chupke chala raha ho 😂","Meme 3: Jab dost bole party meri taraf se aur bill aane pe bhag jaye 😂"]
MOTIVATES = ["Uth ja bacche! Aaj tera din hai! Mehnat kar, result khud bolega 🔥","Zindagi me aage badho, rukna mana hai 🔥","Hasna sabse badi dawa hai, haste raho ❤️","Mehnat karo, Kashyap jaisa bano 😈"]
FACTS = ["Octopus ke 3 dil hote hai 🐙","Honey kabhi kharab nahi hota 🍯","Banana berry hota hai, strawberry nahi 🍌","Shark 400 saal tak jee sakta hai 🦈","Tumhare muh me 700 tarah ke bacteria hote hai 😂"]
QUOTES = ["Mehnat itni khamoshi se karo ki safalta shor macha de 🔥","Jo ruk gaya wo haar gaya, jo chalta raha wo jeet gaya","Kal se nahi, aaj se shuru karo"]
RIDDLES = [("Aisa kaun sa phal hai jo khaya nahi jata?","Badam ka chilka 😂"),("Wo kya hai jo aage badhta hai par peeche nahi hat ta?","Umar"),("Aisi kaun si cheez hai jo paani me girne pe bhi geeli nahi hoti?","Parchhai")]
WYR_LIST = ["Paisa ya Pyar?","Phone ya Dost?","Pahad ya Samundar?","Din ya Raat?","Chai ya Coffee?"]
NHIE_LIST = ["Maine kabhi school bunk nahi kiya","Maine kabhi jhooth nahi bola","Maine kabhi teacher se daant nahi khayi"]
QUIZ_LIST = [("Bharat ki rajdhani kya hai?","A) Delhi B) Mumbai C) Goa","Delhi"),("Taj Mahal kaha hai?","A) Delhi B) Agra C) Jaipur","Agra")]
AUTOBIO_LIST = ["🔥 DEMON BOT 😈 | OWNER: KASHYAP","💀 DEMON MODE ON | KASHYAP IS HERE","👑 KING OF TELEGRAM | KASHYAP 👑","⚡ TEJ HU ME | DEMON BOT LIVE 🔥","🌙 RAAT KA RAJA | DIN KA BADSHAH"]
AUTOBIO_ON = False; AUTOBIO_INDEX = 0
FONT = {'A': [" . ",". .","...",". .",". ."],'B': [".. ",". .",".. ",". .",".. "],'C': [" ..",".  ",".  ",".  "," .."],'D': [".. ",". .",". .",". .",".. "],'E': ["...",".  ",".. ",".  ","..."],'F': ["...",".  ",".. ",".  ",".  "],'G': [" ..",".  ",". .",". ."," .."],'H': [". .",". .","...",". .",". ."],'I': ["..."," . "," . "," . ","..."],'J': ["..."," . "," . ",". ."," . "],'K': [". .",". .",".. ",". .",". ."],'L': [".  ",".  ",".  ",".  ","..."],'M': [". .","...",". .",". .",". ."],'N': [". .","...",". .",". .",". ."],'O': [" . ",". .",". .",". ."," . "],'P': [".. ",". .",".. ",".  ",".  "],'Q': [" . ",". .",". ."," ..","  ."],'R': [".. ",". .",".. ",". .",". ."],'S': [" ..",".  "," . ","  .",".. "],'T': ["..."," . "," . "," . "," . "],'U': [". .",". .",". .",". ."," . "],'V': [". .",". .",". .",". ."," . "],'W': [". .",". .",". .","...",". ."],'X': [". .",". ."," . ",". .",". ."],'Y': [". .",". ."," . "," . "," . "],'Z': ["...","  ."," . ",".  ","..."],' ': ["   ","   ","   ","   ","   "]}
def bindi_art(text):
    text = text.upper()[:14]; lines = [""]*5
    for ch in text:
        f = FONT.get(ch, FONT[' '])
        for i in range(5): lines[i] += f[i] + "  "
    return "\n".join(lines)
ARTS_LIST = ["RAM","JAISHREERAM","HANUMAN","MAHAKAL","SHIV","OM","RADHE","KRISHNA","ILOVEYOU","LOVE","HUG","JAAN","BABY","CRUSH","CUTE","PYAR","MISSYOU","HELLO","BYEE","KING","QUEEN","KASHYAP","INDIA","BHARAT","SORRY","THANKYOU","GOODMORNING","GOODNIGHT","HAPPYBIRTHDAY"]

ALL_COMMANDS_TEXT = """╔════════════════════╗
║ 🔥 DEMON BOT - ALL COMMAND 🔥 ║
━━━━━━━━━━━━━━━━━━
Total 170+ Command | Sirf Owner / Sudo
━━━━━━━━━━━━━━━━━━

ℹ️ INFO / BASIC
/MYID /PEHCHAN /JANKARI /GROUPID
/PING /CHALU /BAREME /UPTIME
/TAG /TAGALL /MALIK /NIYAM /BOL

🎭 FUN / MASTI
/SHAYARI /JOKE /HASO /TRUTH /SACH /DARE /HIMMAT
/PASA /SIKKA /GHUMAO /KAINCHI /JADU
/CHUNO /SAWAL /ANK
/GALE /PANJA /HATH /PYAR /TARIFF /JODI /VICHAR
/GIN /ULTA /BADA /CHOTA /GINO
/SAMAY /TARIKH /BEHISAAB

✨ NEW 30 COMMAND
/POLL /QUIZ /WYR /NHIE /RIDDLE /8BALL /FACT /QUOTE /GUESS /RPS
/SLOT /LOVECALC /FONT /ART /SHOUT
/MOVIE /CRICKET /NEWS /HOROSCOPE
/WARN /MUTE /UNMUTE /PURGE /GIVEAWAY
/COUNT /REMINDER /NOTE /TRANSLATE /AI

🔥 MAST 40 COMMAND
/DICE /COIN /TOSS /LUDO /KING /QUEEN /TOP /ACTIVE
/IDCARD /PROFILE /LUCKY /ZODIAC /TODAY /PARTY /DANCE /SING
/STORY /RAP /POEM /ECHO /SAY /MIMIC /VS /BATTLE
/TEAM /WINNER /LOSER /RESPECT /SHOUTOUT2 /WELCOME2 /BYE2
/GM2 /GN2 /PASSWORD /RANDOMNAME /AGE /COUNTWORD
/REVERSE2 /UPPER2 /LOWER2

👋 SWAGAT
/SWAGATSET /SWAGATOFF /SWAGATTEST

👑 ADMIN
/NIKAL /WAPAS /DHAKKA /CHUP /BOLNEDE
/CHETAVNI /MITAO /CHIPKAO /HATAO

⚙️ AUTO
/AUTOPIN /AUTOREACT /AUTOREPLY /AUTOSHAYARI
/AUTOGM /AUTOGN /AUTOTAGALL /AUTOSTICKER
/AUTOMOTIVATE /AUTOTHANK /AUTOHELLO /AUTOBYE
/AUTOMEME /AUTOGAME /AUTOSHOUT /AUTOREPEAT
/AUTOTRUTH /AUTOPOLL /AUTOQUIZ /AUTOBIRTHDAY
/AUTOSTATS /AUTOJOIN /AUTOLEAVE /AUTOSHOUTOUT
/AUTOCOMPLIMENT /AUTOEMOJI /AUTOPHOTO /AUTOVOICE
/AUTOBIO /AFK /BACK

👑 MASTER
/ALLOFF /ALLON /ADDSUDO /DELSUDO /SUDOLIST

🛠️ HELP
/HELP /MADAD /COMMAND /MENU /ALL

✨ EXTRA
/EXTRA /MEME /MOTIVATE /SONG /BIRTHDAY /STATS
━━━━━━━━━━━━━━━━━━
OWNER: KASHYAP 👑 | BOT: 𝒹𝑒𝓂𝑜𝓃_17_099_𝒷𝑜𝓉
"""

# ===== BASIC =====
async def start(update, context):
    if not await check(update): return
    await send(update, box(fancy("DEMON BOT ON HAI!") + " 🔥\n" + fancy("/COMMAND LIKH KE SARE DEKH")))
async def help_cmd(update, context):
    if not await check(update): return
    await send(update, ALL_COMMANDS_TEXT)
async def command_cmd(update, context):
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
async def myid(update, context):
    u = update.effective_user; username = f"@{u.username}" if u.username else "No Username"
    tag = "Tu hi MALIK hai! 👑" if u.id==OWNER_ID else ("Tu SUDO hai! 🔥" if u.id in SUDOS else "Tu Member hai!")
    await send(update, f"👤 {fancy('NAAM')}: {fancy(u.first_name)}\n🆔 {fancy('ID')}: `{u.id}`\n📎 {fancy('USERNAME')}: {username}\n━━━━━━━━━━━━━━\n{tag}")
async def ping(update, context):
    if not await check(update): return
    await send(update, box(fancy("PING PONG! BOT LIVE") + " 🔥"))
async def chalu(update, context):
    if not await check(update): return
    await send(update, box(fancy("BOT ON HAI!") + " 🔥"))
async def bareme(update, context):
    if not await check(update): return
    await send(update, box(fancy("ME HU DEMON BOT") + " 🔥 Owner: Kashyap"))
async def pehchan(update, context):
    u = update.effective_user; username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"👤 {fancy(u.first_name)}\n🆔 `{u.id}`\n📎 {username}")
async def jankari(update, context):
    if not await check(update): return
    u = update.effective_user; c = update.effective_chat; username = f"@{u.username}" if u.username else "No Username"
    await send(update, f"👤 {fancy(u.first_name)}\n🆔 `{u.id}`\n📎 {username}\n💬 {c.title if c.title else 'DM'}\n💬 CHAT ID: `{c.id}`")
async def groupid(update, context):
    if not await check(update): return
    await send(update, box(f"GROUP ID: {update.effective_chat.id}"))
async def tag(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("AISE: /TAG @username")); return
    await send(update, box(f"HEY {context.args[0]} BULA RAHE HAI 🔥"))
async def malik(update, context):
    if not await check(update): return
    try:
        admins = await update.effective_chat.get_administrators()
        await send(update, box(fancy("ADMIN LOG:") + "\n" + "\n".join([a.user.first_name for a in admins])))
    except: await send(update, box("Admin list nahi mili."))
async def niyam(update, context):
    if not await check(update): return
    await send(update, "📜 " + fancy("NIYAM") + "\n1. Izzat se baat karo\n2. Link spam mat karo\n3. Admin ki izzat karo")
async def uptime(update, context):
    if not await check(update): return
    await send(update, box(f"BOT ON HAI: {int(time.time()-START_TIME)//60} MIN SE 🔥"))
async def bol(update, context):
    if not await check(update): return
    if context.args: await send(update, box(fancy(" ".join(context.args))))

# ===== TAGALL - TERA WALA =====
async def tagall(update, context):
    if not await check(update): return
    if update.effective_chat.type == "private":
        await send(update, box("Ye command sirf group me chalegi!")); return
    await send(update, box("TAG KAR RAHA HU SABKO... 🔥\nRuk ja thoda!"))
    try:
        members = []
        async for m in context.bot.get_chat_members(update.effective_chat.id):
            if not m.user.is_bot:
                members.append(m.user)
        if not members:
            await send(update, box("Koi member nahi mila!")); return
        batch = []
        for user in members:
            batch.append(f"[{user.first_name}](tg://user?id={user.id})")
            if len(batch) == 5:
                text = " ".join(batch) + "\n\nHello Haayy 👋🔥"
                await update.effective_message.reply_text(text, parse_mode="Markdown")
                batch = []
                await asyncio.sleep(1)
        if batch:
            text = " ".join(batch) + "\n\nHello Haayy 👋🔥"
            await update.effective_message.reply_text(text, parse_mode="Markdown")
        total = len(members)
        await send(update, f"✨ Tag All Completed Successfully ✨\n👥 Total Members Tagged: {total}\n💫 Powered by your 𝒹𝑒𝓂𝑜𝓃_17_099_𝒷𝑜𝓉")
    except Exception as e:
        await send(update, box(f"Tag nahi ho paya! Bot ko admin banao.\nError: {e}"))

# ===== FUN =====
async def shayari(update, context):
    if not await check(update): return
    await send(update, f"✦ ❤️ {fancy(random.choice(SHAYARI))} ❤️ ✦")
async def joke(update, context):
    if not await check(update): return
    await send(update, f"😂 {random.choice(JOKES)}")
async def haso(update, context):
    if not await check(update): return
    await send(update, f"😂 {random.choice(JOKES)}")
async def truth(update, context):
    if not await check(update): return
    await send(update, f"❓ {fancy('TRUTH')} ❓\n{random.choice(TRUTHS)}")
async def sach(update, context):
    if not await check(update): return
    await send(update, f"❓ {fancy('SACH')} ❓\n{random.choice(TRUTHS)}")
async def dare(update, context):
    if not await check(update): return
    await send(update, f"🔥 {fancy('DARE')} 🔥\n{random.choice(DARES)}")
async def himmat(update, context):
    if not await check(update): return
    await send(update, f"🔥 {fancy('HIMMAT')} 🔥\n{random.choice(DARES)}")
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
async def panja(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} se PANJA milaya 🤝")
async def hath(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko HATH hilaya 👋")
async def pyar(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} se DOSTI hai ❤️")
async def tariff(update, context):
    if not await check(update): return
    await fun_reply(update, random.choice(['Tu bahut smart hai 🔥','Teri smile best hai ❤️','Tu group ki jaan hai 😈']) + " {name}")
async def jodi(update, context):
    if not await check(update): return
    await send(update, box(f"JODI: {update.effective_user.first_name} ❤️ Dost - {random.randint(50,99)}% MATCH!"))
async def vichar(update, context):
    if not await check(update): return
    await send(update, f"✦ {random.choice(['Zindagi me aage badho 🔥','Mehnat karo, Kashyap jaisa bano 😈','Hasna sabse badi dawa hai ❤️'])} ✦")
async def gin_safe(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("AISE: /GIN 2+2")); return
    expr = " ".join(context.args)
    if not set(expr) <= set("0123456789+-*/(). "):
        await send(update, box("Sirf number aur + - * / allowed hai")); return
    try:
        ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
        def ev(n):
            if isinstance(n, ast.Constant) and isinstance(n.value, (int,float)): return n.value
            if isinstance(n, ast.BinOp): return ops[type(n.op)](ev(n.left), ev(n.right))
            if isinstance(n, ast.UnaryOp): return -ev(n.operand)
            raise ValueError()
        res = ev(ast.parse(expr, mode='eval').body)
        await send(update, box(f"JAWAB: {res}"))
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
async def art(update, context):
    if not await check(update): return
    if not context.args:
        txt = "ART LIST:\n\n" + "\n".join([f"/ART {a}" for a in ARTS_LIST]) + "\n\nYa /ART apna naam likh"
        await send(update, box(txt)); return
    name = " ".join(context.args); await send(update, f"```\n{bindi_art(name)}\n```")

# ===== NEW 30 COMMAND =====
async def poll(update, context):
    if not await check(update): return
    q = " ".join(context.args) if context.args else "Aaj Best Kaun?"
    await send(update, box(f"📊 POLL: {q}\n1. Kashyap 2. Demon 3. Sab Mast"))
async def quiz(update, context):
    if not await check(update): return
    q,a,_ = random.choice(QUIZ_LIST); await send(update, box(f"❓ QUIZ: {q}\n{a}"))
async def wyr(update, context):
    if not await check(update): return
    await send(update, box(f"🤔 Would You Rather?\n{random.choice(WYR_LIST)}"))
async def nhie(update, context):
    if not await check(update): return
    await send(update, box(f"😏 Never Have I Ever:\n{random.choice(NHIE_LIST)}"))
async def riddle(update, context):
    if not await check(update): return
    q,a = random.choice(RIDDLES); await send(update, box(f"🧩 PAHELI: {q}\nJawab: {a}"))
async def eightball(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/8BALL kya me pass hounga?")); return
    await send(update, box(random.choice(["Haan ✅","Nahi ❌","Pakka 🔥","Socho mat kar de 😈","Bilkul nahi","100% Haan"])))
async def fact(update, context):
    if not await check(update): return
    await send(update, box(f"💡 FACT: {random.choice(FACTS)}"))
async def quote(update, context):
    if not await check(update): return
    await send(update, box(f"✨ QUOTE: {random.choice(QUOTES)}"))
async def guess(update, context):
    if not await check(update): return
    await send(update, box(f"Maine 1-100 me ek number socha hai: {random.randint(1,100)} - Guess karo!"))
async def rps(update, context):
    if not await check(update): return
    await send(update, box(f"✂️ ROCK PAPER SCISSORS: Bot ne chuna {random.choice(['ROCK','PAPER','SCISSORS'])}"))
async def slot(update, context):
    if not await check(update): return
    s = [random.choice(["🍒","🔥","⭐","💎","7️⃣"]) for _ in range(3)]
    await send(update, box(f"🎰 SLOT: {' '.join(s)}"))
async def lovecalc(update, context):
    if not await check(update): return
    if len(context.args) < 2: await send(update, box("/LOVECALC Ram Sita")); return
    await send(update, box(f"❤️ {context.args[0]} ❤️ {context.args[1]} = {random.randint(50,99)}% MATCH!"))
async def font(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/FONT Kashyap")); return
    await send(update, box(fancy(" ".join(context.args))))
async def shout(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/SHOUT hello")); return
    await send(update, box(" ".join(context.args).upper() + " !!! 🔊"))
async def movie(update, context):
    if not await check(update): return
    await send(update, box("🎬 MOVIE: Naam batao, main story bata dunga! Abhi ke liye - 3 Idiots dekh lo, mast hai!"))
async def cricket(update, context):
    if not await check(update): return
    await send(update, box("🏏 CRICKET: Aaj ka score check karne ke liye Cricbuzz dekh lo!"))
async def news(update, context):
    if not await check(update): return
    await send(update, box("📰 AAJ KI NEWS:\n1. Group me bot full active hai 🔥\n2. Sab mast hai\n3. Kal party hai!"))
async def horoscope(update, context):
    if not await check(update): return
    await send(update, box(f"🔮 AAJ KA DIN: {random.choice(['Mast rahega 🔥','Paisa aayega 💰','Dost milenge ❤️','Maza aayega 😂'])}"))
async def warn(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: await send(update, box("Reply karke /WARN likh")); return
    uid = update.message.reply_to_message.from_user.id
    WARN_COUNT[uid] = WARN_COUNT.get(uid,0)+1
    await send(update, box(f"⚠️ WARN {WARN_COUNT[uid]}/3 {update.message.reply_to_message.from_user.first_name}! Sudhar ja!"))
async def mute(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try: await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False)); await send(update, box("MUTE KAR DIYA 🤫"))
    except: await send(update, box("Nahi hua."))
async def unmute(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try: await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)); await send(update, box("AB BOL SAKTA HAI!"))
    except: await send(update, box("Nahi hua."))
async def purge(update, context):
    if not await need_admin(update): return
    await send(update, box("PURGE ke liye msg ko reply karke /MITAO likh!"))
async def giveaway(update, context):
    if not await check(update): return
    await send(update, box(f"🎁 GIVEAWAY! Winner hai: {update.effective_user.first_name}! 🔥"))
async def count(update, context):
    if not await check(update): return
    await send(update, box(f"📊 TOTAL MSG: {sum(MSG_COUNT.values())}\nTop Active: {len(MSG_COUNT)} log"))
async def reminder(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/REMINDER 10min chai peena hai")); return
    await send(update, box(f"⏰ REMINDER SET: {' '.join(context.args)}"))
async def note(update, context):
    if not await check(update): return
    await send(update, box(f"📝 NOTE SAVE: {' '.join(context.args) if context.args else 'Kuch likha nahi'}"))
async def translate(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/TRANSLATE hello")); return
    await send(update, box(f"TRANSLATE: {' '.join(context.args)} -> Namaste 🙏"))
async def ai(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/AI tu kaun hai?")); return
    await send(update, box("🤖 AI: Main Demon Bot hu! Tu jo puchhega main mast jawab dunga!"))

# ===== MAST 40 COMMAND =====
async def dice(update, context):
    if not await check(update): return
    await send(update, box(f"🎲 DICE: {random.randint(1,6)} {random.randint(1,6)}"))
async def coin(update, context):
    if not await check(update): return
    await send(update, box(f"🪙 COIN: {random.choice(['HEADS 😎','TAILS 🔥'])}"))
async def toss(update, context):
    if not await check(update): return
    await send(update, box(f"🏏 TOSS: {random.choice(['BATTING','BOWLING'])} aayi hai!"))
async def ludo(update, context):
    if not await check(update): return
    await send(update, box(f"🎲 LUDO: {random.randint(1,6)} aaya! Chal chal jaldi!"))
async def king(update, context):
    if not await check(update): return
    await send(update, box(f"👑 AAJ KA KING: {update.effective_user.first_name} 👑"))
async def queen(update, context):
    if not await check(update): return
    await send(update, box(f"👸 AAJ KI QUEEN: {update.effective_user.first_name} 👸"))
async def top(update, context):
    if not await check(update): return
    top_users = sorted(MSG_COUNT.items(), key=lambda x: x[1], reverse=True)[:5]
    if not top_users: await send(update, box("Abhi koi active nahi hai!")); return
    txt = "🏆 TOP 5 ACTIVE:\n" + "\n".join([f"{i+1}. ID {uid} - {c} msg" for i,(uid,c) in enumerate(top_users)])
    await send(update, box(txt))
async def active(update, context):
    if not await check(update): return
    await send(update, box(f"🔥 AAJ ACTIVE: {len(MSG_COUNT)} log\nTotal Msg: {sum(MSG_COUNT.values())}"))
async def idcard(update, context):
    u = update.effective_user
    await send(update, f"🪪 ID CARD\n👤 {u.first_name}\n🆔 {u.id}\n📎 @{u.username if u.username else 'No Username'}\n⭐ Level: {random.randint(1,100)}")
async def profile(update, context):
    u = update.effective_user
    await send(update, box(f"👤 PROFILE\nNaam: {u.first_name}\nID: {u.id}\nStatus: Group ka Star ⭐"))
async def lucky(update, context):
    if not await check(update): return
    await send(update, box(f"🍀 LUCKY NUMBER: {random.randint(1,99)}\n🍀 LUCKY COLOR: {random.choice(['Red','Black','Blue','Green','White'])}"))
async def zodiac(update, context):
    if not await check(update): return
    await send(update, box(f"♈ ZODIAC: {random.choice(['Mesh','Vrishabh','Mithun','Kark','Singh','Kanya','Tula','Vrischick','Dhanu','Makar','Kumbh','Meen'])}"))
async def today(update, context):
    if not await check(update): return
    await send(update, box(f"📅 AAJ: {datetime.datetime.now().strftime('%d/%m/%Y %A')}\nMood: {random.choice(['Mast 🔥','Full Energy ⚡','Chill 😎'])}"))
async def party(update, context):
    if not await check(update): return
    await send(update, box("🎉 PARTY TIME! 🎉\nSab aa jao, DJ wala babu mera gaana baja de!"))
async def dance(update, context):
    if not await check(update): return
    await send(update, box("💃 DANCE: Naagin dance kar sab! 🐍💃"))
async def sing(update, context):
    if not await check(update): return
    await send(update, box("🎤 SING: Tera yaar hu main, tera yaar hu main... 🎵"))
async def story(update, context):
    if not await check(update): return
    await send(update, box(random.choice(["Ek tha raja, ek thi rani, dono me ho gayi ladai, fir bot ne kara di sulah 😂","Ek gaon me ek bot tha, wo sabki madad karta tha, sab usko Demon kehte the 🔥","Ek ladka tha, usne mehnat ki, aur aaj wo group ka king hai 👑"])))
async def rap(update, context):
    if not await check(update): return
    await send(update, box("🎤 RAP: Main hu Demon, mera style hai venom, group me aaya to sab bole welcome! 🔥"))
async def poem(update, context):
    if not await check(update): return
    await send(update, box("✍️ POEM:\nChandni raat me, bot ki baat me,\nSabka dil jeet liya, ek hi raat me ❤️"))
async def echo(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/ECHO hello")); return
    await send(update, box(" ".join(context.args)))
async def say(update, context):
    if not await check(update): return
    if context.args: await send(update, " ".join(context.args))
async def mimic(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/MIMIC main mast hu")); return
    await send(update, box(f"MIMIC: {' '.join(context.args)} 😂"))
async def vs(update, context):
    if not await check(update): return
    if len(context.args) < 2: await send(update, box("/VS Ram Shyam")); return
    await send(update, box(f"⚔️ VS: {context.args[0]} VS {context.args[1]}\nWinner: {random.choice(context.args)} 🏆"))
async def battle(update, context):
    if not await check(update): return
    await send(update, box(f"⚔️ BATTLE: {update.effective_user.first_name} VS Bot\nWinner: {random.choice([update.effective_user.first_name,'Bot'])} 🏆"))
async def team(update, context):
    if not await check(update): return
    await send(update, box(f"👥 TEAM: {update.effective_user.first_name} ki team me hai - Kashyap, Demon, Sab Dost 🔥"))
async def winner(update, context):
    if not await check(update): return
    await send(update, box(f"🏆 WINNER: {update.effective_user.first_name} jeet gaya! Party de ab! 🎉"))
async def loser(update, context):
    if not await check(update): return
    await send(update, box("😂 Aaj haar gaye to kya hua, kal jeetoge! Try again!"))
async def respect(update, context):
    if not await check(update): return
    await fun_reply(update, "{name} ko full RESPECT 🫡🔥")
async def shoutout2(update, context):
    if not await check(update): return
    await send(update, box(f"📢 SHOUTOUT TO {update.effective_user.first_name} - Group ka Star! ⭐🔥"))
async def welcome2(update, context):
    if not await check(update): return
    await send(update, box(f"Welcome {update.effective_user.first_name}! 🔥 Group me aa gaye, ab maza aayega!"))
async def bye2(update, context):
    if not await check(update): return
    await send(update, box(f"Bye Bye {update.effective_user.first_name}! Jaldi aana! 👋"))
async def gm2(update, context):
    if not await check(update): return
    await send(update, box("☀️ GOOD MORNING SABKO! Uth jao, chai pi lo!"))
async def gn2(update, context):
    if not await check(update): return
    await send(update, box("🌙 GOOD NIGHT SABKO! Kal milte hai! 😴"))
async def password(update, context):
    if not await check(update): return
    chars = string.ascii_letters + string.digits
    pwd = "".join(random.choice(chars) for _ in range(8))
    await send(update, box(f"🔑 PASSWORD: {pwd}\nKisi ko mat batana!"))
async def randomname(update, context):
    if not await check(update): return
    await send(update, box(f"🎲 RANDOM NAAM: {random.choice(['Rocky','Chotu','Babu','King','Queen','Don','Tiger','Hero','Demon','Boss'])}"))
async def age(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/AGE 2005")); return
    try:
        year = int(context.args[0]); age_v = datetime.datetime.now().year - year
        await send(update, box(f"🎂 AGE: {age_v} saal"))
    except: await send(update, box("Sahi saal likh! /AGE 2005"))
async def countword(update, context):
    if not await check(update): return
    if not context.args: await send(update, box("/COUNTWORD hello duniya")); return
    await send(update, box(f"Words: {len(context.args)} | Letters: {len(' '.join(context.args))}"))
async def reverse2(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args)[::-1]))
async def upper2(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args).upper()))
async def lower2(update, context):
    if not await check(update): return
    if context.args: await send(update, box(" ".join(context.args).lower()))

# ===== ADMIN =====
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
    try: await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id); await update.effective_chat.unban_member(update.message.reply_to_message.from_user.id); await send(update, box("DHAKKA DE DIYA! 👋"))
    except: await send(update, box("Nahi hua."))
async def chup(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try: await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False)); await send(update, box("CHUP KAR DIYA 🤫"))
    except: await send(update, box("Nahi hua."))
async def bolnede(update, context):
    if not await need_admin(update): return
    if not update.message.reply_to_message: return
    try: await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)); await send(update, box("AB BOL SAKTA HAI!"))
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

# ===== SWAGAT =====
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

# ===== AUTO + SUDO + EXTRA =====
async def autopin(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper()=="OFF": AUTOPIN_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOPIN OFF!")); return
    AUTOPIN_CHATS.add(update.effective_chat.id); await send(update, box("AUTOPIN ON! 📌"))
async def autoreact(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper()=="OFF": AUTOREACT_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOREACT OFF!")); return
    AUTOREACT_CHATS.add(update.effective_chat.id); await send(update, box("AUTOREACT ON! ❤️"))
async def autoreply(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper()=="OFF": AUTOREPLY_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOREPLY OFF!")); return
    AUTOREPLY_CHATS.add(update.effective_chat.id); await send(update, box("AUTOREPLY ON! 🤖"))
async def autoshayari(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper()=="OFF": AUTOSHAYARI_CHATS.discard(update.effective_chat.id); await send(update, box("AUTOSHAYARI OFF!")); return
    AUTOSHAYARI_CHATS.add(update.effective_chat.id); await send(update, box("AUTOSHAYARI ON! ❤️")); await send(update, random.choice(SHAYARI))
async def autogm(update, context):
    if not await need_admin(update): return
    AUTOGM_CHATS.add(update.effective_chat.id); await send(update, box("AUTOGM ON! ☀️"))
async def autogn(update, context):
    if not await need_admin(update): return
    AUTOGN_CHATS.add(update.effective_chat.id); await send(update, box("AUTOGN ON! 🌙"))
async def gm(update, context):
    if not await check(update): return
    await send(update, box("Good Morning! ☀️🔥 Chai pi li?"))
async def gn(update, context):
    if not await check(update): return
    await send(update, box("Good Night! 😴❤️ Kal milte hai!"))
async def afk(update, context):
    if not await check(update): return
    reason = " ".join(context.args) if context.args else "Busy hu!"
    AFK_USERS[update.effective_user.id] = reason; await send(update, box(f"AFK ON! 😴 {update.effective_user.first_name} ab AFK hai: {reason}"))
async def back(update, context):
    if update.effective_user.id in AFK_USERS: AFK_USERS.pop(update.effective_user.id); await send(update, box("WELCOME BACK! 🔥 AFK khatam!"))
    else: await send(update, box("Tu AFK tha hi nahi!"))
async def addsudo(update, context):
    if update.effective_user.id != OWNER_ID: await send(update, box("SIRF OWNER KAR SAKTA HAI")); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message: uid = update.message.reply_to_message.from_user.id
    if uid is None: await send(update, box("AISE LIKH: /ADDSUDO 123456")); return
    SUDOS.add(uid); await send(update, box(f"HO GAYA! {uid} AB SUDO HAI 🔥"))
async def delsudo(update, context):
    if update.effective_user.id != OWNER_ID: await send(update, box("SIRF OWNER KAR SAKTA HAI")); return
    uid = None
    if context.args:
        try: uid = int(context.args[0])
        except: pass
    elif update.message.reply_to_message: uid = update.message.reply_to_message.from_user.id
    if uid is None: await send(update, box("AISE LIKH: /DELSUDO 123456")); return
    if uid == OWNER_ID: await send(update, box("OWNER KO NAHI HATA SAKTE")); return
    SUDOS.discard(uid); await send(update, box(f"HATA DIYA! {uid} AB SUDO NAHI HAI"))
async def sudolist(update, context):
    if not await check(update): return
    await send(update, box("SUDO LIST:\n" + "\n".join(str(x) for x in SUDOS)))
async def autobio(update, context):
    global AUTOBIO_ON, AUTOBIO_INDEX
    if not await check(update): return
    if context.args and context.args[0].upper()=="OFF": AUTOBIO_ON=False; await send(update, box("AUTOBIO OFF!")); return
    AUTOBIO_ON=True; AUTOBIO_INDEX=0
    try:
        await context.bot.set_my_description(AUTOBIO_LIST[0]); await send(update, box(f"AUTOBIO ON! ✅\nAbhi wali Bio:\n{AUTOBIO_LIST[0]}"))
    except Exception as e: await send(update, box(f"AUTOBIO FAIL: {e}"))
async def autobio_loop(app):
    global AUTOBIO_INDEX
    while True:
        await asyncio.sleep(60)
        if AUTOBIO_ON:
            try:
                AUTOBIO_INDEX = (AUTOBIO_INDEX+1)%len(AUTOBIO_LIST); await app.bot.set_my_description(AUTOBIO_LIST[AUTOBIO_INDEX])
            except: pass
def get_all_sets():
    return [AUTOPIN_CHATS, AUTOREACT_CHATS, AUTOREPLY_CHATS, AUTOSHAYARI_CHATS, AUTOGM_CHATS, AUTOGN_CHATS, AUTO_TAGALL, AUTO_STICKER, AUTO_MOTIVATE, AUTO_THANK, AUTO_HELLO, AUTO_BYE, AUTO_MEME, AUTO_GAME, AUTO_SHOUT, AUTO_REPEAT, AUTO_TRUTH_AUTO, AUTO_POLL, AUTO_QUIZ, AUTO_BIRTHDAY, AUTO_STATS, AUTO_JOIN, AUTO_LEAVE, AUTO_SHOUTOUT, AUTO_COMPLIMENT, AUTO_EMOJI, AUTO_PHOTO, AUTO_VOICE]
async def alloff(update, context):
    if not await need_admin(update): return
    for s in get_all_sets(): s.clear()
    await send(update, box("🔴 ALLOFF HO GAYA! Sab auto OFF!"))
async def allon(update, context):
    if not await need_admin(update): return
    cid = update.effective_chat.id
    for s in get_all_sets(): s.add(cid)
    await send(update, box("🟢 ALLON HO GAYA! 🔥 Sab auto ON!"))
AUTO_MAP = {"autotagall":(AUTO_TAGALL,"AUTOTAGALL"),"autosticker":(AUTO_STICKER,"AUTOSTICKER"),"automotivate":(AUTO_MOTIVATE,"AUTO MOTIVATE"),"autothank":(AUTO_THANK,"AUTO THANK"),"autohello":(AUTO_HELLO,"AUTO HELLO"),"autobye":(AUTO_BYE,"AUTO BYE"),"automeme":(AUTO_MEME,"AUTO MEME"),"autogame":(AUTO_GAME,"AUTO GAME"),"autoshout":(AUTO_SHOUT,"AUTO SHOUT"),"autorepeat":(AUTO_REPEAT,"AUTO REPEAT"),"autotruth":(AUTO_TRUTH_AUTO,"AUTO TRUTH"),"autopoll":(AUTO_POLL,"AUTO POLL"),"autoquiz":(AUTO_QUIZ,"AUTO QUIZ"),"autobirthday":(AUTO_BIRTHDAY,"AUTO BIRTHDAY"),"autostats":(AUTO_STATS,"AUTO STATS"),"autojoin":(AUTO_JOIN,"AUTO JOIN"),"autoleave":(AUTO_LEAVE,"AUTO LEAVE"),"autoshoutout":(AUTO_SHOUTOUT,"AUTO SHOUTOUT"),"autocompliment":(AUTO_COMPLIMENT,"AUTO COMPLIMENT"),"autoemoji":(AUTO_EMOJI,"AUTO EMOJI"),"autophoto":(AUTO_PHOTO,"AUTO PHOTO"),"autovoice":(AUTO_VOICE,"AUTO VOICE")}
def make_auto_handler(set_obj, label):
    async def h(update, context):
        if not await need_admin(update): return
        cid = update.effective_chat.id
        if context.args and context.args[0].upper()=="OFF": set_obj.discard(cid); await send(update, box(f"{label} OFF! ❌")); return
        set_obj.add(cid); await send(update, box(f"{label} ON! 🔥\nAb ye auto kaam karega!"))
        if label=="AUTO POLL": await send(update, box("📊 POLL: Aaj Ka Best Kaun?\n1. Kashyap 2. Demon 3. Sab"))
        if label=="AUTO QUIZ": await send(update, box("❓ QUIZ: Bharat ki Rajdhani?\nA) Delhi B) Mumbai"))
        if label=="AUTO GAME": await send(update, box("🎲 GAME TIME! /PASA ya /SIKKA likh!"))
        if label=="AUTO TRUTH": await send(update, box("❓ TRUTH: Tera crush kaun hai? 😏"))
        if label=="AUTO MOTIVATE": await send(update, box("🔥 MOTIVATE: Uth Ja! Aaj Tera Din Hai!"))
    return h
async def auto_watcher(update, context):
    try:
        msg = update.message
        if not msg or (msg.from_user and msg.from_user.is_bot): return
        chat_id = update.effective_chat.id; user = update.effective_user
        text = (msg.text or "").lower(); orig = msg.text or ""
        MSG_COUNT[user.id] = MSG_COUNT.get(user.id,0)+1
        if msg.reply_to_message and msg.reply_to_message.from_user.id in AFK_USERS:
            await send(update, box(f"😴 {msg.reply_to_message.from_user.first_name} abhi AFK hai! Wajah: {AFK_USERS[msg.reply_to_message.from_user.id]}"))
        if chat_id in AUTO_HELLO and "hi" in text: await send(update, box(f"Hi {user.first_name}! Welcome! 🔥"))
        if chat_id in AUTO_BYE and "bye" in text: await send(update, box(f"Bye Bye {user.first_name}! Jaldi Aana! 👋"))
        if chat_id in AUTO_THANK and ("thank" in text or "thanks" in text): await send(update, box(f"Welcome {user.first_name} ❤️"))
        if chat_id in AUTO_MOTIVATE and any(w in text for w in ["sad","dukhi","thak","tension"]): await send(update, box(f"{user.first_name} Tension mat le, tu best hai ❤️"))
        if chat_id in AUTO_COMPLIMENT and any(w in text for w in ["sad","dukhi","rona"]): await send(update, box(f"{user.first_name} Tu bahut acha hai yaar! ❤️"))
        if chat_id in AUTO_SHOUTOUT and any(w in text for w in ["mast","badiya","great","op"]): await send(update, box(f"Shoutout To {user.first_name} - Mast Bola! 👏🔥"))
        if chat_id in AUTO_MEME and "meme" in text: await send(update, box(random.choice(MEMES)))
        if chat_id in AUTO_GAME and any(w in text for w in ["game","khelo"]): await send(update, box("🎲 GAME: /PASA /SIKKA /JADU likh!"))
        if chat_id in AUTO_TRUTH_AUTO and "truth" in text: await send(update, box(f"❓ TRUTH: {random.choice(TRUTHS)}"))
        if chat_id in AUTO_VOICE and "voice" in text: await send(update, box("🎙️ VOICE MODE ON! Bol ke dikhao!"))
        if chat_id in AUTO_PHOTO and "photo" in text: await send(update, box("📸 PHOTO AA RAHI HAI! Ruk Ja! 🔥"))
        if chat_id in AUTO_SHOUT and orig: await send(update, box(orig.upper() + " !!! 🔊"))
        if chat_id in AUTO_REPEAT and user.id not in SUDOS and orig: await send(update, box(orig))
        if chat_id in AUTO_EMOJI:
            try: await context.bot.set_message_reaction(chat_id, msg.message_id, reaction=[ReactionTypeEmoji(emoji="❤️")])
            except: pass
        if chat_id in AUTOREACT_CHATS:
            try: await context.bot.set_message_reaction(chat_id, msg.message_id, reaction=[ReactionTypeEmoji(emoji="❤️")])
            except: pass
        if chat_id in AUTOPIN_CHATS:
            try: await msg.pin(disable_notification=True)
            except: pass
        if chat_id in AUTOREPLY_CHATS:
            if "hi" in text: await send(update, "Hi! Kaise Ho? 🔥")
            elif "hello" in text: await send(update, "Hello! 😈")
            elif "good morning" in text: await send(update, "Good Morning! Chai Pi Li? ☀️")
            elif "good night" in text: await send(update, "Good Night! 😴")
            elif "bye" in text: await send(update, "Bye! Jaldi Aana! 👋")
    except Exception as e: print("Watcher error:", e)
async def new_member_handler(update, context):
    try:
        for m in update.message.new_chat_members:
            cid = update.effective_chat.id
            if cid in WELCOME: await send(update, box(WELCOME[cid].replace("{name}", m.first_name)))
            elif cid in AUTO_JOIN: await send(update, box(f"Welcome {m.first_name}! 🔥"))
    except: pass
async def left_member_handler(update, context):
    try:
        if update.message.left_chat_member and update.effective_chat.id in AUTO_LEAVE: await send(update, box(f"Ek Gaya! {update.message.left_chat_member.first_name} left kar gaya 😂👋"))
    except: pass
async def extra(update, context):
    if not await check(update): return
    await send(update, box("🔥 EXTRA MENU 🔥\n/meme - Meme\n/motivate - Motivation\n/song - Gaana\n/birthday - Birthday\n/stats - Stats"))
async def meme(update, context):
    if not await check(update): return
    await send(update, box(random.choice(MEMES)))
async def motivate(update, context):
    if not await check(update): return
    await send(update, box(random.choice(MOTIVATES)))
async def song(update, context):
    if not await check(update): return
    await send(update, box("🎵 SONG: Dil to pagal hai, DEMON BOT ka deewana hai! 🔥"))
async def birthday(update, context):
    if not await check(update): return
    await send(update, box("🎂 HAPPY BIRTHDAY! 🎉 PARTY TO BANTI HAI! 🎉"))
async def stats(update, context):
    if not await check(update): return
    await send(update, box(f"📊 STATS:\nTotal Msg: {sum(MSG_COUNT.values())}\nSUDO: {len(SUDOS)}\nUptime: {int(time.time()-START_TIME)//60} MIN"))

app_bot = None
def main():
    global app_bot
    app = ApplicationBuilder().token(TOKEN).build(); app_bot = app.bot
    cmds = {"start": start, "help": help_cmd, "command": command_cmd, "commands": command_cmd, "madad": madad, "menu": menu_cmd, "all": all_cmd, "myid": myid, "ping": ping, "chalu": chalu, "bareme": bareme, "pehchan": pehchan, "jankari": jankari, "groupid": groupid, "tag": tag, "tagall": tagall, "malik": malik, "niyam": niyam, "uptime": uptime, "bol": bol, "shayari": shayari, "joke": joke, "haso": haso, "truth": truth, "sach": sach, "dare": dare, "himmat": himmat, "pasa": pasa, "sikka": sikka, "ghumao": ghumao, "kainchi": kainchi, "jadu": jadu, "chuno": chuno, "sawal": sawal, "ank": ank, "gale": gale, "panja": panja, "hath": hath, "pyar": pyar, "tariff": tariff, "jodi": jodi, "vichar": vichar, "gin": gin_safe, "ulta": ulta, "bada": bada, "chota": chota, "gino": gino, "samay": samay, "tarikh": tarikh, "behisaab": behisaab, "art": art, "poll": poll, "quiz": quiz, "wyr": wyr, "nhie": nhie, "riddle": riddle, "8ball": eightball, "fact": fact, "quote": quote, "guess": guess, "rps": rps, "slot": slot, "lovecalc": lovecalc, "font": font, "shout": shout, "movie": movie, "cricket": cricket, "news": news, "horoscope": horoscope, "warn": warn, "mute": mute, "unmute": unmute, "purge": purge, "giveaway": giveaway, "count": count, "reminder": reminder, "note": note, "translate": translate, "ai": ai, "dice": dice, "coin": coin, "toss": toss, "ludo": ludo, "king": king, "queen": queen, "top": top, "active": active, "idcard": idcard, "profile": profile, "lucky": lucky, "zodiac": zodiac, "today": today, "party": party, "dance": dance, "sing": sing, "story": story, "rap": rap, "poem": poem, "echo": echo, "say": say, "mimic": mimic, "vs": vs, "battle": battle, "team": team, "winner": winner, "loser": loser, "respect": respect, "shoutout2": shoutout2, "welcome2": welcome2, "bye2": bye2, "gm2": gm2, "gn2": gn2, "password": password, "randomname": randomname, "age": age, "countword": countword, "reverse2": reverse2, "upper2": upper2, "lower2": lower2, "nikal": nikal, "wapas": wapas, "dhakka": dhakka, "chup": chup, "bolnede": bolnede, "chetavni": chetavni, "mitao": mitao, "chipkao": chipkao, "hatao": hatao, "swagatset": swagatset, "swagatoff": swagatoff, "swagattest": swagattest, "autopin": autopin, "autoreact": autoreact, "autoreply": autoreply, "autoshayari": autoshayari, "autogm": autogm, "autogn": autogn, "gm": gm, "gn": gn, "afk": afk, "back": back, "addsudo": addsudo, "delsudo": delsudo, "sudolist": sudolist, "autobio": autobio, "alloff": alloff, "allon": allon, "stopall": alloff, "reset": alloff, "extra": extra, "meme": meme, "motivate": motivate, "song": song, "birthday": birthday, "stats": stats}
    for n, fn in cmds.items(): app.add_handler(CommandHandler(n, fn))
    for cmd_name, (set_obj, label) in AUTO_MAP.items(): app.add_handler(CommandHandler(cmd_name, make_auto_handler(set_obj, label)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_watcher), group=1)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member_handler))
    print("DEMON BOT STARTED - SUDOS:", SUDOS)
    try: asyncio.get_event_loop().create_task(autobio_loop(app))
    except: pass
    app.run_polling()
flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__": main()
