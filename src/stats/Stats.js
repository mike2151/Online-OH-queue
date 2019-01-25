import React, { Component } from 'react';
import "../static/css/style.css"
import "bootstrap/dist/css/bootstrap.min.css";

import {Bar, Line} from 'react-chartjs-2';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

import SearchBar from './SearchBar';

class Stats extends Component {

    constructor(props) {
        super(props);

        var d1 = new Date();
        var d2 = new Date();
        d2.setDate(d1.getDate() - 7);
        this.state={
            'mode': 'ask',
            'data': [],
            'labels': [],
            'counts': [],
            'slots': [],
            'timedata': [],
            'queryUser': '',
            'askData': [],
            'answerData': [],
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
        this.displayAskData = this.displayAskData.bind(this);
        this.displayAnswerData = this.displayAnswerData.bind(this);
        this.searchBarCallback = this.searchBarCallback.bind(this);
        this.displayUserQuestionData = this.displayUserQuestionData.bind(this);
    }

    startDateChange(date) {
        this.setState({'startdate': date}, () => {
            if (this.state.mode === 'ask') {
                this.getAskData();
            } else if (this.state.mode === 'answer') {
                this.getAnswerData();
            } else if (this.state.mode === 'traffic') {
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
            } else if (this.state.mode === 'traffic') {
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