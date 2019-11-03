import React, { Component } from 'react'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'

import { getPublicKeyArray } from './Helpers'
import { SUBSCRIBE_URL } from './API'

class Subscriber extends Component {
  constructor(props) {
    super(props)
    this.state = {
      email: '',
      clicked: false,
      permission: false,
      subscripton: {},
      subscriptionResponse: {},
    }
  }

  async _push_subscription(subscription) {
    const email = this.state.email
    const station_id = this.props.station_id;
    const notify_time = '09:00'

    const subscribe_body = {
      station_id: station_id,
      notify_time: notify_time,
      email: email,
      subscription: subscription
    }
    
    const susbcribe_request = await fetch(SUBSCRIBE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(subscribe_body)
    })

    const subscribe_json = susbcribe_request.json()

    return subscribe_json
  }
  
  async _ask_permission() {
    const permissionResult = await Notification.requestPermission()
    return permissionResult
  }

  async _subscribe(registration) {
    const permissionResult = await this._ask_permission()
    
    if (permissionResult === 'granted') {
      this.setState({
        permission: true
      })

      const public_key = await getPublicKeyArray()

      const options = {
        userVisibleOnly: true,
        applicationServerKey: public_key
      }

      const subscription = await registration.pushManager.subscribe(options)
      this.setState({
        subscription: subscription
      })

      let susbcription_response = await this._push_subscription(subscription)
      this.setState({
        subscriptionResponse: susbcription_response
      })
    }
  }
  
  async subscribe() {
    if ('serviceWorker' in navigator) {
      const registration = await navigator.serviceWorker.ready
      this._subscribe(registration)
    }
  }
  
  onSubmitHandler = async (event) => {
    event.preventDefault()
    const email = event.target.email.value
    this.setState({
      email: email
    })
    await this.subscribe()
  }

  render() {
    return (
      <React.Fragment>
        <Form onSubmit={this.onSubmitHandler}>
          <Form.Group controlId="formEmail">
            <Form.Control name='email' type="email" placeholder="Enter email" />
          </Form.Group>
          <Button variant="primary" type="submit">
            Get Notified Daily!
          </Button>
          { <Card.Text>{this.state.subscriptionResponse.error}</Card.Text> ? 'error' in this.state.subscriptionResponse : <React.Fragment></React.Fragment>}
        </Form>
      </React.Fragment>
    )
  }
}

export default Subscriber;