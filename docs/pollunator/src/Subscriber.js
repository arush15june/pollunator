import React, { Component } from 'react'
import { urlBase64ToUint8Array, getPublicKeyArray } from './Helpers'

class Subscriber extends Component {
  constructor(props) {
    super(props)
    this.state = {
      email: '',
      clicked: false,
      permission: false,
      subscripton: {}
      subscriptionResponse: {}
    }

    async function _push_susbcription(subscription) {
      const email = this.state.email

      const subscribe_body = {
          notify_time: '09:00',
          email: email,
          subscription: subscription
      }
      
      const susbcribe_request = await fetch('/api/subscription', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(subscribe_body)
      })

      const subscribe_json = susbcribe_request.json()

      return subscribe_json
    }
    
    async function askPermission() {
      const permissionResult = await Notification.requestPermission()
      return permissionResult
    }

    async function _subscribe() {
      const registration = await navigator.serviceWorker.ready
      const permissionResult = await askPermission()
      if (permissionResult === 'granted') {
        const public_key = getPublicKeyArray()
        const options = {
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(public_key)
        }

        const subscription = await registration.pushManager.subscribe(options)
        this.setState({
            subscription: subscription
        })

        let susbcription_response = await this._push_subscription(susbcription)
        this.setState({
          subscriptionResponse: susbcription_response
        })
      }
    }
    
    askPermission() {

    }

    async onSubmitHandler(event) {
      event.preventDefault()
    }

    render() {
      return (
        <React.Fragment>
          <Form onSubmit={this.onSubmitHandler}>
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
}