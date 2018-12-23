import React from "react";
import ReactDOM from "react-dom";

class LoginForm extends React.Component {
    constructor() {
      super();

      this.state = {
        email: '',
        password: ''
      }

      this.onChange = this.onChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      console.log('Beginning login API call');
      fetch('/api/v1/users/login/', {
        method: 'POST',
        body: data,
        headers: {
          "Content-Type": "application/json"
        }
      }).then((response) => {
        console.log('Logging raw response');
        console.log(response);
        return response.json();
      }).then((body) => {
        console.log('Logging the response body');
        console.log(body);
        if (body.error) {
          alert('Invalid login');
        } else {
          // Logic for adding token to localStorage here
          localStorage.setItem('credentials', body.token);
        }
      });
    }

    onChange(event) {
      console.log(event.target.value);
      this.setState({[event.target.name]: event.target.value});
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="email">Penn Email</label>
          <input id="email" name="email" type="email" value={this.state.email} onChange={this.onChange} />
  
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" value={this.state.password} onChange={this.onChange} />
  
          <button>Log in</button>
        </form>
      );
    }
  }

  export default LoginForm;