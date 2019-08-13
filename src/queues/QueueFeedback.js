import React from "react";
import "../static/css/style.css"
import Slider from 'react-rangeslider'
import 'react-rangeslider/lib/index.css';

class QueueFeedback extends React.Component {
    constructor(props, context) {
      super(props, context);

      this.state = {
        is_valid: false,
        ta_name: "",
        question: "",
        was_helpful: "no_ans",
        help_scale: 0,
        primary_color: '#445B73',
        comments: ""
      }
      this.set_thumps_down = this.set_thumps_down.bind(this);
      this.set_thumps_up = this.set_thumps_up.bind(this);
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
        document.body.style.background = body['primary_theme_color'];
        document.title = body['course_title'] + " OH Queue";
        // change favicon
        var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = body['favicon_url'];
        document.getElementsByTagName('head')[0].appendChild(link);
        this.setState({primary_color: body['primary_theme_color']});
      });
      fetch('/api/v1/feedback/info_for_feedback/', {
        method: 'GET',
        headers: {
            "Authorization": "Token " + localStorage.getItem('credentials')
          }
      }).then((response) => {
        return response.json();
      }).then((feedback_body) => {
        this.setState({is_valid: feedback_body["is_valid"]});
        this.setState({ta_name: feedback_body["ta_name"]});
        this.setState({question: feedback_body["question"]});
      });
    }

    set_thumps_up(e) {
        e.preventDefault();
        this.setState({was_helpful: "true"});
    }

    set_thumps_down(e) {
        e.preventDefault();
        this.setState({was_helpful: "false"});
    }
  
    handleSubmit(event) {
        event.preventDefault();
        if (!(this.state.was_helpful == "true" || this.state.was_helpful == "false")) {
          document.getElementById("validationError").innerHTML = "You must indicate if the TA was helpful";
          return;
        }
        var was_helpful = this.state.was_helpful == "true";
        var rating = this.state.help_scale;
        var additional_comments = this.state.comments;
        var json_body = {};
        json_body["was_helpful"] = was_helpful;
        if (rating != 0) {
            json_body["helpful_scale"] = rating;
        }
        if (additional_comments.length > 0) {
            json_body["comments"] = additional_comments;
        }
        var data = JSON.stringify(json_body);
        fetch('/api/v1/feedback/post_feedback/', {
            method: 'POST',
            headers: {
                "Authorization": "Token " + localStorage.getItem('credentials'),
                'Content-Type':'application/json'
              },
            body: data
          }).then((response) => {
            if (response.ok) {
              let path = '/';
              this.props.history.push(path);
              window.location.reload();
            } else {
              return response.json();
            }
          }).then((body) => {
            
          });
    }

    onChange(event) {
      var current_length = event.target.value.length;
      var remaining_chars = 280 - current_length;
      document.getElementById("comments_label").innerHTML =
       "Optional Comments for the head TAs. <br /> Is there anything we need to know about this interaction? <br /> This will only be visible to the Head TAs, and can be used to report anything you'd like. (" + remaining_chars.toString() + " Characters Remaining)";
      this.setState({[event.target.name]: event.target.value});
    }

    handleOnChange = (value) => {
        this.setState({
            help_scale: value
        })
      }
  
    render() {
        if(this.state.is_valid) {
            var classNames = require('classnames');
            var btnGroupClassUp = classNames(
                {
                'answer-link': this.state.was_helpful == "no_ans" || this.state.was_helpful == "false",
                'answer-link-selected': this.state.was_helpful == "true"
                }
            );
            var btnGroupClassDown = classNames(
                {
                'answer-link-selected': this.state.was_helpful == "false",
                'answer-link': this.state.was_helpful == "no_ans" || this.state.was_helpful == "true"
                }
            );
            var btnStyle = {
                width: '10vw',
            };
            var questionStyle = {
                wordWrap: 'break-word',
                width: '100%'
            }
            const horizontalLabels = {
                0: '0: Skip',
                1: '1: No Help',
                10: '10: Too Much Help'
              }
            var set_thumps_up = this.set_thumps_up;
            var set_thumps_down = this.set_thumps_down;
            var help_scale = this.state.help_scale;
            return (
                <div class="formBg">
                    <div class="question-page">
                        <div class="questionForm">
                        <form class="login-form" onSubmit={this.handleSubmit}>
                            <h2 class="header-login"><center>Office Hours Feedback</center></h2>
                                <center>
                                    
                                    <p style={questionStyle}>Your Question: {this.state.question} <br/></p>
                                    
                                </center>
                                <p>
                                <h5>TA {this.state.ta_name} was helpful and answered my question (Required): </h5><br />
                                <button onClick={(e) => set_thumps_up(e)} className={btnGroupClassUp} style={btnStyle}>Yes</button>
                                <button onClick={(e) => set_thumps_down(e)} className={btnGroupClassDown} style={btnStyle}>No</button>
                                <br /><br />
                                <h5>Rate the level of help you received (Optional):</h5><br />
                            </p>
                            <Slider
                                min={0}
                                max={10}
                                step={1}
                                tooltip={true}
                                value={help_scale}
                                orientation="horizontal"
                                handleLabel={help_scale}
                                labels={horizontalLabels}
                                onChange={this.handleOnChange}
                            /> 
                            <b>{help_scale}</b>
                            <br /><br /><br />
                            <label class="dynamic-text" htmlFor="comments" id="comments_label">Optional Comments for the Head TAs. <br />Is there anything we need to know about this interaction? <br /> This will only be visible to the head TAs, and can be used to report anything you'd like. (280 Characters Remaining):</label>
                            <textarea maxlength="280" id="comments" name="comments" 
                            value={this.state.comments} onChange={this.onChange} />  
                            <button class="margin-top-button">submit</button>
                            <p id="validationError" class="validationErrorText"></p>
                        </form>
                        </div>
                    </div>
                </div>
            );
        } else {
            return (
                <div class="formBg">
                    <div class="question-page">
                        <div class="questionForm">
                            <center><h2>You have no feedback to provide.</h2></center>
                        </div>
                    </div>
                </div>
            );
        }
    }
  }

  export default QueueFeedback;