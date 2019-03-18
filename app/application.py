"""
        Pollunator
    REST API for getting pollution data from CPCB CAAQMS
    and daily notifications
        - arush15june
"""
from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS

from wrapper import PollutionAPIWrapper
from database import init_db, db_session
import models

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

api_handler = PollutionAPIWrapper()

class AllStationsResource(Resource):
    """
        Resource to serve all stations
        only metadata without parameters
    """
    def get(self):
        """
            fetch stations,
            serialize,
            return as json
        """
        stations = models.Station.query.all()
        stations_json = [
            {
                'station_id': station.station_id,
                'station_name': station.station_name,
                'status': station.status,
                'latitude': station.latitude,
                'longitude': station.longitude,
                'time_stamp': str(station.time_stamp),
            } for station in stations
        ]
        return stations_json       

class StationResource(Resource):
    """
    get data for a single stations.
    """
    def get(self, station_id):
        """
            Fetch required station via station_id matched by route,
            sort the parameters to get the latest parmeter,
            serialize the station and parameters,
            return json
        """
        station = api_handler.get_station(station_id=station_id)
        parameters = station.parameters
        sorted_params = sorted(parameters, key=lambda k: k.parameter_date, reverse=True)
        latest_param_data = sorted_params[0].serialize

        station_json = {
            'station_id': station.station_id,
            'station_name': station.station_name,
            'status': station.status,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'time_stamp': str(station.time_stamp),
            'parameters': latest_param_data
        }

        return station_json

api.add_resource(AllStationsResource, '/api/stations')
api.add_resource(StationResource, '/api/stations/<string:station_id>' )

if __name__ == "__main__":
    init_db()
    if models.Station.query.count() == 0:
        print('** Populating Stations')
        api_handler.populate_stations()
    app.run(debug=True)