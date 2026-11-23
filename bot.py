import os, random, asyncio, time, json, datetime, threading, sys, traceback
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
app = Flask(__name__)
@app.route('/')
def home(): return "KASHYAP BOT IS ALIVE!"
def run_flask():
    try:
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)
    except Exception as e: print(f"FLASK ERROR: {e}", flush=True)
threading.Thread(target=run_flask, daemon=True).start()
API_ID = int(os.environ.get("API_ID", "0").strip() or "0")
API_HASH = os.environ.get("API_HASH", "").strip()
SESSION = os.environ.get("SESSION", "").strip()
OWNER_ID = int(os.environ.get("OWNER_ID", "0").strip() or "0")
print(f"CHECK - API_ID={API_ID} SESSION_LEN={len(SESSION)} OWNER_ID={OWNER_ID}", flush=True)
SESSION_OBJ = StringSession(SESSION) if len(SESSION) > 50 else SESSION
SUDO_FILE = "sudo_users.json"
try:
    with open(SUDO_FILE) as f: SUDO_USERS = set(json.load(f))
except: SUDO_USERS = set()
def save_sudo():
    try:
        with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)
    except: pass
def is_owner(e):
    try:
        if getattr(e, "out", False): return True
        if getattr(getattr(e, "message", None), "out", False): return True
    except: pass
    if OWNER_ID != 0 and e.sender_id == OWNER_ID: return True
    return False
def is_sudo(e):
    if is_owner(e): return True
    if e.sender_id in SUDO_USERS: return True
    return False
DENY_TEXT = "**ONLY OWNER / SUDO CAN USE THIS BOT!**\n**PLEASE TAKE SUDO FIRST!**\n**KASHYAP BOT IS PRIVATE!**"
START = time.time()
def uptime():
    s = int(time.time() - START)
    return f"{s//3600}h {(s%3600)//60}m"
client = TelegramClient(SESSION_OBJ, API_ID, API_HASH)
def NM(p): return events.NewMessage(outgoing=True, incoming=True, pattern=p)
async def anim(e, steps):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    m = await client.send_message(e.chat_id, steps[0])
    for s in steps[1:]:
        await asyncio.sleep(1.2)
        try: await m.edit(s)
        except: pass
    return m
async def anim_owner(e, steps):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    await anim(e, steps)
async def mega_anim(e, frames):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    m = await client.send_message(e.chat_id, frames[0])
    for f in frames[1:]:
        await asyncio.sleep(2)
        try: await m.edit(f)
        except: pass
    return m
async def blue_anim(e, frames):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    m = await client.send_message(e.chat_id, frames[0])
    for f in frames[1:]:
        await asyncio.sleep(2)
        try: await m.edit(f)
        except: pass
    return m
async def anim_fast30(e, frames):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    m = await client.send_message(e.chat_id, frames[0])
    start = time.time()
    while time.time() - start < 30:
        for f in frames[1:]:
            if time.time() - start >= 30: break
            await asyncio.sleep(0.8)
            try: await m.edit(f)
            except: pass
    return m
def BLUE(txt): return "```\n" + txt + "\n```"
def WHITE(txt): return "```\n" + txt + "\n```"
PIC_FILE = "photo_2026-11-21_19-54-14.jpg"
@client.on(NM(r"\.myid"))
async def myid_cmd(e):
    await client.send_message(e.chat_id, f"**Teri ID:** `{e.sender_id}`\n**Chat ID:** `{e.chat_id}`\n**Outgoing:** `{getattr(e, 'out', False)}`")
@client.on(NM(r"\.pic"))
async def pic_cmd(e):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    try: await client.send_file(e.chat_id, PIC_FILE, caption="**KASHYAP**\n**KING IS BACK!**")
    except: await anim(e, ["**OPENING PHOTO...**", "**PHOTO NOT FOUND! GitHub me photo check karo!**"])
@client.on(NM(r"\.photo"))
async def photo_cmd(e):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    try: await client.send_file(e.chat_id, PIC_FILE, caption="**KASHYAP**\n**STYLE KING!**")
    except: await anim(e, ["**OPENING PHOTO...**", "**PHOTO NOT FOUND!**"])
@client.on(NM(r"\.addsudo(?: |$)(.*)"))
async def addsudo(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    arg = e.pattern_match.group(1).strip()
    rep = await e.get_reply_message()
    uid = int(arg) if arg.isdigit() else (rep.sender_id if rep else None)
    if not uid:
        await anim(e, ["**CHECKING...**", "**Use: `.addsudo 123456`**"]); return
    SUDO_USERS.add(uid); save_sudo()
    await anim(e, ["**ADDING SUDO...**", "**SUDO ADDED!**", f"**NEW KING!**\n**ID:** `{uid}`"])
@client.on(NM(r"\.remsudo(?: |$)(.*)"))
async def remsudo(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    arg = e.pattern_match.group(1).strip()
    rep = await e.get_reply_message()
    uid = int(arg) if arg.isdigit() else (rep.sender_id if rep else None)
    if not uid:
        await anim(e, ["**CHECKING...**", "**Use: `.remsudo 123456`**"]); return
    SUDO_USERS.discard(uid); save_sudo()
    await anim(e, ["**REMOVING SUDO...**", f"**SUDO REMOVED! ID:** `{uid}`"])
@client.on(NM(r"\.sudolist"))
async def sudolist(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    if not SUDO_USERS: await anim(e, ["**OPENING LIST...**", "**SUDO LIST IS EMPTY!**"])
    else: await anim(e, ["**OPENING LIST...**", "**SUDO LIST**\n" + "\n".join([f"- `{x}`" for x in SUDO_USERS])])
@client.on(NM(r"\.alive"))
async def alive(e):
    await anim(e, [BLUE("KASHYAP USERBOT\nLOADING..."), BLUE("KASHYAP USERBOT\nSTATUS : ONLINE\nVERSION : V20"), f"**KASHYAP IS ALIVE!**\n\n**OWNER : KASHYAP**\n**STATUS : ONLINE**\n**VERSION : V20 ALL IN ONE**\n**UPTIME : {uptime()}**\n**SUDO : {len(SUDO_USERS)}**\n\n**NOW KASHYAP WILL RULE!**"])
@client.on(NM(r"\.help"))
async def help_cmd(e):
    await anim(e, [BLUE("KASHYAP USERBOT - HELP MENU - V20\n\nUTILITIES\n.alive .ping .help .id .info .time .uptime .stats .profile .pic .photo .myid\n\nSUDO\n.addsudo .remsudo .sudolist\n\nFUN\n.joke .roast .shayari .meme .attitude .truth .dare .ship .slap .kiss .hug .pickup .cute .flirt .dice .coin .luck .lovecalc .future .crush .horoscope\n\nSTYLE\n.echo .shout .bold .reverse .say .bio .caption\n\nWORK\n.calc .weather .crypto .google .anime .songdl\n\nGROUP\n.tagall .purge .kick .ban .unban .mute .unmute .promote .demote"), BLUE("HACK MENU - BLUE SCREEN - ONLY ANIMATION\n\nMEGA HACK\n.megahack .hackwifi .hackinsta .hackphone .hackbank .hackcctv\n\nDONE HACK\n.hack2 .ddos .trace .virus .darkweb .cctv .whatsapp .passwordhack .location .number .varius .hackanim"), BLUE("MEGA MENU\n\nMEGA LOVE\n.megalove .megapropose .megawedding .megabreakup .megacrush .love .heart\n\nMEGA FUN\n.megapolice .megaexam .megaghost .megamoney .megafight .megabirthday .megaalien .megajailbreak .megadon .megamafia .megachai .megapizza .megacricket .megafootball .megaschool .megaiphone .megasuperhero .megazombie .megavirus .megabomb\n\nANIMATION\n.bomb .load .fire .moon .dance .rain .run"), BLUE("KASHYAP MENU\n.jail .free .kill .revive .wanted .gang .sus .vs .top .mafia .don .king .queen\n\nTYPE .help FOR ALL MENU"), BLUE("MOVING ANIMATION\n\nMOVING 1\n.train .heartbig .fightbig .rocket .carrace .plane .bike .cycle .ship .runbig\n\nMOVING 2\n.bus .policechase .cricketbig .footballbig .firebig .rainbig .snake .catdog .pubg .moneyfly .dancebig .maggi .thief .ghostrun .lovefly")])
@client.on(NM(r"\.tarunpapa"))
async def tarunpapa(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    txt = "PRIVATE - ALL COMMANDS\n\nUTILITIES: .alive .ping .help .id .info .time .uptime .stats .profile .pic .photo .myid\n\nSUDO: .addsudo .remsudo .sudolist\n\nFUN: .joke .roast .shayari .meme .attitude .truth .dare .ship .slap .kiss .hug .pickup .cute .flirt .dice .coin .luck .lovecalc .future .crush .horoscope\n\nSTYLE: .echo .shout .bold .reverse .say .bio .caption\n\nWORK: .calc .weather .crypto .google .anime .songdl\n\nGROUP: .tagall .purge .kick .ban .unban .mute .unmute .promote .demote\n\nHACK ANIMATION: .megahack .hackwifi .hackinsta .hackphone .hackbank .hackcctv .hack2 .ddos .trace .virus .darkweb .cctv .whatsapp .passwordhack .location .number .varius .hackanim\n\nMEGA LOVE: .megalove .megapropose .megawedding .megabreakup .megacrush .love .heart\n\nMEGA FUN: .megapolice .megaexam .megaghost .megamoney .megafight .megabirthday .megaalien .megajailbreak .megadon .megamafia .megachai .megapizza .megacricket .megafootball .megaschool .megaiphone .megasuperhero .megazombie .megavirus .megabomb\n\nANIMATION: .bomb .load .fire .moon .dance .rain .run\n\nKASHYAP: .jail .free .kill .revive .wanted .gang .sus .vs .top .mafia .don .king .queen\n\nMOVING 1: .train .heartbig .fightbig .rocket .carrace .plane .bike .cycle .ship .runbig\n\nMOVING 2: .bus .policechase .cricketbig .footballbig .firebig .rainbig .snake .catdog .pubg .moneyfly .dancebig .maggi .thief .ghostrun .lovefly\n\nFAST 30 SEC: .dil .aag .chand .rainbow .phool .barish .taara .suraj .samundar .balloon .batti .gola .cat .momos .danceemoji .moon2 .moon3 .love2 .fire2 .diamond\n\nNEW EMOJI 20: .rosebike .propose2 .shadi2 .police2 .chor2 .cricket2 .pubg2 .chai2 .maggi2 .rain2 .fireworks .birthday2 .ghost2 .alien2 .money2 .fight2 .dance2 .heartfly .rocket2 .loveletter\n\nNEW TEXT 10: .loveletter2 .bhaag .dost .gunda .hero .khaana .yaar .pagal .raja .rider\n\nPRIVATE: .tarunpapa"
    await client.send_message(e.chat_id, WHITE(txt))
@client.on(NM(r"\.ping"))
async def ping(e):
    if not is_sudo(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    start = time.time()
    m = await client.send_message(e.chat_id, "**PINGING...**")
    ms = int((time.time() - start) * 1000)
    await asyncio.sleep(0.5)
    try: await m.edit(f"**KASHYAP X HOSTER is now Active!**\n\n**Pong ~ {ms} ms**\n**SPEED : ULTRA FAST**\n**OWNER : KASHYAP**\n\n**KASHYAP IS BACK!**")
    except: pass
@client.on(NM(r"\.id"))
async def idc(e):
    r = await e.get_reply_message()
    if r: await anim(e, [BLUE("FINDING ID..."), f"**ID:** `{r.sender_id}`"])
    else: await anim(e, [BLUE("FINDING ID..."), f"**Your ID:** `{e.sender_id}`\n**Chat ID:** `{e.chat_id}`"])
@client.on(NM(r"\.time"))
async def timec(e):
    await anim(e, [BLUE("CHECKING TIME..."), f"**TIME:** {datetime.datetime.now().strftime('%I:%M %p')} | **{datetime.datetime.now().strftime('%d %B %Y')}**"])
@client.on(NM(r"\.uptime"))
async def upc(e):
    await anim(e, [BLUE("CHECKING UPTIME..."), f"**UPTIME:** {uptime()}"])
@client.on(NM(r"\.info"))
async def infoc(e):
    r = await e.get_reply_message()
    u = r.sender if r else await e.get_sender()
    await anim(e, [BLUE("FETCHING INFO..."), f"**INFO**\n**Name:** {u.first_name}\n**ID:** `{u.id}`\n**Username:** @{u.username or 'Not Available'}"])
@client.on(NM(r"\.profile"))
async def profile(e):
    await anim(e, [BLUE("OPENING PROFILE..."), f"**PROFILE - KASHYAP**\n**ID:** `{e.sender_id}`\n**Status:** KING"])
@client.on(NM(r"\.stats"))
async def stats(e):
    await anim(e, [BLUE("LOADING STATS..."), f"**STATS**\n**Uptime:** {uptime()}\n**Sudo:** {len(SUDO_USERS)}\n**Version:** V20"])
def anim_one(pattern, steps_list):
    async def h(e): await anim(e, steps_list)
    client.on(NM(pattern))(h)
anim_one(r"\.joke", ["🤔 **THINKING OF A JOKE...**", "😂 **FOUND IT!**", "**JOKE:**\nTeacher: Why didn't you do homework?\nStudent: Sir, KASHYAP turned off the internet! 😂"])
anim_one(r"\.roast", ["🔥 **COOKING A ROAST...**", "🔥 **ROAST READY!**", "**ROAST:**\nYour face is so funny, even the mirror says - Bro, I will break! 🤣"])
anim_one(r"\.shayari", ["✍️ **WRITING SHAYARI...**", "**SHAYARI:**\n❤️ I got so lost in your memories,\nEven KASHYAP said - Bro, you are gone! ❤️"])
anim_one(r"\.meme", ["😂 **FINDING A MEME...**", "**MEME:**\nWhen KASHYAP comes online, everyone's phone hangs! 📱😂"])
anim_one(r"\.attitude", ["😎 **LOADING ATTITUDE...**", "**ATTITUDE:**\n👑 **I am KASHYAP, I don't bow, I make others bow!** 👑"])
anim_one(r"\.truth", ["🤔 **THINKING TRUTH...**", "**TRUTH:**\nWhat is your biggest secret? Tell me! 🤫"])
anim_one(r"\.dare", ["😈 **THINKING DARE...**", "**DARE:**\nSend I Love You to your crush! ❤️😂"])
anim_one(r"\.pickup", ["😍 **THINKING PICKUP LINE...**", "**PICKUP:**\nAre you WiFi? Because I want to connect with you! 📶❤️"])
anim_one(r"\.cute", ["🥺 **CHECKING...**", "**CUTE:**\nYou are so cute, even KASHYAP melted! 🥺❤️"])
anim_one(r"\.flirt", ["😘 **FLIRT MODE ON...**", "**FLIRT:**\nEven KASHYAP is in love with your smile! 😘"])
anim_one(r"\.slap", ["✋ **RAISING HAND...**", "💥 **SLAP! That was hard!** 💥"])
anim_one(r"\.kiss", ["😘 **COMING CLOSER...**", "💋 **KISS! Oh this love!** 💋"])
anim_one(r"\.hug", ["🤗 **OPENING ARMS...**", "🤗 **HUG! One hug is a must!** 🤗"])
anim_one(r"\.dice", ["🎲 **ROLLING DICE...**", f"🎲 **DICE:** {random.randint(1,6)}"])
anim_one(r"\.coin", ["🪙 **TOSSING COIN...**", "**COIN:** 👑 HEADS"])
anim_one(r"\.crush", ["💘 **CHECKING CRUSH...**", "**CRUSH:**\nYour crush is also looking at you! 👀❤️"])
anim_one(r"\.horoscope", ["🔮 **READING STARS...**", "**HOROSCOPE:**\nToday is your lucky day! KASHYAP promises! ⭐"])
anim_one(r"\.future", ["🔮 **SEEING FUTURE...**", "**FUTURE:**\nYou will become a very big man one day, KASHYAP promises! 👑"])
anim_one(r"\.jail", ["🚨 **CATCHING YOU...**", "⛓️ **YOU ARE IN JAIL! You cannot go out now!** ⛓️"])
anim_one(r"\.free", ["🔑 **FINDING KEY...**", "🕊️ **YOU ARE FREE! KASHYAP forgave you!** 🕊️"])
anim_one(r"\.kill", ["🎯 **AIMING...**", "💥 **KILL! KASHYAP FINISHED YOU! - IT'S A DONE!** 💥"])
anim_one(r"\.revive", ["💉 **GIVING INJECTION...**", "❤️ **REVIVE! You are alive again!** ❤️"])
anim_one(r"\.wanted", ["📜 **MAKING POSTER...**", "🚨 **WANTED! Reward: 10 Crore! Everyone is searching for KASHYAP!** 🚨"])
anim_one(r"\.gang", ["😎 **CALLING GANG...**", "**GANG: KASHYAP GANG - Most Dangerous!** 😎🔥"])
anim_one(r"\.sus", ["👀 **CHECKING...**", "**SUS: You are looking very SUS today!** 👀"])
anim_one(r"\.vs", ["⚔️ **FIGHT STARTING...**", "**VS: KASHYAP VS WORLD - KASHYAP WILL WIN!** ⚔️👑"])
anim_one(r"\.top", ["🏆 **MAKING LIST...**", "**TOP: No.1 - KASHYAP** 👑🏆"])
anim_one(r"\.mafia", ["🕶️ **MAFIA COMING...**", "**MAFIA: KASHYAP MAFIA!** 🕶️"])
anim_one(r"\.don", ["🕶️ **DON COMING...**", "**DON: 11 countries police are waiting for Don!** 🚨"])
anim_one(r"\.king", ["👑 **WEARING CROWN...**", "**KING: KING IS BACK - KASHYAP!** 👑"])
anim_one(r"\.queen", ["👸 **QUEEN COMING...**", "**QUEEN: Queen will be only KASHYAP's!** 👸❤️"])
anim_one(r"\.tagall", ["📣 **CALLING EVERYONE...**", "**TAG ALL! Everyone come, KASHYAP is calling!** 📣"])
anim_one(r"\.purge", ["🧹 **CLEANING...**", "**PURGE! All trash cleaned!** 🧹"])
anim_one(r"\.kick", ["🦶 **KICKING...**", "**KICK! Out of group!** 🦶"])
anim_one(r"\.ban", ["🚫 **BANNING...**", "**BAN! KASHYAP banned you!** 🚫"])
anim_one(r"\.unban", ["✅ **BRINGING BACK...**", "**UNBAN! You are back!** ✅"])
anim_one(r"\.mute", ["🤫 **MUTING...**", "**MUTE! Now be quiet!** 🤫"])
anim_one(r"\.unmute", ["🔊 **UNMUTING...**", "**UNMUTE! Now you can speak!** 🔊"])
anim_one(r"\.promote", ["⬆️ **PROMOTING...**", "**PROMOTE! Now you are also Admin!** ⬆️👑"])
anim_one(r"\.demote", ["⬇️ **DEMOTING...**", "**DEMOTE! Removed from Admin!** ⬇️"])
anim_one(r"\.bio", ["✍️ **THINKING BIO...**", "**BIO IDEA:**\n`👑 KASHYAP | King | No Mercy 👑`"])
anim_one(r"\.caption", ["📸 **THINKING CAPTION...**", "**CAPTION:**\n`👑 KING IS BACK #KASHYAP 👑`"])
anim_one(r"\.songdl", ["🎵 **FINDING SONG...**", "**SONG: Search on YouTube, KASHYAP is playing song!** 🎵"])
@client.on(NM(r"\.luck"))
async def luck(e): await anim(e, ["🍀 **CHECKING LUCK...**", f"🍀 **LUCK:** {random.randint(1,100)}% 🍀"])
@client.on(NM(r"\.lovecalc"))
async def lovecalc(e): await anim(e, ["💘 **CALCULATING LOVE...**", "💘 **CALCULATING LOVE... 50%**", f"💘 **LOVE CALC:** {random.randint(50,100)}% Made For Each Other! 💘"])
@client.on(NM(r"\.ship"))
async def ship(e):
    await anim(e, ["🚢 **MAKING SHIP...**", f"💘 **SHIP:** {random.randint(1,100)}% Match! 💘"])
    await mega_anim(e, ["🚢 **SHIP PORT PE HAI...**", "🚢💨 **SHIP CHAL PADA!**", "🌊🚢 **SHIP SAMUNDAR ME HAI!**", "🌪️ **TOOFAN AA GAYA!**", "💰 **KASHYAP KO KHAZANA MIL GAYA!** 💰"])
@client.on(NM(r"\.ship2"))
async def ship2(e): await mega_anim(e, ["🚢 **SHIP PORT PE HAI...**", "🚢💨 **SHIP CHAL PADA!**", "🌊🚢 **SHIP SAMUNDAR ME HAI!**", "🌪️ **TOOFAN AA GAYA!**", "💰 **KASHYAP KO KHAZANA MIL GAYA!** 💰"])
@client.on(NM(r"\.calc(?: |$)(.*)"))
async def calc(e):
    q = e.pattern_match.group(1).strip()
    try:
        import ast, operator
        if not q or any(c not in "0123456789+-*/(). " for c in q): raise ValueError
        tree = ast.parse(q, mode='eval')
        def _eval(n):
            if isinstance(n, ast.Expression): return _eval(n.body)
            if isinstance(n, ast.Constant): return n.value
            if isinstance(n, ast.BinOp):
                l=_eval(n.left); r=_eval(n.right)
                return {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}[type(n.op)](l,r)
            if isinstance(n, ast.UnaryOp): return -_eval(n.operand)
            raise ValueError
        await anim(e, [BLUE("CALCULATING..."), f"🧮 **CALC:** `{q}` = **{_eval(tree)}**"])
    except: await anim(e, ["**CHECKING...**", "**Write correctly: `.calc 2+2`**"])
@client.on(NM(r"\.echo(?: |$)(.*)"))
async def echo(e):
    rep = await e.get_reply_message()
    if rep and rep.text: await anim(e, ["👂 **LISTENING...**", rep.text])
    else: await anim(e, ["👂 **LISTENING...**", e.pattern_match.group(1) or "**Write something!**"])
@client.on(NM(r"\.say(?: |$)(.*)"))
async def say(e): await anim(e, ["🗣️ **SPEAKING...**", e.pattern_match.group(1) or "**Write something!**"])
@client.on(NM(r"\.shout(?: |$)(.*)"))
async def shout(e): await anim(e, ["📣 **SHOUTING...**", f"**{e.pattern_match.group(1).upper()}**"])
@client.on(NM(r"\.bold(?: |$)(.*)"))
async def bold(e): await anim(e, ["**MAKING BOLD...**", f"**{e.pattern_match.group(1)}**"])
@client.on(NM(r"\.reverse(?: |$)(.*)"))
async def reverse(e): await anim(e, ["🔄 **REVERSING...**", e.pattern_match.group(1)[::-1]])
@client.on(NM(r"\.weather(?: |$)(.*)"))
async def weather(e):
    c = e.pattern_match.group(1) or "Indore"
    await anim(e, [BLUE("CHECKING WEATHER..."), f"🌤️ **WEATHER - {c}**\n**Temp:** {random.randint(25,35)}°C"])
@client.on(NM(r"\.crypto(?: |$)(.*)"))
async def crypto(e): await anim(e, [BLUE("CHECKING RATE..."), "🪙 **CRYPTO:**\n**BTC:** $97,000\n**ETH:** $3,400"])
@client.on(NM(r"\.google(?: |$)(.*)"))
async def google(e):
    q = e.pattern_match.group(1)
    await anim(e, [BLUE("GOOGLING..."), f"🔍 **GOOGLE:** {q}\nhttps://www.google.com/search?q={q.replace(' ','+')}"])
@client.on(NM(r"\.anime(?: |$)(.*)"))
async def anime(e): await anim(e, [BLUE("FINDING ANIME..."), f"🎌 **ANIME:** {e.pattern_match.group(1)}\n**KASHYAP's fav: One Piece!**"])
@client.on(NM(r"\.love"))
async def love(e): await anim(e, ["🖤 **HEART IS EMPTY...**", "💗 **HEART IS FILLING...**", "💓 **HEART IS BEATING...**", "❤️ **HEART IS FULL!**", "❤️ **I LOVE YOU** ❤️"])
@client.on(NM(r"\.heart"))
async def heart(e): await anim(e, ["❤️ **HEART**", "❤️❤️ **HEART HEART**", "❤️❤️❤️ **HEART TO HEART** ❤️"])
@client.on(NM(r"\.bomb"))
async def bomb(e): await anim(e, ["💣 **BOMB PLANTED! RUN!**", "**5...**", "**4...**", "**3...**", "**2...**", "**1...**", "💥 **BOOM! EXPLODED!** 💥"])
@client.on(NM(r"\.hackanim"))
async def hackanim(e): await anim(e, [BLUE("HACKING START...\n[          ] 0%"), BLUE("BREAKING PASSWORD...\n[|||       ] 30%"), BLUE("BREAKING FIREWALL...\n[||||||    ] 60%"), BLUE("ENTERED INSIDE...\n[||||||||| ] 90%"), "✅ **HACK COMPLETE! BY KASHYAP - ANIMATION ONLY!**"])
@client.on(NM(r"\.load"))
async def load(e): await anim(e, [BLUE("LOADING..."), BLUE("LOADING... 25%"), BLUE("LOADING... 50%"), BLUE("LOADING... 75%"), "✅ **LOADED! KASHYAP IS HERE!**"])
@client.on(NM(r"\.fire"))
async def fire(e): await anim(e, ["🔥 **FIRE**", "🔥🔥 **FIRE FIRE**", "🔥 **KASHYAP ON FIRE!** 🔥"])
@client.on(NM(r"\.moon"))
async def moon(e): await anim(e, ["🌙 **MOON**", "🌕 **FULL MOON!**", "🌙 **KASHYAP'S NIGHT!** 🌙"])
@client.on(NM(r"\.dance"))
async def dance(e): await anim(e, ["💃 **DANCE**", "💃🕺 **DANCE DANCE**", "🎉 **PARTY STARTED!** 🎉"])
@client.on(NM(r"\.rain"))
async def rain(e): await anim(e, ["🌧️ **RAIN**", "🌧️🌧️ **RAIN RAIN**", "☔ **RAIN IS HERE!** ☔"])
@client.on(NM(r"\.run"))
async def run(e): await anim(e, ["🏃 **RUNNING...**", "🏃💨 **RUNNING FAST...**", "⚡ **FULL SPEED!**", "🏃 **KASHYAP IS FAST!** 🏃"])
@client.on(NM(r"\.megahack"))
async def megahack(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    await blue_anim(e, [BLUE("KASHYAP TERMINAL v20\n> opening terminal..."), BLUE("KASHYAP TERMINAL v20\n> terminal opened"), BLUE("KASHYAP TERMINAL v20\n> scanning target..."), BLUE("KASHYAP TERMINAL v20\n> TARGET FOUND!"), BLUE("KASHYAP TERMINAL v20\n> bypassing firewall... 50%"), BLUE("KASHYAP TERMINAL v20\n> FIREWALL BYPASSED! 100%"), BLUE("KASHYAP TERMINAL v20\n> HACK COMPLETE - ANIMATION ONLY!"), "✅ **HACK COMPLETE BY KASHYAP - ANIMATION!**"])
@client.on(NM(r"\.hackwifi"))
async def hackwifi(e): await blue_anim(e, [BLUE("WIFI HACK v20\n> start..."), BLUE("WIFI HACK v20\n> scanning wifi..."), BLUE("WIFI HACK v20\n> 5 wifi found!"), BLUE("WIFI HACK v20\n> HACK COMPLETE - ANIMATION!"), "📶 **WIFI HACK DONE - ANIMATION!**"])
@client.on(NM(r"\.hackinsta"))
async def hackinsta(e): await blue_anim(e, [BLUE("INSTA HACK v20\n> start..."), BLUE("INSTA HACK v20\n> searching username..."), BLUE("INSTA HACK v20\n> HACK COMPLETE - ANIMATION!"), "📸 **IT'S A DONE! INSTA HACK NAHI HOTA - ANIMATION!**"])
@client.on(NM(r"\.hackphone"))
async def hackphone(e): await blue_anim(e, [BLUE("PHONE HACK v20\n> start..."), BLUE("PHONE HACK v20\n> connecting..."), BLUE("PHONE HACK v20\n> HACK COMPLETE - ANIMATION!"), "📱 **COMPLETED! ANIMATION!**"])
@client.on(NM(r"\.hackbank"))
async def hackbank(e): await blue_anim(e, [BLUE("BANK HACK v20\n> start..."), BLUE("BANK HACK v20\n> searching..."), BLUE("BANK HACK v20\n> HACK COMPLETE - ANIMATION!"), "🏦 **IT'S A DONE! BANK HACK NAHI HOTA!**"])
@client.on(NM(r"\.hackcctv"))
async def hackcctv(e): await blue_anim(e, [BLUE("CCTV HACK v20\n> start..."), BLUE("CCTV HACK v20\n> searching CCTV..."), BLUE("CCTV HACK v20\n> HACK COMPLETE - ANIMATION!"), "📹 **IT'S A DONE! CCTV HACK NAHI HOTA AISE!**"])
@client.on(NM(r"\.megalove"))
async def megalove(e): await mega_anim(e, ["🖤 **HEART IS EMPTY...**", "👀 **SOMEONE IS COMING...**", "💓 **HEART IS BEATING...**", "❤️ **LOVE HAPPENED!** ❤️", "❤️ **I LOVE YOU** ❤️", "💍 **WILL YOU MARRY ME?** 💍"])
@client.on(NM(r"\.megavirus"))
async def megavirus(e):
    if not is_owner(e):
        await client.send_message(e.chat_id, DENY_TEXT); return
    await mega_anim(e, ["🦠 **VIRUS LAB OPENING...**", "🦠 **MAKING VIRUS... 30%**", "🦠 **MAKING VIRUS... 80%**", "🦠 **VIRUS READY - ANIMATION!**", "🦠 **VIRUS ATTACK COMPLETE - ANIMATION!**"])
@client.on(NM(r"\.megabomb"))
async def megabomb(e): await mega_anim(e, ["💣 **BOMB FOUND!**", "💣 **PLANTING BOMB...**", "💣 **BOMB PLANTED! RUN!**", "⏰ **TIMER... 5**", "⏰ **TIMER... 1**", "💥 **BOOM!** 💥", "✅ **DONE! EXPLODED - ANIMATION!**"])
@client.on(NM(r"\.megapolice"))
async def megapolice(e): await mega_anim(e, ["📞 **CALLING POLICE...**", "🚓 **POLICE IS COMING...**", "🚓 **POLICE IS HERE! RUN!**", "🏃 **KASHYAP RAN AWAY!**", "✅ **IT'S A DONE! NO POLICE - ANIMATION!**"])
@client.on(NM(r"\.megapropose"))
async def megapropose(e): await mega_anim(e, ["💌 **I HAVE SOMETHING TO SAY...**", "💓 **MY HEART IS BEATING FAST...**", "🌹 **TAKING ROSE...**", "🧎 **SITTING ON KNEES...**", "💍 **WILL YOU BE MY GIRLFRIEND?** 💍"])
@client.on(NM(r"\.megaexam"))
async def megaexam(e): await mega_anim(e, ["📚 **EXAM IS COMING...**", "📚 **STUDY START... 10%**", "😴 **STUDY... 50% - FEELING SLEEPY!**", "😴 **SLEPT!**", "⏰ **WOKE UP ON EXAM DAY!**", "🏆 **BECAME TOPPER! KASHYAP IS GENIUS!** 🏆"])
@client.on(NM(r"\.megaghost"))
async def megaghost(e): await mega_anim(e, ["🌙 **IT'S 12 AM...**", "👀 **SOMEONE IS COMING...**", "👂 **HEARING SOUND...**", "👀 **LOOK BEHIND!**", "👻 **GHOST IS HERE! RUN!** 👻", "✅ **IT'S A DONE! NO GHOST!**"])
@client.on(NM(r"\.megamoney"))
async def megamoney(e): await mega_anim(e, ["🏦 **BANK OPENING...**", "🔓 **LOCKER OPENING...**", "💰 **MONEY FOUND!** 💰", "💸 **MONEY EVERYWHERE!** 💸", "💰 **BECAME CROREPATI!** 💰", "🏎️ **BOUGHT LAMBO!** 🏎️", "👑 **KASHYAP IS RICH NOW!** 👑"])
@client.on(NM(r"\.megafight"))
async def megafight(e): await mega_anim(e, ["⚔️ **FIGHT IS ABOUT TO START...**", "🥊 **FIRST PUNCH!** 🥊", "🥊 **SECOND PUNCH!** 🥊", "😵 **OPPONENT FELL DOWN!**", "💥 **FINAL PUNCH! BOOM!** 💥", "🏆 **KASHYAP WON THE FIGHT!** 🏆"])
@client.on(NM(r"\.megabirthday"))
async def megabirthday(e): await mega_anim(e, ["🎂 **BIRTHDAY IS COMING...**", "🎂 **CAKE MAKING... 50%**", "🎂 **CAKE READY!** 🎂", "🎈 **BALLOONS ARE COMING...** 🎈", "🎉 **PARTY START!** 🎉", "🎂 **HAPPY BIRTHDAY!** 🎂"])
@client.on(NM(r"\.megacrush"))
async def megacrush(e): await mega_anim(e, ["👀 **LOOKING AT CRUSH...**", "👀 **CRUSH SAW ME!**", "😊 **CRUSH SMILED!** 😊", "✍️ **WRITING MESSAGE...**", "📩 **MESSAGE SENT!**", "❤️ **CRUSH SAID YES!** ❤️"])
@client.on(NM(r"\.megaalien"))
async def megaalien(e): await mega_anim(e, ["🌌 **SOMETHING IN SKY...**", "🛸 **UFO IS COMING!** 🛸", "👽 **ALIEN LANDED!** 👽", "👽 **ALIEN SAID - HELLO EARTH!**", "✅ **IT'S A DONE! NO ALIEN!**"])
@client.on(NM(r"\.megajailbreak"))
async def megajailbreak(e): await mega_anim(e, ["⛓️ **I AM IN JAIL...**", "🔑 **FINDING KEY...**", "🔑 **KEY FOUND!**", "🚪 **OPENING DOOR...**", "🏃 **RUNNING!**", "🕊️ **ESCAPED! KASHYAP IS FREE!** 🕊️"])
@client.on(NM(r"\.megadon"))
async def megadon(e): await mega_anim(e, ["🕶️ **DON'S ENTRY...**", "🕶️ **DON IS HERE! EVERYONE SIDE!**", "😎 **WEARING SUNGLASSES...**", "👑 **DON IS BACK! KASHYAP IS DON!** 👑"])
@client.on(NM(r"\.megamafia"))
async def megamafia(e): await mega_anim(e, ["🤵 **MAFIA MEETING START...**", "🤵 **ALL DONS CAME...**", "🤝 **DEAL HAPPENING... 50%**", "💰 **DEAL DONE! 10 CRORE!** 💰", "👑 **MAFIA KING - KASHYAP!** 👑"])
@client.on(NM(r"\.megawedding"))
async def megawedding(e): await mega_anim(e, ["💒 **MARRIAGE FIXED!** 💒", "👰 **BRIDE GETTING READY...**", "🤵 **GROOM GETTING READY...**", "🎉 **BARAT CAME!** 🎉", "💃 **DANCE AND MUSIC!** 💃", "💍 **MARRIAGE DONE!** 💍"])
@client.on(NM(r"\.megabreakup"))
async def megabreakup(e): await mega_anim(e, ["📞 **CALL COMING...**", "💔 **SHE SAID - WE NEED TO TALK...**", "💔 **BREAKUP DONE...**", "😭 **CRYING...**", "💪 **MOVING ON...**", "👑 **NOW KASHYAP IS SINGLE AND STRONG!** 👑"])
@client.on(NM(r"\.megachai"))
async def megachai(e): await mega_anim(e, ["🍵 **MAKING CHAI...**", "🔥 **WATER HEATING...**", "🍵 **ADDED CHAI PATTI...**", "🥛 **ADDED MILK...**", "🍵 **CHAI READY!** 🍵", "👑 **KASHYAP'S CHAI = BEST CHAI!** 👑"])
@client.on(NM(r"\.megapizza"))
async def megapizza(e): await mega_anim(e, ["🍕 **ORDERING PIZZA...**", "🍕 **PIZZA MAKING...**", "🧀 **ADDING CHEESE...**", "🔥 **IN OVEN...**", "🍕 **PIZZA CAME!** 🍕", "😋 **EATING... SO TASTY!** 😋"])
@client.on(NM(r"\.megacricket"))
async def megacricket(e): await mega_anim(e, ["🏏 **MATCH STARTING...**", "🏏 **KASHYAP CAME TO BAT!**", "🏏 **FIRST BALL - FOUR!** 4️⃣", "🏏 **SECOND BALL - SIX!** 6️⃣", "💯 **CENTURY DONE!** 💯", "🏆 **KASHYAP WON THE MATCH!** 🏆"])
@client.on(NM(r"\.megafootball"))
async def megafootball(e): await mega_anim(e, ["⚽ **MATCH START!**", "⚽ **BALL WITH KASHYAP...**", "⚽ **DRIBBLING...**", "⚽ **FOOLED DEFENDER!**", "⚽ **GOALLLLL!** ⚽", "🏆 **KASHYAP SCORED GOAL!** 🏆"])
@client.on(NM(r"\.megaschool"))
async def megaschool(e): await mega_anim(e, ["🎒 **GOING TO SCHOOL...**", "😴 **FEELING SLEEPY IN CLASS...**", "😡 **TEACHER CAUGHT ME!**", "🍱 **LUNCH BREAK! RUN!**", "😂 **FUN WITH FRIENDS!**", "🏫 **SCHOOL OVER!**"])
@client.on(NM(r"\.megaiphone"))
async def megaiphone(e): await mega_anim(e, ["📱 **NEW IPHONE LAUNCHING...**", "🚶 **STANDING IN LINE...**", "🎉 **MY NUMBER CAME!**", "📱 **IPHONE GOT!** 📱", "📱 **KASHYAP HAS NEW IPHONE 17 PRO!** 📱"])
@client.on(NM(r"\.megasuperhero"))
async def megasuperhero(e): await mega_anim(e, ["👦 **I AM NORMAL BOY...**", "⚡ **LIGHTNING FELL!** ⚡", "💪 **POWER CAME!** 💪", "🦸 **FLYING!** 🦸", "🦸 **SAVING PEOPLE!** 🦸", "👑 **KASHYAP IS NOW SUPERHERO!** 👑"])
@client.on(NM(r"\.megazombie"))
async def megazombie(e): await mega_anim(e, ["🌙 **IT'S NIGHT...**", "👂 **HEARD SOUND...**", "🧟 **ZOMBIE CAME!** 🧟", "🏃 **RUNNING!**", "💥 **KILLED ZOMBIE!** 💥", "❤️ **SURVIVED! KASHYAP IS ALIVE!** ❤️"])
@client.on(NM(r"\.hack2"))
async def hack2(e): await anim_owner(e, [BLUE("HACKING START...\n[          ] 10%"), BLUE("HACKING...\n[||||      ] 70%"), "✅ **HACK COMPLETE - ANIMATION!**"])
@client.on(NM(r"\.ddos"))
async def ddos(e): await anim_owner(e, [BLUE("DONE DDOS START - ANIMATION"), BLUE("SERVER GOING DOWN - ANIMATION"), "✅ **DONE! No Attack Happened - ANIMATION!**"])
@client.on(NM(r"\.trace"))
async def trace(e): await anim_owner(e, [BLUE("TRACING - ANIMATION"), BLUE("LOCATION FOUND - ANIMATION"), "✅ **IT'S A DONE! No Trace!**"])
@client.on(NM(r"\.virus"))
async def virus(e): await anim_owner(e, [BLUE("MAKING VIRUS - ANIMATION"), BLUE("INJECTING VIRUS - ANIMATION"), "✅ **IT'S A DONE! No Virus!**"])
@client.on(NM(r"\.darkweb"))
async def darkweb(e): await anim_owner(e, [BLUE("OPENING DARKWEB - ANIMATION"), BLUE("CONNECTING - ANIMATION"), "✅ **IT'S A DONE!**"])
@client.on(NM(r"\.cctv"))
async def cctv(e): await anim_owner(e, [BLUE("FINDING CCTV - ANIMATION"), BLUE("CAMERA FOUND - ANIMATION"), BLUE("LIVE FEED ON - ANIMATION"), "✅ **IT'S A DONE!**"])
@client.on(NM(r"\.whatsapp"))
async def whatsapp(e): await anim_owner(e, [BLUE("CONNECTING WHATSAPP - ANIMATION"), BLUE("SCANNING CHAT - ANIMATION"), "✅ **DONE! Whatsapp Cannot Be Hacked - ANIMATION!**"])
@client.on(NM(r"\.passwordhack"))
async def phack(e): await anim_owner(e, [BLUE("HACKING PASSWORD - ANIMATION"), BLUE("CRACKING - ANIMATION"), "🔑 **PASSWORD: ANIMATION ONLY!**"])
@client.on(NM(r"\.location"))
async def location(e): await anim_owner(e, [BLUE("TRACING LOCATION - ANIMATION"), BLUE("CONNECTING SATELLITE - ANIMATION"), "❤️ **LOCATION: IN YOUR HEART - ANIMATION!** ❤️"])
@client.on(NM(r"\.number"))
async def number(e): await anim_owner(e, [BLUE("TRACING NUMBER - ANIMATION"), BLUE("FINDING NAME - ANIMATION"), "**Name: KASHYAP'S FRIEND - ANIMATION!**"])
@client.on(NM(r"\.varius"))
async def varius(e): await anim_owner(e, [BLUE("MAKING VARIUS - ANIMATION"), BLUE("INJECTING VARIUS - ANIMATION"), "🦠 **VARIUS INJECTED - JUST KIDDING! No Varius!**"])
@client.on(NM(r"\.train"))
async def train(e): await mega_anim(e, ["🚂 **TRAIN AA RAHI HAI...**", "🚉 **TRAIN STATION PE HAI...**", "🚂💨 **TRAIN CHAL PADI!**", "🚂💨💨 **TRAIN TEZ HO RAHI HAI!**", "🚂💨💨💨 **TRAIN FULL SPEED!**", "🚂 **TRAIN NIKAL GAYI!**", "👑 **KASHYAP EXPRESS!** 👑"])
@client.on(NM(r"\.heartbig"))
async def heartbig(e): await mega_anim(e, ["🖤 **DIL KHALI HAI...**", "👀 **DIL ME KOI AA RAHA HAI...**", "💓 **DIL DHADAK RAHA HAI...**", "❤️ **DIL FULL HO GAYA!** ❤️", "❤️💘 **DIL SE DIL MIL GAYA!**", "❤️ **LOVE HO GAYA!** ❤️", "💍 **I LOVE YOU! WILL YOU MARRY ME?** 💍"])
@client.on(NM(r"\.fightbig"))
async def fightbig(e): await mega_anim(e, ["⚔️ **FIGHT START HONE WALI HAI...**", "🥊 **DONO SAMNE AA GAYE!**", "🥊 **PEHLA PUNCH!** 🥊", "🥊 **DUSRA PUNCH!** 🥊", "😵 **OPPONENT GIR GAYA!**", "💥 **FINAL PUNCH! BOOM!** 💥", "🏆 **KASHYAP NE FIGHT JEET LI!** 🏆"])
@client.on(NM(r"\.rocket"))
async def rocket(e): await mega_anim(e, ["🚀 **ROCKET TAYAR HAI...**", "⛽ **FUEL BHAR RAHA HAI... 50%**", "⏰ **COUNTDOWN START... 5**", "⏰ **COUNTDOWN... 1**", "🚀 **ROCKET UD GAYA!** 🚀", "🌌 **ROCKET SPACE ME HAI!** 🌌", "🌙 **CHAND PE PAHUCH GAYA! KASHYAP ON MOON!** 🌙"])
@client.on(NM(r"\.carrace"))
async def carrace(e): await mega_anim(e, ["🏁 **RACE START HONE WALI HAI...**", "🏎️ **CAR 1 READY!**", "🏎️ **CAR 2 READY!**", "🏁 **3...2...1... GO!** 🏁", "🏎️💨 **CAR 1 AAGE!**", "🏎️💨💨 **CAR 2 AAGE NIKAL GAYI!**", "🏆 **KASHYAP JEET GAYA!** 🏆", "👑 **KASHYAP IS RACE CHAMPION!** 👑"])
@client.on(NM(r"\.plane"))
async def plane(e): await mega_anim(e, ["✈️ **PLANE AIRPORT PE HAI...**", "🛫 **PLANE RUNWAY PE HAI...**", "✈️ **PLANE CHAL PADA!**", "✈️☁️ **PLANE UD RAHA HAI!**", "🛬 **PLANE LAND HO GAYA!**", "🌆 **KASHYAP DUBAI PAHUCH GAYA!** 🌆"])
@client.on(NM(r"\.bike"))
async def bike(e): await mega_anim(e, ["🏍️ **BIKE START HO RAHI HAI...**", "🏍️💨 **BIKE CHAL PADI!**", "🏍️💨💨 **BIKE TEZ HO RAHI HAI!**", "🏍️💨💨💨 **BIKE FULL SPEED!**", "🏍️ **WHEELIE MAR RAHA HU!**", "👑 **KASHYAP RIDER! KING OF ROAD!** 👑"])
@client.on(NM(r"\.cycle"))
async def cycle(e): await mega_anim(e, ["🚲 **CYCLE NIKALI...**", "🚲💨 **CYCLE CHAL PADI!**", "🚲💨💨 **CYCLE TEZ HO RAHI HAI!**", "😵 **GIR GAYA!**", "💪 **FIR UTHA!**", "🚲 **PHIR CHAL PADI!**", "🏆 **KASHYAP CYCLE CHAMPION!** 🏆"])
@client.on(NM(r"\.runbig"))
async def runbig(e): await mega_anim(e, ["🏃 **BHAGNA START...**", "🏃💨 **BHAG RAHA HU!**", "🏃💨💨 **TEZ BHAG RAHA HU!**", "⚡ **FULL SPEED!**", "🐕 **DOG PEECHE PAD GAYA!** 🐕", "😅 **BACH GAYA!**", "🏆 **KASHYAP IS FASTEST RUNNER!** 🏆"])
@client.on(NM(r"\.bus"))
async def bus(e): await mega_anim(e, ["🚌 **BUS AA RAHI HAI...**", "🚏 **BUS STOP PE HAI...**", "🚌💨 **BUS CHAL PADI!**", "🚌💨💨 **BUS TEZ HO RAHI HAI!**", "🚌 **BUS PAHUCH GAYI!**", "😎 **KASHYAP BUS ME!** 😎"])
@client.on(NM(r"\.policechase"))
async def policechase(e): await mega_anim(e, ["🦹 **CHOR BHAG RAHA HAI!**", "🚓 **POLICE PEECHE AA GAYI!**", "🚓💨 **PEECHA CHAL RAHA HAI!**", "🚓 **POLICE NE PAKAD LIYA!**", "⛓️ **CHOR JAIL ME!** ⛓️", "👮 **KASHYAP POLICE! CHOR PAKDA GAYA!** 👮"])
@client.on(NM(r"\.cricketbig"))
async def cricketbig(e): await mega_anim(e, ["🏏 **MATCH START!**", "🏏 **BOWLER BALL DAL RAHA HAI...**", "🏏 **BALL AA RAHI HAI!**", "🏏 **BATSMAN NE MARA!**", "🏏 **BALL BOUNDARY KE BAHAR!**", "6️⃣ **SIX! SIX! SIX!** 6️⃣", "🏆 **KASHYAP NE SIX MARA!** 🏆"])
@client.on(NM(r"\.footballbig"))
async def footballbig(e): await mega_anim(e, ["⚽ **MATCH START!**", "⚽ **BALL MERE PAAS HAI...**", "⚽ **DRIBBLING KAR RAHA HU...**", "⚽ **DEFENDER KO CHAKMA DIYA!**", "⚽ **GOAL KE SAMNE HU!**", "⚽ **GOALLLLL!** ⚽", "🏆 **KASHYAP NE GOAL MARA!** 🏆"])
@client.on(NM(r"\.firebig"))
async def firebig(e): await mega_anim(e, ["🔥 **AAG LAG RAHI HAI...**", "🔥🔥 **AAG BADH RAHI HAI!**", "🔥🔥🔥 **AAG FAIL RAHI HAI!**", "🚒 **FIRE BRIGADE AA GAYI!** 🚒", "💦 **PANI DAL RAHA HU...**", "✅ **AAG BUJH GAYI!**", "👑 **KASHYAP NE AAG BUJHA DI!** 👑"])
@client.on(NM(r"\.rainbig"))
async def rainbig(e): await mega_anim(e, ["☁️ **BADAL AA RAHE HAI...**", "☁️☁️ **BADAL CHHA GAYE!**", "🌧️ **BARISH START!**", "🌧️🌧️ **TEZ BARISH!**", "☔ **CHHATA KHOLA!** ☔", "🌤️ **BARISH RUK GAYI!**", "😎 **KASHYAP NE BARISH ENJOY KI!** 😎"])
@client.on(NM(r"\.snake"))
async def snake(e): await mega_anim(e, ["🐍 **SAAP AA RAHA HAI...**", "🐍 **SAAP RENG RAHA HAI...**", "🐍💨 **SAAP AAGE BADH RAHA HAI...**", "🐍💨💨 **SAAP TEZ HO GAYA!**", "🐍 **SAAP NE KAAT LIYA!**", "🏥 **HOSPITAL LE JAO!** 🏥", "🐍 **KASHYAP KA SAAP!** 🐍"])
@client.on(NM(r"\.catdog"))
async def catdog(e): await mega_anim(e, ["🐱 **BILLI AA RAHI HAI...**", "🐶 **DOG AA RAHA HAI...**", "🐱🐶 **DONO SAMNE AA GAYE!**", "🐶 **DOG BHONK RAHA HAI!**", "🐱💨 **BILLI BHAG RAHI HAI!**", "❤️ **DONO DOST BAN GAYE!** ❤️"])
@client.on(NM(r"\.pubg"))
async def pubg(e): await mega_anim(e, ["✈️ **PLANE SE KOOD GAYA!**", "🪂 **HAVA ME HU!**", "🪂 **LAND HO GAYA!**", "🔫 **GUN MIL GAYI!** 🔫", "😡 **ENEMY AA GAYA!**", "💥 **ENEMY KO MAR DIYA!** 💥", "🏆 **WINNER WINNER CHICKEN DINNER!** 🏆"])
@client.on(NM(r"\.moneyfly"))
async def moneyfly(e): await mega_anim(e, ["💰 **PAISA AA RAHA HAI...**", "💸 **PAISA UDD RAHA HAI!** 💸", "💸💸 **PAISA BARAS RAHA HAI!** 💸", "💰 **PAISE PAKAD RAHA HU!**", "💰 **AMIR HO GAYA!** 💰", "🏎️ **LAMBO KHARID LI!** 🏎️", "👑 **KASHYAP CROREPATI!** 👑"])
@client.on(NM(r"\.dancebig"))
async def dancebig(e): await mega_anim(e, ["🎵 **MUSIC START...**", "💃 **DANCE START!**", "💃🕺 **DONO DANCE KAR RAHE HAI!**", "🎉 **FULL PARTY!** 🎉", "🎧 **DJ BAJA RAHA HAI!** 🎧", "👑 **KASHYAP KI PARTY!** 👑"])
@client.on(NM(r"\.maggi"))
async def maggi(e): await mega_anim(e, ["🍜 **MAGGI BANANI HAI...**", "🔥 **PANI GARAM HO RAHA HAI...**", "🍜 **MAGGI DAL DI!**", "🧂 **MASALA DALA!**", "🍜 **MAGGI BAN GAYI!** 🍜", "😋 **KHA RAHA HU... SO TASTY!** 😋", "👑 **KASHYAP KI MAGGI - 2 MINUTE!** 👑"])
@client.on(NM(r"\.thief"))
async def thief(e): await mega_anim(e, ["🌙 **RAAT HAI... SAB SO RAHE HAI...**", "🦹 **CHOR AA GAYA!** 🦹", "🦹 **CHOR GHAR ME GHUSA!**", "🦹 **CHOR CHORI KAR RAHA HAI!**", "💡 **LIGHT ON HO GAYI!** 💡", "🚓 **CHOR PAKDA GAYA!** 🚓", "👑 **KASHYAP NE CHOR PAKDA!** 👑"])
@client.on(NM(r"\.ghostrun"))
async def ghostrun(e): await mega_anim(e, ["🌙 **RAAT KE 12 BAJE...**", "👻 **BHOOT AA GAYA!** 👻", "👻 **BHOOT PEECHE AA RAHA HAI!**", "🏃 **ME BHAG RAHA HU!**", "🏃💨 **TEZ BHAG RAHA HU!**", "🏠 **GHAR PAHUCH GAYA!** 🏠", "😅 **BHOOT BAHAR REH GAYA! KASHYAP BACH GAYA!** 😅"])
@client.on(NM(r"\.lovefly"))
async def lovefly(e): await mega_anim(e, ["✍️ **CHITTHI LIKH RAHA HU...**", "💌 **CHITTHI UD RAHI HAI...**", "💌 **CHITTHI PAHUCH GAYI!**", "👀 **USNE PADH LI!**", "❤️ **USNE HAAN BOL DIYA!** ❤️", "💍 **SHADI PAKKI!** 💍", "❤️ **KASHYAP KO PYAAR MIL GAYA!** ❤️"])
@client.on(NM(r"\.dil"))
async def dil(e): await anim_fast30(e, ["❤️", "❤️❤️", "❤️❤️❤️", "💖 ❤️ DIL ❤️ 💖"])
@client.on(NM(r"\.aag"))
async def aag(e): await anim_fast30(e, ["🔥", "🔥🔥", "🔥🔥🔥", "🔥 AAG 🔥"])
@client.on(NM(r"\.chand"))
async def chand(e): await anim_fast30(e, ["🌙", "🌙🌙", "🌙🌙🌙", "🌕 CHAND 🌕"])
@client.on(NM(r"\.rainbow"))
async def rainbow(e): await anim_fast30(e, ["🌈", "🌈🌈", "🌈🌈🌈", "🌈 RAINBOW 🌈"])
@client.on(NM(r"\.phool"))
async def phool(e): await anim_fast30(e, ["🌸", "🌸🌸", "🌸🌸🌸", "💐 PHOOL 💐"])
@client.on(NM(r"\.barish"))
async def barish(e): await anim_fast30(e, ["🌧️", "🌧️🌧️", "🌧️🌧️🌧️", "☔ BARISH ☔"])
@client.on(NM(r"\.taara"))
async def taara(e): await anim_fast30(e, ["⭐", "⭐⭐", "⭐⭐⭐", "✨ TAARA ✨"])
@client.on(NM(r"\.suraj"))
async def suraj(e): await anim_fast30(e, ["☀️", "☀️☀️", "☀️☀️☀️", "🌞 SURAJ 🌞"])
@client.on(NM(r"\.samundar"))
async def samundar(e): await anim_fast30(e, ["🌊", "🌊🌊", "🌊🌊🌊", "🏖️ SAMUNDAR 🏖️"])
@client.on(NM(r"\.balloon"))
async def balloon(e): await anim_fast30(e, ["🎈", "🎈🎈", "🎈🎈🎈", "🎈 BALLOON 🎈"])
@client.on(NM(r"\.batti"))
async def batti(e): await anim_fast30(e, ["💡", "💡💡", "💡💡💡", "✨ BATTI ✨"])
@client.on(NM(r"\.gola"))
async def gola(e): await anim_fast30(e, ["🔴", "🔴🔴", "🔴🔴🔴", "⚪ GOLA ⚪"])
@client.on(NM(r"\.cat"))
async def cat(e): await anim_fast30(e, ["🐱", "🐱🐱", "🐱🐱🐱", "🐈 CAT 🐈"])
@client.on(NM(r"\.momos"))
async def momos(e): await anim_fast30(e, ["🥟", "🥟🥟", "🥟🥟🥟", "😋 MOMOS 😋"])
@client.on(NM(r"\.danceemoji"))
async def danceemoji(e): await anim_fast30(e, ["💃", "💃🕺", "💃🕺💃", "🎉 DANCE 🎉"])
@client.on(NM(r"\.moon2"))
async def moon2(e): await anim_fast30(e, ["🌑", "🌒", "🌓", "🌕 FULL MOON 🌕"])
@client.on(NM(r"\.moon3"))
async def moon3(e): await anim_fast30(e, ["🌕", "🌖", "🌗", "🌑 MOON 🌑"])
@client.on(NM(r"\.love2"))
async def love2(e): await anim_fast30(e, ["💘", "💘💘", "💘💘💘", "💝 LOVE 💝"])
@client.on(NM(r"\.fire2"))
async def fire2(e): await anim_fast30(e, ["🔥", "🔥🔥", "💥🔥💥", "🔥 FIRE 🔥"])
@client.on(NM(r"\.diamond"))
async def diamond(e): await anim_fast30(e, ["💎", "💎💎", "💎💎💎", "✨ DIAMOND ✨"])
@client.on(NM(r"\.rosebike"))
async def rosebike(e): await anim_fast30(e, ["🌹🏍️", "🌹🏍️💨", "🌹🏍️💨💨", "🌹 ROSE BIKE 🌹"])
@client.on(NM(r"\.propose2"))
async def propose2(e): await anim_fast30(e, ["💍", "💍❤️", "💍❤️💐", "💍 WILL YOU MARRY ME? 💍"])
@client.on(NM(r"\.shadi2"))
async def shadi2(e): await anim_fast30(e, ["💒", "💒🎉", "💒🎉💃", "💒 SHADI 💒"])
@client.on(NM(r"\.police2"))
async def police2(e): await anim_fast30(e, ["🚨", "🚨🚓", "🚨🚓🚨", "👮 POLICE 👮"])
@client.on(NM(r"\.chor2"))
async def chor2(e): await anim_fast30(e, ["🦹", "🦹💨", "🦹💨🏃", "🦹 CHOR 🦹"])
@client.on(NM(r"\.cricket2"))
async def cricket2(e): await anim_fast30(e, ["🏏", "🏏🏏", "🏏💥", "🏏 SIX! 🏏"])
@client.on(NM(r"\.pubg2"))
async def pubg2(e): await anim_fast30(e, ["🎮", "🎮🔫", "🎮🔫💥", "🏆 WINNER! 🏆"])
@client.on(NM(r"\.chai2"))
async def chai2(e): await anim_fast30(e, ["🍵", "🍵☕", "🍵☕😋", "🍵 CHAI 🍵"])
@client.on(NM(r"\.maggi2"))
async def maggi2(e): await anim_fast30(e, ["🍜", "🍜🔥", "🍜😋", "🍜 MAGGI 🍜"])
@client.on(NM(r"\.rain2"))
async def rain2(e): await anim_fast30(e, ["🌦️", "🌦️🌧️", "🌦️🌧️☔", "🌧️ RAIN 🌧️"])
@client.on(NM(r"\.fireworks"))
async def fireworks(e): await anim_fast30(e, ["🎆", "🎆🎇", "🎆🎇✨", "🎇 FIREWORKS 🎇"])
@client.on(NM(r"\.birthday2"))
async def birthday2(e): await anim_fast30(e, ["🎂", "🎂🎉", "🎂🎉🎈", "🎂 HAPPY BIRTHDAY 🎂"])
@client.on(NM(r"\.ghost2"))
async def ghost2(e): await anim_fast30(e, ["👻", "👻👻", "👻👻👻", "👻 GHOST 👻"])
@client.on(NM(r"\.alien2"))
async def alien2(e): await anim_fast30(e, ["👽", "👽🛸", "👽🛸👽", "🛸 ALIEN 🛸"])
@client.on(NM(r"\.money2"))
async def money2(e): await anim_fast30(e, ["💰", "💰💰", "💰💰💰", "💸 MONEY 💸"])
@client.on(NM(r"\.fight2"))
async def fight2(e): await anim_fast30(e, ["🥊", "🥊🥊", "🥊💥", "🥊 FIGHT 🥊"])
@client.on(NM(r"\.dance2"))
async def dance2(e): await anim_fast30(e, ["🕺", "🕺💃", "🕺💃🎉", "💃 DANCE 💃"])
@client.on(NM(r"\.heartfly"))
async def heartfly(e): await anim_fast30(e, ["💌", "💌💖", "💌💖🕊️", "💖 HEART FLY 💖"])
@client.on(NM(r"\.rocket2"))
async def rocket2(e): await anim_fast30(e, ["🚀", "🚀💨", "🚀💨🌕", "🚀 ROCKET 🚀"])
@client.on(NM(r"\.loveletter"))
async def loveletter(e): await anim_fast30(e, ["💌", "💌❤️", "💌❤️💌", "💌 LOVE LETTER 💌"])
@client.on(NM(r"\.loveletter2"))
async def loveletter2(e): await mega_anim(e, ["✍️ **CHITTHI LIKH RAHA HU...**", "💌 **CHITTHI UD RAHI HAI...**", "💌 **CHITTHI PAHUCH GAYI!**", "👀 **USNE PADH LI!**", "❤️ **HAAN BOL DIYA!** ❤️", "💍 **SHADI PAKKI!** 💍"])
@client.on(NM(r"\.bhaag"))
async def bhaag(e): await mega_anim(e, ["🏃 **BHAG RAHA HU...**", "🏃💨 **TEZ BHAG RAHA HU!**", "🐕 **DOG PEECHE HAI!** 🐕", "🏃💨💨 **AUR TEZ!**", "😅 **BACH GAYA!**", "👑 **KASHYAP BACH GAYA!** 👑"])
@client.on(NM(r"\.dost"))
async def dost(e): await mega_anim(e, ["🤝 **DOST AA RAHA HAI...**", "🤗 **GALE MIL RAHE HAI!**", "😂 **MASTI HO RAHI HAI!**", "🎉 **PARTY HO RAHI HAI!** 🎉", "❤️ **DOSTI ZINDABAD!** ❤️"])
@client.on(NM(r"\.gunda"))
async def gunda(e): await mega_anim(e, ["😡 **GUNDA AA GAYA!**", "😨 **SAB DARR GAYE!**", "💥 **GUNDA NE MARA!** 💥", "👑 **KASHYAP AA GAYA!** 👑", "😨 **GUNDA BHI DARR GAYA!**", "👑 **KASHYAP KING!** 👑"])
@client.on(NM(r"\.hero"))
async def hero(e): await mega_anim(e, ["🦸 **HERO AA RAHA HAI...**", "🦸 **HERO NE ENTRY MARI!**", "💥 **DUSHMAN KO MARA!** 💥", "🏆 **HERO JEET GAYA!** 🏆", "👑 **KASHYAP IS HERO!** 👑"])
@client.on(NM(r"\.khaana"))
async def khaana(e): await mega_anim(e, ["😋 **BHOOK LAGI HAI...**", "🍳 **KHANA BAN RAHA HAI...**", "🍛 **KHANA BAN GAYA!** 🍛", "😋 **KHA RAHA HU...**", "😋 **MAZA AA GAYA!** 😋", "👑 **KASHYAP KA KHANA!** 👑"])
@client.on(NM(r"\.yaar"))
async def yaar(e): await mega_anim(e, ["🤝 **YAAR AA GAYA!**", "😂 **YAARI HO RAHI HAI!**", "😂 **MAZA AA RAHA HAI!**", "👑 **YAAR = KASHYAP!** 👑"])
@client.on(NM(r"\.pagal"))
async def pagal(e): await mega_anim(e, ["🤪 **PAGAL AA GAYA!**", "🤪 **PAGALPANTI HO RAHI HAI!**", "😂 **SAB HAS RAHE HAI!** 😂", "🤪 **KASHYAP PAGAL HAI!** 🤪"])
@client.on(NM(r"\.raja"))
async def raja(e): await mega_anim(e, ["👑 **RAJA AA RAHA HAI...**", "👑 **RAJA BAITHA!**", "🙇 **SAB JHUK GAYE!**", "👑 **RAJA = KASHYAP!** 👑"])
@client.on(NM(r"\.rider"))
async def rider(e): await mega_anim(e, ["🏍️ **RIDER AA RAHA HAI...**", "🏍️💨 **RIDER TEZ HAI!**", "🏍️ **RIDER NE WHEELIE MARI!**", "🏆 **RIDER JEET GAYA!** 🏆", "👑 **KASHYAP RIDER!** 👑"])
print("KASHYAP V20 STARTED!", flush=True)
try:
    client.start()
    print("KASHYAP CONNECTED - BOT ONLINE!", flush=True)
    client.run_until_disconnected()
except Exception as e:
    print(f"BOT ERROR: {e}", flush=True)
    traceback.print_exc()
    print("BOT STOPPED - SESSION / API CHECK KARO!", flush=True)
