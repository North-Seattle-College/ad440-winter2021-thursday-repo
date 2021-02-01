import React from 'react';
import Container from 'react-bootstrap/esm/Container';
import OverlayTrigger from 'react-bootstrap/esm/OverlayTrigger';
import Tooltip from 'react-bootstrap/esm/Tooltip';
import {useHistory} from "react-router-dom";

let Home = () => {
  const history = useHistory();

  let endpoints = ['/users', '/users/{userId}/tasks'];
  let containerStyle = {display: 'flex', justifyContent: 'center'};
  let endpointStyle = {cursor: 'pointer', minWidth: '15rem'};

  return (
    <Container className="text-center mt-5">
      <h2>Supported Endpoints:</h2>
      <hr/>
      {endpoints.map(endpoint => {
        let endpointHistory = endpoint;  
           
        if (endpoint === '/users/{userId}/tasks') endpointHistory = '/users/2/tasks';

        return (
          <div style={containerStyle}>
            <OverlayTrigger overlay={<Tooltip id="tooltip-left">Click to Trigger</Tooltip>} placement='left'>
              <p key={endpoint} onClick={() => history.push(endpointHistory)} style={endpointStyle}>{endpoint}</p>
            </OverlayTrigger>
          </div>

        )
      })}
    </Container>
  )
}

export default Home;