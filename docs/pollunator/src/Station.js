import React, { Component } from 'react';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

class Station extends Component { 
  
    parameterList() {
      const parameters = this.props.stationData.parameters.parameters
      const param_list = parameters.map(param => {
        return <p>{param.name}: <span className='font-weight-bold'>{param.value}</span> {param.date}</p>
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
                <Card.Text>
                  {this.parameterList()}
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