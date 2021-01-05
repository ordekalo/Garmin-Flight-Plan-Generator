from typing import Optional

from objects import *


def get_waypoint(identifier: str, all_waypoint: List[Waypoint]) -> Optional[Waypoint]:
    for waypoint in all_waypoint:
        if waypoint.identifier == identifier:
            return waypoint
    return None


def get_route(flight_plan_index: str, all_routes: List[Route]) -> Optional[Route]:
    for route in all_routes:
        if route.flight_plan_index == flight_plan_index:
            return route
    return None


def get_route_point_order(route_point: RoutePoint):
    return route_point.order
