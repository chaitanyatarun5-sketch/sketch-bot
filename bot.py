import telebot, random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "9231054279:AAHGDTAW4Y9Zn5OfiFG5C4RVKQMUohkksKg"
bot = telebot.TeleBot(BOT_TOKEN)

JOKES = [
"Teacher: Homework kyu nahi kiya? Student: Sir, light chali gayi thi, aur dimaag bhi 😂",
"Pappu: Mummy aaj top kiya! Kaise? Sabse pehle aaya, sabse pehle ghar bhi aa gaya 😂",
"Boy: Tum bahut cute ho. Girl: Pata hai, mere papa ne bhi bola tha 😎",
"Padhai me mann nahi lagta, par phone ki battery khatam ho to dil rota hai 😭",
"Girlfriend: Kitna pyaar karte ho? Boy: Jitna tu data khatam karti hai 😂",
"Maths Teacher: Fail kyu hue? Student: Sir aapne hi bola tha 0 ki koi value nahi hoti 😜",
"Dost: Exam kaisa gaya? Main: Bas pen chala, dimaag nahi 😅",
"Mummy: Beta padh le. Beta: Topper bhi to kabhi padhta tha 😂",
"WiFi slow ho to lagta hai duniya ruk gayi hai 😩",
"Exam me 2 cheez kaam aati hai, ek yaad, dusri padosi ka paper 😂",
"Subah uthna sabse bada struggle hai, alarm se zyada mummy khatarnak hai 😅",
"Single hone ka fayda: Koi nahi puchta kahan ho, kiske saath ho 😎",
"Teacher: Class me kyu sote ho? Student: Sapne me bhi padhai karta hu 😴",
"Jab tak phone me 1% battery hai, tab tak umeed hai 😂",
"Dost: Party kab dega? Main: Jab salary aayegi. Dost: Tu to student hai. Main: Tabhi to 😭",
"Online class me sabse zyada camera off hota hai, aur neend on 😴",
"Papa: Result kaisa raha? Beta: 2 me top kiya, 3 me topper ko dekh ke aaya 😂",
"Ladki: Mere liye kya kar sakte ho? Ladka: Recharge tak kar dunga 😂",
"Zindagi me 2 hi tension hai, ek exam, dusra uska result 😅",
"Bhai ka style hi alag hai, padhai me zero, attitude me hero 😎",
"Teacher: Chup kyu ho? Student: Soch raha hu aap itna acha kaise padhate ho 😜",
"Khana kha ke neend aana, yehi meri asli talent hai 😴",
"Phone gir jaye to dil ruk jata hai, dil toot jaye to phone uthana padta hai 😂",
"Exam ke ek din pehle sab topper lagte hai, exam ke baad sab philosopher 😅",
"Mummy: Jab main tumhari umar ki thi... Bas yahi se kahani khatam 😂",
"Dost: Setting karwa de. Main: Khud ki setting kharab hai, teri kya karwau 😭",
"Barish me bheegna acha lagta hai, jab tak mummy ka danda na dikhe 😂",
"Padhai chhod, pehle chai pee lete hai, dimaag khulega ☕",
"Teacher kahe - Ye last question hai, samajh jao 5 aur baki hai 😅",
"Love me padna aasan hai, bahar nikalna syllabus se zyada mushkil hai 😂"
]

SHAYARI = [
"Teri yaad me humne chai bhi pee li, ab neend aaye to kya kare, KASHYAP BOT se hi baat kar li 🔥",
"Chandni raat me teri yaad aayi, dil ne kaha kash tu paas hoti ✨",
"Dosti me doori to aati rehti hai, phir bhi sacchi dosti dilo ko mila deti hai ❤️",
"Zindagi ek safar hai, haste hue guzarna, gham aaye to KASHYAP BOT ko yaad karna 😎",
"Tera naam likha hai dil ke panno pe, mitaye se bhi na mitega is zamane me 💌",
"Raato ko neend nahi aati, teri yaad satati hai, dil kehta hai tu hi meri duniya hai 🌙",
"Hasna sikha hai humne gham chupake, log samajhte hai hum khush hai bahut 😊",
"Waqt guzar gaya, yaadein reh gayi, tu door gaya, teri baatein reh gayi 💔",
"Dil to pagal hai, tujhe hi chahta hai, duniya chahe kuch bhi kahe, bas tu hi yaad aata hai ❤️",
"Chai ka cup aur teri yaad, dono ke bina subah adhoori lagti hai ☕",
"Na chahiye daulat, na chahiye shohrat, bas chahiye tera saath, aur ek cup chai 😌",
"Duniya ki bheed me kho gaya tha, teri ek muskan ne phir se jaga diya ✨",
"Khushboo teri yaadon ki, ab bhi dil me basi hai, tu door hai phir bhi, teri yaad paas hai 🌸",
"Gham ki raat lambi hai, par subah zaroor aayegi, himmat rakh dost, kismat bhi paltegi 💪",
"Tu mila to laga, zindagi mil gayi, warna hum to bas waqt guzar rahe the 🕰️",
"Dosti ka rishta sabse pyara hai, jo nibhaye wo hi sabse nyara hai 🤝",
"Yaad teri aati hai, dil tadap jata hai, tu kya jane, kitna yaad aata hai 😔",
"Has lo dost, zindagi choti hai, kal ka kya bharosa, aaj hi jee lo 😂",
"Teri muskan pe fida hai dil, tu hanse to lage duniya haseen hai 😍",
"Door reh kar bhi paas lagte ho, tum dil ke kitne khaas lagte ho ❤️",
"Waqt ne sikha diya, kaun apna kaun paraya, ab hum akele hi khush hai, yehi jeena sikhaya 💯",
"Chand ko dekh ke teri yaad aayi, chand bhi sharma gaya, jab teri baat aayi 🌙",
"Zindagi me har mod pe, ek naya sabak milta hai, gir ke uthna hi, asli jeet hoti hai 🔥",
"Tere bina dil lagta nahi, tu jo mile to duniya se kya lena 💖",
"Raat bhar teri yaad me, chandni se baatein ki, chand ne bhi kaha, tu kitni yaad aati hai ✨",
"Dil ka dard chupana aasan nahi, has ke jeena bhi aasan nahi, phir bhi haste hai hum, kyuki rona aata nahi 😊",
"Teri ek jhalak ke liye, hum zamana chhod denge, tu hanse to hum, apni khushi chhod denge 😍",
"Yaariyan nibhani hai, to dil se nibhao, matlab se nibhane wale, bas waqt ke saathi hai 🤝",
"Khwaab me tu aayi, dil khil gaya, subah uthi to laga, sapna hi tha 💭",
"KASHYAP BOT se dosti kar lo, gham bhi bhul jaoge, aur hasna bhi seekh jaoge 😎"
]

def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton("/start"), KeyboardButton("/help"))
    m.add(KeyboardButton("/joke"), KeyboardButton("/shayari"))
    m.add(KeyboardButton("/papa"), KeyboardButton("/myid"))
    m.add(KeyboardButton("/ping"), KeyboardButton("/inbox"))
    return m

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "KASHYAP BOT ON HAI! 🔥\n/HELP LIKH KE COMMANDS DEKH.", reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.send_message(m.chat.id, """/MYID - APNI ID DEKHO
/PING - BOT SPEED CHECK
/PAPA - PAPA WALA REPLY
/SHAYARI - SHAYARI ❤️
/JOKE - JOKE
/SKETCH - PHOTO KA SKETCH
/CARTOON - CARTOON STYLE
/INBOX - OWNER KE LIYE""", reply_markup=main_menu())

@bot.message_handler(commands=['myid'])
def id_cmd(m):
    bot.send_message(m.chat.id, f"Your ID: `{m.from_user.id}`\nName: {m.from_user.first_name}", parse_mode="Markdown")

@bot.message_handler(commands=['ping'])
def ping_cmd(m):
    bot.send_message(m.chat.id, "PONG! Bot full speed me chal raha hai ⚡")

@bot.message_handler(commands=['papa'])
def papa_cmd(m):
    bot.send_message(m.chat.id, "PAPA AA GAYE! 😎 Ab sab chup, KASHYAP BOT ka papa aa gaya hai 🔥")

@bot.message_handler(commands=['joke'])
def joke_cmd(m):
    bot.send_message(m.chat.id, random.choice(JOKES))

@bot.message_handler(commands=['shayari'])
def shayari_cmd(m):
    bot.send_message(m.chat.id, random.choice(SHAYARI))

@bot.message_handler(commands=['inbox'])
def inbox_cmd(m):
    msg = m.text.replace("/inbox","").strip()
    if not msg:
        bot.send_message(m.chat.id, "Aise likho: /inbox Hello bhai, bot mast hai!")
        return
    bot.send_message(m.chat.id, "Tera message owner tak pahunch gaya! ✅")

@bot.message_handler(content_types=['photo'])
def photo_cmd(m):
    bot.send_message(m.chat.id, "Photo mil gayi! /sketch ya /cartoon likh ke style bana lo 📸")

print("KASHYAP BOT STARTED")
bot.infinity_polling()
