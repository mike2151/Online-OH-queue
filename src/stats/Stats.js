import React, { Component } from 'react';
import "../static/css/style.css"

class Stats extends Component {

    constructor(props) {
        super(props);

        this.state={
            'mode': 'ask'
        }
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
            console.log('Logging the frequent asker data');
            console.log(body);
        });
    }

    render() {
        return (
            <div>
                <p>Hi there</p>
            </div>
        )
    }
}

export default Stats;