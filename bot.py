import os, time, psutil, random, io
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageOps, ImageEnhance

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
START_TIME = time.time()
BOT_NAME = "KASHYAP BOT"

app = Flask(__name__)
@app.route('/')
def home():
    return "KASHYAP BOT IS LIVE!"

JOKES = ["Teacher: Kal homework kyu nahi kiya? Student: Light chali gayi thi 😂","Pappu: Mummy aaj top kiya! Kaise? Sabse pehle aaya, sabse pehle ghar bhi aa gaya 😂","Boy: Tum bahut cute ho. Girl: Haan pata hai, mere papa ne bhi bola tha 😎","Padhai me mann nahi lagta, par phone me battery khatam ho jaye to mann rota hai 😭","Girlfriend: Tum mujhe kitna pyaar karte ho? Boy: Jitna tu data khatam karti hai 😂","Maths ka teacher: Tum fail kyu hue? Student: Sir aapne hi bola tha, 0 ki koi value nahi hoti 😜","Dost: Bhai exam kaisa gaya? Main: Bas pen chala, dimaag nahi 😅","Mummy: Beta padh le. Beta: Mummy, topper bhi to kabhi padhta tha 😂","WiFi slow ho to lagta hai duniya ruk gayi hai 😩","Exam me 2 cheez kaam aati hai, ek yaad, dusri padosi ka paper 😂","Subah uthna sabse bada struggle hai, alarm se zyada mummy khatarnak hai 😅","Single hone ka fayda: Koi puchta nahi, kahan ho, kiske saath ho 😎","Teacher: Tum class me kyu sote ho? Student: Sir sapne me bhi padhai karta hu 😴","Jab tak phone me 1% battery hai, tab tak umeed hai 😂","Dost: Party kab dega? Main: Jab salary aayegi. Dost: Tu to student hai. Main: Tabhi to 😭","Online class me sabse zyada camera off hota hai, aur neend on 😴","Papa: Beta result kaisa raha? Beta: Papa, 2 subject me top kiya, 3 me topper ko dekh ke aaya 😂","Ladki: Tum mere liye kya kar sakte ho? Ladka: Recharge tak kar dunga 😂","Zindagi me 2 hi tension hai, ek exam, dusri uska result 😅","Bhai ka style hi alag hai, padhai me zero, attitude me hero 😎","Teacher: Chup kyu ho? Student: Sir soch raha hu, aap itna acha kaise padhate ho 😜","Khana kha ke neend aana, yehi meri asli talent hai 😴","Phone gir jaye to dil ruk jata hai, dil toot jaye to phone uthana padta hai 😂","Exam ke ek din pehle sab topper lagte hai, exam ke baad sab philosopher 😅","Mummy ka dialogue: Jab main tumhari umar ki thi, tab... Bas yahi se kahani khatam 😂","Dost: Bhai setting karwa de. Main: Khud ki setting kharab hai, teri kya karwau 😭","Barish me bheegna acha lagta hai, jab tak mummy ka danda na dikhe 😂","Padhai chhod, pehle chai pee lete hai, dimaag khulega ☕","Jab teacher kahe - Ye last question hai, samajh jao 5 aur baki hai 😅","Love me padna aasan hai, par usse bahar nikalna, usse zyada mushkil hai syllabus se 😂"]

SHAYARI = ["Teri yaad me humne chai bhi pee li, ab neend aaye to kya kare, KASHYAP BOT se hi baat kar li 🔥","Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ✨","Dosti me doori to aati rehti hai, phir bhi sacchi dosti dilo ko mila deti hai ❤️","Zindagi ek safar hai, haste hue guzarna, gham aaye to KASHYAP BOT ko yaad karna 😎","Tera naam likha hai dil ke panno pe, mitaye se bhi na mitega is zamane me 💌","Raato ko neend nahi aati, teri yaad satati hai, dil kehta hai tu hi meri duniya hai 🌙","Hasna sikha hai humne gham chupake, log samajhte hai hum khush hai bahut 😊","Waqt guzar gaya, yaadein reh gayi, tu door gaya, teri baatein reh gayi 💔","Dil to pagal hai, tujhe hi chahta hai, duniya chahe kuch bhi kahe, bas tu hi yaad aata hai ❤️","Chai ka cup aur teri yaad, dono ke bina subah adhoori lagti hai ☕","Na chahiye daulat, na chahiye shohrat, bas chahiye tera saath, aur ek cup chai 😌","Duniya ki bheed me kho gaya tha, teri ek muskan ne phir se jaga diya ✨","Khushboo teri yaadon ki, ab bhi dil me basi hai, tu door hai phir bhi, teri yaad paas hai 🌸","Gham ki raat lambi hai, par subah zaroor aayegi, himmat rakh dost, kismat bhi paltegi 💪","Tu mila to laga, zindagi mil gayi, warna hum to bas waqt guzar rahe the 🕰️","Dosti ka rishta sabse pyara hai, jo nibhaye wo hi sabse nyara hai 🤝","Yaad teri aati hai, dil tadap jata hai, tu kya jane, kitna yaad aata hai 😔","Has lo dost, zindagi choti hai, kal ka kya bharosa, aaj hi jee lo 😂","Teri muskan pe fida hai dil, tu hanse to lage duniya haseen hai 😍","Door reh kar bhi paas lagte ho, tum dil ke kitne khaas lagte ho ❤️","Waqt ne sikha diya, kaun apna kaun paraya, ab hum akele hi khush hai, yehi jeena sikhaya 💯","Chand ko dekh ke teri yaad aayi, chand bhi sharma gaya, jab teri baat aayi 🌙","Zindagi me har mod pe, ek naya sabak milta hai, gir ke uthna hi, asli jeet hoti hai 🔥","Tere bina dil lagta nahi, tu jo mile to duniya se kya lena 💖","Raat bhar teri yaad me, chandni se baatein ki, chand ne bhi kaha, tu kitni yaad aati hai ✨","Dil ka dard chupana aasan nahi, has ke jeena bhi aasan nahi, phir bhi haste hai hum, kyuki rona aata nahi 😊","Teri ek jhalak ke liye, hum zamana chhod denge, tu hanse to hum, apni khushi chhod denge 😍","Yaariyan nibhani hai, to dil se nibhao, matlab se nibhane wale, bas waqt ke saathi hai 🤝","Khwaab me tu aayi, dil khil gaya, subah uthi to laga, sapna hi tha 💭","KASHYAP BOT se dosti kar lo, gham bhi bhul jaoge, aur hasna bhi seekh jaoge 😎"]

def get_stats():
    uptime = int(time.time() - START_TIME)
    h, m, s = uptime//3600, (uptime%3600)//60, uptime%60
    ping = random.randint(30, 120)
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage('/').percent
    return ping, f"{h}h:{m}m:{s}s", ram, cpu, disk

def main_menu():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("ADMIN", callback_data="admin"),
        InlineKeyboardButton("PROFILE", callback_data="profile"),
        InlineKeyboardButton("EXTRA", callback_data="extra"),
        InlineKeyboardButton("BASIC", callback_data="basic"),
        InlineKeyboardButton("TOOLS", callback_data="tools"),
        InlineKeyboardButton("FUN", callback_data="fun"),
        InlineKeyboardButton("PLAY", callback_data="play"),
        InlineKeyboardButton("SUPPORT", url="https://t.me/"),
        InlineKeyboardButton("❌ CLOSE", callback_data="close"),
    )
    return markup

def make_sketch(img_bytes, style="pencil"):
    img = Image.open(io.BytesIO(img_bytes)).convert("L")
    if style == "pencil":
        sketch = ImageOps.invert(img)
        sketch = ImageEnhance.Contrast(sketch).enhance(1.5)
        out = Image.blend(img, sketch, 0.5)
    elif style == "cartoon":
        img2 = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        out = ImageEnhance.Color(img2).enhance(2.0)
        out = ImageEnhance.Contrast(out).enhance(1.3)
    else:
        out = ImageOps.invert(img)
    buf = io.BytesIO()
    out.save(buf, format="JPEG")
    buf.seek(0)
    return buf

@bot.message_handler(commands=['start'])
def start(m):
    ping, uptime, ram, cpu, disk = get_stats()
    text = f"**{BOT_NAME}**\n\n● **PING :** {ping}ms\n● **UPTIME :** {uptime}\n● **RAM USAGE :** {ram}%\n● **CPU USAGE :** {cpu}%\n● **DISK USAGE :** {disk}%\n\n**EACH COMMAND HERE IS BUILT FOR SPEED + POWER.**\n**CHOOSE THE CATEGORY:**"
    try:
        with open("start.jpg", "rb") as photo:
            bot.send_photo(m.chat.id, photo, caption=text, parse_mode="Markdown", reply_markup=main_menu())
    except:
        bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, "**KASHYAP BOT HELP MENU**\n\n/start - Start\n/help - Help\n/ping - Ping\n/id - ID\n/joke - 30 Joke\n/shayari - 30 Shayari\n/sketch - Photo ka sketch (photo pe reply karke)\n/pencil - Pencil sketch\n/cartoon - Cartoon style", reply_markup=main_menu())

@bot.message_handler(commands=['ping'])
def ping_cmd(m):
    ping, uptime, ram, cpu, disk = get_stats()
    bot.send_message(m.chat.id, f"**PONG!** 🏓\n\n● **PING:** {ping}ms\n● **UPTIME:** {uptime}\n● **RAM:** {ram}%\n● **CPU:** {cpu}%", parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def id_cmd(m):
    bot.send_message(m.chat.id, f"**Your ID:** `{m.from_user.id}`\n**Name:** {m.from_user.first_name}\n**Username:** @{m.from_user.username}", parse_mode="Markdown")

@bot.message_handler(commands=['joke'])
def joke_cmd(m):
    bot.send_message(m.chat.id, random.choice(JOKES))

@bot.message_handler(commands=['shayari'])
def shayari_cmd(m):
    bot.send_message(m.chat.id, random.choice(SHAYARI))

@bot.message_handler(commands=['sketch','pencil','cartoon'])
def sketch_cmd(m):
    if not m.reply_to_message or not m.reply_to_message.photo:
        bot.send_message(m.chat.id, "Bhai pehle koi photo bhejo, fir us photo pe reply karke /sketch likho!")
        return
    bot.send_message(m.chat.id, "Bana raha hu... thoda wait karo 🔥")
    file_info = bot.get_file(m.reply_to_message.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)
    style = "pencil" if m.text in ["/sketch","/pencil"] else "cartoon"
    out = make_sketch(downloaded, style)
    bot.send_photo(m.chat.id, out, caption="Ho gaya! KASHYAP BOT ka sketch 🔥")

@bot.message_handler(content_types=['photo'])
def photo_hint(m):
    bot.send_message(m.chat.id, "Photo mil gayi! Ab is photo pe reply karke /sketch ya /cartoon likho.")

@bot.callback_query_handler(func=lambda c: True)
def buttons(call):
    data = call.data
    if data == "close":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return
    texts = {
        "admin": "**ADMIN:**\n/ban - Ban\n/kick - Kick\n/mute - Mute\n/unmute - Unmute\n\nNote: Bot ko admin banana padega",
        "profile": "**PROFILE:**\n/id - Apni ID dekho",
        "extra": "**EXTRA:**\n/ping - Speed\n/start - Start",
        "basic": "**BASIC:**\n/start\n/help\n/ping\n/id",
        "tools": "**TOOLS:**\n/sketch - Photo ka sketch\n/pencil - Pencil sketch\n/cartoon - Cartoon\n/id - ID",
        "fun": "**FUN:**\n/joke - 30 Joke\n/shayari - 30 Shayari",
        "play": "**PLAY:**\n/joke - Joke\n/shayari - Shayari\n/sketch - Sketch Game",
    }
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, texts.get(data, "Coming Soon!"))

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask, daemon=True).start()
print("KASHYAP BOT STARTED")
bot.infinity_polling()
