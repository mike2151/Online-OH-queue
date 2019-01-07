import React, { Component } from 'react';
import "../static/css/style.css"

class SearchBar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            'prefix': '',
            'students': [],
            'suggestions': []
        }

        this.getSuggestions = this.getSuggestions.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    componentDidMount() {
        fetch('/api/v1/stats/getstudents/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('credentials')
            }
        }).then((response) => {
            return response.json();
        }).then((body) => {
            this.setState({'students': body.value}, () => {
                console.log(this.state.students);
            });
        })
    }

    getSuggestions(prefix) {
        if (prefix) {
            var suggestions = this.state.students.filter((email) => {
                return email.startsWith(prefix);
            })
            suggestions.slice(0, 5);
            this.setState({'suggestions': suggestions});
        } else {
            this.setState({'suggestions': []});
        }
    }

    onChange(event) {
        this.setState({'prefix': event.target.value}, () => {
            this.getSuggestions(this.state.prefix);
        });
    }

    render() {
        var suggestionsHTML = this.state.suggestions.map((email) => {
            return (
                <p onClick={this.props.callback}>{email}</p>
            )
        })
        return (
            <div>
                <input type="text" className="form-control" placeholder="Student email" value={this.state.prefix} onChange={this.onChange} />
                {suggestionsHTML}
            </div>
        )
    }
}

export default SearchBar;