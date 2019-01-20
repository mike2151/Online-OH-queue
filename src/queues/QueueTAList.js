import React, { Component } from 'react';
import QueueTA from "./QueueTA";
import "../static/css/style.css"

import WebSocketInstance from '../sockets/WebSocket'


class QueueTaList extends Component {

  constructor(props) {
    super(props);
    this.fetchData = this.fetchData.bind(this);
    this.logout = this.logout.bind(this);
    this.state = {
      isTA: false,
      queues: [],
      default_document: "Online OH Queue"
    };

    WebSocketInstance.connect();
    this.waitForSocketConnection(() => {
      WebSocketInstance.addCallbacks(this.update.bind(this))
    });
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
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
    // see if TA
    fetch('/api/v1/users/is_ta/', {
      method: 'GET',
      headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
    }).then((response) => {
      return response.json();
    }).then((body) => {
      if (body["is_ta"]) {
          this.setState({isTA: true});

          fetch('/api/v1/queue/list_ta/', {
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

  update(message) {
    this.fetchData();
    this.forceUpdate();
  }

  componentDidMount() {
    this.fetchData()
    fetch('/api/v1/theme/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((body) => {
      document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      this.setState({default_document: body['course_title'] + " OH Queue"});
      document.title = this.state.default_document;
      // change favicon
      var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = body['favicon_url'];
      document.getElementsByTagName('head')[0].appendChild(link);
    });
  }

  render() {
    if(this.state.isTA) {

      var numQueues = this.state.queues.length;

      // get the number of current questions in the queues
      var numQuestions = 0;
      for (var i = 0; i < numQueues; i++) {
        numQuestions = numQuestions + this.state.queues[i].question_contents.length;
      }
      if (numQuestions != 0) {
        document.title = "(" + numQuestions.toString() + ") " + this.state.default_document; 
      } else {
        document.title = this.state.default_document;
      }

      let screenWidth = window.innerWidth;
      
      if (numQueues === 0 || screenWidth < 800) {
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
        <h3 class="center-screen">You do not have appropriate permissions to access this page.
        <br /> <a href="/login">Login here</a></h3>
      )
    }
  }
}

export default QueueTaList;

