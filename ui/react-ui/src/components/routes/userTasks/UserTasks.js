import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';

var UserTasks = () => {
  const [userTasks, setUserTasks] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    fetch(`https://nsc-functionsapp-team1.azurewebsites.net/api/${userId}/tasks?`)
    .then(response => response.json())
    .then(data => setUserTasks(data))
    .catch((error) => console.error(error))

    // eslint-disable-next-line react-hooks/exhaustive-deps
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