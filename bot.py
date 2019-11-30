import time,logging,requests,telebot,_json

# Openweathermap Weather codes and corressponding emojis
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F609'    # default emojis

###
TOKEN = "your_token"
bot = telebot.TeleBot(token=TOKEN)



def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    print(message)
    name=message.from_user.first_name+" "+defaultEmoji
    initial_message='Karen_weather_bot  started\nPlease enter the city name as \'text\''
    bot.reply_to(message, initial_message)


@bot.message_handler(func=lambda msg: msg.text is not None)
def send_weather(message):
    api_key="your_key"
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    city_name=message.text
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    print(message)
    print("User:"+message.from_user.first_name +" Text: "+message.text)
    print(x)
    if x["cod"] != "404":
        chat_id=message.from_user.id
        cityName = x.get('name')
        countryName = x.get('sys').get('country')
        temp_current = int(x.get('main').get('temp'))-273,15
        max_temperature =int(x.get('main').get('temp_max'))-273,15
        min_temperature = int(x.get('main').get('temp_min'))-273,15
        description_brief = x.get('weather')[0].get('main')
        weatherID = x.get('weather')[0].get('id')     # gets ID of weather description, used for emoji
        emoji = getEmoji(weatherID)
        bot_response= cityName + ', ' + countryName + ': ' + str(temp_current) + '°C\n' + 'Max: ' + str(max_temperature) + '°C - ' + 'Min: ' + str(min_temperature)+ '°C\n' +   description_brief +str(emoji) + str(emoji)
        bot.reply_to(bot.send_location(chat_id,x.get('coord').get('lat'),x.get('coord').get('lon')),bot_response)
    else:
        bot.reply_to(message,"City not found")

"""
    Return related emojis according to weather
"""
def getEmoji(weatherID):
    if weatherID:
        if str(weatherID)[0] == '2' or weatherID == 900 or weatherID==901 or weatherID==902 or weatherID==905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID==903 or weatherID== 906:
            return snowflake + ' ' + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID==802 or weatherID==803 or weatherID==803 or weatherID==804:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji    # Default emoji

    else:
        return defaultEmoji   # Default emoji


while True:
    try:
        print("Start....")
        bot.polling()
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
