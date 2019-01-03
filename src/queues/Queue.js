import React from "react";
import "../static/css/style.css"

class Queue extends React.Component {

  constructor(props) {
    super(props); 
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
  
    render() {
      var user_email = this.props.user_email;
      var user_in_queue = false;
      for (var question in this.props.queue.questions) {
        if (user_email === question.author_email) {
          user_in_queue = true;
          break;
        }
      }

      return (
        <div>
          <center><h2 class="queue-title">{this.props.queue.name}</h2>
          <p class="wait-time">Average Wait Time: <br />
          {this.props.queue.average_wait_time} Minutes</p>
          {user_in_queue ? 
            <a href={ '/' + this.props.queue.name + "/ask" } class="ask-link">Ask Question</a> :
            <a href={ '/' + this.props.queue.name + "/edit" } class="ask-link">Edit Question</a>
          }
          
          <table class="queue">
          <tr>
            <th>Name</th>
          </tr>

          {this.props.queue.question_contents.map(function(question, index){
                return user_email === question.author_email ?
                  <tr><td>{index+1} - {question.first_name} {question.last_name} 
                  <a href={ '/' + question.id + "/delete" } class="delete-link">Delete</a></td></tr>
                :
                  <tr><td>{index+1} - {question.first_name} {question.last_name}</td></tr>
            })}
          </table></center>
        </div>
      );
    }
  }

  export default Queue;