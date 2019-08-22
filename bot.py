import time
import requests
import telebot

TOKEN = "938633123:AAGsU0pSh2vsLJNS71q9V9OKZLlMjBnbWpg"
bot = telebot.TeleBot(token=TOKEN)

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Benvenuto!!')

@bot.message_handler(commands=['conqui']) # welcome message handler
def send_conqui(message):
    bot.reply_to(message, 'Ciao alfix!')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')

@bot.message_handler(commands=['dw'])
def download_(message):
    CHAT_ID=requests.get(f"https://api.telegram.org/bot938633123:AAGsU0pSh2vsLJNS71q9V9OKZLlMjBnbWpg/getUpdates").json()['result'][-1]['message']['chat']['id']
    bot.send_photo(CHAT_ID, open('C:\\Users\\Marco\\Downloads\\wp.jpg', 'rb'))




@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

while True:
    try:
        bot.polling()
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
