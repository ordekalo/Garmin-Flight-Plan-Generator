from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import List


class WaypointType(Enum):
    USER_WAYPOINT = "USER WAYPOINT"
    AIRPORT = "AIRPORT"
    VOR = "VOR"


@dataclass
class Waypoint:
    identifier: str
    type: WaypointType
    country_code: str
    lat: float
    lon: float
    comment: str
    elevation: float

    def __init__(self, identifier: str, lat: float, lon: float,
                 waypoint_type: WaypointType = WaypointType.USER_WAYPOINT,
                 country_code: str = "IL"):
        self.identifier = identifier
        self.type = waypoint_type
        self.country_code = "" if country_code == "NULL" else "IL"
        self.lat = lat
        self.lon = lon
        self.comment = ""
        self.elevation = 0 if self.type == WaypointType.AIRPORT else ""


@dataclass
class RoutePoint:
    waypoint: Waypoint
    order: int

    def __init__(self, waypoint: Waypoint, order: int = 0):
        self.waypoint = waypoint
        self.order = order


@dataclass
class Route:
    flight_plan_index: int
    route_name: str
    route_description: str
    created: str
    route_points: List[RoutePoint]

    def __init__(self, route_name: str, flight_plan_index: int = 1, route_description: str = ""):
        self.flight_plan_index = flight_plan_index
        self.route_name = route_name
        self.route_description = route_description
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.route_points = []
