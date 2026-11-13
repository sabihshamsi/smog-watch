"""Smog Watch: live PM2.5 ranking for several cities.

Fetches current air-quality data from the Open-Meteo Air Quality API
(no API key needed) and prints each city's PM2.5 and US AQI.

Usage:
    python smog_watch.py
"""

import requests

from cities import CITIES

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


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
    for city in CITIES:
        result = fetch_city(city)
        if result is None:
            continue
        print(
            f"{result['city']}, {result['country']}: "
            f"PM2.5 {result['pm2_5']} ug/m3, US AQI {result['aqi']} "
            f"at {result['time']}"
        )


if __name__ == "__main__":
    main()
