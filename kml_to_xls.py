from typing import List
from xml.dom import minidom
import xlsxwriter
from objects import Waypoint

# Constants for KML tag names
KML_NAME_TAG = 'name'
KML_COORDINATES_TAG = 'coordinates'

# Load and parse the KML file
mydoc = minidom.parse('input/example.kml')

# Extract waypoint names
names = mydoc.getElementsByTagName(KML_NAME_TAG)

# Extract coordinates
coordinates = mydoc.getElementsByTagName(KML_COORDINATES_TAG)

all_waypoints: List[Waypoint] = []

# Combined parsing for names and coordinates
for i in range(len(names)):
    full_name = str(names[i].firstChild.data).strip()

    # Skip unnecessary names
    if full_name in ('GPS device', 'vice', 'Waypoints', 'ints'):
        continue

    # Clean up the name to generate an identifier
    clean_name = ''.join(e for e in full_name if e.isalnum())
    identifier = clean_name[:5]

    # Extract and parse coordinates (lon, lat)
    try:
        coords = coordinates[i].firstChild.data.strip().split(',')
        lon = float(coords[0])
        lat = float(coords[1])
    except (ValueError, IndexError) as e:
        print(f"Error parsing coordinates for {full_name}: {e}")
        continue

    # Create Waypoint object and skip if longitude is zero
    waypoint = Waypoint(name=full_name, identifier=identifier, lat=lat, lon=lon)
    if waypoint.lon == 0:
        continue

    all_waypoints.append(waypoint)

# Create an XLSX file and add the waypoints to it
workbook = xlsxwriter.Workbook('output/Garmin_Waypoints.xlsx')
worksheet = workbook.add_worksheet("waypoint-table")

# Write column headers
labels = ["name", "identifier", "type", "country-code", "lat", "lon", "comment", "elevation"]
for i, label in enumerate(labels):
    worksheet.write(0, i, label)

# Write waypoint data
for row_index, waypoint in enumerate(all_waypoints, start=1):
    worksheet.write(row_index, 0, waypoint.name)
    worksheet.write(row_index, 1, waypoint.identifier)
    worksheet.write(row_index, 2, waypoint.type.value)
    worksheet.write(row_index, 3, waypoint.country_code)
    worksheet.write(row_index, 4, waypoint.lat)
    worksheet.write(row_index, 5, waypoint.lon)
    worksheet.write(row_index, 6, waypoint.comment)
    worksheet.write(row_index, 7, waypoint.elevation)

# Close the workbook
workbook.close()

print("Converted KML to XLSX successfully!")
