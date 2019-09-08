import React, { Component } from 'react';
import "../static/css/style.css"

class Summary extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isTA: false,
      questions: []
    };
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

    fetch('/api/v1/users/is_ta/', {
      method: 'GET',
      headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
    }).then((response) => {
      return response.json();
    }).then((body) => {
      if (body["is_ta"]) {
        this.setState({isTA: true});
        fetch('/api/v1/summary/', {
          method: 'GET',
          headers: {
              "Authorization": "Token " + localStorage.getItem('credentials')
            }
        }).then((response) => {
          return response.json();
        }).then((body) => {
            this.setState({questions: body});
        });
      } else {
          this.setState({isTA: false});
      }
    });
    
  }

  render() {
    if(this.state.isTA) {
      return (
        <div>
          <center><h2>Office Hours Questions This Week:</h2></center>
          <table class="summary">
            <tr>
                <th>Question</th><th>Queue</th><th>Asker</th><th>Answerer</th><th>Date</th>
            </tr>
            {this.state.questions.map(function(question, index){
                var date = (question.ask_date.split(".")[0]).split("T")[0];
                return <tr><td class="description">{index+1} - {question.description}</td><td class="answerer">{question.host_queue}</td><td class="answerer">{question.author_first_name} {question.author_last_name}</td><td class="answerer">{question.answerer_first_name} {question.answerer_last_name}</td><td class="answerer">{date}</td></tr>
            })}
          </table>
        </div>
      );
    } else {
      return (
        <h3 class="center-screen">You do not have appropriate permissions to access this page.
        <br /> <a href="/login">Login here</a></h3>
      )
    }
      
  }
}

export default Summary;
