import React from "react";
import ReactDOM from "react-dom";

class LoginForm extends React.Component {
    constructor() {
      super();
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      
      fetch('/api/v1/users/login/', {
        method: 'POST',
        body: data,
      });
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="email">Penn Email</label>
          <input id="email" name="email" type="email" />
  
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" />
  
          <button>Log in</button>
        </form>
      );
    }
  }

  export default LoginForm;