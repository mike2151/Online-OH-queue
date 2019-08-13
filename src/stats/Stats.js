import React, { Component } from 'react';
import "../static/css/style.css"
import "bootstrap/dist/css/bootstrap.min.css";

import {Bar, Line} from 'react-chartjs-2';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

import SearchBar from './SearchBar';
import TASearchBar from './TASearchBar';

class Stats extends Component {

    constructor(props) {
        super(props);

        var d1 = new Date();
        var d2 = new Date();
        d2.setDate(d1.getDate() - 7);
        d1.setDate(d2.getDate() + 8);
        this.state={
            'mode': 'ask',
            'data': [],
            'labels': [],
            'counts': [],
            'slots': [],
            'timedata': [],
            'queryUser': '',
            'queryTA': '',
            'askData': [],
            'answerData': [],
            'allFeedbackData': [],
            'slotData': {},
            'authenticated': false,
            'startdate': d2,
            'enddate': d1
        }

        this.radioClick = this.radioClick.bind(this);
        this.startDateChange = this.startDateChange.bind(this);
        this.endDateChange = this.endDateChange.bind(this);
        this.getAskData = this.getAskData.bind(this);
        this.getAnswerData = this.getAnswerData.bind(this);
        this.getAllFeedbackData = this.getAllFeedbackData.bind(this);
        this.displayAskData = this.displayAskData.bind(this);
        this.displayAnswerData = this.displayAnswerData.bind(this);
        this.displayAllFeedbackData = this.displayAllFeedbackData.bind(this);
        this.searchBarCallback = this.searchBarCallback.bind(this);
        this.taSearchBarCallback = this.taSearchBarCallback.bind(this);
        this.displayUserQuestionData = this.displayUserQuestionData.bind(this);
        this.displayFeedbackData = this.displayFeedbackData.bind(this);
    }

    startDateChange(date) {
        this.setState({'startdate': date}, () => {
            if (this.state.mode === 'ask') {
                this.getAskData();
            } else if (this.state.mode === 'answer') {
                this.getAnswerData();
            } else if (this.state.mode === 'all_feedback') {
                this.getAllFeedbackData();
            } 
            else if (this.state.mode === 'traffic') {
                this.getTrafficData();
            }
        });
    }

    endDateChange(date) {
        this.setState({'enddate': date}, () => {
            if (this.state.mode === 'ask') {
                this.getAskData();
            } else if (this.state.mode === 'answer') {
                this.getAnswerData();
            } else if (this.state.mode === 'all_feedback') {
                this.getAllFeedbackData();
            }  else if (this.state.mode === 'traffic') {
                this.getTrafficData();
            }
        })
    }

    getAskData() {
        var d1 = this.state.startdate.toISOString().split('T')[0];
        var d2 = this.state.enddate.toISOString().split('T')[0];
        fetch('/api/v1/stats/frequentasker/' + d1 + '/' + d2 + '/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            return response.json();
        }).then((body) => {
            this.setState({'askData': (body.value ? body.value : []), 'authenticated': body.authenticated});
        });
    }

    displayAskData() {
        if (this.state.authenticated) {
            var askDataJSX = (this.state.askData).map((dataObj) => {
                return (
                    <tr>
                        <td>{dataObj.email}</td>
                        <td>{dataObj.email.substring(0, dataObj.email.indexOf('@'))}</td>
                        <td>{dataObj.fname}</td>
                        <td>{dataObj.lname}</td>
                        <td>{dataObj.count}</td>
                    </tr>
                );
            });
            
            return (
                <div>
                    <span>Date Range Beginning&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.startdate}
                        onChange={this.startDateChange}
                    />
                    <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.enddate}
                        onChange={this.endDateChange}
                    />
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Email</th>
                                <th scope="col">PennKey</th>
                                <th scope="col">First Name</th>
                                <th scope="col">Last Name</th>
                                <th scope="col"># of Questions Asked</th>
                            </tr>
                        </thead>
                        <tbody>
                            {askDataJSX}
                        </tbody>
                    </table>
                </div>
            );
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    getAnswerData() {
        var d1 = this.state.startdate.toISOString().split('T')[0];
        var d2 = this.state.enddate.toISOString().split('T')[0];
        fetch('/api/v1/stats/frequentanswer/' + d1 + '/' + d2 + '/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            return response.json();
        }).then((body) => {
            this.setState({'answerData': body.value, 'authenticated': body.authenticated});
        });
    }

    getAllFeedbackData() {
        var d1 = this.state.startdate.toISOString().split('T')[0];
        var d2 = this.state.enddate.toISOString().split('T')[0];
        fetch('/api/v1/stats/all_feedback_data/' + d1 + '/' + d2 + '/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            return response.json();
        }).then((body) => {
            this.setState({'allFeedbackData': body.value, 'authenticated': body.authenticated});
        });
    }

    displayAnswerData() {
        if (this.state.authenticated) {
            var answerDataJSX = (this.state.answerData).map((dataObj) => {
                return (
                    <tr>
                        <td>{dataObj.email}</td>
                        <td>{dataObj.email.substring(0, dataObj.email.indexOf('@'))}</td>
                        <td>{dataObj.fname}</td>
                        <td>{dataObj.lname}</td>
                        <td>{dataObj.count}</td>
                    </tr>
                );
            });
            
            return (
                <div>
                    <span>Date Range Beginning&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.startdate}
                        onChange={this.startDateChange}
                    />
                    <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.enddate}
                        onChange={this.endDateChange}
                    />
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Email</th>
                                <th scope="col">PennKey</th>
                                <th scope="col">First Name</th>
                                <th scope="col">Last Name</th>
                                <th scope="col"># of Questions Answered</th>
                            </tr>
                        </thead>
                        <tbody>
                            {answerDataJSX}
                        </tbody>
                    </table>
                </div>
            );
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    displayAllFeedbackData() {
        if (this.state.authenticated) {
            var feedbackDataJSX = (this.state.allFeedbackData).map((dataObj) => {
                var rowStyle = {
                    maxWidth: '15vw',
                    wordWrap: 'break-word'
                };
                return (
                    <tr>
                        <td style={rowStyle}>{dataObj.ta_email}</td>
                        <td style={rowStyle}>{dataObj.was_helpful === "True" ? "Yes" : "No"}</td>
                        <td style={rowStyle}>{dataObj.helpful_scale}</td>
                        <td style={rowStyle}>{dataObj.comments}</td>
                        <td style={rowStyle}>{dataObj.date}</td>
                    </tr>
                );
            });
            
            return (
                <div>
                    <span>Date Range Beginning&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.startdate}
                        onChange={this.startDateChange}
                    />
                    <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.enddate}
                        onChange={this.endDateChange}
                    />
                    <table className="table table-hover">
                            <thead>
                                <tr>
                                    <th scope="col">Email</th>
                                    <th scope="col">Was Helpful</th>
                                    <th scope="col">Helpful Rating</th>
                                    <th scope="col">Comments</th>
                                    <th scope="col">Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                {feedbackDataJSX}
                            </tbody>
                    </table>
                </div>
            );
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    getUserQuestionData() {
        if (this.state.queryUser) {
            fetch('/api/v1/stats/' + this.state.queryUser + '/questions/', {
                method: 'GET',
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('credentials')
                }
            }).then((response) => {
                return response.json();
            }).then((body) => {
                var timedata = Object.keys(body.timeseries).map((day) => {
                    return {'x': new Date(day), 'y': body.timeseries[day]};
                });
                this.setState({'data': body, 'timedata': timedata, 'authenticated': body.authenticated});
            });
        } else {
            this.setState({'data': undefined});
        }
    }

    getTAFeedbackData() {
        if (this.state.queryTA) {
            var d1 = this.state.startdate.toISOString().split('T')[0];
            var d2 = this.state.enddate.toISOString().split('T')[0];
            fetch('/api/v1/stats/' + this.state.queryTA + '/feedback/' + d1 + '/' + d2 + '/', {
                method: 'GET',
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem('credentials')
                }
            }).then((response) => {
                return response.json();
            }).then((body) => {
                this.setState({'data': body, 'authenticated': body.authenticated});
            });
        } else {
            this.setState({'data': undefined});
        }
    }

    displayUserQuestionData() {
        if (this.state.authenticated) {
            if (this.state.queryUser && this.state.data && this.state.data.questions) {
                var questionTbl = this.state.data.questions.map((text) => {
                    return (
                        <tr>
                            <td>{text}</td>
                        </tr>
                    )
                })
                return (
                    <div>
                        <div>
                            <SearchBar 
                                callback={this.searchBarCallback}
                            />
                            <Line
                                data={{
                                    labels: ['Red', 'Blue'],
                                    datasets: [
                                        {
                                            label: "# of Questions Asked on Each Day",
                                            data: this.state.timedata,
                                            backgroundColor: 'rgba(75, 192, 192, 1)',
                                            borderColor: 'rgba(54, 162, 235, 1)',
                                        }
                                    ]
                                }}
                                options={{
                                    scales: {
                                        xAxes: [{
                                            scaleLabel: {
                                                display: true,
                                                labelString: 'Date'
                                            },
                                            type: 'time',
                                            time: {
                                                unit: 'month'
                                            }
                                        }],
                                        yAxes: [{
                                            scaleLabel: {
                                                display: true,
                                                labelString: 'Count of Questions Asked by ' + this.state.queryUser
                                            },
                                            ticks: {
                                                beginAtZero:true
                                            }
                                        }]
                                    }
                                }}
                            />
                        </div>
                        <br />
                        <br />
                        <p>Questions from {this.state.queryUser}</p>
                        <div>
                            <table className="table table-hover">
                                <tbody>
                                    {questionTbl}
                                </tbody>
                            </table>
                        </div>
                    </div>
                );
            } else {
                return (
                    <div>
                        <SearchBar 
                            callback={this.searchBarCallback}
                        />
                        <p>Search a student's email to get started.</p>
                    </div>
                );
            }
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    displayFeedbackData() {
        if (this.state.authenticated) {
            if (this.state.queryTA && this.state.data && this.state.data.feedback) {
                var rowStyle = {
                    maxWidth: '15vw',
                    wordWrap: 'break-word'
                };
                var feedbackData = (this.state.data.feedback).map((dataObj) => {
                    return (
                        <tr>
                            <td style={rowStyle}>{dataObj.ta_email}</td>
                            <td style={rowStyle}>{dataObj.was_helpful === "True" ? "Yes" : "No"}</td>
                            <td style={rowStyle}>{dataObj.helpful_scale}</td>
                            <td style={rowStyle}>{dataObj.comments}</td>
                            <td style={rowStyle}>{dataObj.date}</td>
                        </tr>
                    );
                });
                // calculate aggregate stats
                var num_respondents = 0;
                var sum_rating = 0;
                var num_rating_given = 0;
                var sum_was_helpful = 0;
                (this.state.data.feedback).map((dataObj) => {
                    num_respondents = num_respondents + 1;
                    if (dataObj.was_helpful == "True") {
                        sum_was_helpful = sum_was_helpful + 1;
                    }
                    if (dataObj.helpful_scale) {
                        sum_rating = sum_rating + dataObj.helpful_scale;
                        num_rating_given = num_rating_given + 1;
                    }
                });
                var average_rating = 0;
                if (num_rating_given != 0) {
                    average_rating = sum_rating / num_rating_given
                };
                var percent_helpful = 0.0;
                if (num_respondents != 0) {
                    percent_helpful = 100.00 * (sum_was_helpful / num_respondents);
                }
                return (
                    <div>
                        <div>
                            <span>Date Range Beginning&nbsp;&nbsp;</span>
                            <DatePicker
                                selected={this.state.startdate}
                                onChange={this.startDateChange}
                            />
                            <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                            <DatePicker
                                selected={this.state.enddate}
                                onChange={this.endDateChange}
                            /> <br />
                            <TASearchBar 
                                callback={this.taSearchBarCallback}
                            />
                        </div>
                        <br />
                        <br />
                        <center><h4>Feedback for {this.state.queryTA}</h4></center>
                        <div>
                            <h5>Aggregate Feedback</h5>
                            <p>Num Respondents: {num_respondents}</p>
                            <p>Percent Helpful: {percent_helpful} %</p> 
                            <p>Average Helpful Rating: {average_rating}</p> 
                            <br />
                            <h5>Individual Feedback Reports</h5>
                            <table className="table table-hover">
                                <thead>
                                    <tr>
                                        <th scope="col">Email</th>
                                        <th scope="col">Was Helpful</th>
                                        <th scope="col">Helpful Rating</th>
                                        <th scope="col">Comments</th>
                                        <th scope="col">Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {feedbackData}
                                </tbody>
                        </table>
                        </div>
                    </div>
                );
            } else {
                return (
                    <div>
                        <span>Date Range Beginning&nbsp;&nbsp;</span>
                        <DatePicker
                            selected={this.state.startdate}
                            onChange={this.startDateChange}
                        />
                        <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                        <DatePicker
                            selected={this.state.enddate}
                            onChange={this.endDateChange}
                        /> <br />
                        <TASearchBar 
                            callback={this.taSearchBarCallback}
                        />
                        <p>Search TA by email...</p>
                    </div>
                );
            }
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    getTrafficData() {
        var d1 = this.state.startdate.toISOString().split('T')[0];
        var d2 = this.state.enddate.toISOString().split('T')[0];
        fetch('/api/v1/stats/traffictime/' + d1 + '/' + d2 + '/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            return response.json();
        }).then((body) => {
            var timeslots = [];
            var amounts = [];
            for (var key in body.value) {
                timeslots.push(key);
                amounts.push(body.value[key]);
            }
            this.setState({'slots': timeslots, 'counts': amounts, 'data': body, 'slotData': body.value, 'authenticated': body.authenticated});
        })
    }

    displayTrafficData() {
        if (this.state.authenticated && this.state.data && this.state.data.value) {
            var trafficDataJSX = Object.keys(this.state.data.value).map((slot) => {
                return (
                    <tr>
                        <td>{slot}</td>
                        <td>{this.state.data.value[slot]}</td>
                    </tr>
                )
            })
            return (
                <div>
                    <span>Date Range Beginning&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.startdate}
                        onChange={this.startDateChange}
                    />
                    <span>&nbsp;&nbsp;Date Range End&nbsp;&nbsp;</span>
                    <DatePicker
                        selected={this.state.enddate}
                        onChange={this.endDateChange}
                    />
                    <div>
                        <table className="table table-hover">
                            <thead>
                                <tr>
                                    <th scope="col">Time Slot</th>
                                    <th scope="col"># of Questions Asked</th>
                                </tr>
                            </thead>
                            <tbody>
                                {trafficDataJSX}
                            </tbody>
                        </table>
                    </div>
                </div>
            )
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    radioClick(event) {
        this.setState({'mode': event.target.id}, () => {
            if (this.state.mode === 'ask') {
                this.getAskData();
            } else if (this.state.mode === 'answer') {
                this.getAnswerData();
            } else if (this.state.mode === 'all_feedback') {
                this.getAllFeedbackData();
            } else if (this.state.mode === 'userquestions') {
                this.getUserQuestionData();
            } else if (this.state.mode === 'traffic') {
                this.getTrafficData();
            }
        });
    }

    searchBarCallback(event) {
        this.setState({'queryUser': event.target.innerHTML}, () => {
            this.getUserQuestionData();
        });
    }

    taSearchBarCallback(event) {
        this.setState({'queryTA': event.target.innerHTML}, () => {
            this.getTAFeedbackData();
        });
    }

    componentDidMount() {
        document.title = 'Online OH Queue';
        this.getAskData();
    }

    render() {
        const activeRadio = "btn btn-secondary active";
        const passiveRadio = "btn btn-secondary";
        var dataJSX = this.displayAskData();
        if (this.state.mode === 'answer') {
            dataJSX = this.displayAnswerData();
        } else if (this.state.mode === 'userquestions') {
            dataJSX = this.displayUserQuestionData();
        } else if (this.state.mode === 'traffic') {
            dataJSX = this.displayTrafficData();
        } else if (this.state.mode === 'feedback') {
            dataJSX = this.displayFeedbackData();
        } else if (this.state.mode === 'all_feedback') {
            dataJSX = this.displayAllFeedbackData();
        }

        var labelsJSX = (
            <div></div>
        )

        if (this.state.authenticated) {
            labelsJSX = (
                <div className="stats-nav">
                    <div className="btn-group btn-group-toggle" data-toggle="buttons">
                        <label className={this.state.mode === 'ask' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="ask" autocomplete="off" checked onClick={this.radioClick} /> Questions per Student
                        </label>
                        <label className={this.state.mode === 'answer' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="answer" autocomplete="off" onClick={this.radioClick} /> Answers per TA
                        </label>
                        <label className={this.state.mode === 'traffic' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="traffic" autocomplete="off" onClick={this.radioClick} /> Traffic at Each Slot
                        </label>
                        <label className={this.state.mode === 'userquestions' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="userquestions" autocomplete="off" onClick={this.radioClick} /> Time Series of User's Questions
                        </label>
                        <label className={this.state.mode === 'feedback' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="feedback" autocomplete="off" onClick={this.radioClick} /> Feedback For TA
                        </label>
                        <label className={this.state.mode === 'all_feedback' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="all_feedback" autocomplete="off" onClick={this.radioClick} /> Feedback For All TAs
                        </label>
                    </div>
                </div>
            )
        }

        return (
            <div className="stats-page">
                {labelsJSX}
                
                <div className="stats-chart">
                    {dataJSX}
                </div>
            </div>
        )
    }
}

export default Stats;