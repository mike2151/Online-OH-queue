import React from "react";


class Queue extends React.Component {
  
    render() {
      return (
        <div>
          <h2>{this.props.queue.name}</h2>
          <ul>
             {this.props.queue.questions.map(function(question, index){
                return <li>{question}</li>;
            })}
          </ul>
        </div>
      );
    }
  }

  export default Queue;