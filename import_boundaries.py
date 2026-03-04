import os
import json
import sys
import django

# --- WINDOWS PATH FIX (Ensures GDAL is found) ---
if os.name == 'nt':
    CONDA_ENV_PATH = r"C:\Users\oduor\miniconda3\envs\webgis_env"
    os.environ['PATH'] = os.path.join(CONDA_ENV_PATH, 'Library', 'bin') + os.pathsep + os.environ.get('PATH', '')
    os.environ['PROJ_LIB'] = os.path.join(CONDA_ENV_PATH, 'Library', 'share', 'proj')

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

# 2. Import GIS modules after setup
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from reports.models import SubCounty

def import_data():
    file_path = 'nairobi_subcounties.geojson'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found in {os.getcwd()}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    print("Starting import...")

    for feature in data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        # --- UPDATED: Using 'shapeName' as discovered ---
        name = properties.get('shapeName') or "Unknown Location"

        # Convert geometry to GEOS object
        try:
            geom = GEOSGeometry(json.dumps(geometry))

            # Ensure it is a MultiPolygon (Model requirement)
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon(geom)

            # Save to Database (using update_or_create to avoid 'Unknown' duplicates)
            sub_county, created = SubCounty.objects.update_or_create(
                name=name,
                defaults={'geom': geom}
            )

            if created:
                print(f"✅ Imported: {name}")
                count += 1
            else:
                print(f"🟡 Updated: {name}")
        
        except Exception as e:
            print(f"⚠️ Failed to import {name}: {e}")

    print(f"\n🚀 Success! Added {count} sub-counties to your local database.")

if __name__ == "__main__":
    import_data()