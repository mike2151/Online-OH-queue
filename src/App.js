import React, { Component } from 'react';
import LandingPage from "./landing-page/LandingPage";
import QueueList from "./queues/QueueList";


class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: false,
      queues: []
    };
  }

  componentDidMount() {
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

  render() {
    if(this.state.isLoggedIn) {
      return (
       <QueueList queues={this.state.queues} />
      );
    } else {
      return (
        <div id="root">
          <LandingPage/>
        </div>
      );
    }
  }
}

export default App;
