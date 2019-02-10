class YouTube:
    def __init__(self, apiKey):
        self.apikey = apiKey
        self.pewdiepie = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
        self.tseries = 'UCq-Fj5jknLsUf-MWSy4_brA'


    def getSubscribers(self, channelId):
        from requests import get
        from json import loads
        from time import sleep
        try:
            r = get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id={0}&key={1}'.format(channelId, self.apikey))
            subscriberCount = loads(r.text)['items'][0]['statistics']['subscriberCount']
            return int(subscriberCount)
        except (ConnectionError, ConnectionRefusedError, ConnectionResetError):
            sleep(1)
            return self.getSubscribers(channelId)


    def fetchData(self):
        pCount = self.getSubscribers(self.pewdiepie)
        tCount = self.getSubscribers(self.tseries)
        diffCount = max(pCount, tCount) - min(pCount, tCount)
        return pCount, tCount, diffCount