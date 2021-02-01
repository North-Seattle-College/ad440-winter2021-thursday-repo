import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import Users from '../routes/users/Users';
import UserSingleTask from '../routes/userSingleTask/UserSingleTask';
 
function App() {
  return (
    <div className="App">
      <Router>
        <Route exact path='/' component={Home} />
        {/* Jak */}
        <Route exact path='/users' component={Users}/>
        {/* David */}
        {/* <Route path='/users/:userId' component={UserTasks}/> */}
        {/* Farhad */}
        <Route exact path='/users/:userId/tasks' component={UserTasks}/>
        {/* Allison */}
        <Route exact path='/users/:userId/tasks/:taskId' component={UserSingleTask}/>
      </Router>
    </div>
  );
}

export default App;
