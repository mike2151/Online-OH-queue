import React from "react";
import "../style/style.css"

class Queue extends React.Component {
  
    render() {
      return (
        <div>
          <center><h2 class="queue-title">{this.props.queue.name}</h2>
          <p class="wait-time">Average Wait Time: <br />
           {this.props.queue.average_wait_time} Minutes</p>
          <a href={ '/' + this.props.queue.name + "/ask" } class="ask-link">Ask Question</a>
          <table class="queue">
          <tr>
            <th>Name</th>
          </tr>

          {this.props.queue.question_contents.map(function(question, index){
                return <tr><td>{index+1} - {question.first_name} {question.last_name}</td></tr>
            })}
          </table></center>
        </div>
      );
    }
  }

  export default Queue;