import React from "react";
import Queue from "./Queue";
import "../static/css/style.css"


class QueueList extends React.Component {
  
    render() {
      return (
        <div>
          <div class="top-right">
            <button className="btn btn-primary btn-margin btn-xl" onClick={this.logout}>Log out</button>
          </div>
          <div class="horizontalList">
            {this.props.queues.map(function(queue, index){
                return <div class="queue-table"><Queue queue={queue}/></div>;
            })}
          </div>
        </div>
      );
    }
  }

  export default QueueList;