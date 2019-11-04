from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
import datetime
from sqlalchemy.orm import relationship, backref
from database import Base

class Parameter(Base):
    """
        Hold a single parameter and its information

        :param str name: name of parameter
        :param datetime date: date related to parameter
        :param datetime from_date: parameter valid from datetime
        :param datetime to_date: parameter valid till datetime
        :param float concentration: concentration value of parameter
        :param str unit: unit of parameter
        :param str remark: remark note
    """
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True)
    param_list_id = Column('param_list_id', Integer(), ForeignKey('param_list.id'))
    name = Column(String(20))
    date = Column(DateTime())
    from_date = Column(DateTime())
    to_date = Column(DateTime())
    concentration = Column(Float(), default=-1)
    unit = Column(String(15), default='')
    avg_concentration = Column(Float(), default=-1)
    remark = Column(String(10), default='')

    @property
    def value(self):
        return f'{self.concentration} {self.unit}'

    def __repr__(self):
        return f'<Parameter {self.name} {self.value} {self.date}>'

class ParameterList(Base):
    """
        Holds a list of parameters

        :param datetime create_date: when the parameter list was created
        :param datetime parameter_date:  date related to the parameters
        :param list<Parameter> parmaters: list of parameters
    """
    __tablename__ = 'param_list'
    id = Column(Integer, primary_key=True)
    station_rel_id = Column('station_rel_id', Integer(), ForeignKey('stations.id'))
    create_date = Column(DateTime(), default=datetime.datetime.utcnow())
    parameter_date = Column(DateTime())
    parameters = relationship('Parameter')

    @property
    def serialize(self):
        return {
            'date': str(self.parameter_date),
            'parameters': [
                {
                    'name': param.name,
                    'concentration': param.concentration,
                    'unit': param.unit,
                    'date': str(param.date),
                    'avg_concentration': param.avg_concentration,
                    'value': param.value
                }
                    for param in self.parameters
                ]
        }

    def get_param(self, param_name):
        """
            Find param_name in parameters or return None

            :return param models.Parameter
        """
        return next(filter(self.parameters, lambda param: param.name == param_name), None)

    def __repr__(self):
        return f'<ParameterList created: {self.create_date} parameters: {self.parameter_date} {len(self.parameters)}>'

class IPAddress(Base):
    """
    Store an IP Address.
    """
    __tablename__ = 'ipaddress'
    id = Column(Integer, primary_key=True)
    station_rel_id = Column('station_rel_id', Integer(), ForeignKey('stations.id'))
    value = Column(String(25))

    def __repr__(self):
        return f'<IPAddress {self.value}>'

class Station(Base):
    """
    Store a station and its parameters.

    :param str station_id: site id, used for referring to the station
    :param list<IPAddress> ip_address: list of ip addresses
    :param str station_name: name of station
    :param str address: address of station
    :param datetime time_stamp: last timestamp when data was fetched
    :param str status: last status of station
    :param str latitude: latitude of station
    :param str longitude: longitude of station
    :param list<ParamterList> parameters: list of parameters via parameterlist
    """
    __tablename__ = 'stations'
    id = Column(Integer(), primary_key=True)
    station_id = Column(String(50), unique=True, default='site_-1')
    ip_address = relationship('IPAddress')
    station_name = Column(String(50), default='N/A')
    address = Column(String(150), default='N/A')
    time_stamp = Column(DateTime())
    status = Column(String(15))
    latitude = Column(String(20))
    longitude = Column(String(20))
    parameters = relationship('ParameterList', backref=backref('station'))

    @property
    def sorted_parameters(self):
        """
            List of parameters sorted by date.

            :return sorted_params list[models.ParameterList]
        """
        return sorted(self.parameters, key=lambda k: k.parameter_date, reverse=True)

    def __repr__(self):
        return f'<Station {self.station_id} {self.station_name}>'

DEFAULT_NOTIF_TIME = datetime.time(hour=9)

class Subscriber(Base):
    """
    Store subscription info: endpoint, key info, user email, station id, notification time

    :param str station_id: station_id to notify
    :param str email: user email.
    :param str endpoint: WebPush endpoint.
    :param str dh_param: WebPush ECDH parameter.
    :param str auth: WebPush Auth key.
    :param datetime notify_time: Notify user at this time daily.
    """
    __tablename__ = 'subscriptions'
    id = Column(Integer(), primary_key=True)
    station_id = Column(String(20))
    email = Column(String(150), unique=True)
    endpoint = Column(String(256), nullable=False)
    dh_param = Column(String(256), nullable=False)
    auth = Column(String(256), nullable=False)
    notify_time = Column(DateTime(), default=DEFAULT_NOTIF_TIME)
    job_set = Column(Boolean(), default=False)
    add_time = Column(DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Subscriber {self.email} {self.station_id}>'

    @property
    def subscription_info(self):
        return {
            'endpoint': self.endpoint,
            'keys': {
                'p256dh': self.dh_param,
                'auth': self.auth
            }
        }

    def get_station(self, *args, **kwargs):
        return Station.query.filter_by(station_id=self.station_id).first()

    def notification_data(self, param=['PM25', 'PM10']):
        """
            Generate notification dict for the subscriber. 
        """
        
        station = self.get_station()
        latest_params = station.sorted_parameters[0]

        # params_list = []
        # for param_name in param:
        #     param_data = latest_params.get_param(param_name)
        #     if param_data is not None:
        #         params_list.append(param_data)
            
        title_string = f'{station.station_name}\n'
        body_string = f'Date: {station.time_stamp}\n'
        body_string += ''.join(
            [ 
                f'{param_val.name} | {param_val.value}\n'
                for param_val in latest_params.parameters
            ]
        )
            
        notification = {
            'title': title_string,
            'body': body_string
        }

        return notification