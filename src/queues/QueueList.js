import React from "react";
import Queue from "./Queue";
import "../static/css/style.css"
import { Route , withRouter}  from 'react-router-dom';



class QueueList extends React.Component {

  constructor(props) {
    super(props); 
    this.logout = this.logout.bind(this);
  }

  componentDidMount() {
    document.title = "Online OH Queue";
    fetch('/api/v1/theme/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((body) => {
      document.body.style.setProperty('--primary-color', body['primary_theme_color']);
    });
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
   }
  
  render() {

    var user_email = this.props.user_email;

    let screenWidth = window.innerWidth;

    var numQueues = this.props.queues.length;
    if (numQueues == 0 || screenWidth < 800) {
      numQueues = 1;
    }
    var widthOfEachQueue = 100.0 / numQueues;
    var widthStr = widthOfEachQueue.toString() + "vw";
    var queueTableStyle = {
      width: widthStr
    };

    if (this.props.queues.length == 0) {
      return (
        <div>
          <div class="top-right">
            <button className="btn btn-primary" onClick={this.logout}>Log out</button>
          </div>
          <h2 class="center-screen">There are no office hours queues available</h2>
        </div>
      )
    }
    
    if (screenWidth < 800) {
      return (
        <div>
          <div class="top-right">
            <button className="btn btn-primary" onClick={this.logout}>Log out</button>
          </div>
          <div class="verticalList">
            {this.props.queues.map(function(queue, index){
                return <div style={queueTableStyle} class="queue-table" >
                <Queue queue={queue} user_email={user_email}/></div>;
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
            {this.props.queues.map(function(queue, index){
                return <div style={queueTableStyle} class="queue-table" >
                <Queue queue={queue} user_email={user_email}/></div>;
            })}
          </div>
        </div>
      );
    }
  }
  }

  export default withRouter(QueueList);