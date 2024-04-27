import requests


class SubscriberAPI:
    BASE_URL = "https://api.socialcounts.org"

    def __init__(self):
        self.session = requests.Session()

    def get_subscribers(self, channel_id) -> (int, int):
        url = f"{self.BASE_URL}/youtube-live-subscriber-count/{channel_id}"
        response = self.session.get(url).json()
        return int(response['est_sub']), int(response['API_sub'])
