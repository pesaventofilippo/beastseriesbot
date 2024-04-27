from json import load
from time import sleep
from telepotpro import Bot
from pony.orm import db_session
from modules.api import SubscriberAPI
from modules.database import Chat, Data

with open("settings.json") as f:
    settings = load(f)

bot = Bot(settings['token'])
api = SubscriberAPI()


@db_session
def updateData():
    data = Data.get(id=0)
    data.mrbeast, _ = api.get_subscribers("UCX6OQ3DkcsbYNE6H8uQQuVA")
    data.tseries, _ = api.get_subscribers("UCq-Fj5jknLsUf-MWSy4_brA")


@db_session
def leaderboard() -> str:
    data = Data.get(id=0)

    mrbeast = f"<b>MrBeast:</b> <code>{data.mrbeast:,}</code>"
    tseries = f"<b>T-Series:</b> <code>{data.tseries:,}</code>"
    p1 = mrbeast if data.mrbeast > data.tseries else tseries
    p2 = tseries if data.mrbeast > data.tseries else mrbeast

    return (f"<b>Current subscribers status:</b>\n"
            f"🏆 {p1}\n"
            f"🥈 {p2}\n"
            f"<b>Gap:</b> <code>{data.diff:,}</code> subs")


@db_session
def reply(msg):
    chatId = msg['chat']['id']
    name = msg['from']['first_name']
    text = msg.get("text").replace("@" + bot.getMe()['username'], "")

    if not (chat := Chat.get(chatId=chatId)):
        chat = Chat(chatId=chatId)

    if text == "/start":
        bot.sendMessage(chatId, f"<b>Hi, {name}!</b>\n"
                                f"I'm the BeastSeries Bot 🤖. I monitor the live subsriber count of MrBeast vs. T-Series.\n"
                                f"I can also send you notifications if you use /alert!\n\n"
                                f"{leaderboard()}\n\n"
                                f"<i>Hint: use</i> /subs <i>to only show the stats.</i>", parse_mode="HTML")

    elif text == "/subs":
        bot.sendMessage(chatId, leaderboard(), parse_mode="HTML")

    elif text == "/alert":
        chat.wantsAlert = not chat.wantsAlert
        if chat.wantsAlert:
            bot.sendMessage(chatId, "🔔 <i>Alerts have been successfully activated for this chat!</i>\n"
                                    "Use /alert again to toggle them off.", parse_mode="HTML")
        else:
            bot.sendMessage(chatId, "🔕 <i>Alerts have been successfully deactivated for this chat.</i>\n"
                                    "Use /alert again to toggle them on.", parse_mode="HTML")


def main():
    with db_session:
        if not Data.exists():
            Data(id=0)

    bot.message_loop({'chat': reply})
    while True:
        updateData()
        sleep(120)


if __name__ == "__main__":
    main()
