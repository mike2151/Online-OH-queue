import React, { Component } from 'react';
import LandingPage from "./landing-page/LandingPage";
import QueueList from "./queues/QueueList";

import "bootstrap/dist/css/bootstrap.min.css";
import './static/css/style.css'

import WebSocketInstance from './sockets/WebSocket'


class App extends Component {

  constructor(props) {
    super(props);
    this.fetchData = this.fetchData.bind(this);
    this.state = {
      isLoggedIn: false,
      queues: []
    };

    WebSocketInstance.connect();
    this.waitForSocketConnection(() => {
      WebSocketInstance.addCallbacks(this.update.bind(this))
    });
  }

  waitForSocketConnection(callback) {
    const component = this;
    setTimeout(
      function () {
        if (WebSocketInstance.state() === 1) {
          callback();
          return;
        } else {
          component.waitForSocketConnection(callback);
        }
    }, 100); 
  }

  fetchData() {
    fetch('/api/v1/queue/list/', {
      method: 'GET',
      headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
    }).then((response) => {
      return response.json();
    }).then((body) => {
      if (body.detail) {
        if (body.detail.localeCompare("Invalid token.") == 0) {
          // invalid token
        }
      } else {
        this.setState({isLoggedIn: true});
        this.setState({queues: body});
      }
    });
  }

  update(message) {
    this.fetchData();
    this.forceUpdate();
  }

  componentDidMount() {
    this.fetchData()
  }

  render() {
    if(this.state.isLoggedIn) {
      return (
        <div>
          <QueueList queues={this.state.queues} />
        </div>
      );
    } else {
      return (
        <div id="landing-page">
          <LandingPage/>
        </div>
      );
    }
  }
}

export default App;
