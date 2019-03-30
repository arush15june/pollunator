import React, { Component } from 'react'
import Form from 'react-bootstrap/Form'

class StationList extends Component {

  stationsRenderList() {
    let station_list = this.props.stationList   
    let render_list = station_list.map( station => {
      return <option value={station.station_id}>{station.station_name}</option>
    })
    return render_list
  }

  render() {
    let station_options = this.stationsRenderList()
    return (
      <React.Fragment>
        <Form onChange={this.props.selectHandler}>
          <Form.Group controlId='formStationsList'>
            <Form.Label>Stations</Form.Label>
            <Form.Control controlId="station" as='select'>
              {station_options}
            </Form.Control>
          </Form.Group>
        </Form>
      </React.Fragment>
    )
  }
}

export default StationList