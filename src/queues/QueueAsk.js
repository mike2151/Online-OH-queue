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
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
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
          console.log("failure!");
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
                <label htmlFor="description" id="description_label">Question Description (280 Characters Remaining):</label>
                <textarea maxlength="280" id="description" name="description" 
                 value={this.state.question} onChange={this.onChange} />  
                <button class="margin-top-button">submit</button>
              </form>
            </div>
          </div>
        </div>
      );
    }
  }

  export default QueueAsk;