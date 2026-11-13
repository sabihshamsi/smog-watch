"""Smog Watch: live PM2.5 ranking for several cities.

Fetches current air-quality data from the Open-Meteo Air Quality API
(no API key needed) and prints each city's PM2.5 and US AQI.

Usage:
    python smog_watch.py
    python smog_watch.py --city Lahore
    python smog_watch.py --save ranking.csv
"""

import argparse
import csv
from datetime import datetime, timezone

import requests

from cities import CITIES, find_city

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def aqi_label(aqi):
    """Return the US EPA health label for a US AQI value."""
    if aqi is None:
        return "Unknown"
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def fetch_city(city):
    """Fetch current PM2.5 and US AQI for one city.

    Returns a dict with the city name, pm2_5 (µg/m³), aqi, and the
    timestamp of the reading, or None if the request failed.
    """
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "current": "pm2_5,us_aqi_pm2_5",
        "timezone": "auto",
    }
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Could not fetch data for {city['name']}: {exc}")
        return None

    current = response.json().get("current", {})
    return {
        "city": city["name"],
        "country": city["country"],
        "pm2_5": current.get("pm2_5"),
        "aqi": current.get("us_aqi_pm2_5"),
        "time": current.get("time"),
    }


def save_csv(results, path):
    """Save the ranked results to a CSV file with a fetch timestamp."""
    fetched_at = datetime.now(timezone.utc).isoformat()
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rank", "city", "country", "pm2_5_ug_m3", "us_aqi", "label", "reading_time", "fetched_at_utc"])
        for rank, result in enumerate(results, start=1):
            writer.writerow([
                rank,
                result["city"],
                result["country"],
                result["pm2_5"],
                result["aqi"],
                aqi_label(result["aqi"]),
                result["time"],
                fetched_at,
            ])
    print(f"\nSaved {len(results)} rows to {path}")


def main():
    parser = argparse.ArgumentParser(description="Rank cities by live PM2.5 air quality.")
    parser.add_argument("--city", help="Check a single city by name, e.g. --city Lahore")
    parser.add_argument("--save", metavar="FILE", help="Save the ranking to a CSV file")
    args = parser.parse_args()

    if args.city:
        selected = find_city(args.city)
        if selected is None:
            print(f"Unknown city: {args.city}")
            print("Available cities:", ", ".join(c["name"] for c in CITIES))
            return
        cities = [selected]
    else:
        cities = CITIES

    print("Smog Watch - live PM2.5 from Open-Meteo\n")
    results = []
    for city in cities:
        result = fetch_city(city)
        if result is not None:
            results.append(result)

    # Worst air first (highest AQI at the top).
    results.sort(key=lambda r: (r["aqi"] is None, -(r["aqi"] or 0)))

    print(f"{'Rank':<5}{'City':<14}{'PM2.5':>8}  {'AQI':>4}  Label")
    print("-" * 60)
    for rank, result in enumerate(results, start=1):
        pm25 = f"{result['pm2_5']:.1f}" if result["pm2_5"] is not None else "n/a"
        aqi = str(result["aqi"]) if result["aqi"] is not None else "n/a"
        print(
            f"{rank:<5}{result['city']:<14}{pm25:>8}  "
            f"{aqi:>4}  {aqi_label(result['aqi'])}"
        )

    if args.save:
        save_csv(results, args.save)


if __name__ == "__main__":
    main()
