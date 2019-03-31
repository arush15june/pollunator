import React, { Component } from 'react';
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import StationList from './StationList'
import Station from './Station'

import MinHeap from './MinHeap'

import { STATIONS_URL } from './API'

class StationsContainer extends Component {
  constructor(props) {
    super(props)
    this.state = {
      stationList: [],
      stationDistanceList: [],
      coords: {},
      selectedStation: {}
    }
  }

  async fetchStationData(station_id) {
    let API_URL = `${STATIONS_URL}/${station_id}`
    let station_data_request = await fetch(API_URL);
    let station_data_json = await station_data_request.json()

    return station_data_json
  }

  getStationFromStationId(station_id) {
    let station_el = this.state.stationList.filter( st => 
      st.station_id === station_id 
    )[0]

    if (station_el === undefined) return {}

    return station_el
  }
  
  async setUserCoordinates() {
    const geolocation = navigator.geolocation
    
    let setCoordState = (pos) => {
      this.setState({
        coords: pos
      })
      this.setStationOnEuclideanDistance()
    }
    
    if (geolocation) { 
      await geolocation.getCurrentPosition(setCoordState)
    }
  }

  selectChangeHandler = async (event) => {
    this.setState({
      selectedStation: {}
    })
    
    let station_id = event.target.value
    let station_data = await this.fetchStationData(station_id)

    this.setState({
      selectedStation: station_data
    })
  }
  
  euclideanDistance(x1, y1, x2, y2) {
    return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2))
  }
  
  async setStationOnEuclideanDistance() {
    if (this.state.coords.length !== 0 && this.state.stationList.length !== 0) {
      let lat = this.state.coords.coords.latitude
      let long = this.state.coords.coords.longitude
      
      let mh = new MinHeap(this.state.stationList.length, (station) => {
        return station.distance
      })

      for (let i = 0; i < this.state.stationList.length; i++) {
        let station = this.state.stationList[i]
        let station_lat = station.latitude
        let station_long = station.longitude
        let distance = this.euclideanDistance(lat, long, station_lat, station_long)
        
        station.distance = distance
        mh.insert(station)
      }
      
      mh.heap[0].station_name += ' [Nearest Geolocated Station]'
      
      this.setState({
        selectedStation: {}
      })
      await this.setSelectedStationFromStation(mh.heap[0])

      this.setState({
        stationList: mh.heap
      })
    }
  }
  
  async fetchStations() {
    let stationsRequest = await fetch(STATIONS_URL)
    let stationsData = await stationsRequest.json()
        
    this.setState({
        stationList: stationsData
      }
    )
  }

  async setSelectedStationFromStation(station) {
    let selectedStationData = await this.fetchStationData(station.station_id)

    this.setState({
      selectedStation: selectedStationData
    })
  }
  
  async setSelectedStationFromIndex(index) {
    let station = this.state.stationList[index]
    await this.setSelectedStationFromStation(station)
  }
  
  async componentDidMount() {
    await this.fetchStations()
    await this.setSelectedStationFromIndex(0)
    this.setUserCoordinates()
  }
  
  render() {
    return (
      <React.Fragment>
        <Container>
          <Row>
            <Col>
              <StationList stationList={this.state.stationList} selectHandler={this.selectChangeHandler}/>
            </Col>
          </Row>
          <Row>
            <Col>
              <Station stationData={this.state.selectedStation} />
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  }
}

export default StationsContainer;