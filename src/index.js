import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import QueueAsk from './queues/QueueAsk';
import QueueTaList from './queues/QueueTAList';
import SignUpForm from './signup-in/Signup';
import LoginForm from './signup-in/Login';
import Summary from './stats/Summary';
import Stats from './stats/Stats';
import {BrowserRouter, Switch, Route, Redirect} from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

ReactDOM.render((
    <BrowserRouter>
        <Switch>
            <Route exact path='/' component={App} />
            <Route exact path='/signup' component={SignUpForm} />
            <Route exact path='/login' component={LoginForm} />
            <Route exact path='/answer' component={QueueTaList} />
            <Route exact path='/summary' component={Summary} />
            <Route exact path='/stats' component={Stats} />
            <Route path="/:queue/ask" component={QueueAsk}/> 
        </Switch>
    </BrowserRouter>
    ), document.getElementById('root')
);

serviceWorker.unregister();