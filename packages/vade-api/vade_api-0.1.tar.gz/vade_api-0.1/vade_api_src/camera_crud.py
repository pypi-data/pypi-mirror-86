from vade_api_src.vade_enums import *
from vade_api_src.camera_structs import *
import requests

class CameraCrud:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key

    def create_camera(self, camera: VadeCamera):
        url = "https://crud.{}.inf.vadenet.org/v1/cameras".format(self.production_level.value)
        data = camera.database_representation()
        header = {"apiKey": self.api_key}
        resp = requests.post(url, json=data, headers=header)
        try:
            ret_cam = json.loads(resp.text)["camera"]
            camera.uuid = ret_cam["uuid"]
            camera.api_key = ret_cam["apiKey"]
        except:
            print(resp.text)
        if (resp.status_code == 200) or (resp.status_code == 201):
            return True
        else:
            return False

    def does_camera_exist(self, camera: VadeCamera, mutate: bool=True):
        if camera.uuid and camera.api_key:
            return True
        url = "https://crud.{}.inf.vadenet.org/v1/cameras/imei/{}".format(self.production_level.value, camera.imei)
        header = {"apiKey": self.api_key}
        resp = requests.get(url, headers=header)
        try:
            ret_cam = json.loads(resp.text)["camera"]
            if mutate:
                camera.uuid = ret_cam["uuid"]
                camera.api_key = ret_cam["apiKey"]
            return True
        except:
            return False

