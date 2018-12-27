import React from "react";

import "bootstrap/dist/css/bootstrap.min.css";
import "../style/style.css"

class LandingPage extends React.Component {
  render() {
    return (
    <header className="masthead d-flex">
        <div className="container text-center my-auto">
          <h1 className="mb-1 title-text">Office Hours Queue</h1>
          <a className="btn btn-primary btn-margin btn-xl" href="/signup">
            Sign up
          </a>
          <a className="btn btn-primary btn-xl" href="/login">
            Log in
          </a>
        </div>
        <div className="overlay" />
      </header>
    );
  }
}

export default LandingPage;