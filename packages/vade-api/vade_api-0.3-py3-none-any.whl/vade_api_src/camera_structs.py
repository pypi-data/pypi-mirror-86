import json
import pytz
from tzwhere import tzwhere
from datetime import datetime, timezone
import os

tzwhere = tzwhere.tzwhere()

class VadeEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json()


class GeoPoint:
    lat: float
    long: float

    def __init__(self, lat, long):
        if isinstance(lat, str):
            self.lat = float(lat)
        if isinstance(long, str):
            self.long = float(long)
        else:
            self.lat = lat
            self.long = long

    @staticmethod
    def from_json(j: dict):
        try:
            new_one = GeoPoint(lat=j["location"]["coordinates"][1], long=j["location"]["coordinates"][0])
            return new_one
        except:
            return None

    @classmethod
    def fromAny(cls, lat, long):
        new_one = GeoPoint(0.0, 0.0)
        try:
            if isinstance(lat, str):
                new_one.lat = float(lat)
            if isinstance(long, str):
                new_one.long = float(long)
            if isinstance(lat, float):
                new_one.lat = lat
            if isinstance(long, float):
                new_one.long = long
            return new_one
        except Exception as e:
            return None

    def toJSON(self):
        return {
            "coordinates": [self.long, self.lat]
        }

class DefaultGeoPoints:
    new_york = GeoPoint(40.701363, -74.015451)
    raleigh = GeoPoint(35.786388, -78.647284)
    marcom_st = GeoPoint(35.778966, -78.686155)
    austin_texas = GeoPoint(30.4036922, -97.8540649)


class VadeCamera:
    uuid: str = None
    imei: str = None
    name: str = None
    api_key: str = None
    geo_point: GeoPoint
    mdid: str = None
    start_time: [int] = [8, 30]
    stop_time: [int] = [20, 30]
    weekdays: [int] = [1, 2, 3, 4, 5, 6, 7]
    time_between_captures = 60

    def database_representation(self) -> dict:
        ret_dict = {
            "imei": self.imei,
            "name": self.name,
            # "mdid": self.mdid,
            "parameters": {
                "timeBetweenCaptures": 60,
                "startTime": self.start_time,
                "stopTime": self.stop_time,
                "weekdays": self.weekdays
            },
            "location": {
                "type": "Point",
                "coordinates": [self.geo_point.long, self.geo_point.lat]
            }
        }
        if self.uuid is not None:
            ret_dict["uuid"] = self.uuid
        if self.api_key is not None:
            ret_dict["apiKey"] = self.api_key
        return ret_dict

    @classmethod
    def from_vade_database_dict(cls, j: dict):
        new_cam = VadeCamera()
        try:
            new_cam.uuid = j["uuid"]
            new_cam.imei = j["imei"]
            new_cam.name = j["name"]
            new_cam.api_key = j["apiKey"]
            new_cam.geo_point = GeoPoint(j["location"]["coordinates"][0], j["location"]["coordinates"][1])
            new_cam.mdid = j.get("mdid", None)
            new_cam.start_time = j["cameraParams"]["startTime"]
            new_cam.stop_time = j["cameraParams"]["stopTime"]
            new_cam.weekdays = j["cameraParams"]["weekdays"]
            new_cam.time_between_captures = j["cameraParams"]["timeBetweenCaptures"]
            return new_cam
        except Exception as e:
            return None

    @staticmethod
    def default_image(as_bytes: bool = True):
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path += "/resources/default_vade_image.jpg"
        byte = open(file_path, "rb")
        if as_bytes:
            return byte
        return None

    @staticmethod
    def default_camera():
        cam_dict = {
            "uuid": "d7da94a9-1b97-47bc-8fd1-eba9e16033b2",
            "imei": "aaaa-aaaa-aaaa-aaaa",
            "name": "test-camera-please-dont-touch",
            "location": {
                "type": "Point",
                "coordinates": [-90.0715, 29.951] #always follows long,lat format
            },
            "cameraParams": {
                "startTime": [8, 30],
                "stopTime": [20, 30],
                "timeBetweenCaptures": 60,
                "weekdays": [1, 2, 3, 4, 5, 6, 7]
            },
            "apiKey": "6e610db5-51aa-4f93-b3f6-4424bfc4bb31",
        }
        return VadeCamera.from_vade_database_dict(cam_dict)


class EasyLinkCamera(VadeCamera):
    access_link: str = None
    city: str = None
    description: str = None
    last_image: bytearray = None

    @staticmethod
    def imei_from_geopoint(point: GeoPoint):
        return "cctv_{}_{}".format(point.lat, point.long)

    def __eq__(self, other):
        is_stance = isinstance(other, self.__class__)
        other_imei = getattr(other, 'imei', None)
        same_imei = (other_imei == self.imei)
        return (is_stance and same_imei)
            # getattr(other, 'age', None) == self.age)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        val = hash(self.imei)
        return hash(self.imei)

    def to_json(self)->dict:
        rep = self.database_representation()
        rep["url"] = self.access_link
        rep["description"] = self.mdid
        return rep

    def is_trafficland(self):
        if not self.access_link:
            return None
        if "trafficland" in self.access_link:
            return True
        return False

    @classmethod
    def from_json(cls, j: dict,):
        try:
            new_cam = EasyLinkCamera()
            new_cam.imei = j["imei"]
            new_cam.name = j["name"]
            new_cam.geo_point = GeoPoint(j["location"]["coordinates"][1], j["location"]["coordinates"][0])
            new_cam.uuid = j["uuid"]
            new_cam.api_key = j["apiKey"]
            new_cam.description = j["description"]
            new_cam.access_link = j["url"]
            return new_cam
        except:
            return None

    @classmethod
    def from_json_with_city(cls, j: dict, city: str, require_vade_db_fields: bool=True):
        try:
            new_cam = EasyLinkCamera()
            if require_vade_db_fields:
                new_cam.api_key = j["apiKey"]
                new_cam.uuid = j["uuid"]
            else:
                try: new_cam.uuid = j["uuid"]
                except: x = 5
                try: new_cam.uuid = j["apiKey"]
                except: x = 5
            new_cam.name = j["name"]
            new_cam.geo_point = GeoPoint(j["location"]["coordinates"][1], j["location"]["coordinates"][0])
            new_cam.city = city
            new_cam.imei = j["imei"]
            new_cam.description = j["description"]
            new_cam.access_link = j["url"]
            return new_cam
        except:
            return None

    def is_in_working_hours(self):
        try:
            # get the time camera is witnessing
            timezone_str = tzwhere.tzNameAt(latitude=self.geo_point.lat, longitude=self.geo_point.long)
            cam_timezone = pytz.timezone(timezone_str)
            utc_dt = datetime.now(timezone.utc)
            curr_camera_time = utc_dt.astimezone(cam_timezone)

            # check if camera time is in its working hours
            if (curr_camera_time.weekday() + 1) not in self.weekdays:
                return False

            camera_start_time = curr_camera_time
            camera_start_time = camera_start_time.replace(hour=self.start_time[0], minute=self.start_time[1])
            camera_end_time = curr_camera_time
            camera_end_time = camera_end_time.replace(hour=self.stop_time[0], minute=self.stop_time[1])
            if camera_start_time <= curr_camera_time <= camera_end_time:
                return True
            else:
                return False

        except Exception as e:
            print("- Failed to get working hours for camera: {} b\c: {}".format(self.uuid, str(e)))
            return True
