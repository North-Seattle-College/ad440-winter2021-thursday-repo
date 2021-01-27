import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';

var UserTasks = () => {
  const [userTasks, setUserTasks] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    // we should change this url to `https://nsc-functionsapp-team1.azurewebsites.net/api/${userId}/tasks?`
    // because this is the function app that gets updates get deployed to.
    fetch(`https://w21httptriggernataliatest.azurewebsites.net/api/${userId}/tasks?`)
      .then(response => response.json())
      .then(data => setUserTasks(data))
      .catch((error) => console.error(error))
  }, []);

  return (
    <div className='user-tasks-container'>
      <BootstrapTable 
        heatherItems={userTasks.length > 0 ? Object.keys(userTasks[0]) : []}
        rows={userTasks.length > 0 ? userTasks : []}
      />
    </div>
  )
}

export default UserTasks;