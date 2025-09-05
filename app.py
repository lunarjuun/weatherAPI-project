import requests
from datetime import datetime, date, timedelta

def hent_data():
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
    headers = {"User-Agent": "Weather-API-project (internship mini project)"}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    data = hent_data()
    print(data)

if __name__ == "__main__":
    main()