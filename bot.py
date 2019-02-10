from telepot import Bot
from time import sleep
from schedule import every, run_pending
from pony.orm import db_session, select
from modules.database import Chat
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
lastDiff = youtube.fetchData()[2:3]


@db_session
def sendAlerts():
    global lastDiff
    diff = youtube.fetchData()[2:3]

    if (diff // 1000) < (lastDiff // 1000):
        pendingChats = select(chat for chat in Chat if chat.wantsAlert)[:]
        for chat in pendingChats:
            if chat.isGroup:
                chatid_right = int("-100" + str(chat.chatId))
            else:
                chatid_right = chat.chatId
            bot.sendMessage(chatid_right, "⚠️ <b>Lasagna Alert!</b>\n"
                                          "PewDiePie is only {0} suscribers ahead of T-Series.\n"
                                          "15 minutes ago it was {1}.".format(diff, lastDiff), parse_mode="HTML")

    elif (diff // 1000) > (lastDiff // 1000):
        pendingChats = select(chat for chat in Chat if chat.wantsAlert)[:]
        for chat in pendingChats:
            if chat.isGroup:
                chatid_right = int("-100" + str(chat.chatId))
            else:
                chatid_right = chat.chatId
            bot.sendMessage(chatid_right, "❇️ <b>Lasagna News!</b>\n"
                                          "PewDiePie is now {0} suscribers ahead of T-Series.\n"
                                          "15 minutes ago it was {1}.".format(diff, lastDiff), parse_mode="HTML")
    lastDiff = diff


@db_session
def reply(msg):
    chatId = msg['chat']['id']
    text = msg['text'].replace("@bitchlasagna_bot", "")
    name = msg['from']['first_name']

    if not Chat.exists(lambda c: c.chatId == int(str(chatId).replace("-100", ""))):
        if chatId > 0:
            Chat(chatId=chatId, isGroup=False)
        else:
            Chat(chatId=int(str(chatId).replace("-100", "")), isGroup=True)

    chat = Chat.get(chatId=int(str(chatId).replace("-100", "")))

    if text == "/start":
        pewd, tser, diff = youtube.fetchData()
        bot.sendMessage(chatId, "<b>Welcome, {0}!</b>\n"
                                "I'm the BitchLasagna Bot. I can monitor the current situation of PewDiePie vs. T-Series "
                                "subcount, and send you a daily message with some infos, if you want.\n\n"
                                "<b>PewDiePie:</b> {1} subs\n"
                                "<b>T-Series:</b> {2} subs\n"
                                "<b>Difference:</b> {3} subs".format(name, pewd, tser, diff), parse_mode="HTML")

    elif text == "/alert":
        chat.wantsAlert = True
        bot.sendMessage(chatId, "✅ Alerts have been successfully activated for this chat!")

    elif text == "/alertoff":
        chat.wantsAlert = False
        bot.sendMessage(chatId, "🛑 Alerts have been successfully disabled for this chat!")


bot.message_loop({'chat': reply})
every(15).minutes.do(sendAlerts)

while True:
    sleep(30)
    run_pending()