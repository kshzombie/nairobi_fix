import os
import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from reports.models import SubCounty

class Command(BaseCommand):
    help = 'Imports Nairobi sub-county boundaries from a GeoJSON file'

    def handle(self, *args, **options):
        # 1. Define the path to your file
        data_path = os.path.join('data', 'nairobi_sub_counties.json')

        if not os.path.exists(data_path):
            self.stdout.write(self.style.ERROR(f"File not found at {data_path}"))
            return

        # 2. Open and load the data
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        # 3. Now 'data' is defined, so we can loop through it
        for feature in data['features']:
            props = feature['properties']
            # Target 'shapeName' specifically as per your boundary document
            sc_name = props.get('shapeName')

            if not sc_name:
                sc_name = "Unknown Sub-County"

            geom_data = json.dumps(feature['geometry'])
            geom = GEOSGeometry(geom_data)

            # GeoDjango typically expects MultiPolygon
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon(geom)

            # Create or update the record
            SubCounty.objects.update_or_create(
                name=sc_name,
                defaults={'geom': geom}
            )
            count += 1
            self.stdout.write(f"Imported: {sc_name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} sub-counties!'))
