from vade_api_src.vade_enums import *


class ZoneCrud:

    api_key: str
    production_level: ProductionLevel

    def __init__(self, api_key: str, production_level: ProductionLevel):
        self.production_level = production_level
        self.api_key = api_key
