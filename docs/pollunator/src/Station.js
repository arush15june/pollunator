import React, { Component } from 'react';
import Card from 'react-bootstrap/Card'
import CardColumns from 'react-bootstrap/CardColumns'

import Subscriber from './Subscriber'
import Parameter from './Parameter'

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

class Station extends Component { 
  
    _parameter_list() {
      const parameters = this.props.stationData.parameters.parameters
      const param_list = parameters.map(param => {
        return <Parameter parameterData={param} />
      })

      return param_list      
    }
  
    render() {
      let station_data = this.props.stationData

      return (
        <React.Fragment>
          { !isEmpty(station_data) ? (                         
            <Card>
              <Card.Header>{station_data.station_name}</Card.Header>
              <Card.Body>
                <Card.Title>{station_data.status}</Card.Title>
                <Card.Text>
                  Latitude: {station_data.latitude} Longitude: {station_data.longitude} Timestamp: {station_data.parameters.date}
                </Card.Text>
                <CardColumns>
                  {this._parameter_list()}
                </CardColumns>
                <Card.Text>
                  <Subscriber station_id={this.props.stationData.station_id} />
                </Card.Text>
                {/* <Button variant="primary">Go somewhere</Button> */}
              </Card.Body>
            </Card>
            ) : (
              <React.Fragment></React.Fragment>
            )
          }
        </React.Fragment>
      )
    }
}

export default Station;