# FULL USERBOT - GURU WALA
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
import os, random, time

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "APNA_HASH")
STRING = os.getenv("STRING_SESSION", "APNI_STRING")

client = TelegramClient(StringSession(STRING), API_ID, API_HASH)

SUDO_USERS = [123456789]
WATCH_LIST = {}
AUTOPIN_DM = set()
AUTOPIN_GROUP = {}
AUTO_REACT = {}
MY_ORIGINAL = {}

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

ARTS_LIST = ["RAM","JAISHREERAM","HANUMAN","MAHAKAL","SHIV","OM","RADHE","KRISHNA","ILOVEYOU","LOVE","HUG","JAAN","JAANU","BABY","CRUSH","CUTE","PYAR","MISSYOU","HELLO","BYEE","PAPA","MUMMY","BRO","BHAI","DOSTI","FRIEND","BESTIE","KING","QUEEN","KASHYAP","INDIA","BHARAT","SORRY","THANKYOU","GOODMORNING","GOODNIGHT","HAPPYBIRTHDAY","SINGLE","HELICOPTER","MERA"]
def pretty_name(key):
    m = {"JAISHREERAM":"JAI SHREE RAM","ILOVEYOU":"I LOVE YOU","MISSYOU":"MISS YOU","GOODMORNING":"GOOD MORNING","GOODNIGHT":"GOOD NIGHT","HAPPYBIRTHDAY":"HAPPY BIRTHDAY","THANKYOU":"THANK YOU"}
    return m.get(key, key)

JOKES = [
"Teacher: Tum itne late kyu aaye? Student: Sir, board pe likha tha School Ahead, Go Slow",
"Pappu: Mummy, aaj school me mujhe 100 me se 90 mile! Mummy: Wah! Kis me? Pappu: 50 Hindi me, 40 English me",
"Boy: Tumhari smile bahut pyari hai. Girl: Thanks. Boy: Main to apni wali ki baat kar raha tha jab tumhe dekhta hu to aa jati hai",
"Ek baar ek aadmi ne Google se pucha - Meri biwi kaha hai? Google bola - Teri himmat kaise hui mujhse puchne ki, main khud usi se darta hu",
"Pati: Aaj khana kaisa bana hai? Patni: Acha hai. Pati: To fir roz aisa hi bana diya kar, jaisa aaj hotel se mangwaya hai",
"Dost: GURU, teri GF kaisi hai? Dusra: Bilkul WiFi jaisi, sabke saath connect ho jati hai",
"Girlfriend: Baby, tum mujhe kitna pyar karte ho? Boyfriend: Jitna Jio ka net, kabhi khatam nahi hota",
"Teacher: Agar tumhe 100 rupaye mile to kya karoge? Pappu: Udhari chuka dunga. Teacher: Aur 1000 mile to? Pappu: Udhari badha dunga",
"GURU ne pucha - Exam kaisa gaya? Maine bola - Bilkul mere future jaisa, andhera hi andhera",
"Doctor: Tumhe kya problem hai? Patient: Sir, mujhe sab kuch bhool jata hai. Doctor: Kab se? Patient: Kab se kya sir?",
]

SHAYARI = [
"Teri yaad me humne jamana bhoola diya, Tere pyar me humne khud ko bhoola diya, Tu jo mili to laga zindagi mil gayi, Par tu jo gayi to laga zindagi hi chali gayi",
"Mohabbat me humne kya kuch nahi kiya, Din raat teri yaad me guzara kiya, Tu jo mile to laga sab kuch mil gaya",
"Tere chehre pe muskan humesha rahe, Teri zindagi me kabhi gam na aaye, Tu jaha bhi rahe khush rahe",
"Dosti me duri to aati rehti hai, Fir bhi dosti dilo ko mila deti hai, Jo dost dil se sacche hote hai, Unki yaad har pal tadpati hai",
"Raat bhar chandni me teri yaad aayi, Dil ne kaha aaj fir teri kami mehsoos hui",
"Zindagi me har koi pyar karta hai, Koi dil se karta hai, koi matlab se, Jo dil se karta hai wo kabhi bhoolta nahi",
"Tumse milke dil ko sukoon mila, Tumse bichad ke dil ko dard mila",
"Chand ko dekh ke yaad teri aayi, Taro ko dekh ke yaad teri aayi, Har cheez me bas tu hi tu nazar aayi",
"Pyar me humne dil laga liya, Dil laga ke humne dil gawa diya",
"Jab se tu mili hai, zindagi badal gayi, Har khushi ab teri muskan se jud gayi",
"Dost wo jo har pal saath de, Muskil me bhi haath thaam le",
"Teri muskan pe hum fida ho gaye, Teri adao pe hum kurban ho gaye",
"Waqt guzar jayega, yaadein reh jayengi, Log bhool jayenge, baatein reh jayengi",
"Zindagi ek safar hai, isme sab milte hai, Koi dil me bas jata hai, koi dil tod jata hai",
"Meri har dua me bas tu hi tu hai, Meri har khushi me bas tu hi tu hai",
]

@client.on(events.NewMessage(pattern=r"\.help"))
async def help_cmd(event):
    await event.reply(
        "USERBOT ON HAI GURU\n\n"
        "BINDI ART\n"
        ".art RAM\n"
        ".art - 40 ki list\n\n"
        "JOKE / SHAYARI\n"
        ".joke\n"
        ".shayari\n\n"
        "WATCH\n"
        ".watch - Reply karke\n"
        ".unwatch\n"
        ".watchlist\n\n"
        "AUTO-PIN\n"
        ".autopin on - Group me Reply karke\n"
        ".autopin off\n"
        ".dmautopin on - DM me Reply karke\n"
        ".dmautopin off\n"
        ".dmautopin list\n\n"
        "EXTRAS - UTILITIES\n"
        ".join <link>\n"
        ".ping\n"
        ".help\n"
        ".stopall\n\n"
        "EXTRAS - CLONE\n"
        ".clone - Reply karke\n"
        ".rmclone\n"
        ".nc <name>\n"
        ".setpic\n\n"
        "EXTRAS - REACT\n"
        ".ar <emoji>\n"
        ".ar off\n"
        ".stopar"
    )

@client.on(events.NewMessage(pattern=r"\.ping"))
async def ping_cmd(event):
    start = time.time()
    m = await event.reply("Ping...")
    ms = int((time.time() - start) * 1000)
    await m.edit(f"Pong! {ms}ms - USERBOT ON HAI GURU")

@client.on(events.NewMessage(pattern=r"\.join\s+(.+)"))
async def join_cmd(event):
    link = event.pattern_match.group(1)
    try:
        await client(functions.channels.JoinChannelRequest(link))
        await event.reply(f"Join ho gaya GURU: {link}")
    except Exception as e:
        await event.reply(f"Join nahi hua GURU: {e}")

@client.on(events.NewMessage(pattern=r"\.stopall"))
async def stopall_cmd(event):
    AUTOPIN_DM.clear(); AUTOPIN_GROUP.clear(); AUTO_REACT.clear(); WATCH_LIST.clear()
    await event.reply("SAB BAND HO GAYA GURU! Auto-pin, Auto-react, Watch - sab halt!")

@client.on(events.NewMessage(pattern=r"\.art(?:\s+(.*))?"))
async def art_cmd(event):
    arg = event.pattern_match.group(1)
    if not arg:
        txt = "BINDI ART LIST GURU:\n\n"
        for a in ARTS_LIST:
            txt += f".art {a}\n"
        await event.reply(txt); return
    key = arg.replace(" ", "").upper()
    await event.reply(f"```\n{bindi_art(pretty_name(key))}\n```")

@client.on(events.NewMessage(pattern=r"\.joke"))
async def joke_cmd(event):
    await event.reply(f"JOKE GURU:\n\n{random.choice(JOKES)}")

@client.on(events.NewMessage(pattern=r"\.shayari"))
async def shayari_cmd(event):
    await event.reply(f"SHAYARI GURU:\n\n{random.choice(SHAYARI)}")

@client.on(events.NewMessage(pattern=r"\.watch"))
async def watch_cmd(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .watch likho GURU!"); return
    name = reply.sender.first_name if reply.sender else "User"
    WATCH_LIST[reply.sender_id] = name
    await event.reply(f"{name} ko WATCH pe laga diya GURU!")

@client.on(events.NewMessage(pattern=r"\.unwatch"))
async def unwatch_cmd(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .unwatch likho GURU!"); return
    if reply.sender_id in WATCH_LIST:
        del WATCH_LIST[reply.sender_id]; await event.reply("Watch se hata diya GURU!")
    else:
        await event.reply("Ye to watch pe tha hi nahi GURU!")

@client.on(events.NewMessage(pattern=r"\.watchlist"))
async def watchlist_cmd(event):
    if not WATCH_LIST:
        await event.reply("Koi watch pe nahi hai GURU!"); return
    txt = "WATCH LIST GURU:\n\n"
    for name in WATCH_LIST.values():
        txt += f"- {name}\n"
    await event.reply(txt)

@client.on(events.NewMessage(pattern=r"\.add"))
async def add_cmd(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .add likho GURU!"); return
    if reply.sender_id not in SUDO_USERS:
        SUDO_USERS.append(reply.sender_id); await event.reply("SUDO bana diya GURU!")
    else:
        await event.reply("Pehle se sudo hai GURU!")

@client.on(events.NewMessage(pattern=r"\.sudo"))
async def sudo_cmd(event):
    txt = "SUDO LIST GURU:\n\n"
    for uid in SUDO_USERS:
        txt += f"- {uid}\n"
    await event.reply(txt)

@client.on(events.NewMessage(pattern=r"\.autopin (on|off)"))
async def autopin_cmd(event):
    action = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .autopin on likho GURU!"); return
    chat_id = event.chat_id
    if chat_id not in AUTOPIN_GROUP:
        AUTOPIN_GROUP[chat_id] = set()
    if action == "on":
        AUTOPIN_GROUP[chat_id].add(reply.sender_id); await event.reply("GROUP AUTO-PIN ON GURU!")
    else:
        AUTOPIN_GROUP[chat_id].discard(reply.sender_id); await event.reply("GROUP AUTO-PIN OFF GURU!")

@client.on(events.NewMessage(pattern=r"\.dmautopin (on|off|list)"))
async def dmautopin_cmd(event):
    action = event.pattern_match.group(1)
    if action == "list":
        if not AUTOPIN_DM:
            await event.reply("Koi DM pin pe nahi hai GURU!"); return
        txt = "DM PIN LIST GURU:\n"
        for uid in AUTOPIN_DM:
            txt += f"- {uid}\n"
        await event.reply(txt); return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .dmautopin on likho GURU!"); return
    if action == "on":
        AUTOPIN_DM.add(reply.sender_id); await event.reply("DM AUTO-PIN ON GURU! Ab iske DM ke har message PIN honge")
    else:
        AUTOPIN_DM.discard(reply.sender_id); await event.reply("DM AUTO-PIN OFF GURU!")

@client.on(events.NewMessage(pattern=r"\.clone"))
async def clone_cmd(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .clone likho GURU!"); return
    try:
        me = await client.get_me()
        full_me = await client(functions.users.GetFullUserRequest(me.id))
        MY_ORIGINAL['first_name'] = me.first_name; MY_ORIGINAL['last_name'] = me.last_name or ""; MY_ORIGINAL['bio'] = full_me.full_user.about or ""
        target = await client.get_entity(reply.sender_id)
        full_target = await client(functions.users.GetFullUserRequest(reply.sender_id))
        await client(UpdateProfileRequest(first_name=target.first_name or "User", last_name=target.last_name or "", about=full_target.full_user.about or ""))
        if target.photo:
            photo = await client.download_profile_photo(reply.sender_id)
            if photo:
                await client(UploadProfilePhotoRequest(await client.upload_file(photo)))
        await event.reply(f"CLONE HO GAYA GURU! Ab tu {target.first_name} jaisa dikhega! Wapas ke liye .rmclone likh")
    except Exception as e:
        await event.reply(f"Clone fail GURU: {e}")

@client.on(events.NewMessage(pattern=r"\.rmclone"))
async def rmclone_cmd(event):
    if not MY_ORIGINAL:
        await event.reply("Pehle .clone kiya hi nahi GURU!"); return
    try:
        await client(UpdateProfileRequest(first_name=MY_ORIGINAL.get('first_name', 'User'), last_name=MY_ORIGINAL.get('last_name', ''), about=MY_ORIGINAL.get('bio', '')))
        photos = await client.get_profile_photos('me', limit=1)
        if photos:
            await client(DeletePhotosRequest(photos))
        await event.reply("RESTORE HO GAYA GURU! Wapas apni wali profile aa gayi!")
    except Exception as e:
        await event.reply(f"Restore fail GURU: {e}")

@client.on(events.NewMessage(pattern=r"\.nc\s+(.+)"))
async def nc_cmd(event):
    new_name = event.pattern_match.group(1)
    try:
        await client(functions.channels.EditTitleRequest(event.chat_id, new_name)); await event.reply(f"Chat ka naam badal diya GURU: {new_name}")
    except Exception as e:
        try:
            await client(functions.messages.EditChatTitleRequest(event.chat_id, new_name)); await event.reply(f"Chat ka naam badal diya GURU: {new_name}")
        except Exception as e2:
            await event.reply(f"Naam nahi badla GURU: {e2}")

@client.on(events.NewMessage(pattern=r"\.setpic"))
async def setpic_cmd(event):
    reply = await event.get_reply_message()
    if not reply or not reply.photo:
        await event.reply("Photo pe reply karke .setpic likho GURU!"); return
    try:
        photo = await reply.download_media()
        await client(functions.channels.EditPhotoRequest(event.chat_id, await client.upload_file(photo))); await event.reply("Group pic badal di GURU!")
    except Exception as e:
        await event.reply(f"Pic nahi badli GURU: {e}")

@client.on(events.NewMessage(pattern=r"\.ar\s+(.+)"))
async def ar_cmd(event):
    arg = event.pattern_match.group(1).strip()
    if arg.lower() == "off":
        AUTO_REACT.clear(); await event.reply("Auto-react OFF GURU!"); return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply("Reply karke .ar ❤️ likho GURU!"); return
    emoji = arg.split()[0]; AUTO_REACT[reply.sender_id] = emoji
    await event.reply(f"AUTO-REACT ON GURU! Ab iske har message pe {emoji} lagega")

@client.on(events.NewMessage(pattern=r"\.ar off"))
async def ar_off_cmd(event):
    AUTO_REACT.clear(); await event.reply("Auto-react OFF GURU!")

@client.on(events.NewMessage(pattern=r"\.stopar"))
async def stopar_cmd(event):
    AUTO_REACT.clear(); await event.reply("Saare Auto-react band GURU!")

@client.on(events.NewMessage(incoming=True))
async def watcher(event):
    if event.sender_id in AUTO_REACT:
        try:
            emoji = AUTO_REACT[event.sender_id]
            await client(functions.messages.SendReactionRequest(peer=event.chat_id, msg_id=event.message.id, reaction=[types.ReactionEmoji(emoticon=emoji)], big=False, add_to_recent=True))
        except: pass
    if event.is_private:
        if event.sender_id in AUTOPIN_DM:
            try: await client.pin_message(event.chat_id, event.message.id)
            except Exception as e: print(f"DM Pin fail: {e}")
    else:
        chat_id = event.chat_id
        if chat_id in AUTOPIN_GROUP and event.sender_id in AUTOPIN_GROUP[chat_id]:
            try: await client.pin_message(chat_id, event.message.id)
            except Exception as e: print(f"Group Pin fail: {e}")

print("FULL USERBOT GURU WALA CHALU HO GAYA...")
client.start()
client.run_until_disconnected()
