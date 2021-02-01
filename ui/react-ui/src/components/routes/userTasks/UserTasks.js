import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/esm/Container';
import {useParams, useHistory} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Button from 'react-bootstrap/Button';



var UserTasks = () => {
  var [userTasks, setUserTasks] = useState(['loading']);

  var {userId} = useParams();
  const history = useHistory();

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
      <Button variant="dark" style={{marginLeft: '1rem', marginBottom: '2rem'}} onClick={() => history.push('/')}>Back to Home</Button>
      <Container>
        <h3>All Tasks for user with userId {userId}</h3>
        {tasks}
      </Container>
    </>
  )
}

export default UserTasks;