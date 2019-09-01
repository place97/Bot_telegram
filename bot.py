import time,logging,requests,telebot,_json

TOKEN = "938633123:AAGsU0pSh2vsLJNS71q9V9OKZLlMjBnbWpg"
bot = telebot.TeleBot(token=TOKEN)
defaultEmoji = u'\U0001F609'
thermometer= u'\U0001F321'


def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    print(message)
    name=message.from_user.first_name+" "+defaultEmoji
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
def send_weather(message):
    api_key="d6fc917ff572a05b14832847e59b5302"
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    city_name=message.text
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    print(message)
    print("User:"+message.from_user.first_name +" Text: "+message.text)
    print(x)
    if x["cod"] != "404":
        y = x["main"]
        current_temperature =int(y["temp"])-273,15
        max_temperature = int(y["temp_max"])-273,15
        min_temperature = int(y["temp_min"])-273,15
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        bot_response=("Temperatura attuale:  " +str(thermometer)+" "+
                    str(current_temperature) +" °C"+
                    "\nTemperatura max : " +str(thermometer)+" "+
                    str(max_temperature) +" °C"+
                    "\nTemperatura min : " +str(thermometer)+" "+
                    str(min_temperature) +" °C"+
                    "\nUmidità :  " +
                    str(current_humidiy) +" %"
                    "\nInfo :  " +
                        str(weather_description))
        bot.reply_to(message,bot_response)
    else:
        bot.reply_to(message,"City not found")


while True:
    try:
        print("Start....")
        bot.polling()
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
