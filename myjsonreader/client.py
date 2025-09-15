import requests
class JsonReader:
    def __init__(self, base_url, user_agent="myjsonreader/0.1"):
        self.base_url = base_url
        self.headers = {"User-Agent": user_agent}

    def fetch(self, endpoint="", params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
       