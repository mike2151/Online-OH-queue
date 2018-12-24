import React from "react";
import Queue from "./Queue";
import "./style.css"


class QueueList extends React.Component {
  
    render() {
      return (
          <div class="horizontalList">
            {this.props.queues.map(function(queue, index){
                return <div class="queue-table"><Queue queue={queue}/></div>;
            })}
          </div>
      );
    }
  }

  export default QueueList;