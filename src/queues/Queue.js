import React from "react";
import "../static/css/style.css"
import $ from 'jquery'

class Queue extends React.Component {

  constructor(props) {
    super(props); 
    this.deleteQuestion = this.deleteQuestion.bind(this);
    this.state = {
      csrftoken: ""
    };
  }

    componentDidMount() {
      document.title = "Online OH Queue";
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = $.trim(cookies[i]);
              if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                  break;
              }
          }
      }
      this.setState({csrftoken: cookieValue});

      fetch('/api/v1/theme/', {
        method: 'GET',
      }).then((response) => {
        return response.json();
      }).then((body) => {
        document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      });

    }

    deleteQuestion(question_id) {
      var post_name = "/api/v1/questions/delete/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "question_id": question_id
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (!body["success"]) {
          // handle non success
        }
      });
    }
  
    render() {
      var user_email = this.props.user_email;
      var deleteQuestionFunc = this.deleteQuestion;
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
                return user_email === question.author_email ?
                  <tr><td>{index+1} - {question.first_name} {question.last_name} 
                  <button onClick={() => deleteQuestionFunc(question.id)}
                  class="delete-link">Delete</button>
                  <a href={ '/' + question.id + "/edit" } class="delete-link">Edit</a> 
                  </td></tr>
                :
                  <tr><td>{index+1} - {question.first_name} {question.last_name}</td></tr>
            })}
          </table></center>
        </div>
      );
    }
  }

  export default Queue;