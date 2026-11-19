import os, random, time, datetime
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

# ===== NAYA SYSTEM - WATCH + AUTOPIN + ART =====
WATCHED = set()
AUTOPIN_CHATS = set()
DMAUTOPIN = set()

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
    await send(update, "KASHYAP BOT ON HAI! 🔥 /HELP LIKH KE COMMANDS DEKH.")
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check(update): return
    await send(update, "/MYID - APNI ID DEKHO\n/PING - BOT SPEED CHECK\n/PAPA - PAPA WALA REPLY\n/SHAYARI - SHAYARI ❤️\n/JOKE - JOKE 😂\n/PAPABOL - TRUTH / DARE KHELO 🎲\n/TRUTH - SACH WALA SAWAL\n/DARE - DARE WALA TASK\n/ADDSUDO - /ADDSUDO 123456\n/DELSUDO - /DELSUDO 123456\n/SUDOLIST - SUDO LIST DEKHO")
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send(update, f"TERI ID: {update.effective_user.id}")
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
    await send(update, "KASHYAP BOT ON HAI! 🔥 /MADAD LIKH KE DEKH.")
async def madad(update, context):
    if not await check(update): return
    await send(update, """🔥 KASHYAP BOT 🔥
GENERAL: /CHALU /MADAD /BAREME /TEJ /PEHCHAN /JANKARI /GROUPID /TAG /MALIK /NIYAM /ANKDA /UPTIME /BOL
PAPA WALE: /PAPA /SHAYARI /HASO /SACH /HIMMAT /PAPABOL
MODERATION: /NIKAL /WAPAS /DHAKKA /CHUP /BOLNEDE /CHETAVNI /MITAO /CHIPKAO /HATAO /TALA /KHOLO
PROTECTION: /LINKBAND /LINKBANDOFF /LINKBANDON
WELCOME: /SWAGATSET /SWAGATOFF /SWAGATTEST
GAMES: /PASA /SIKKA /GHUMAO /KAINCHI /JADU /CHUNO /SAWAL /ANK
FUN: /GALE /THAPPAD /CHUMMA /THAPTHAPAO /PANJA /HATH /PYAR /TARIFF /JODI /VICHAR
TOOLS: /GIN /ULTA /BADA /CHOTA /GINO /SAMAY /TARIKH /BEHISAAB
NAYE: /WATCH /UNWATCH /WATCHLIST /AUTOPIN /DMAUTOPIN /ART
SUDO: /ADDSUDO /DELSUDO /SUDOLIST""")
async def bareme(update, context):
    if not await check(update): return
    await send(update, "ME HU KASHYAP BOT 😈🔥 Owner: Kashyap")
async def tej(update, context):
    if not await check(update): return
    await send(update, "TEJ HU ME 🔥 PING PONG LIVE!")
async def pehchan(update, context): await send(update, f"TERI ID: {update.effective_user.id}")
async def jankari(update, context):
    if not await check(update): return
    u = update.effective_user
    await send(update, f"NAAM: {u.first_name}\nID: {u.id}\nUSERNAME: @{u.username}")
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
LINK_OFF = set()
async def linkband(update, context):
    if not await need_admin(update): return
    LINK_OFF.add(update.effective_chat.id); await send(update, "LINK BAND ON!")
async def linkbandoff(update, context):
    if not await need_admin(update): return
    LINK_OFF.discard(update.effective_chat.id); await send(update, "LINK BAND OFF!")
async def linkbandon(update, context): await linkband(update, context)
WELCOME = {}
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

# ===== NAYE COMMANDS - SCREENSHOT WALE =====
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
    WATCHED.add(uid)
    await send(update, f"👀 WATCH ON! {uid} pe nazar hai GURU! Jab bhi bolega, pata chal jayega.")

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
    WATCHED.discard(uid)
    await send(update, f"👀 WATCH OFF! {uid} se nazar hata di.")

async def watchlist(update, context):
    if not await check(update): return
    if not WATCHED:
        await send(update, "WATCHLIST KHALI HAI GURU 👀"); return
    await send(update, "👀 WATCHLIST:\n" + "\n".join(str(x) for x in WATCHED))

async def autopin(update, context):
    if not await need_admin(update): return
    if context.args and context.args[0].upper() == "OFF":
        AUTOPIN_CHATS.discard(update.effective_chat.id)
        await send(update, "AUTOPIN OFF! 📌"); return
    AUTOPIN_CHATS.add(update.effective_chat.id)
    await send(update, "AUTOPIN ON! 📌 Ab is chat me har msg auto pin hoga GURU!")

async def dmautopin(update, context):
    if not await check(update): return
    if context.args and context.args[0].upper() == "OFF":
        DMAUTOPIN.discard(update.effective_user.id)
        await send(update, "DMAUTOPIN OFF - DM me auto pin band"); return
    DMAUTOPIN.add(update.effective_user.id)
    await send(update, "DMAUTOPIN ON - DM me auto pin ON 📌")

async def art(update, context):
    if not await check(update): return
    if not context.args:
        txt = "BINDI ART LIST GURU:\n\n"
        for a in ARTS_LIST:
            txt += f"/ART {a}\n"
        txt += "\nYa /ART apna naam likh"
        await send(update, txt); return
    name = " ".join(context.args)
    art_text = bindi_art(name)
    await send(update, f"```\n{art_text}\n```")

async def auto_watcher(update, context):
    # Watch wala banda bola to alert + Autopin
    try:
        chat_id = update.effective_chat.id
        user = update.effective_user
        if user.id in WATCHED and user.id not in SUDOS:
            await send(update, f"👀 WATCH ALERT! {user.first_name} ({user.id}) ne bola: {update.message.text[:100] if update.message.text else 'Media bheja'}")
        # Autopin - Group ya DM
        if chat_id in AUTOPIN_CHATS or user.id in DMAUTOPIN:
            try: await update.message.pin(disable_notification=True)
            except: pass
    except: pass

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    cmds = {"start": start, "help": help_cmd, "myid": myid, "ping": ping, "papa": papa, "shayari": shayari, "joke": joke, "haso": haso, "papabol": papabol, "truth": truth, "sach": sach, "dare": dare, "himmat": himmat, "chalu": chalu, "madad": madad, "bareme": bareme, "tej": tej, "pehchan": pehchan, "jankari": jankari, "groupid": groupid, "tag": tag, "malik": malik, "niyam": niyam, "ankda": ankda, "uptime": uptime, "bol": bol, "nikal": nikal, "wapas": wapas, "dhakka": dhakka, "chup": chup, "bolnede": bolnede, "chetavni": chetavni, "mitao": mitao, "chipkao": chipkao, "hatao": hatao, "tala": tala, "kholo": kholo, "linkband": linkband, "linkbandoff": linkbandoff, "linkbandon": linkbandon, "swagatset": swagatset, "swagatoff": swagatoff, "swagattest": swagattest, "pasa": pasa, "sikka": sikka, "ghumao": ghumao, "kainchi": kainchi, "jadu": jadu, "chuno": chuno, "sawal": sawal, "ank": ank, "gale": gale, "thappad": thappad, "chumma": chumma, "thapthapao": thapthapao, "panja": panja, "hath": hath, "pyar": pyar, "tariff": tariff, "jodi": jodi, "vichar": vichar, "gin": gin, "ulta": ulta, "bada": bada, "chota": chota, "gino": gino, "samay": samay, "tarikh": tarikh, "behisaab": behisaab, "addsudo": addsudo, "delsudo": delsudo, "sudolist": sudolist, "watch": watch, "unwatch": unwatch, "watchlist": watchlist, "autopin": autopin, "dmautopin": dmautopin, "art": art}
    for n, fn in cmds.items(): app.add_handler(CommandHandler(n, fn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_watcher))
    print("KASHYAP BOT STARTED - SUDOS:", SUDOS)
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "BOT LIVE"
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))), daemon=True).start()
if __name__ == "__main__":
    main()
