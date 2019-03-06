"""
    CAAQMS API

    Access the CAAQMS API via Python.
"""
import time
import datetime
import base64
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Supress InsecureRequestWarning

DATETIME_STRING_FORMAT = '%d %b %Y, %H:%M' # 05 Mar 2019, 23:15
string_to_datetime = (lambda time_string: datetime.datetime.strptime(time_string, DATETIME_STRING_FORMAT))
datetime_to_string = (lambda timestamp: timestamp.strftime(DATETIME_STRING_FORMAT))

class PollutionAPI(object):
    """
        Scrape and store API Response from CPCB All India CAAQMS Portal.
        URL: https://app.cpcbccr.com
        URI: /caaqms/caaqms_landing_map_all

        Response
        ----
            Content-Type: json

            JSON Structure

            /caaqms/caaqms_landing_map_all
            {
                "map": {
                    "timestamp": <str:"05-03-2019 22:25:49" data timestamp (app format)>,
                    "station_list": [<station>]
                }
            }
            <station>
            {
                "ip_address": [<str:list of ip addresses],
                "station_id": <str:station_id(?)>,
                "aqi_info": {
                    "aqi_status": <str:"NA"(?)>
                },
                "station_type": <str:"CAAQMS"(?)>,
                "data_format": <str:"CSV"(?)>,
                "time_stamp": <str: ISO Format Time">,
                "vendor": <str:""(?)>,
                "Ambient": {
                    "AAQMS": {
                        "validation_status": <str:"Success"(?)>,
                        "parameter_map": [<parameter_map>]
                    }
                },
                "parameter_latest_update_date": <str:"2018-06-28 04:45:00" paramter update timestamp (app format)>,
                "status": <str:"Live" status of sensor>,
                "station_name": <str: "DTU, Delhi - CPCB">,
                "latitude": <str:latitude>,
                "longitude": <str:longitude>
            }
            <parameter_map>
            {
                "parameter_name": <str: "WS" parameter name from <parameters> >,
                "last_updated": <str: "2019-03-05 22:00:00" app format timetamp string>,
                "data_quality": <str: "U"(?)>,
                "remark": <str: "0" (?)>,
                "value": <str: "0.72">
            }
            <parameters>
            WS
            RF
            PM25
            SR
            RH
            Temp
            MP_Xylene
            Oxylene
            Ethyle
            Toulene (Toluene)
            Benzene
            PM10
            SO2
            Ozone
            CO
            NH3
            NOX
            WD
            NO2
            NO

            /caaqms/caaqms_viewdata_v2
            {
                'siteInfo': {
                    'photo': <str: image link (usually not there)>,
                    'siteName': <str: name of site>,
                    'address': <str: address of site>,
                    'lastUpdateddatetime': <str: timestamp of last update>,
                    'siteId': <str: station id>,
                    "city": <str: "Kaithal">,
                    "state":  <str: "Haryana">,
                    "stationType": <str: "CAAQMS">,
                    "stationStatus": <str: "Live">,
                    "parameters": <str: 21, no of parameters>,
                    "dataAvailPerc": <str: "84.13 % (?)>"
                }
                'tableData': {
                    'headers': [{<headers for columns in next key}],
                    'bodyContent': [list of <parameter> >]
                }
            }
            <parameter>
            {
                "parameters": <str: "PM2.5" pollutant>,
                "date": <str: "06 Mar 2019">,
                "time": <str: "00:15">,
                "fromDate": <str: "06 Mar 2019 00:15">,
                "toDate": <str: "06 Mar 2019 00:30">,
                "concentration": <decimal: 39.01>,
                "unit": <str: "ug/m3">,
                "Concentration_24Hr": <decimal: 55.39, avg conc over 24 Hr>,
                "remark": <str: "" (?)>
            },

    """
    URL = 'https://app.cpcbccr.com'
    
    ALL_STATIONS_URI = {
        'URI': '/caaqms/caaqms_landing_map_all',
        'POST_DATA': 'eyJyZWdpb24iOiJsYW5kaW5nX2Rhc2hib2FyZCJ9' 
    }
    
    STATION_VIEW_DATA_URI = {
        'URI': '/caaqms/caaqms_viewdata_v2',
        'POST_DATA': (lambda site_id: base64.b64encode(f'''{{"site_id":"{site_id}","user_id":"user_211","user_name":"KSPCB","user_role":"Admin","org":["KSPCB"]}}'''.encode()).decode())
    }

    STATION_DELTA_DATA_URI = {
        'URI': '/caaqms/caaqms_load_delta_v2',
        'POST_DATA': (lambda site_id, delta, time_stamp: base64.b64encode(f'''{{"delta":"{delta}","time_stamp":"{time_stamp}","site_id":"{site_id}"}}'''.encode()).decode())
    }


    def __init__(self, *args, **kwargs):
        self.stations = {}

    def _get(self, URI, *args, **kwargs):
        return requests.get(self.URL+URI, verify=False, *args, **kwargs)

    def _post(self, URI, *args, **kwargs):
        return requests.post(self.URL+URI, verify=False, *args, **kwargs)

    def get_all_stations(self, *args, **kwargs):
        """
            get data for all stations

            return dict station: `/caaqms/caaqms_landing_map_all` JSON Response
        """
        payload = self.ALL_STATIONS_URI['POST_DATA']
        request = self._post(self.ALL_STATIONS_URI['URI'], data=payload)
        json_data = request.json()
        stations = json_data['map']['station_list']

        self.stations = stations
        
        return stations

    def get_station_data(self, station, *args, **kwargs):
        """
        get station_data for a `site_id`
        
        return dict site_data: {
            'site_data': <site information>,
            'parameters': <parameters>
        }
        """
        payload = self.STATION_VIEW_DATA_URI['POST_DATA'](site_id)
        request = self._post(self.STATION_VIEW_DATA_URI['URI'], data=payload)

        json_data = request.json()

        site_info_key = 'siteInfo'
        table_data_key = 'tableData'
        body_content_key = 'bodyContent'    

        site_data = {
            'site_data': json_data[site_info_key],
            'parameters': json_data[table_data_key][body_content_key]
        }

        return site_data
    
    # def get_station_delta(self, site_id, delta, time_stamp, *args, **kwargs):
    #     """
    #         get historical data based on delta.
    #     """
    #     payload = self.STATION_VIEW_DATA_URI['POST_DATA'](site_id, delta, time_stamp)
    #     request = self._post(self.STATION_VIEW_DATA_URI['URI'], data=payload)

    #     json_data = request.json()

    #     site_info_key = 'siteInfo'
    #     table_data_key = 'tableData'
    #     body_content_key = 'bodyContent'    

    #     site_data = {
    #         'site_data': json_data[site_info_key],
    #         'parameters': json_data[table_data_key][body_content_key]
    #     }

    #     return site_data

class Parameter(object):
    """
        Container for parameter
        Data:
            parameters 
            date
            time
            from_date
            to_date
            concentration
            unit
            Concentration_24Hr
            remark 
    """
    def __init__(self, *args, **kwargs):
        self.parameter = kwargs.get('parameters')
        
        try:
            """ Transform date """
            date = kwargs.get('date')
            time = kwargs.get('time')
            datetime_string = f'{date}, {time}'
            self.date = string_to_datetime(datetime_string)
        except:
            pass
            
        try:
            self.from_date = string_to_datetime(datetime_string)
            self.to_date = string_to_datetime(datetime_to_string)
        except:
            pass

        self.concentration = kwargs.get('concentration', -1)
        self.unit = kwargs.get('unit', '')
        self.avg_concentration = kwargs.get('Concentration_24Hr', -1)
        self.remark = kwargs.get('remark', '')

    @property
    def value(self):
        return f'{self.parameter} {self.unit}'

    def __str__(self, *args, **kwargs):
        return f"<Parameter {self.parameter} {self.concentration}{self.unit}>"


class Station(object):
    """
        Container for stations
        Data:
            station_name,
            station_id,
            address,
            time_stamp,
            parameters,
            status,
            latitude,
            longitude

        Accepts PollutionAPI.get_station_data response.
    """
    def __init__(self, *args, **kwargs):
        self.station_name = kwargs.get('station_name', 'N/A')
        self.station_id = kwargs.get('station_id', -1)
        self.address = kwargs.get('address', 'N/A')
        self.time_stamp = kwargs.get('time_stamp', datetime.datetime.utcnow())
        
        parameters_list = kwargs.get('parameters', [])
        self.parameters = [Parameter(**parameter_dict) for parameter_dict in parameters_list ]

        self.status = kwargs.get('status', 'N/A')
        
        self.latitude = kwargs.get('latitude', '')
        self.longitude = kwargs.get('longitude', '')

    def __str__(self, *args, **kwargs):
        return f"<Station {self.station_name} {self.station_id}>"

def get_station(json_data, *args, **kwargs):
    """
        Transform get_station_data responses.
    """
    station_data = {
        'station_id': json_data['site_data']['siteId'],
        'address': json_data['site_data']['address'],
        'time_stamp': json_data['site_data']['lastUpdateddatetime'],
        'status': json_data['site_data']['stationStatus'],
        'station_name': json_data['site_data']['siteName'],
        'parameters': json_data['parameters']
    }

    station = Station(**station_data)
    return station
    

if __name__ == '__main__':
    api = PollutionAPI()
    stations = api.get_all_stations()
    station_data_list = []

    start = time.time()
    for station in stations:
        print()
        print(f"Collecting data for {station['station_id']}")
        start = time.time()
        data = api.get_station_data(station['station_id'])
        station_data_list.append(data)

        station_instance = get_station(data)
        print(station_instance)
        print([str(param) for param in station_instance.parameters])

        end = time.time() - start
        print(f"Time taken: {end}")

    end = time.time() - start
    print(f"Total Time Taken: {end}")    
    
    
    first_site_id = stations[0]['station_id']
    print(first_site_id)
    
    first_station_data = api.get_station_data(first_site_id)
    print(first_station_data)

    for pollutant in first_station_data['parameters']:
        print(f'''---- {pollutant['parameters']} ----''')
        print(f'''     {pollutant['date']}           ''')
        print(f'''Concentration: {pollutant['concentration']}{pollutant['unit']}''')
        print('''-----------------------------------''')