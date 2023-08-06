from vade_api_src.camera_crud import *
from vade_api_src.spot_crud import *
from vade_api_src.user_crud import *
from vade_api_src.zone_crud import *
from vade_api_src.ingest import *
import time


class VadeCrudApi:

    crud_key: str
    production_level: ProductionLevel
    camera_crud: CameraCrud
    zone_crud: ZoneCrud
    user_crud: UserCrud
    spot_crud: SpotCrud
    ingest: Ingest

    def __init__(self, crud_key: str, production_level: ProductionLevel):
        self.crud_key = crud_key
        self.production_level = production_level
        self.camera_crud = CameraCrud(crud_key, production_level)
        self.zone_crud = ZoneCrud(crud_key, production_level)
        self.user_crud = UserCrud(crud_key, production_level)
        self.spot_crud = SpotCrud(crud_key, production_level)
        self.ingest = Ingest(crud_key, production_level)