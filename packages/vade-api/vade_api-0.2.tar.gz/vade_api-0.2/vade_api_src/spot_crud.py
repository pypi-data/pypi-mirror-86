from vade_api_src.vade_enums import *
from vade_api_src.spot_structs import *
import requests
import json

class SpotCrud:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key

    def get_spot_page(self, page_size: int = 50, page_number: int = 1):
        url = "https://crud.{}.inf.vadenet.org/v1/spots?pageSize={}&pageNumber={}".format(self.production_level.value, page_size, page_number)
        header = {"apiKey": self.api_key}
        ret_spots = []
        req = requests.get(url, headers=header)
        try:
            resp = json.loads(req.text)
            bad_spots = 0
            for spot in resp["spots"]:
                new_spot = VadeSpotCrud.from_json(spot)
                if new_spot:
                    ret_spots.append(new_spot)
                else:
                    bad_spots += 1
            print("successfully got {} spot, and {} bad spots".format(len(ret_spots), bad_spots))
            return ret_spots
        except Exception as e:
            print("failed to get spot page: {}".format(str(e)))
