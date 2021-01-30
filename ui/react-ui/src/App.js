import React, {Component} from 'react'
import {BrowserRouter as Router, Route} from 'react-router-dom';
import Users from './Pages/Users';

class App extends Component{
  render(){
    return(
        <Router>
          <div>
            <p>All Users</p>
            <Route path='/allUsers' exact component={Users}></Route>
          </div>
        </Router>

    )   
    }
}

export default App;