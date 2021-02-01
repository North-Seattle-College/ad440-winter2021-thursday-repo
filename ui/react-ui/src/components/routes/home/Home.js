import React from 'react';
import Container from 'react-bootstrap/esm/Container';
import {useHistory} from "react-router-dom";

var Home = () => {
  const history = useHistory();

  let endpoints = ['/users', '/users/{userId}/tasks'];
  
  return (
    <Container className="text-center mt-5">
      <h2>Supported Endpoints:</h2>
      <hr/>
      {endpoints.map(endpoint => {
        let endpointHistory = endpoint;     
        if (endpoint === '/users/{userId}/tasks') endpointHistory = '/users/2/tasks';

        return <p key={endpoint} onClick={() => history.push(endpointHistory)} style={{cursor: 'pointer'}}>{endpoint}</p>
      })}
    </Container>
  )
}

export default Home;