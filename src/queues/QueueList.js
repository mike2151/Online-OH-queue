import React from "react";
import Queue from "./Queue";
import "../static/css/style.css"
import { Route , withRouter}  from 'react-router-dom';


class QueueList extends React.Component {

  constructor(props) {
    super(props); 
    this.logout = this.logout.bind(this);
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
   }
  
    render() {

      var numQueues = this.props.queues.length;
      if (numQueues == 0) {
        numQueues = 1;
      }
      var widthOfEachQueue = 100.0 / numQueues;
      var widthStr = widthOfEachQueue.toString() + "vw";
      var queueTableStyle = {
        width: widthStr
      };
      

      return (
        <div>
          <div class="top-right">
            <button className="btn btn-primary btn-margin btn-xl" onClick={this.logout}>Log out</button>
          </div>
          <div class="horizontalList">
            {this.props.queues.map(function(queue, index){
                return <div style={queueTableStyle} class="queue-table" ><Queue queue={queue}/></div>;
            })}
          </div>
        </div>
      );
    }
  }

  export default withRouter(QueueList);