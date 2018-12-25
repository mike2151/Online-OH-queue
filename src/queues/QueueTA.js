import React from "react";
import $ from 'jquery'

class Queue extends React.Component {

    constructor() {
      super();
      this.answerQuestion = this.answerQuestion.bind(this);
      this.state = {
        csrftoken: ""
      };
    }

    componentDidMount() {
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
    }
    
  
    answerQuestion(questionId) {
      var post_name = "/api/v1/questions/answer/";
      fetch(post_name, {
        method: 'POST',
        body: JSON.stringify({
          "queue": this.props.queue.name,
          "question_id": questionId
        }),
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials'),
          "X-CSRFToken": this.state.csrftoken
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        console.log(body);
        if (!body["success"]) {
          // handle non success
        }
      });
    }

    render() {
      var answerQuestionFunc = this.answerQuestion;
      return (
        <div>
          <center><h2 class="queue-title">{this.props.queue.name}</h2>
          <p class="wait-time">Average Wait Time: <br />
           {this.props.queue.average_wait_time} Minutes</p>
          <table class="queue">
          <tr>
            <th>Student</th>
          </tr>

          {this.props.queue.question_contents.map(function(question, index){
                return <tr><td>
                {index+1} - {question.first_name} {question.last_name}
                <br/> Question: {question.question_content}
                <br/><center><button onClick={() => answerQuestionFunc(question.id)}
                 class="answer-link">Answer</button></center> 
                </td></tr>
            })}
          </table></center>
        </div>
      );
    }
  }

  export default Queue;