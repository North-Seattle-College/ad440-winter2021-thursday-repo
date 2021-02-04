import './App.css';
import {BrowserRouter as Router, Route,} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
import Users from '../routes/users/Users';
import UserSingleTask from '../routes/userSingleTask/UserSingleTask';
import userIdReport from '../routes/reports/userIdReport/UserIdReport';
 
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
        <Route exact path='/reports/userId' component={userIdReport}/>
      </Router>
    </div>
  );
}

export default App;
