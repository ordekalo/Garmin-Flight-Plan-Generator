from typing import Optional, List
from objects import *


def get_waypoint(identifier: str, all_waypoints: List[Waypoint]) -> Optional[Waypoint]:
    # Using next with a default value of None if not found
    return next((waypoint for waypoint in all_waypoints if waypoint.identifier == identifier), None)


def get_route(flight_plan_index: int, all_routes: List[Route]) -> Optional[Route]:
    # Similar approach using next() for routes
    return next((route for route in all_routes if route.flight_plan_index == flight_plan_index), None)


def get_route_point_order(route_point: RoutePoint) -> int:
    return route_point.order
