import React from "react";
import Queue from "./Queue";
import "../static/css/style.css"
import { Route , withRouter}  from 'react-router-dom';


class QueueList extends React.Component {

  constructor(props) {
    super(props); 
    this.logout = this.logout.bind(this);
  }

  logout() {
    localStorage.removeItem('credentials');
    this.props.history.push('/login');
   }
  
    render() {
      return (
        <div>
          <div class="top-right">
            <button className="btn btn-primary btn-margin btn-xl" onClick={this.logout}>Log out</button>
          </div>
          <div class="horizontalList">
            {this.props.queues.map(function(queue, index){
                return <div class="queue-table"><Queue queue={queue}/></div>;
            })}
          </div>
        </div>
      );
    }
  }

  export default withRouter(QueueList);