import React, { Component } from 'react';

class ViewQueues extends Component {
  render() {
    fetch('/api/v1/queue/create/', {
        method: 'GET',
        headers: {
            "Authorization": "Token " + localStorage.getItem('credentials')
          }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (body.error) {
          alert('You are not validated!');
        } else {
          console.log(body);
        }
      });

    return (
      <div >
        <h1>Queues!</h1>
      </div>
    );
  }
}

export default ViewQueues;
