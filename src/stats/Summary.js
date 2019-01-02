import React, { Component } from 'react';
import "../static/css/style.css"

class Summary extends Component {

  constructor(props) {
    super(props);
    this.state = {
      questions: []
    };
  }

  componentDidMount() {
    fetch('/api/v1/summary', {
      method: 'GET',
      headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
    }).then((response) => {
      return response.json();
    }).then((body) => {
        this.setState({questions: body});
    });

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
      return (
        <div>
          <center><h2>Office Hours Questions This Week:</h2></center>
          <table class="summary">
            <tr>
                <th>Question</th><th>Answerer</th>
            </tr>
            {this.state.questions.map(function(question, index){
                return <tr><td class="description">{index+1} - {question.description}</td><td class="answerer">{question.answered_by_email}</td></tr>
            })}
          </table>
        </div>
      );
  }
}

export default Summary;
