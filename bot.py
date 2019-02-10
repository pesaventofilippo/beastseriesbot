from telepot import Bot
from time import sleep
from schedule import every, run_pending
from modules.youtube import YouTube

try:
    f = open('settings/token.txt', 'r')
    token = f.readline().strip()
    f.close()
except FileNotFoundError:
    token = input("Please paste the bot Token here: ")
    f = open('settings/token.txt', 'w')
    f.write(token)
    f.close()

try:
    f = open('settings/apikey.txt', 'r')
    apikey = f.readline().strip()
    f.close()
except FileNotFoundError:
    apikey = input("Please paste the YouTube v3 API Key here: ")
    f = open('settings/apikey.txt', 'w')
    f.write(apikey)
    f.close()

bot = Bot(token)
youtube = YouTube(apikey)


def reply(msg):
    chatId = msg['chat']['id']
    text = msg['text'].replace("@bitchlasagna_bot", "")
    name = msg['from']['first_name']

    if text == "/start":
        pewd, tser, diff = youtube.fetchData()
        bot.sendMessage(chatId, "<b>Welcome, {0}!</b>\n"
                                "I'm the BitchLasagna Bot. I can monitor the current situation of PewDiePie vs. T-Series "
                                "subcount, and send you a daily message with some infos, if you want.\n\n"
                                "<b>PewDiePie:</b> {1} subs\n"
                                "<b>T-Series:</b> {2} subs\n"
                                "<b>Difference:</b> {3} subs".format(name, pewd, tser, diff), parse_mode="HTML")


bot.message_loop({'chat': reply})
every().hour.do(youtube.logData)

while True:
    sleep(30)
    run_pending()
