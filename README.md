# Smog Watch

Smog Watch fetches **live PM2.5 air-quality data** for several cities from the
[Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api),
labels each city (Good / Moderate / Unhealthy / Hazardous), and ranks the
cities from worst to best air. No API key is needed.

## What it does

- Fetches the current PM2.5 (µg/m³) and US AQI for each city, live, using `requests`.
- Labels every city with the US EPA category for its AQI.
- Ranks cities from worst air to cleanest air.
- Can save a ranked snapshot to a CSV file with `--save`.
- Can check a single city with `--city`.

## Install

```bash
git clone <your-repo-url>
cd smog-watch
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python smog_watch.py
```

Check one city, or save the ranking to CSV:

```bash
python smog_watch.py --city Lahore
python smog_watch.py --save ranking.csv
```

## Sample output

(Sample output will be added here after the first live run.)

## Data source

Data: Open-Meteo Air Quality API (CAMS atmospheric composition forecasts).
Attribution: Open-Meteo, with CAMS data via the Copernicus Atmosphere
Monitoring Service. See <https://open-meteo.com/en/docs/air-quality-api>.
