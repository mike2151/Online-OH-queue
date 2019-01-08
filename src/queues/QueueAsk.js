import React from "react";
import "../static/css/style.css"

class QueueAsk extends React.Component {
    constructor() {
      super();

      this.state = {
        description: ''
      }

      this.onChange = this.onChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
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
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      if (event.target.description.value.length === 0) {
        document.getElementById("validationError").innerHTML = "Question cannot be blank";
        return;
      }
      const post_url = '/api/v1/queue/' + this.props.match.params.queue + '/ask'
      fetch(post_url, {
        method: 'POST',
        body: data,
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
      }).then((response) => {
        if (response.ok) {
          let path = '/';
          this.props.history.push(path);
        } else {
          return response.json();
        }
      }).then((body) => {
        if (typeof body === "undefined") {}
        else {
          document.getElementById("validationError").innerHTML = body;
        }
      });
    }

    onChange(event) {
      var current_length = event.target.value.length;
      var remaining_chars = 280 - current_length;
      document.getElementById("description_label").innerHTML =
       "Question Description (" + remaining_chars.toString() + " Characters Remaining)";
      this.setState({[event.target.name]: event.target.value});
    }
  
    render() {
      return (
        <div class="formBg">
          <div class="question-page">
            <div class="questionForm">
              <form class="login-form" onSubmit={this.handleSubmit}>
                <h2 class="header-login"><center>Ask A Question</center></h2>
                <label class="dynamic-text" htmlFor="description" id="description_label">Question Description (280 Characters Remaining):</label>
                <p class="dynamic-text">Please enter your question or problem. You may update this later without losing your place in line. Non-questions (e.g., "I don't have a question right now.") or questions that are not relevant to this queue or not specific enough may cause you to forfeit your spot.</p>
                <textarea maxlength="280" id="description" name="description" 
                 value={this.state.question} onChange={this.onChange} />  
                <button class="margin-top-button">submit</button>
                <p id="validationError" class="validationErrorText"></p>
              </form>
            </div>
          </div>
        </div>
      );
    }
  }

  export default QueueAsk;