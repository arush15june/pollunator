"""
    Wrapper for PollutionAPI
"""
import models
import datetime
from database import init_db, db_session
from api import PollutionAPI, Station, Parameter, get_station, string_to_datetime

class StationPopulationError(Exception):
    pass

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
        
        # Rollback if commit fails
        try:
            db_session.commit()
        except:
            db_session.rollback()
            raise StationPopulationError()
            
    class StationUpdateError(Exception):
        pass
            
    def get_station(self, *args, **kwargs):
        """
            Get station data via
            api.get_station_data
            and update database.


            kwargs station_id str: station id to get data for.
                kwargs for filter_by
                filter by station_id

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
        
        # Verify if the address is not N/A.
        if station.address == 'N/A':
            UPDATE_STATION = True

        station_timestamp_delta_30min = station.time_stamp + datetime.timedelta(minutes=30) 
        current_time = datetime.datetime.utcnow()

        if current_time > station_timestamp_delta_30min:
            UPDATE_STATION = True

        # Fetch New Data
        if UPDATE_STATION:
            # API Failure, return available station data.
            station_data = self.api.get_station_data(station.station_id)

            station_instance = get_station(station_data)
        
            # Update Station Info
            station.address = station_instance.address
            station.time_stamp = station_instance.time_stamp
            station.status = station_instance.status

            if len(getattr(station_instance, 'parameters', [])) > 0:
                # Create ParameterList
                parameter_model_list = [models.Parameter(**parameter.get_dict()) for parameter in station_instance.parameters]
                parameter_list = models.ParameterList(parameters=parameter_model_list, parameter_date=station_instance.parameters[0].date)

                station.parameters.append(parameter_list)

            # Commit to database, Rollback if commit fails
            try:
                db_session.commit()
            except:
                db_session.rollback()
                raise StationUpdateError()

        return station