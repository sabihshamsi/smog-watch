# Smog Watch

Smog Watch fetches **live PM2.5 air-quality data** for several cities from the
[Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api),
labels each city (Good / Unhealthy / Hazardous), and ranks the
cities from worst to best air. No API key is needed.

## What it does

- Fetches the current PM2.5 (µg/m³) and US AQI for each city, live, using `requests`.
- Labels every city Good, Unhealthy or Hazardous, using a simplified
  three-band scale based on the US AQI (Good 0-100, Unhealthy 101-200,
  Hazardous over 200).
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

Real output from a live run on 13 November 2026:

```
Smog Watch - live PM2.5 from Open-Meteo

Rank City             PM2.5   AQI  Label
------------------------------------------------------------
1    Delhi            106.4   251  Hazardous
2    Lahore            77.1   178  Unhealthy
3    Peshawar          88.9   149  Unhealthy
4    Islamabad         33.4    96  Good
5    Karachi           29.1    81  Good
6    Quetta            15.8    68  Good
```

Values change every run because the data is fetched live from the API.

## Data source

Data: Open-Meteo Air Quality API (CAMS atmospheric composition forecasts).
Attribution: Open-Meteo, with CAMS data via the Copernicus Atmosphere
Monitoring Service. See <https://open-meteo.com/en/docs/air-quality-api>.
