import csv
from django.core.management.base import BaseCommand
from Crimes.models import CrimeRecord
from datetime import datetime
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Geolocator setup
geolocator = Nominatim(user_agent="crime_loader")
location_cache = {}

def get_lat_lon(location_name):
    if location_name in location_cache:
        return location_cache[location_name]

    try:
        location = geolocator.geocode(f"{location_name}, Bengaluru, India", timeout=10)
        if location:
            lat_lon = (round(location.latitude, 6), round(location.longitude, 6))
            location_cache[location_name] = lat_lon
            time.sleep(1)
            return lat_lon
    except GeocoderTimedOut:
        print(f"Timeout for: {location_name}")
    return (None, None)

class Command(BaseCommand):
    help = 'Load updated crime data from CSV'

    def handle(self, *args, **kwargs):
        with open('bengaluru_crime_sample_data_updated.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                try:
                    date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                    location = row['Location']
                    crime_type = row['Crime Type'].strip().title()
                    modus_operandi = row['Modus Operandi']
                    weapon_used = row['Weapon Used']
                    description = row['Description']
                    case_status = row['Case Status']
                    ipc = row.get('IPC Section', 'Unknown')
                    punishment = row.get('Punishment', 'Not specified')

                    # Avoid duplicates
                    if CrimeRecord.objects.filter(date=date, location=location, crime_type=crime_type).exists():
                        continue

                    latitude, longitude = get_lat_lon(location)

                    CrimeRecord.objects.create(
                        date=date,
                        location=location,
                        crime_type=crime_type,
                        modus_operandi=modus_operandi,
                        weapon_used=weapon_used,
                        description=description,
                        case_status=case_status,
                        latitude=latitude,
                        longitude=longitude,
                        Indian_Penal_Code=ipc,
                        punishment=punishment
                    )
                    count += 1

                except Exception as e:
                    print(f"Error at row: {row}\n{e}")
        
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully loaded {count} records into the database."))
