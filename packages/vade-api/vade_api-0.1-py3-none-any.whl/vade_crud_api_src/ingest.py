from vade_api_src.vade_enums import *
from vade_api_src.camera_structs import VadeCamera
import time
import requests


class Ingest:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key

    def ingest_post_camera(self, camera: VadeCamera, image_bytes: bytearray):
        url = "https://ingest.{}.inf.vadenet.org/v1/upload".format(self.production_level.value)
        header = {"apiKey": self.api_key, "User-Agent": camera.imei}
        time_taken = int(time.time())
        payload = {"apiKey": self.api_key, "timeTaken": time_taken, "cameraID": camera.uuid}
        files = [('file', image_bytes)]
        try:
            req = requests.post(url, headers=header, data=payload, files=files)
            if req.status_code == 200:
                print("successfully uploaded image for camera: {}".format(camera.uuid))
                return True
            else:
                print("failed to upload camera {}: {}".format(camera.uuid, req.text))
                return False
        except Exception as e:
            print("failed to upload image: {}".format(str(e)))

