"""
        Pollunator
    REST API for getting pollution data from CPCB CAAQMS
    and daily notifications
        - arush15june
"""
from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import dateutil

from wrapper import PollutionAPIWrapper
from database import init_db, db_session

import models
import pusher
import subscriber

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
    serve data for a single station.
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

class PushNotificationResource(Resource):
    """
    Handle new Subscribers for notifications.
    """
    root_post_parser = reqparse.RequestParser()
    root_post_parser.add_argument('email', location='json')
    root_post_parser.add_argument('notify_time', location='json')
    root_post_parser.add_argument('subscription_info', type=dict, location='json')
    

    subscription_info_parser = reqparse.RequestParser()
    subscription_info_parser.add_argument('endpoint', location=('subscription_info',))
    subscription_info_parser.add_argument('keys', type='dict', location=('subscription_info',))

    key_arg_parser = reqparse.RequestParser()
    key_arg_parser.add_argument('p256dh', location=('keys',))
    key_arg_parser.add_argument('auth', location=('keys',))

    def post(self):
        """
            receive subscription parameters and other data,
            add to database,
            setup background job to send notifications
            return response or error
        """
        root_args = root_post_parser.parse_args() 
        subscription_args = subscription_info_parser.parse_args(req=root_args)
        key_args = key_arg_parser.parse_args(req=subscription_args)

        email = root_args['email']

        sub = subscriber.get_subscriber(email=email)
        if not sub[0]:
            return {
                'error': 'Subscription already exists for this email'
            }   

        notify_time = root_args['notify_time']

        endpoint = subscription_args['endpoint']
        
        p256dh = key_args['p256dh']
        auth = key_args['auth']
        
        data = {
            'email': email,
            'notify_time': notify_time_str,
            'endpoint': endpoint,
            'p256dh': p256dh,
            'auth': auth
        }

        subscriber.add_subscriber(**data)

        return {
            'email': subscriber.email,
            'notify_time': subscriber.notify_time.strftime('%H:%M')
        }
        
api.add_resource(AllStationsResource, '/api/stations')
api.add_resource(StationResource, '/api/stations/<string:station_id>' )
api.add_resource(PushNotificationResource, '/api/subscribe')

@app.route('/publickey', methods=['GET'])
def vapid_public_key():
    return pusher.Pusher.APP_SERVER_KEY

if __name__ == "__main__":
    init_db()
    if models.Station.query.count() == 0:
        print('** Populating Stations')
        api_handler.populate_stations()
    app.run(debug=True)