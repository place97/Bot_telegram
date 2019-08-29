from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.comparisons import levenshtein_distance
import time,logging,requests,telebot


logging.basicConfig(level=logging.CRITICAL)
TOKEN = "938633123:AAGsU0pSh2vsLJNS71q9V9OKZLlMjBnbWpg"
bot = telebot.TeleBot(token=TOKEN)

bot_msg = ChatBot(
    "Karen",
    storage_adapter = "chatterbot.storage.SQLStorageAdapter",
    database = "./db.sqlite3",
    logic_adapters = [

        "chatterbot.logic.BestMatch",
        'chatterbot.logic.MathematicalEvaluation',
    ],
    statement_comparison_function = levenshtein_distance,
    response_selection_method = get_most_frequent_response
)

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    print(message)
    name=message.from_user.first_name
    bot.reply_to(message, 'Ciao '+name)


@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')

@bot.message_handler(commands=['dw'])
def download_(message):
    print(message.from_user.id)
    chat_id=message.from_user.id
    bot.send_photo(chat_id, open('C:\\Users\\Marco\\Downloads\\wp.jpg', 'rb'))


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


@bot.message_handler(func=lambda msg: msg.text is not None)
def conversation(message):
    texts = message.text
    print("User:"+message.from_user.first_name +" Text: "+message.text)
    trainer = ChatterBotCorpusTrainer(bot_msg)
    trainer.train('chatterbot.corpus.italian.conversations')
    bot_response = str(bot_msg.get_response(texts))
    print("Bot:"+bot_response)
    bot.reply_to(message,bot_response)



while True:
    try:
        bot.polling()
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
