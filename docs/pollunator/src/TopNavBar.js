import React, { Component } from 'react';
import Navbar from 'react-bootstrap/Navbar'

// import logo from './logo.svg';
import './App.css';

class TopNavBar extends Component {
  render() {
    return (
      <React.Fragment>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand>Pollunator</Navbar.Brand>
        </Navbar>
      </React.Fragment>
    )
  }
}

export default TopNavBar;
