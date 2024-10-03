from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class WaypointType(Enum):
    USER_WAYPOINT = "USER WAYPOINT"
    AIRPORT = "AIRPORT"
    VOR = "VOR"


@dataclass
class Waypoint:
    name: str
    identifier: str
    type: WaypointType
    country_code: str
    lat: float
    lon: float
    comment: str = ""
    elevation: float = field(default=0, init=False)

    def __init__(self, name: str, identifier: str, lat: float, lon: float,
                 waypoint_type: WaypointType = WaypointType.USER_WAYPOINT,
                 country_code: str = ""):
        self.name = name.upper()
        self.identifier = identifier.upper()
        self.type = waypoint_type
        # Assign "IL" if country_code is missing or NULL, otherwise use given value
        self.country_code = "IL" if country_code in ("NULL", "") else country_code
        self.lat = lat
        self.lon = lon
        # Airport-specific logic for elevation
        if self.type == WaypointType.AIRPORT:
            self.elevation = 0  # Use a default elevation for airports
        else:
            self.elevation = ""  # For non-airport waypoints, no elevation


@dataclass
class RoutePoint:
    waypoint: Waypoint
    order: int = 0


@dataclass
class Route:
    flight_plan_index: int
    route_name: str
    route_description: str = ""
    created: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
    route_points: List[RoutePoint] = field(default_factory=list)

    def __init__(self, route_name: str, flight_plan_index: int = 1, route_description: str = ""):
        self.flight_plan_index = flight_plan_index
        self.route_name = route_name.upper()
        self.route_description = route_description
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.route_points = []
