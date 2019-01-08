import React from "react";
import "../static/css/style.css"

class QueueEdit extends React.Component {
    constructor() {
      super();

      this.state = {
        description: '',
        question_id: ''
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
        document.title = body['course_title'] + " OH Queue";
        // change favicon
        var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = body['favicon_url'];
        document.getElementsByTagName('head')[0].appendChild(link);
      });
      var question_id = this.props.match.params.questionid;
      this.setState({question_id: question_id.toString()});
      fetch('/api/v1/questions/detail/' + question_id.toString() + "/", {
        method: 'GET',
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (body["success"]) {
          this.setState({description: body["description"]})
          document.getElementById("description").value = body["description"];
          var current_length = document.getElementById("description").value.length;
          var remaining_chars = 280 - current_length;
          document.getElementById("description_label").innerHTML =
          "Question Description (" + remaining_chars.toString() + " Characters Remaining)";
        }
      });
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      if (event.target.description.value.length == 0) {
        document.getElementById("validationError").innerHTML = "Question cannot be blank";
        return;
      }
      const put_url = '/api/v1/queue/question/' + this.state.question_id + '/edit/'
      fetch(put_url, {
        method: 'PUT',
        body: data,
        headers: {
          "Authorization": "Token " + localStorage.getItem('credentials')
        }
      }).then((response) => {
        return response.json();
      }).then((body) => {
        if (body["success"]) {
          let path = '/';
          this.props.history.push(path);
        } else {
          document.getElementById("validationError").innerHTML = body["error"];
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
                <h2 class="header-login"><center>Edit Question</center></h2>
                <label htmlFor="description" id="description_label">Question Description (280 Characters Remaining):</label>
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

  export default QueueEdit;