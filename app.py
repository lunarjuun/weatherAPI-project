from myjsonreader import JsonReader
from datetime import datetime
import requests, csv

API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
USER_AGENT = "weatherapp/0.1"
CSV_FILE = "weather.csv"

PERIODS = [ # time period intervals
    (0, 8, "00-08"),
    (8, 12, "08-12"),
    (12, 18, "12-18"),
    (18, 24, "18-00"),
]

def geocode(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    r = requests.get(url, params={"q": city, "format": "json", "limit": 1}, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    results = r.json()
    return (float(results[0]["lat"]), float(results[0]["lon"])) if results else None

def group_by_day(data):
    grouped = {}
    for e in data["properties"]["timeseries"]:
        dt = datetime.fromisoformat(e{"time"}.replace("Z", "+00:00"))
        day = dt.date()
        temp = e["data"]["instant"]["details"]["air_temperature"]
        grouped.setdefault(day, [].append((dt, temp)))
    return grouped

def main():
    while True:
        print("|------------------------------------------------------|")
        print("> Velkommen til WeatherAPI!")
        
        print("...")
        city = input("> Tast inn bynavn: ").strip()
        print("...")
        
        coords = geocode(city)
        if not coords: 
            print(f'> Feil: Kan ikke finne en by med navnet "{city}".')
            continue

        lat, lon = coords
        api = JsonReader(API_URL)
        data = api.fetch(params={"lat": lat, "lon": lon})

        forecast = []
        print(f"Temperatur for {city.capitalize()} {datetime.now().strftime('%d.%m.%Y')}:")
        print("|------------------------------------------------------|")
        for e in data["properties"]["timeseries"][:24]:
            dt = datetime.fromisoformat(e["time"].replace("Z", "+00:00"))
            temp = e["data"]["instant"]["details"]["air_temperature"]
            print(f"Kl {dt.strftime('%H:%M')} {temp:.0f} grader")
            forecast.append([city.capitalize(), dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S"), temp])

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["City", "Date", "Time", "Temperature"])
            writer.writerows(forecast)
        
        continue

        # print(f"Lagret {len(forecast)} rader til {CSV_FILE}")

if __name__ == "__main__":
    main()
