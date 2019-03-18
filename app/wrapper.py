"""
    Wrapper for PollutionAPI
"""
import models
import datetime
from database import init_db, db_session
from api import PollutionAPI, Station, Parameter, get_station, string_to_datetime

class PollutionAPIWrapper():
    """
        Wrapper for PollutionAPI
        and the Database updating
        Stations.
    """

    def __init__(self, *args, **kwargs):
        self.api = PollutionAPI()

    def populate_stations(self, *args, **kwargs):
        """
            Initial Data
            Populate without parameters
            via api.get_all_stations
        """  
        stations = self.api.get_all_stations()
        for station in stations:
            station_data = {
                'station_id': station['station_id'],
                'ip_address': [models.IPAddress(value=ip) for ip in station['ip_address']],
                'station_name': station['station_name'],
                'status': station['status'],
                'latitude': station['latitude'],
                'longitude': station['longitude'],
                'time_stamp': string_to_datetime(station['time_stamp']),
            }
            station_db_instance = models.Station(**station_data)
            db_session.add(station_db_instance)
        
        db_session.commit()

    def get_station(self, *args, **kwargs):
        """
            Get station data via
            api.get_station_data
            and update database.

            kwargs:
                kwargs for filter_by
                filter by site_id

                - Check if the station is to be updated
                  via kwargs.get('update')
                - Try getting a station from the database
                - Add data which can only be found in api.get_station_data
                  if its not there
                - Check if data is older than 30 minutes,
                  update if it is.
                - Update station based on UPDATE_STATION
                    - fetch latest station data
                    - update address, time_stamp, status
                    - add to parameter_list
                    - commit to database
                - return to station
        """
        UPDATE_STATION = False

        # Explicity update station
        update = kwargs.get('update', False)
        if update:
            UPDATE_STATION = True
            kwargs.pop('update')

        # Get station from database using filter_by
        station = models.Station.query.filter_by(**kwargs).first()
        
        # Get station_id
        station_id = station.station_id

        # Verify if the address is not N/A.
        if station.address == 'N/A':
            UPDATE_STATION = True

        station_timestamp_30min_delta = station.time_stamp - datetime.timedelta(minutes=30) 
        current_time_delta = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)

        if current_time_delta > station_timestamp_30min_delta :
            UPDATE_STATION = True

        # Fetch New Data
        if UPDATE_STATION:
            station_data = self.api.get_station_data(station_id)
            station_instance = get_station(station_data)
        
            # Update Station Info
            station.address = station_instance.address
            station.time_stamp = station_instance.time_stamp
            station.status = station_instance.status

            # Create ParameterList
            parameter_model_list = [models.Parameter(**parameter.get_dict()) for parameter in station_instance.parameters]
            parameter_list = models.ParameterList(parameters=parameter_model_list, parameter_date=station_instance.parameters[0].date)
            
            station.parameters.append(parameter_list)

            # Commit to database
            db_session.commit()

        return station