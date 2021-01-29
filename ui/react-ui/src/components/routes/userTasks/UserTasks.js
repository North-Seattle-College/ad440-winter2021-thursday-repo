import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';

var UserTasks = () => {
  const [userTasks, setUserTasks] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    // url should be replaced with => https://nsc-functionsapp-team1.azurewebsites.net/api/${userId}/tasks?
    fetch(`https://w21httptriggernataliatest.azurewebsites.net/api/${userId}/tasks?`)
    .then(response => response.json())
    .then(data => setUserTasks(data))
    .catch((error) => console.error(error))

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className='user-tasks-container'>
      <h3>all tasks for user with userId {userId}</h3>
      {userTasks.length > 0 ? 
        <BootstrapTable 
          heatherItems={userTasks.length > 0 ? Object.keys(userTasks[0]) : []}
          rows={userTasks.length > 0 ? userTasks : []}
        /> :
        <h4>there is no task for this user</h4>
      }
    </div>
  )
}

export default UserTasks;