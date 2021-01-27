import './App.css';
import {BrowserRouter as Router, Route} from 'react-router-dom'; 
import UserTasks from '../routes/userTasks/UserTasks.js';

function App() {
  return (
    <div className="App">
      <Router>
        {/* Jak */}
        {/* <Route path='/users/' component={}/> */}
        {/* David */}
        {/* <Route path='/users/:userId' component={UserTasks}/> */}
        {/* Farhad */}
        <Route path='/users/:userId/tasks' component={UserTasks}/>
      </Router>
    </div>
  );
}

export default App;
