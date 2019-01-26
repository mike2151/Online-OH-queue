import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import QueueAsk from './queues/QueueAsk';
import QueueEdit from './queues/QueueEdit';
import QueueTaList from './queues/QueueTAList';
import Summary from './stats/Summary';
import Stats from './stats/Stats';
import {BrowserRouter, Switch, Route} from 'react-router-dom';
import * as serviceWorker from './serviceWorker';

ReactDOM.render((
    <BrowserRouter>
        <Switch>
            <Route exact path='/' component={App} />
            <Route exact path='/answer' component={QueueTaList} />
            <Route exact path='/summary' component={Summary} />
            <Route exact path='/statistics' component={Stats} />
            <Route path="/:queue/ask" component={QueueAsk}/> 
            <Route path="/:questionid/edit" component={QueueEdit}/> 
        </Switch>
    </BrowserRouter>
    ), document.getElementById('root')
);

serviceWorker.unregister();