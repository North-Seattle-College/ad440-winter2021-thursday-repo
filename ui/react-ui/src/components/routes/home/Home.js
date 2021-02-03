import React from 'react';
import Container from 'react-bootstrap/esm/Container';

let Home = () => {
  let usersEndpoint = '/users';
  let userTasksEndpoint = '/users/{userId}/tasks';
  var userIdEndpoint = '/users/{userid}';

  //test results endpoints
  var TaskIdTestReport = 'reports/taskid';
  return (
    <Container className="text-center mt-5">
      <h2>Supported Endpoints:</h2>
      <hr/>
      <p>{usersEndpoint}</p>
      <p>{userIdEndpoint}</p>
      <p>{userTasksEndpoint}</p>

      <h2>Test Results Supported Endpoints</h2>
      <hr/>
      <p>{TaskIdTestReport}</p>

    </Container>

    
  )
}

export default Home;