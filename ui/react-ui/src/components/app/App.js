import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
import Users from '../routes/users/Users';
import userIdReport from '../routes/reports/userIdReport/UserIdReport';
import TasksReport from '../routes/reports/userIdReport/UserIdTasksReport';
 
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
        <Route exact path='/reports/userId' component={userIdReport}/>
        <Route exact path='/report/users/{user_id}/tasks' component={TasksReport}/>
      </Router>
    </div>
  );
}

export default App;
