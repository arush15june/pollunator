import React, { Component } from 'react';
import StationsContainer from './Stations'
import TopNavBar from './TopNavBar'

// import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <TopNavBar />
        <StationsContainer />
      </React.Fragment>
    )
  }
}

export default App;
