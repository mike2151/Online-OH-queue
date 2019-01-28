import React from "react";
import "../static/css/style.css";
import {withRouter}  from 'react-router-dom';

class UserInfo extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        first_name: '',
        last_name: ''
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
    }

    handleValidation(data) {
        var violationExists = false;
        var message = "";
  
        var last_name = data.get("last_name");
        var first_name = data.get("first_name");
        if (last_name.length === 0) {
          message = "Last name must be at least one character";
          violationExists = true;
        }
        if (first_name.length === 0) {
            message = "First name must be at least one character";
            violationExists = true;
        }
  
        document.getElementById("errorText").innerHTML = message;
        return !violationExists;
  
    }

    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      if (this.handleValidation(data)) {
        fetch('/api/v1/users/update/', {
            method: 'POST',
            body: data,
          }).then((response) => {
            return response.json();
          }).then((body) => {
            if (body.error) {
              document.getElementById("errorText").innerHTML = "Please enter a valid name";
            } else {
              this.props.history.push('/');
            }
          });
      }
    }

    onChange(event) {
      this.setState({[event.target.name]: event.target.value});
    }
  
    render() {
      return (
        <div class="formBg">
          <div class="login-page">
            <div class="userForm">
              <form class="login-form" onSubmit={this.handleSubmit}>
                <h2 class="header-login"><center>Provide more information:</center></h2>
                <label htmlFor="first_name">First Name:</label>
                <input id="first_name" name="first_name" maxLength={64} type="text" value={this.state.first_name} onChange={this.onChange} />  
                <label htmlFor="last_name">Last Name:</label>
                <input id="last_name" name="last_name" type="text" value={this.state.last_name} onChange={this.onChange} />
                <button>Update</button>
                <p id="errorText" class="validationErrorText"></p>
              </form>
            </div>
          </div>
        </div>
      );
    }
  }

  export default withRouter(LoginForm);