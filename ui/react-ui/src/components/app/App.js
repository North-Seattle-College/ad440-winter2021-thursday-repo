import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
import Users from '../routes/users/Users';
import usersUserIdTasksTaskIdReport from '../routes/reports/UserIdTaskIdReport/UsersUserIdTasksTaskIdReport';
 
function App() {
  return (
    <div className="App">
      <Router>
        <Route exact path='/' component={Home} />
        {/* Jak */}
        <Route exact path='/users' component={Users}/>
        {/* David */}
        <Route path='/users/:userId' component={User}/>
        {/* Farhad */}
        <Route exact path='/users/:userId/tasks' component={UserTasks}/>
        {/* Test results routes */}
        <Route exact path='/reports/users/userid/tasks/taskid' component={UsersUserIdTasksTaskIdReport}/>
      </Router>
    </div>
  );
}

export default App;
