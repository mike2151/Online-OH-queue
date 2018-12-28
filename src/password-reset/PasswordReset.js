import React from "react";
import "../static/css/style.css"

class PasswordReset extends React.Component {
  
    render() {
      return (
        <div class="formBg">
            <div class="login-page">
                <div class="userForm">
                    <form class="login-form" method="post">
                        <h2 class="header-login"><center>Reset Password React</center></h2>
                        <label htmlFor="id_email">Email:</label>
                        <input type="email" name="email" maxlength="254" required="" id="id_email"/>
                        <button type="submit">Submit</button>
                    </form>
                </div>
            </div>
        </div>
      );
    }
  }

  export default PasswordReset;