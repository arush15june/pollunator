import React, { Component } from 'react'
import Card from 'react-bootstrap/Card'
import Moment from 'react-moment'

class Parameter extends Component {
  render() {
    const param = this.props.parameterData
    
    return (
      <React.Fragment>
        <Card style={{ width: '18rem' }}>
          <Card.Body>
            <Card.Title>{param.name} | {param.value}</Card.Title>
            <Card.Text>
              
            </Card.Text>
            <Card.Text>
              <Moment>{param.date}</Moment>
            </Card.Text>
          </Card.Body>
        </Card>                                                     
      </React.Fragment>
    )
  }
}

export default Parameter