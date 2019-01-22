import telepot, requests, json


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

bot = telepot.Bot(token)
pewdiepie = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
tseries = "UCq-Fj5jknLsUf-MWSy4_brA"


def getSubscribers(channelId, apiKey):
    try:
        r = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id=' + channelId + '&key=' + apiKey)
        subscriberCount = json.loads(r.text)["items"][0]["statistics"]["subscriberCount"]
        return subscriberCount
    except Exception:
        return None