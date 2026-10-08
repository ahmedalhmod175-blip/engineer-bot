import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# تشغيل خادم ويب مصغر (Flask) لإبقاء السيرفر مستيقظاً على Render
app = Flask('')

@app.route('/')
def home():
    return "المحرك الذكي لـ مهندس النقاء يعمل بنجاح في السحاب... 🚀"

def run_flask():
    # Render يطلب دائماً بورت 10000 أو المنفذ التلقائي للمنصة
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# التوكن الجديد والمحدث الخاص بك
API_TOKEN = '8265769018:AAHfl30WEkflJYucuOBrRJtxZT0O0OMhJYg'
bot = telebot.TeleBot(API_TOKEN)

# يوزر قناتك الهاي كواليتي للاشتراك الإجباري
CHANNEL_USERNAME = '@PureVibes_HQ' 

def is_user_subscribed(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return True

def download_tiktok(url):
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best',
        # استخدام وكيل شبكة متخفٍ إذا دعت الحاجة لتفادي حظر تيك توك
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if is_user_subscribed(CHANNEL_USERNAME, user_id):
        bot.reply_to(message, "مرحباً بك في بوت خدمات تيك توك! 📥\nأرسل لي رابط أي فيديو تيك توك الآن لأقوم بتنقيته فوراً.")
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("اشترك في القناة أولاً 📢", url=f"https://t.me{CHANNEL_USERNAME.replace('@', '')}")
        markup.add(btn)
        bot.send_message(message.chat.id, "عذراً يا صديقي! يجب عليك الاشتراك في قناتنا أولاً لتتمكن من استخدام البوت مجاناً:", reply_markup=markup)

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def handle_tiktok_link(message):
    user_id = message.from_user.id
    if not is_user_subscribed(CHANNEL_USERNAME, user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton("اشترك في القناة هنا 📢", url=f"https://t.me{CHANNEL_USERNAME.replace('@', '')}")
        markup.add(btn)
        bot.send_message(message.chat.id, "عذراً! الرجاء الاشتراك في القناة أولاً لتفعيل ميزة التحميل الفوري:", reply_markup=markup)
        return

    url = message.text
    status_msg = bot.reply_to(message, "جاري معالجة الرابط وتطهير الفيديو... انتظر لحظة ⏳")
    
    try:
        download_tiktok(url)
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التنقية والتحميل بنجاح! 🔥\nقناتنا: @PureVibes_HQ")
        
        # أمر الحذف الفوري للحفاظ على مساحة السيرفر السحابي مجاناً كما طلبت
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')
            
        bot.delete_message(message.chat.id, status_msg.message_id)
    except Exception as e:
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')
        bot.edit_message_text("عذراً، حدث خطأ أثناء معالجة الفيديو. تأكد من أن الرابط صافٍ ومأخوذ من التطبيق مباشرة.", message.chat.id, status_msg.message_id)

if __name__ == '__main__':
    # تشغيل خادم Flask في الخلفية (Background Thread) لمنع نوم السيرفر
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("المحرك الذكي يعمل الآن بنجاح في السحاب... 🚀")
    bot.infinity_polling()
