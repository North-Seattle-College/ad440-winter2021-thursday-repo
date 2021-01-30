import React from 'react';

var Home = () => {
  var userTasksEndpoint = '/users/{userId}/tasks';
  
  return (
    <div>
      <h2>Supported Endpoints:</h2>
      <li>{userTasksEndpoint}</li>
    </div>
  )
}

export default Home;