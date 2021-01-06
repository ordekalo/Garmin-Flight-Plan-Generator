from openpyxl import load_workbook
from xml.dom import minidom
from functions import get_waypoint, get_route, get_route_point_order
from objects import *

wb = load_workbook('static/waypoints.xlsx')
waypoint_table = wb['waypoint-table']

all_waypoints = []

for row in waypoint_table:
    # parsing
    name = row[0].value
    identifier = row[1].value
    waypoint_type = row[2].value
    country_code = row[3].value
    lat = row[4].value
    lon = row[5].value
    comment = row[6].value

    # creating object
    waypoint: Waypoint = Waypoint(name=name, identifier=identifier, waypoint_type=waypoint_type,
                                  country_code=country_code,
                                  lat=lat, lon=lon)

    # adding to list
    if identifier != "identifier":
        all_waypoints.append(waypoint)

wb2 = load_workbook('input/flight_plans.xlsx')
info_table = wb2['info']
route_points_table = wb2['routes']

all_routes = []

for row in info_table:
    # parsing
    flight_plan_index = row[0].value
    route_name = row[1].value
    route_description = row[2].value

    # creating object
    route: Route = Route(route_name=route_name, flight_plan_index=flight_plan_index,
                         route_description=route_description)

    # adding to list
    if flight_plan_index != "flight-plan-index":
        all_routes.append(route)

for row in route_points_table:
    # parsing
    flight_plan_index = row[0].value
    identifier = row[1].value
    order = row[2].value

    if identifier == "identifier":
        continue

    # fetching waypoint by identifier
    waypoint = get_waypoint(identifier=identifier, all_waypoint=all_waypoints)
    if not waypoint:
        print(f"waypoint {identifier} doesn\'t exist!")
        quit()

    # fetching route by flight_plan_index
    route = get_route(flight_plan_index=flight_plan_index, all_routes=all_routes)
    if not route:
        print(f"route {flight_plan_index} doesn\'t exist!")
        quit()

    # creating object
    route_point: RoutePoint = RoutePoint(waypoint=waypoint, order=order)

    route.route_points.append(route_point)

# sort route points by order
for route in all_routes:
    route.route_points.sort(key=get_route_point_order)

# # print test
# for route in all_routes:
#     print(route.__dict__)
#     for route_point in route.route_points:
#         print(route_point.__dict__)


for fpl in all_routes:
    root = minidom.Document()

    flight_plan = root.createElement('flight-plan')
    flight_plan.setAttribute('xmlns', 'http://www8.garmin.com/xmlschemas/FlightPlan/v1')
    root.appendChild(flight_plan)

    # >created
    created = root.createElement('created')
    created.appendChild(root.createTextNode(fpl.created))
    flight_plan.appendChild(created)

    # >waypoint-table
    waypoint_table = root.createElement('waypoint-table')
    flight_plan.appendChild(waypoint_table)

    for route_point in fpl.route_points:
        # >>waypoint
        waypoint_obj = route_point.waypoint
        waypoint = root.createElement('waypoint')
        waypoint_table.appendChild(waypoint)

        # >>>identifier
        identifier = root.createElement('identifier')
        identifier.appendChild(root.createTextNode(waypoint_obj.identifier))
        waypoint.appendChild(identifier)

        # >>>type
        type = root.createElement('type')
        type.appendChild(root.createTextNode(waypoint_obj.type))
        waypoint.appendChild(type)

        # >>>country-code
        country_code = root.createElement('country-code')
        country_code.appendChild(root.createTextNode(waypoint_obj.country_code))
        waypoint.appendChild(country_code)

        # >>>lat
        lat = root.createElement('lat')
        lat.appendChild(root.createTextNode(str(waypoint_obj.lat)))
        waypoint.appendChild(lat)

        # >>>lon
        lon = root.createElement('lon')
        lon.appendChild(root.createTextNode(str(waypoint_obj.lon)))
        waypoint.appendChild(lon)

        # >>>comment
        comment = root.createElement('comment')
        comment.appendChild(root.createTextNode(waypoint_obj.comment))
        waypoint.appendChild(comment)

        if waypoint_obj.elevation != "":
            # elevation
            elevation = root.createElement('elevation')
            elevation.appendChild(root.createTextNode(waypoint_obj.elevation))
            waypoint.appendChild(elevation)

    # route
    route = root.createElement('route')
    flight_plan.appendChild(route)

    # >route-name
    route_name = root.createElement('route-name')
    route_name.appendChild(root.createTextNode(fpl.route_name))
    route.appendChild(route_name)

    # >route-description
    route_description = root.createElement('route-description')
    route_description.appendChild(root.createTextNode(fpl.route_description))
    route.appendChild(route_description)

    # flight-plan-index
    flight_plan_index = root.createElement('flight-plan-index')
    flight_plan_index.appendChild(root.createTextNode(str(fpl.flight_plan_index)))
    route.appendChild(flight_plan_index)

    for route_point in fpl.route_points:
        waypoint_obj = route_point.waypoint
        # >route-point
        route_point = root.createElement('route-point')
        route.appendChild(route_point)

        # >>waypoint-identifier
        waypoint_identifier = root.createElement('waypoint-identifier')
        waypoint_identifier.appendChild(root.createTextNode(waypoint_obj.identifier))
        route_point.appendChild(waypoint_identifier)

        # >>waypoint-type
        waypoint_type = root.createElement('waypoint-type')
        waypoint_type.appendChild(root.createTextNode(waypoint_obj.type))
        route_point.appendChild(waypoint_type)

        # >>waypoint-country-code
        waypoint_country_code = root.createElement('waypoint-country-code')
        waypoint_country_code.appendChild(root.createTextNode(waypoint_obj.country_code))
        route_point.appendChild(waypoint_country_code)

    xml_str = root.toprettyxml(indent="\t")

    save_path_file = f"output/{fpl.flight_plan_index}-{fpl.route_name}.fpl"

    with open(save_path_file, "w") as f:
        f.write(xml_str)

print("Finish Creating Garmin Flight Plans!")
