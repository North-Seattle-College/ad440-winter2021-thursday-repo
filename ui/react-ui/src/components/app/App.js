import './App.css';
import {BrowserRouter as Router, Route,} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
import Users from '../routes/users/Users';
import TaskIdReport from '../routes/reports/taskIdReport/TaskIdReport';
import userIdReport from '../routes/reports/userIdReport/UserIdReport';
import usersReport from '../routes/reports/usersReport/UserReport';
 
function App() {
  return (
    <div className="App">
      <Router>
        <Route exact path='/' component={Home} />
        {/* Jak */}
        <Route exact path='/users' component={Users}/>
        {/* David */}
        <Route exact path='/users/:userId' component={User}/>
        {/* Farhad */}
        <Route exact path='/users/:userId/tasks' component={UserTasks}/>
    
        {/* Test results routes */}
        <Route exact path='/reports/taskId' component={TaskIdReport}/>
        <Route exact path='/reports/userId' component={userIdReport}/>
        <Route exact path='/reports/users' component={usersReport}/>
      </Router>
    </div>
  );
}

export default App;
