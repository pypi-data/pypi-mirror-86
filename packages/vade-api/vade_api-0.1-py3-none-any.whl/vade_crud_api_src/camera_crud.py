from vade_api_src.vade_enums import *
from vade_api_src.camera_structs import *


class CameraCrud:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key

