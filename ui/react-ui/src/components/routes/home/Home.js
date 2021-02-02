import React from 'react';

var Home = () => {
  var userTasksEndpoint = '/users/{userId}/tasks';
  
  var userIdEndpoint = '/users/{userid}';

  return (
    <div className='home-container'>
      <h2>Supported Endpoints:</h2>
      <li>{userTasksEndpoint}</li>
      <li>{userIdEndpoint}</li>
    </div>
  )
}

export default Home;