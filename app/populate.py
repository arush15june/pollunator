from database import init_db
import models
from wrapper import PollutionAPIWrapper

init_db()
api_handler = PollutionAPIWrapper()

if models.Station.query.count() == 0:
        print('** Populating Stations')
        api_handler.populate_stations()