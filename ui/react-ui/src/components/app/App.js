import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';
import Home from '../routes/home/Home.js';
import User from '../routes/userid/userid.js';
 
function App() {
  return (
    <div className="App">
      <Router>
        <Route path='/' exact component={Home} />
        {/* Jak */}
        {/* <Route path='/users/' component={}/> */}
        {/* David */}
        <Route path='/users/:userId' component={User}/>
        {/* Farhad */}
        <Route path='/users/:userId/tasks' component={UserTasks}/>
      </Router>
    </div>
  );
}

export default App;
