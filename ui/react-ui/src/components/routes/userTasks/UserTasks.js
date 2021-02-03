import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/esm/Container';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';

var UserTasks = () => {
  var [userTasks, setUserTasks] = useState(['loading']);
  var {userId} = useParams();

  useEffect(() => {
    setUserTasks(['loading']);

    fetch(`https://nsc-functionsapp-team1.azurewebsites.net/api/users/${userId}/tasks?`)
    .then(response => response.json())
    .then(data => setUserTasks(data))
    .catch((error) => console.error(error))

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  var tasks;

  if (userTasks[0] === 'loading') tasks = <Container>...loading</Container>;
  else {
    if (userTasks.length > 0) {
      tasks = <BootstrapTable heatherItems={Object.keys(userTasks[0])} rows={userTasks} />;
    }
    else tasks = <h5>There is no task for this user</h5>;
  }

  return (
    <>
      <BackButton />
      <Container>
        <h3>All Tasks for user with userId {userId}</h3>
        {tasks}
      </Container>
    </>
  )
}

export default UserTasks;