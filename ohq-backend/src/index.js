import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import SignUpForm from './Signup';
import LoginForm from './Login';
import {BrowserRouter, Switch, Route, Redirect} from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

ReactDOM.render((
    <BrowserRouter>
        <Switch>
            <Route exact path='/' component={App} />
            <Route eaxct path='/signup' component={SignUpForm} />
            <Route eaxct path='/login' component={LoginForm} />
        </Switch>
    </BrowserRouter>
    ), document.getElementById('root')
);

serviceWorker.unregister();