import React, { Component } from 'react';
import "../static/css/style.css"

class Stats extends Component {

    constructor(props) {
        super(props);

        this.state={
            'mode': 'ask',
            'data': {}
        }

        this.radioClick = this.radioClick.bind(this);
    }

    getAskData(data) {
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
            console.log(body);
            this.setState({'data': body});
        });
    }

    radioClick(event) {
        this.setState({'mode': event.target.id}, () => {
            console.log(this.state.mode);
        });
    }

    render() {
        /* var dataHTML;
        if (this.state['mode'] == 'ask') {
            var askData = this.getAskData();
            var tableRowHtml = askData.map((email) => {
                return (
                    <tr>
                        <td>{email}</td>
                        <td>{askData[email]}</td>
                    </tr>
                )
            });
            dataHTML = (
                <div>
                    <table>
                        <tr>
                            <th>Email</th>
                            <th>Number of Questions</th>
                        </tr>
                        {tableRowHtml}
                    </table>
                </div>
            )
        } */
        const activeRadio = "btn btn-secondary active";
        const passiveRadio = "btn btn-secondary";
        return (
            <div>
                <p>Hi there</p>

                <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label className={this.state.mode == 'ask' ? activeRadio : passiveRadio}>
                        <input type="radio" name="options" id="ask" autocomplete="off" checked onClick={this.radioClick} /> Active
                    </label>
                    <label className={this.state.mode == 'answer' ? activeRadio : passiveRadio}>
                        <input type="radio" name="options" id="answer" autocomplete="off" onClick={this.radioClick} /> Radio
                    </label>
                    <label className={this.state.mode == 'traffic' ? activeRadio : passiveRadio}>
                        <input type="radio" name="options" id="traffic" autocomplete="off" onClick={this.radioClick} /> Radio
                    </label>
                </div>
            </div>
        )
    }
}

export default Stats;