import React from "react";
import Queue from "./Queue";
import "./style.css"


class QueueList extends React.Component {
  
    render() {
      return (
          <div class="horizontalList">
            {this.props.queues.map(function(queue, index){
                return <Queue queue={queue}/>;
            })}
          </div>
      );
    }
  }

  export default QueueList;