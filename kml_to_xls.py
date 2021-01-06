from typing import List
from xml.dom import minidom
import xlsxwriter

# parse an xml file by name
from objects import Waypoint

mydoc = minidom.parse('input/example.kml')

names = mydoc.getElementsByTagName('name')

all_names = []
all_identifiers = []
# all names
for name in names:
    full_name = str(name.firstChild.data)
    if full_name in ('GPS device', 'vice', 'Waypoints', 'ints'):
        continue
    all_names.append(full_name)

    clean_name = ''.join(e for e in full_name if e.isalnum())
    identifier = clean_name[:5]
    all_identifiers.append(identifier)

coordinates = mydoc.getElementsByTagName('coordinates')

all_lons = []
all_lats = []
for point in coordinates:
    data = str(point.firstChild.data)
    arr = data.split(',')
    lon = arr.pop()
    all_lons.append(lon)
    lat = arr.pop()
    all_lats.append(lat)

all_waypoints: List[Waypoint] = []
for i in range(len(all_names)):
    waypoint = Waypoint(name=all_names[i], identifier=all_identifiers[i], lat=float(all_lats[i]),
                        lon=float(all_lons[i]))
    if waypoint.lon == 0:
        continue
    all_waypoints.append(waypoint)

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('output/Garmin_Waypoints.xlsx')
worksheet = workbook.add_worksheet("waypoint-table")

labels = ["name", "identifier", "type", "country-code", "lat", "lon", "comment", "elevation"]

for i in range(len(labels)):
    worksheet.write(0, i, labels[i])

for j in range(len(all_waypoints)):
    worksheet.write(j + 1, 0, all_waypoints[j].name)
    worksheet.write(j + 1, 1, all_waypoints[j].identifier)
    worksheet.write(j + 1, 2, all_waypoints[j].type.value)
    worksheet.write(j + 1, 3, all_waypoints[j].country_code)
    worksheet.write(j + 1, 4, all_waypoints[j].lat)
    worksheet.write(j + 1, 5, all_waypoints[j].lon)
    worksheet.write(j + 1, 6, all_waypoints[j].comment)
    worksheet.write(j + 1, 7, all_waypoints[j].elevation)

workbook.close()

print("Converted KML to XLSX successfully!")
