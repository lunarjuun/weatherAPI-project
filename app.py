from myjsonreader import JsonReader
from datetime import datetime

def main():
    api = JsonReader("https://api.met.no/weatherapi/locationforecast/2.0/compact")
    data = api.fetch(params={"lat": 59.91, "lon": 10.75})
    
    entry = data["properties"]["timeseries"][0]
    dt = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
    temperature = entry["data"]["instant"]["details"]["air_temperature"]

    city = "Oslo" #hardcoded for now since api only has coords not city name
    print("City: {}".format(city))
    print("Date: {}".format(dt.strftime("%Y-%m-%d")))
    print("Time: {}".format(dt.strftime("%H:%M:%S")))
    print("Temperature: {} °C".format(temperature))

if __name__ == "__main__":
    main()

    # lagre i minne eller lagre i fil (minne er raskere å utvikle og raskere og kjøre, men fil har mer plass til mer data)
    # CSV eller XML (lagre data på fil, raskere å bruke enn å sette opp MongoDB eller Mysql)

# import requests
# from datetime import datetime, date, timedelta

# def hent_data():
#     url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
#     headers = {"User-Agent": "Weather-API-project (internship mini project)"}
#     response = requests.get(url, headers=headers)
#     return response.json()

# def main():
#     data = hent_data()
#     print(data)

# if __name__ == "__main__":
#     main()

#     # 59.91222135734928, 10.756120375589227