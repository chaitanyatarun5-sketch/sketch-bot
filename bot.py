from flask import Flask
import threading
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot chal raha hai..."

def run_web():
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

import random, os
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import uuid

TOKEN = os.getenv("TOKEN")
ALLOWED_USER_IDS = [8532606474, 9239452757]

def is_allowed(update):
    if update.effective_user is None:
        return False
    return update.effective_user.id in ALLOWED_USER_IDS

JOKES = [
    "😂 TEACHER: KAL SCHOOL KYU NAHI AAYE? STUDENT: GIRLFRIEND SE MILNE GAYA THA 😜",
    "🤣 PAPPU: PAPA, EXAM ME FAIL HO GAYA. PAPA: KOI BAAT NAHI BETA, TU TO PAIDA HOTE HI FAIL THA 😅",
    "😂 SANTA: DOCTOR SAHAB, MUJHE BHOOLNE KI BIMARI HAI. DOCTOR: KAB SE? SANTA: KAB SE KYA? 🤔",
    "😜 EK LADKA LADKI SE: TUM BAHUT SUNDAR HO. LADKI: JHOOTH MAT BOLO. LADKA: THEEK HAI, TUM BAHUT GANDI HO 😂",
    "🤣 PAPPU: YAAR YE WHATSAPP KYA HAI? CHINTU: JAHA LOG ONLINE REH KAR BHI REPLY NAHI KARTE 📱",
    "😂 BIWI: SUNO, AGAR MAIN KAHIN KHO JAU TO KYA KAROGE? PATI: MAIN AKHBAR ME VIGYAPAN DUNGA. BIWI: KIS AKHBAR ME? PATI: SABSE SASTE WALE ME 📰",
    "😜 TEACHER: BATAO, TAJ MAHAL KAHA HAI? PAPPU: SIR, GOOGLE MAPS ME 📍",
    "🤣 SANTA KA BETA: PAPA, MAIN BADA HOKE KYA BANUNGA? SANTA: BETA, PEHLE BADA TO HO JA 😂",
    "😂 LADKA: TUMHARI AANKHEN BAHUT SUNDAR HAI. LADKI: TO CHASHMA PEHEN LO, DIKHAYI NAHI DETA KYA? 👓",
    "😜 PAPPU: MUMMY, AAJ SCHOOL ME MERI PITAI HUI. MUMMY: KYU? PAPPU: HOMEWORK NAHI KIYA THA 😭",
    "🤣 EK AADMI DOCTOR KE PAAS GAYA: DOCTOR, MUJHE SAB KUCH DO-DO DIKHTA HAI. DOCTOR: BAITH JAO, TUM CHAR LOG EK SAATH MAT BAITHO 👀",
    "😂 CHINTU: YAAR, MERI GIRLFRIEND NE MUJHE BLOCK KAR DIYA. PAPPU: TO NAYA ACCOUNT BANA LE. CHINTU: USNE MUJHE HI BLOCK KIYA HAI 🚫",
    "😜 PATI: TUM KHANA BAHUT ACHHA BANATI HO. PATNI: TO KHANA KHA KE BARTAN BHI DHO DO 🍽️",
    "🤣 TEACHER: AGAR TUMHE 100 RUPAYE MILEN TO KYA KAROGE? PAPPU: SIR, UDHAR WAPAS KAR DUNGA, BAHUT UDHAR HAI 💸",
    "😂 SANTA: BANTA, YE MOBILE KA PASSWORD KYA HAI? BANTA: PATA NAHI, MAINE TO LOCK HI NAHI LAGAYA 🔓",
    "😜 LADKA: I LOVE YOU. LADKI: MERE PAAS BOYFRIEND HAI. LADKA: TO KYA HUA, MERE PAAS BHI GIRLFRIEND HAI ❤️",
    "🤣 PAPPU: PAPA, MUJHE CYCLE CHAHIYE. PAPA: PEHLE CYCLE CHALANA SEEKH, PHIR DILWA DUNGA 🚲",
    "😂 BIWI: MUJHE 1000 RUPAYE CHAHIYE. PATI: KIS LIYE? BIWI: FACIAL KARWANA HAI. PATI: ARRE, CHEHRA TO WAHI RAHEGA 💄",
    "😜 EK CHOR POLICE SE: SIR, MAINE CHORI NAHI KI. POLICE: TO YE TV TERE GHAR ME KAISE AAYA? CHOR: SIR, TV KHUD CHAL KE AAYA HAI 📺",
    "🤣 TEACHER: TUM ITNE LATE KYU AAYE? STUDENT: SIR, SAPNA DEKH RAHA THA KI SCHOOL JA RAHA HU, UTHTE HI LATE HO GAYA 😴",
    "😂 SANTA: YAAR, MERI BIWI MUJHSE BAHUT LADTI HAI. BANTA: MERI WALI TO LADTI BHI NAHI, SEEDHA BELAN MARTI HAI 😅",
    "😜 PAPPU: YAAR, EXAM ME CHEATING KARTE PAKDA GAYA. CHINTU: TO KYA HUA? PAPPU: TEACHER NE BOLA, TUM TO TOPPER HO 😎",
    "🤣 LADKI: TUM MUJHSE KITNA PYAR KARTE HO? LADKA: JITNA JIO KA NET, KABHI KHATAM NAHI HOTA 📶",
    "😂 PATI: AAJ KHANE ME KYA HAI? PATNI: JO KAL THA. PATI: KAL KYA THA? PATNI: JO PARSO THA 🍛",
    "😜 EK LADKA: BHAI, GIRLFRIEND KAISE PATAYE? DUSRA: BHAI, PEHLE PAISE KAMA, GIRLFRIEND KHUD PAT JAYEGI 💰",
    "🤣 TEACHER: PAPPU, TUMHARE PAPA KYA KARTE HAI? PAPPU: SIR, JO MAIN KARTA HU, WO HI KARTE HAI - KUCH NAHI 😂",
    "😂 SANTA: DOCTOR, MERI YAADDASHT KAMZOR HO GAYI HAI. DOCTOR: KITNE SAAL SE? SANTA: YAAD NAHI 🤯",
    "😜 CHINTU: YAAR, KAL MAINE 100 RUPAYE KA NOTE DEKHA, UTHAYA NAHI. PAPPU: KYU? CHINTU: WO KISI AUR KA THA 💵",
    "🤣 BIWI: TUM MUJHE KABHI GHUMANE NAHI LE JATE. PATI: LE TO JATA HU, ROZ SAPNE ME SWITZERLAND GHUMATA HU ✈️",
    "😂 PAPPU: MUMMY, AAJ MAINE EK ACHHA KAAM KIYA. MUMMY: KYA? PAPPU: EK BUDHE AADMI KO ROAD CROSS KARWAYA. MUMMY: WO JANA NAHI CHAHTA THA TO? 👴"
]

SHAYARI = [
    "❤️ TERI YAAD ME DIL NE YE KAHA, TU HI MERI DUNIYA HAI 🌍",
    "💔 MOHABBAT ME HUMNE KHUD KO MITA DIYA, PHIR BHI TU MILA NAHI 😢",
    "❤️ DIL TO PAGAL HAI, TUJHE HI CHAHTA HAI 😍",
    "🌙 RAATEIN LAMBI HAI, YAADEIN TERI HAI, NEEND NAHI AATI, BAAT TERI HAI ✨",
    "💖 TUM MILE TO LAGA, ZINDAGI MIL GAYI, TUM GAYE TO LAGA, SAB KUCH CHALA GAYA 😔",
    "💔 ISHQ ME HUMNE JO PAYA, WO DARD HI PAYA, PHIR BHI DIL NE TUJHE HI CHAHA 🥺",
    "😍 TERI MUSKAAN PE FIDA HU MAIN, TU MILE TO DUA HU MAIN 🙏",
    "🌙 CHANDNI RAAT ME TERI YAAD AAYI, DIL NE KAHA TU HI MERI KHUSHBOO HAI 🌸",
    "❤️ NA JAANE KYU DIL TUJHE HI CHAHTA HAI, HAR DUA ME TERA HI NAAM AATA HAI 🤲",
    "😍 TUJHE DEKH KE DIL NE YE SOCHA, KAASH TU MERI HOTI 💭",
    "💫 DOOR REH KAR BHI TU PAAS LAGTA HAI, YE ISHQ BHI KYA KAMAAL KARTA HAI ✨",
    "🪄 TERI BAATON ME WO JAADU HAI, DIL HAR BAAR TERA HO JATA HAI 💖",
    "❤️ ZINDAGI ME EK TU HI TO HAI, JISKE BINA SAB ADHURA HAI 🥺",
    "💔 TERI YAADON KA SAHARA HAI, WARNA ZINDAGI ME KYA RAKHA HAI 😔",
    "😜 MOHABBAT TO BAS EK BAHANA HAI, ASLI MAZA TO TUJHE SATANE ME HAI 😂",
    "💓 DIL KI DHADKAN TU HAI, MERI HAR KHUSHI TU HAI 💖",
    "🤲 TUJHSE MILNE KI TAMANNA HAI, TUJHE PANE KI DUA HAI ❤️",
    "🌙 RAAT BHAR TERI YAAD ME JAGTE HAI, SUBAH HOTE HI PHIR SO JATE HAI 😴",
    "😊 TU JO HANSE TO DUNIYA HANSE, TU JO ROYE TO DIL ROYE 💔",
    "💔 ISHQ KIYA TO DARD MILA, DARD ME BHI SUKOON MILA 🌹",
    "😍 TERI AANKHON ME DOOB JANE KA MANN KARTA HAI, TERI BAHON ME KHO JANE KA MANN KARTA HAI 🤗",
    "💔 NA TU MILI, NA MAIN MILA, BAS YE DIL AKELE REH GAYA 😢",
    "🥺 TERE BINA JEENA MUSHKIL HAI, TERE SAATH JEENA BHI MUSHKIL HAI ❤️",
    "😍 CHUPKE SE DIL ME AA GAYE TUM, PATA BHI NA CHALA AUR CHHA GAYE TUM ✨",
    "💖 TERI EK JHALAK KE LIYE, HUM ZAMANA BHOOL JATE HAI 🌍",
    "❤️ DIL NE KAHA TU HI MERI MANZIL HAI, TU HI MERI RAAH HAI 🛤️",
    "😊 TUJHE SOCH KE HI MUSKURATA HU, TU JO MILE TO KYA HOGA 💭",
    "💔 PYAR ME HUMNE WAFA KI, TUMNE BEWAFAI KI, PHIR BHI DIL NE TUMHE HI CHAHA 😢",
    "❤️ TERI YAAD AATI HAI TO DIL ROTA HAI, TU JO SAMNE AAYE TO DIL HANSTA HAI 😍",
    "🌹 ZINDAGI KA SAFAR TU HI HAI, MERI HAR KHUSHI TU HI HAI 💖"
]

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text("BOT ON HAI! 🔥 /HELP LIKH KE COMMANDS DEKH.\nINLINE KE LIYE KISI BHI CHAT ME @BOTUSERNAME JOKE LIKH.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text("/START - BOT START\n/HELP - COMMANDS\n/PAPA - PAPA WALA REPLY\n/SHAYARI - 30 ME SE 1 SHAYARI ❤️\n/JOKE - 30 ME SE 1 JOKE 😂\nINLINE - KISI BHI CHAT ME @BOTUSERNAME JOKE / SHAYARI LIKH")

async def papa_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text("BOT ON HAI! 🔥")

async def shayari_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(random.choice(SHAYARI))

async def joke_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(random.choice(JOKES))

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower().strip()
    results = []
    if "shayari" in query:
        items = random.sample(SHAYARI, 5)
        for i, text in enumerate(items):
            results.append(InlineQueryResultArticle(id=str(uuid.uuid4()), title=f"SHAYARI {i+1} ❤️", input_message_content=InputTextMessageContent(text), description=text[:60]))
    else:
        items = random.sample(JOKES, 5)
        for i, text in enumerate(items):
            results.append(InlineQueryResultArticle(id=str(uuid.uuid4()), title=f"JOKE {i+1} 😂", input_message_content=InputTextMessageContent(text), description=text[:60]))
    await update.inline_query.answer(results, cache_time=0)

async def main():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start_cmd))
    app_bot.add_handler(CommandHandler("help", help_cmd))
    app_bot.add_handler(CommandHandler("papa", papa_cmd))
    app_bot.add_handler(CommandHandler("shayari", shayari_cmd))
    app_bot.add_handler(CommandHandler("joke", joke_cmd))
    app_bot.add_handler(InlineQueryHandler(inline_query))
    await app_bot.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
