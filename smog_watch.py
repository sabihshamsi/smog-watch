"""Smog Watch: live PM2.5 ranking for several cities.

Fetches current air-quality data from the Open-Meteo Air Quality API
(no API key needed) and prints each city's PM2.5 and US AQI.

Usage:
    python smog_watch.py
"""

import requests

from cities import CITIES

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


def main():
    print("Smog Watch - live PM2.5 from Open-Meteo\n")
    results = []
    for city in CITIES:
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


if __name__ == "__main__":
    main()
