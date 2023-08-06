from vade_api_src.vade_enums import *
from vade_api_src.camera_structs import GeoPoint
from datetime import datetime
from dateutil import parser


class VadeSpotPoint:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y


class VadeSpotBounds:
    points: [int] = []

    @staticmethod
    def from_json(j: dict):
        try:
            new_bounds = VadeSpotBounds()
            if isinstance(j, dict):
                for bound in j["bounds"]:
                    new_bounds.points.append(VadeSpotPoint(x=bound[0], y=bound[1]))
                return new_bounds
            else:
                for bound in j:
                    new_bounds.points.append(VadeSpotPoint(x=bound[0], y=bound[1]))
                return new_bounds
        except:
            return None


class VadeSpotRealtime:
    uuid: str = None
    name: str = None
    mdid: str = None
    location: GeoPoint = None
    occupancy_threshold: float = None
    raw_score: float = None
    last_updated: datetime
    occupied: bool = None

    @staticmethod
    def from_json(j: dict):
        try:
            new_spot = VadeSpotRealtime()
            new_spot.uuid = j["uuid"]
            new_spot.name = j["name"]
            new_spot.mdid = j.get("mdid", None)
            new_spot.location = GeoPoint.from_json(j)
            if not new_spot.location:
                print("failed to create spot from json: spot has no location")
                print("original data: {}".format(j))
                return None
            new_spot.occupancy_threshold = j.get("occupancyThreshold", None)
            new_spot.raw_score = j.get("rawScore", 0.0)
            updated_str = j.get("lastUpdated", None)
            if updated_str:
                new_spot.last_updated = parser.parse(updated_str)
                new_spot.occupied = j["occupied"]
            return new_spot
        except Exception as e:
            print("failed to create spot from json: {}".format(str(e)))
            print("original data: {}".format(j))
            return None


class VadeSpotCrud(VadeSpotRealtime):

    zone: str = None
    bounds: VadeSpotBounds = []
    primary_camera: str = None
    type: VadeSpotType = VadeSpotType.STANDARD
    secondary_cameras: [str] = None

    @staticmethod
    def from_json(j: dict):
        try:
            new_spot = VadeSpotRealtime.from_json(j=j)
            new_spot.type = VadeSpotType.from_str(j.get("type", "standard"))
            new_spot.zone = j.get("zone", None)
            new_spot.bounds = VadeSpotBounds.from_json(j["bounds"])
            if not new_spot.bounds:
                return None
            new_spot.primary_camera = j["primaryCamera"]
            new_spot.secondary_cameras = j.get("secondaryCameras", None)
            new_spot.occupancy_threshold = j.get("occupancyThreshold", None)
            return new_spot
        except Exception as e:
            print("failed to create spot from json: {}".format(str(e)))
            return None


