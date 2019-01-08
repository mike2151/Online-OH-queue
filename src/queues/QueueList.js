import React from "react";
import Queue from "./Queue";
import "../static/css/style.css"
import {withRouter}  from 'react-router-dom';



class QueueList extends React.Component {

  constructor(props) {
    super(props); 
    this.logout = this.logout.bind(this);
    this.is_user_not_in_queues = this.is_user_not_in_queues.bind(this)
    this.state = {
      oh_link: ""
    };
  }

  componentDidMount() {
    document.title = "Online OH Queue";
    fetch('/api/v1/theme/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((body) => {
      document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      this.setState({oh_link: body['oh_url']});
      document.title = body['course_title'] + " OH Queue";
      // change favicon
      var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = body['favicon_url'];
      document.getElementsByTagName('head')[0].appendChild(link);
    });
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
   }

  is_user_not_in_queues(user_email) {
    for (var q in this.props.queues) {
     var queue = this.props.queues[q];
     for (var i in queue.student_question_contents) {
       var question = queue.student_question_contents[i];
       if (user_email === question["email"]) {
         return false;
       }
     }
    }
    return true;
  } 
  
  render() {

    var user_email = this.props.user_email;

    let screenWidth = window.innerWidth;

    var numQueues = this.props.queues.length;
    if (numQueues === 0 || screenWidth < 800) {
      numQueues = 1;
    }
    var widthOfEachQueue = 100.0 / numQueues;
    var widthStr = widthOfEachQueue.toString() + "vw";
    var queueTableStyle = {
      width: widthStr
    };

    var user_not_in_queue = this.is_user_not_in_queues(user_email);


    if (this.props.queues.length == 0) {
      if (this.state.oh_link.length == 0) {
        return (
          <div>
            <div class="top-right">
              <button className="btn btn-primary" onClick={this.logout}>Log out</button>
            </div>
            <h2 class="center-screen">There are no office hours queues available</h2>
          </div>
        )
      } else {
        return (
          <div>
            <div class="top-right">
              <button className="btn btn-primary" onClick={this.logout}>Log out</button>
            </div>
            <div class="center-screen">
            <h2 >There are no office hours queues available.</h2>
            <p><a href={this.state.oh_link}>Click Here for Office Hours Schedule</a></p>
            </div>
          </div>
        )
      }
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
                <Queue queue={queue} user_email={user_email} user_not_in_queue={user_not_in_queue}/></div>;
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
                <Queue queue={queue} user_email={user_email} user_not_in_queue={user_not_in_queue}/></div>;
            })}
          </div>
        </div>
      );
    }
  }
  }

  export default withRouter(QueueList);