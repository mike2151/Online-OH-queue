import React from "react";
import ReactDOM from "react-dom";

class SignUpForm extends React.Component {
    constructor() {
      super();
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleSubmit(event) {
      event.preventDefault();
      const data = new FormData(event.target);
      
      fetch('/api/v1/users/register/', {
        method: 'POST',
        body: data,
      });
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="email">Enter Penn Email</label>
          <input id="email" name="email" type="email" />
  
          <label htmlFor="first_name">First Name</label>
          <input id="first_name" name="first_name" type="text" />
  
          <label htmlFor="last_name">Last Name</label>
          <input id="last_name" name="last_name" type="text" />

          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" />
  
          <button>Sign Up</button>
        </form>
      );
    }
  }

  export default SignUpForm;