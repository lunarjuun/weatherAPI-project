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
        dt = datetime.fromisoformat(e["time"].replace("Z", "+00:00"))
        day = dt.date()
        temp = e["data"]["instant"]["details"]["air_temperature"]
        grouped.setdefault(day, []).append((dt, temp))
    return grouped

def summarize_period(temps):
    if not temps:
        return None
    t_values = [t for _, t in temps]
    return min(t_values), max (t_values), sum (t_values) / len(t_values)

def summarize_day(entries):
    summary = []
    all_temps = [t for _, t in entries]
    day_avg = sum(all_temps) / len(all_temps)
    for start, end, label in PERIODS:
        period = [(dt, t) for dt, t in entries if start <= dt.hour < end]
        if period:
            summary.append((label, *summarize_period(period)))
    return day_avg, summary

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

        grouped = {}
        for e in data["properties"]["timeseries"]:
            dt = datetime.fromisoformat(e["time"].replace("Z", "+00:00"))
            day = dt.date()
            temp = e["data"]["instant"]["details"]["air_temperature"]
            grouped.setdefault(day, []).append((dt, temp))

        print(f"Temperatur for {city.capitalize()}:")
        print("|------------------------------------------------------|")

        forecast = []
        for day, entries in list(grouped.items())[:7]:
            temps = [t for _, t in entries]
            day_avg = sum(temps) / len(temps)
            print(f"{day.strftime('%A %d.%m.%Y')} (snittemperatur {day_avg:.1f}°C):")

            for start, end, label in PERIODS:
                period_temps = [t for dt, t in entries if start <= dt.hour < end]
                if not period_temps:
                    continue
                t_min = min(period_temps)
                t_max = max(period_temps)
                t_avg = sum(period_temps) / len(period_temps)
                print(f"{label}: fra {round(t_min)} til {round(t_max)} grader (snittemperatur {t_avg:.1f})")
                forecast.append([
                    city.capitalize(),
                    day.strftime("%Y-%m-%d"),
                    label,
                    round(t_min, 1),
                    round(t_max, 1),
                    round(t_avg, 1),
                    round(day_avg, 1)
                ])

            print("|------------------------------------------------------|")

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["City", "Date", "Period", "MinTemp", "MaxTemp", "AvgTemp", "DayAvg"])
            writer.writerows(forecast)

        print(f"> Lagret {len(forecast)} rader til {CSV_FILE}.")
        continue

if __name__ == "__main__":
    main()