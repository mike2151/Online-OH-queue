import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import QueueAsk from './queues/QueueAsk';
import QueueFeedback from './queues/QueueFeedback';
import QueueEdit from './queues/QueueEdit';
import QueueTaList from './queues/QueueTAList';
import SignUpForm from './signup-in/Signup';
import LoginForm from './signup-in/Login';
import Summary from './stats/Summary';
import Stats from './stats/Stats';
import {BrowserRouter, Switch, Route} from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

ReactDOM.render((
    <BrowserRouter>
        <Switch>
            <Route exact path='/' component={App} />
            <Route exact path='/signup' component={SignUpForm} />
            <Route exact path='/login' component={() => <LoginForm activated={false} />} />
            <Route exact path='/activated' component={() => <LoginForm activated={true} />} />
            <Route exact path='/answer' component={QueueTaList} />
            <Route exact path='/feedback' component={QueueFeedback} />
            <Route exact path='/summary' component={Summary} />
            <Route exact path='/statistics' component={Stats} />
            <Route path="/:queue/ask" component={QueueAsk}/> 
            <Route path="/:questionid/edit" component={QueueEdit}/> 
        </Switch>
    </BrowserRouter>
    ), document.getElementById('root')
);

serviceWorker.unregister();