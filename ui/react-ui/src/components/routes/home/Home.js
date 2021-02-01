import React from 'react';
import Container from 'react-bootstrap/esm/Container';

let Home = () => {
  let usersEndpoint = '/users';
  let userTasksEndpoint = '/users/{userId}/tasks';
  
  return (
    <Container className="text-center mt-5">
      <h2>Supported Endpoints:</h2>
      <hr/>
      <p>{usersEndpoint}</p>
      <p>{userTasksEndpoint}</p>
    </Container>
  )
}

export default Home;