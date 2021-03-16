import './App.css';
import {BrowserRouter as Router, Route,} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
import Users from '../routes/users/UsersPaginated';
import UserSingleTask from '../routes/userSingleTask/UserSingleTask';
import TaskIdReport from '../routes/reports/taskIdReport/TaskIdReport';
import userIdReport from '../routes/reports/userIdReport/UserIdReport';
import usersReport from '../routes/reports/usersReport/UserReport';
import TasksReport from '../routes/reports/userIdReport/UserIdTasksReport'
import Create from '../routes/create/Create';
 
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
        {/* Allison */}
        <Route exact path='/users/:userId/tasks/:taskId' component={UserSingleTask}/>
    
        {/* Test results routes */}
        <Route exact path='/reports/taskId' component={TaskIdReport}/>
        <Route exact path='/reports/userId' component={userIdReport}/>
        <Route exact path='/reports/users' component={usersReport}/>
        <Route exact path='/reports/tasks' component={TasksReport}/>

        {/* Create user + task */}
        <Route exact path='/create' component={Create} />
      </Router>
    </div>
  );
}

export default App;