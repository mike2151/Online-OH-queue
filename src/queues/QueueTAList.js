import React, { Component } from 'react';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isTA: false,
      queues: []
    };
  }

  componentDidMount() {
    // see if TA
    fetch('/api/v1/users/is_ta', {
        method: 'GET',
        headers: {
            "Authorization": "Token " + localStorage.getItem('credentials')
          }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (body["is_ta"]) {
            this.setState({isTA: true});
        } else {
            this.setState({isTA: false});
        }
      });

  }

  render() {
    return (
        <div>
            <p>Yo</p>
        </div>
    )
  }
}

export default App;
