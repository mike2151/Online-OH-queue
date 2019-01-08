import React, { Component } from 'react';
import "../static/css/style.css"
import "bootstrap/dist/css/bootstrap.min.css";

import {Bar, Line} from 'react-chartjs-2';

import SearchBar from './SearchBar';

class Stats extends Component {

    constructor(props) {
        super(props);

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
            'authenticated': false
        }

        this.radioClick = this.radioClick.bind(this);
        this.getAskData = this.getAskData.bind(this);
        this.getAnswerData = this.getAnswerData.bind(this);
        this.displayAskData = this.displayAskData.bind(this);
        this.displayAnswerData = this.displayAnswerData.bind(this);
        this.searchBarCallback = this.searchBarCallback.bind(this);
        this.displayUserQuestionData = this.displayUserQuestionData.bind(this);
    }

    getAskData() {
        fetch('/api/v1/stats/frequentasker/', {
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
        fetch('/api/v1/stats/frequentanswer/', {
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
            );
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    }

    /* displayAnswerData() {
        if (this.state.authenticated) {
            return (
                <Bar 
                    labels={["Red", "Blue"]}
                    data={{
                        labels: this.state.labels,
                        datasets: [{
                            label: '# of Questions Answered',
                            data: this.state.counts,
                            backgroundColor: 'rgba(75, 192, 192, 1)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    }}
                    width={100}
                    height={50}
                    options={{
                        maintainAspectRatio: false,
                        scales: {
                            xAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'TA'
                                }
                            }],
                            yAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Count of Questions Answered'
                                },
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        }
                    }}
                />
            )
        } else {
            return (
                <div>
                    <p>You are not authenticated.</p>
                </div>
            )
        }
    } */

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
                var timedata = Object.keys(body).map((day) => {
                    return {'x': new Date(day), 'y': body[day]};
                });
                this.setState({'data': body, 'timedata': timedata, 'authenticated': body.authenticated});
            });
        } else {
            this.setState({'data': undefined});
        }
    }

    displayUserQuestionData() {
        if (this.state.authenticated) {
            if (this.state.queryUser && this.state.timedata) {
                return (
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
        fetch('/api/v1/stats/traffictime/', {
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
        if (this.state.authenticated) {
            return (
                <Bar 
                    labels={["Red", "Blue"]}
                    data={{
                        labels: this.state.slots,
                        datasets: [{
                            label: '# of Questions',
                            data: this.state.counts,
                            backgroundColor: 'rgba(75, 192, 192, 1)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    }}
                    width={100}
                    height={50}
                    options={{
                        maintainAspectRatio: false,
                        scales: {
                            xAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time slot'
                                }
                            }],
                            yAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Count of Questions'
                                },
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        }
                    }}
                />
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

        return (
            <div className="stats-page">
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
                
                <div className="stats-chart">
                    {dataJSX}
                </div>
            </div>
        )
    }
}

export default Stats;