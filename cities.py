"""City coordinates used by Smog Watch.

Each city is a name plus its WGS84 latitude/longitude, which is what the
Open-Meteo Air Quality API needs to return data for that place.
"""

CITIES = [
    {"name": "Karachi", "country": "Pakistan", "latitude": 24.8607, "longitude": 67.0011},
    {"name": "Lahore", "country": "Pakistan", "latitude": 31.5204, "longitude": 74.3587},
    {"name": "Islamabad", "country": "Pakistan", "latitude": 33.6844, "longitude": 73.0479},
    {"name": "Peshawar", "country": "Pakistan", "latitude": 34.0151, "longitude": 71.5249},
    {"name": "Quetta", "country": "Pakistan", "latitude": 30.1798, "longitude": 66.9750},
    {"name": "Delhi", "country": "India", "latitude": 28.7041, "longitude": 77.1025},
]


def find_city(name):
    """Return the city dict matching *name* (case-insensitive), or None."""
    name = name.strip().lower()
    for city in CITIES:
        if city["name"].lower() == name:
            return city
    return None
