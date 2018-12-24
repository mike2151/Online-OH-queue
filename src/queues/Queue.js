import React from "react";


class Queue extends React.Component {
  
    render() {
      return (
        <div>
          <h2>{this.props.queue.name}</h2>
          <a href={ '/' + this.props.queue.name + "/ask" } >Ask Question</a>
          <table class="queue">
          <tr>
            <th>Name</th>
          </tr>

          {this.props.queue.question_contents.map(function(question, index){
                return <tr><td>{question.first_name}</td></tr>
            })}
          </table>
        </div>
      );
    }
  }

  export default Queue;