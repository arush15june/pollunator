from database import init_db
import models

init_db()

if models.Station.query.count() == 0:
        print('** Populating Stations')
        api_handler.populate_stations()