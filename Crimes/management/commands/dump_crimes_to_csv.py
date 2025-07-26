import csv
from django.core.management.base import BaseCommand
from Crimes.models import CrimeRecord  # update this if your model name/path is different

class Command(BaseCommand):
    help = 'Dump all crimes from DB to CSV file'

    def handle(self, *args, **kwargs):
        with open('exported_crime_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['date', 'location', 'crime_type', 'modus_operandi', 'weapon_used', 'description', 'case_status', 'latitude', 'longitude'])

            for crime in CrimeRecord.objects.all():
                writer.writerow([
                    crime.date,
                    crime.location,
                    crime.crime_type,
                    crime.modus_operandi,
                    crime.weapon_used,
                    crime.description,
                    crime.case_status,
                    crime.latitude,
                    crime.longitude,
                ])

        self.stdout.write(self.style.SUCCESS('✅ All crimes exported to exported_crime_data.csv'))
