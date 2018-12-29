import React, { Component } from 'react';
import QueueTA from "./QueueTA";
import "../static/css/style.css"

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
      let screenWidth = window.innerWidth;

      var numQueues = this.state.queues.length;
      if (numQueues == 0 || screenWidth < 800) {
        numQueues = 1;
      }
      var widthOfEachQueue = 100.0 / numQueues;
      var widthStr = widthOfEachQueue.toString() + "vw";
      var queueTableStyle = {
        width: widthStr
      };
      
      if (screenWidth < 800) {
        return (
          <div>
            <div class="top-right">
              <button className="btn btn-primary" onClick={this.logout}>Log out</button>
            </div>
            <div class="verticalList">
              {this.state.queues.map(function(queue, index){
                  return <div style={queueTableStyle} class="queue-table" ><QueueTA queue={queue}/></div>;
              })}
            </div>
          </div>
        );
      } else {
        return (
          <div>
            <div class="top-right">
              <button className="btn btn-primary btn-xl" onClick={this.logout}>Log out</button>
            </div>
            <div class="horizontalList">
              {this.state.queues.map(function(queue, index){
                  return <div style={queueTableStyle} class="queue-table" ><QueueTA queue={queue}/></div>;
              })}
            </div>
          </div>
        );
      }
    } else {
      return (
        <p>You do not have appropriate permissions to access this page</p>
      )
    }
  }
}

export default QueueTaList;

