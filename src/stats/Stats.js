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
            'data': {},
            'labels': ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            'counts': [12, 19, 3, 5, 2, 3],
            'timedata': [{
                x: new Date('January 3, 2019'),
                y: 1
            }, {
                t: new Date(),
                y: 10
            }],
            'queryuser': ''
        }

        this.radioClick = this.radioClick.bind(this);
        this.getAskData = this.getAskData.bind(this);
        this.getAnswerData = this.getAnswerData.bind(this);
    }

    getAskData() {
        fetch('/api/v1/stats/frequentasker/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            console.log("Getting a response");
            return response.json();
        }).then((body) => {
            console.log('Logging the frequent asker data');
            this.setState({'data': body}, () => {
                console.log(this.state.data);
                var emails = [];
                var amounts = [];
                for (var key in body) {
                    emails.push(key);
                    amounts.push(body[key]);
                }
                this.setState({'labels': emails, 'counts': amounts});
            });
        });
    }

    getAnswerData() {
        fetch('/api/v1/stats/frequentanswer/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            console.log("Getting a response");
            return response.json();
        }).then((body) => {
            console.log('Logging the frequent answerer data');
            this.setState({'data': body}, () => {
                console.log(this.state.data);
                var emails = [];
                var amounts = [];
                for (var key in body) {
                    emails.push(key);
                    amounts.push(body[key]);
                }
                this.setState({'labels': emails, 'counts': amounts});
            });
        });
    }

    getUserQuestionData() {
        fetch('/api/v1/stats/frequentanswer/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            console.log("Getting a response");
            return response.json();
        }).then((body) => {
            console.log('Logging the frequent answerer data');
            this.setState({'data': body}, () => {
                console.log(this.state.data);
                var emails = [];
                var amounts = [];
                for (var key in body) {
                    emails.push(key);
                    amounts.push(body[key]);
                }
                this.setState({'labels': emails, 'counts': amounts});
            });
        });
    }

    radioClick(event) {
        this.setState({'mode': event.target.id}, () => {
            console.log(this.state.mode);
            if (this.state.mode == 'ask') {
                //this.getAskData();
            } else if (this.state.mode == 'answer') {
                //this.getAnswerData();
            }
        });
    }

    getBarGraphHtml() {
        return (
            <Bar 
                labels={["Red", "Blue"]}
                data={{
                    labels: this.state.labels,
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
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }}
            />
        )
    }

    getTimeSeriesHtml() {
        return (
            <Line
                data={{
                    labels: ['Red', 'Blue'],
                    datasets: [
                        {
                            label: "it's lit",
                            data: this.state.timedata
                        }
                    ]
                }}
                options={{
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {
                                unit: 'month'
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }}
            />
        )
    }

    componentDidMount() {
        //this.getAskData();
    }

    render() {
        var timeSeries = this.getTimeSeriesHtml();
        
        const activeRadio = "btn btn-secondary active";
        const passiveRadio = "btn btn-secondary";
        return (
            <div className="stats-page">
                <div className="stats-nav">
                    <div className="btn-group btn-group-toggle" data-toggle="buttons">
                        <label className={this.state.mode == 'ask' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="ask" autocomplete="off" checked onClick={this.radioClick} /> Questions per Student
                        </label>
                        <label className={this.state.mode == 'answer' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="answer" autocomplete="off" onClick={this.radioClick} /> Answers per TA
                        </label>
                        <label className={this.state.mode == 'traffic' ? activeRadio : passiveRadio}>
                            <input type="radio" name="options" id="traffic" autocomplete="off" onClick={this.radioClick} /> Traffic at Each Slot
                        </label>
                    </div>
                    <SearchBar />
                </div>
                
                <div className="stats-chart">
                    {timeSeries}
                </div>
            </div>
        )
    }
}

export default Stats;