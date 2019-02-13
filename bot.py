from telepot import Bot
from time import sleep
from schedule import every, run_pending
from pony.orm import db_session, select
from modules.database import Chat, Data
from modules.youtube import YouTube

from pprint import pprint


@db_session
def initialize():
    global bot
    global youtube

    try:
        f = open('token.txt', 'r')
        token = f.readline().strip()
        f.close()
    except FileNotFoundError:
        token = input("Please paste the bot Token here: ")
        f = open('token.txt', 'w')
        f.write(token)
        f.close()

    try:
        f = open('apikey.txt', 'r')
        apikey = f.readline().strip()
        f.close()
    except FileNotFoundError:
        apikey = input("Please paste the YouTube v3 API Key here: ")
        f = open('apikey.txt', 'w')
        f.write(apikey)
        f.close()

    bot = Bot(token)
    youtube = YouTube(apikey)

    if not Data.exists(lambda d: d.id == 0):
        fetch = youtube.fetchData()
        Data(id=0, pewdiepie=fetch[0], tseries=fetch[1], difference=fetch[2])


@db_session
def updateData():
    data = Data.get(id=0)
    data.pewdiepie, data.tseries, data.difference = youtube.fetchData()


@db_session
def reply(msg):
    chatId = msg['chat']['id']
    fromId = msg['from']['id']
    name = msg['from']['first_name']
    text = msg['text'].replace(bot.getMe()['username'], "")

    if not Chat.exists(lambda c: c.chatId == str(chatId)):
        if chatId > 0:
            Chat(chatId=str(chatId), isGroup=False)
        else:
            Chat(chatId=str(chatId), isGroup=True)
    chat = Chat.get(chatId=str(chatId))
    data = Data.get(id=0)

    if chat.isGroup:
        member = bot.getChatMember(chatId, fromId)
        if member['status'] not in ['creator', 'administrator']:
            return

    if text == "/start":
        bot.sendMessage(chatId, "<b>Welcome, {0}!</b>\n"
                                "I'm the BitchLasagna Bot. I can monitor the current situation of PewDiePie vs. T-Series "
                                "subcount, send notifications on critical situations and more.\n\n"
                                "<b>PewDiePie:</b> {1} subs\n"
                                "<b>T-Series:</b> {2} subs\n"
                                "<b>Difference:</b> {3} subs".format(name, data.pewdiepie, data.tseries, data.difference),
                        parse_mode="HTML")

    elif text == "/help":
        bot.sendMessage(chat, "Hi, <b>{0}</b>! I'm the <b>BitchLasagna Bot</b>.\n"
                              "Here's a brief list of what I can do:\n\n"
                              "/start - Welcome message\n"
                              "/help - Show this list\n"
                              "/show - Send current subscribers count\n"
                              "/alert - Toggle on or off trigger notifications.\n"
                              "<b>NB</b>: In a group, only admins can use this bot."
                              "<i>Reminder: due to limited API availability, subscribers data is updated about every 2 minutes.</i>",
                        parse_mode="HTML")

    elif text == "/show":
        bot.sendMessage(chatId, "<b>Current subscribers status</b>\n"
                                "<b>PewDiePie:</b> {0} subs\n"
                                "<b>T-Series:</b> {1} subs\n"
                                "<b>Difference:</b> {2} subs".format(data.pewdiepie, data.tseries, data.difference),
                        parse_mode="HTML")

    elif text == "/alert":
        chat.wantsAlert = not chat.wantsAlert
        if chat.wantsAlert:
            bot.sendMessage(chat, "✅ <i>Alerts have been successfully activated for this chat!</i>\n"
                                  "Use /alert again to toggle them off.", parse_mode="HTML")
        else:
            bot.sendMessage(chat, "❌ <i>Alerts have been successfully deactivated for this chat.</i>\n"
                                  "Use /alert again to toggle them on.", parse_mode="HTML")


initialize()
bot.message_loop({'chat': reply})
every(2).minutes.do(updateData)

while True:
    sleep(30)
    run_pending()