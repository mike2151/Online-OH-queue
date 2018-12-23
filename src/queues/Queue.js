import React from "react";


class Queue extends React.Component {
  
    render() {
      return (
        <div>
          <h2>{this.props.queue.name}</h2>
        </div>
      );
    }
  }

  export default Queue;