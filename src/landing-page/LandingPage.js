import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";
import "../static/css/style.css"

class LandingPage extends React.Component {

  componentDidMount() {
    document.title = "Online OH Queue";

    fetch('/api/v1/theme/', {
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((body) => {
      document.body.style.setProperty('--primary-color', body['primary_theme_color']);
      document.getElementById("header").innerHTML = body['course_title'] + " Office Hours Queue";
      document.title = body['course_title'] + " OH Queue";
    });
  }

  render() {
    return (
    <header className="masthead d-flex">
        <div className="container text-center my-auto">
          <h1 id="header" className="mb-1 title-text">Office Hours Queue</h1>
          <a className="btn btn-primary btn-margin btn-xl" href="/signup">
            Sign up
          </a>
          <a className="btn btn-primary btn-margin btn-xl" href="/login">
            Log in
          </a>
        </div>
        <div className="overlay" />
      </header>
    );
  }
}

export default LandingPage;