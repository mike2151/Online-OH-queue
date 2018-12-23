import React, { Component } from 'react';

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
        <div>
        <h1>Queues!</h1>
      </div>
      );
    } else {
      return (
        <div>
        <a href="/signup">Sign up</a>
      </div>
      );
    }
  }
}

export default App;
