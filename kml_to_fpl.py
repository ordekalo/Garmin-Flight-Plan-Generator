from typing import List
from xml.dom import minidom
from objects import Waypoint, Route, RoutePoint
import os

# Constants for KML tags
KML_NAME_TAG = 'name'
KML_COORDINATES_TAG = 'coordinates'

def parse_kml(file_path: str) -> List[Waypoint]:
    """
    Parse a KML file and extract waypoint data.

    :param file_path: Path to the KML file
    :return: List of Waypoint objects
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    # Parse the KML file
    mydoc = minidom.parse(file_path)

    # Extract names and coordinates from KML
    names = mydoc.getElementsByTagName(KML_NAME_TAG)
    coordinates = mydoc.getElementsByTagName(KML_COORDINATES_TAG)

    all_waypoints = []
    
    # Iterate over waypoints and coordinates
    for i in range(len(names)):
        full_name = str(names[i].firstChild.data).strip()

        # Skip invalid or unnecessary names
        if full_name in ('GPS device', 'vice', 'Waypoints', 'ints'):
            continue

        # Generate a clean identifier (first 5 alphanumeric characters)
        clean_name = ''.join(e for e in full_name if e.isalnum())
        identifier = clean_name[:5]

        # Extract coordinates (lon, lat)
        try:
            coords = coordinates[i].firstChild.data.strip().split(',')
            lon = float(coords[0])
            lat = float(coords[1])
        except (ValueError, IndexError) as e:
            print(f"Error parsing coordinates for {full_name}: {e}")
            continue

        # Create a Waypoint object
        waypoint = Waypoint(name=full_name, identifier=identifier, lat=lat, lon=lon)
        if waypoint.lon == 0:
            continue

        all_waypoints.append(waypoint)

    return all_waypoints


def create_fpl(waypoints: List[Waypoint], output_path: str):
    """
    Convert a list of waypoints into a Garmin-compatible FPL (Flight Plan) file.

    :param waypoints: List of Waypoint objects
    :param output_path: Output path for the generated FPL file
    """
    from xml.dom.minidom import Document

    # Create the FPL document
    doc = Document()

    # Create root element 'flight-plan'
    flight_plan = doc.createElement('flight-plan')
    flight_plan.setAttribute('xmlns', 'http://www8.garmin.com/xmlschemas/FlightPlan/v1')
    doc.appendChild(flight_plan)

    # Add the 'created' element
    created = doc.createElement('created')
    created.appendChild(doc.createTextNode('2024-01-01T00:00:00Z'))  # Replace with current date if needed
    flight_plan.appendChild(created)

    # Add 'waypoint-table'
    waypoint_table = doc.createElement('waypoint-table')
    flight_plan.appendChild(waypoint_table)

    # Add waypoints to waypoint-table
    for waypoint in waypoints:
        wp_element = doc.createElement('waypoint')
        waypoint_table.appendChild(wp_element)

        # Add waypoint details
        for tag, value in [('identifier', waypoint.identifier),
                           ('type', waypoint.type.value),
                           ('country-code', waypoint.country_code),
                           ('lat', str(waypoint.lat)),
                           ('lon', str(waypoint.lon)),
                           ('comment', waypoint.comment)]:
            element = doc.createElement(tag)
            element.appendChild(doc.createTextNode(value))
            wp_element.appendChild(element)

        if waypoint.elevation:
            elevation = doc.createElement('elevation')
            elevation.appendChild(doc.createTextNode(str(waypoint.elevation)))
            wp_element.appendChild(elevation)

    # Add 'route'
    route_elem = doc.createElement('route')
    flight_plan.appendChild(route_elem)

    # Add route details
    route_name = doc.createElement('route-name')
    route_name.appendChild(doc.createTextNode("Generated Route"))
    route_elem.appendChild(route_name)

    route_description = doc.createElement('route-description')
    route_description.appendChild(doc.createTextNode("Description of the generated route"))
    route_elem.appendChild(route_description)

    flight_plan_index = doc.createElement('flight-plan-index')
    flight_plan_index.appendChild(doc.createTextNode("1"))
    route_elem.appendChild(flight_plan_index)

    # Add route points
    for idx, waypoint in enumerate(waypoints):
        route_point = doc.createElement('route-point')
        route_elem.appendChild(route_point)

        waypoint_identifier = doc.createElement('waypoint-identifier')
        waypoint_identifier.appendChild(doc.createTextNode(waypoint.identifier))
        route_point.appendChild(waypoint_identifier)

        waypoint_type = doc.createElement('waypoint-type')
        waypoint_type.appendChild(doc.createTextNode(waypoint.type.value))
        route_point.appendChild(waypoint_type)

        waypoint_country_code = doc.createElement('waypoint-country-code')
        waypoint_country_code.appendChild(doc.createTextNode(waypoint.country_code))
        route_point.appendChild(waypoint_country_code)

    # Write the FPL document to file
    with open(output_path, 'w') as f:
        f.write(doc.toprettyxml(indent="  "))

    print(f"FPL file created at: {output_path}")


if __name__ == "__main__":
    # Path to the input KML file
    kml_file_path = 'input/example.kml'

    # Output path for the generated FPL file
    fpl_output_path = 'output/generated_flight_plan.fpl'

    # Parse KML and create waypoints
    waypoints = parse_kml(kml_file_path)

    # Create FPL file from waypoints
    create_fpl(waypoints, fpl_output_path)

    print("KML to FPL conversion completed!")
