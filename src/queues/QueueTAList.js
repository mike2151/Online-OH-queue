import React, { Component } from 'react';
import QueueTA from "./QueueTA";
import "./style.css"

class QueueTaList extends Component {

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

            fetch('/api/v1/queue/list/', {
              method: 'GET',
              headers: {
                  "Authorization": "Token " + localStorage.getItem('credentials')
                }
            }).then((response) => {
              return response.json();
            }).then((body) => {
              if (body.detail) {
              } else {
                this.setState({queues: body});
              }
            });

        } else {
            this.setState({isTA: false});
        }
      });

  }

  render() {
    if(this.state.isTA) {
      return (
        <div class="horizontalList">
            {this.state.queues.map(function(queue, index){
                return <div class="queue-table"><QueueTA queue={queue}/></div>;
            })}
          </div>
      )
    } else {
      return (
        <p>You do not have appropriate permissions to access this page</p>
      )
    }
  }
}

export default QueueTaList;
