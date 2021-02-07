import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Container from 'react-bootstrap/esm/Container';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';

var User = () => {
  const [user, setUser] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    fetch(`https://nsc-functionsapp-team1.azurewebsites.net/api/users/${userId}?`)
      .then(response => response.json())
      .then(data => {
        var updatedData = {};

        if (Object.keys(data).length > 0) Object.keys(data).forEach(key => updatedData[key.toLowerCase()] = data[key]);
        
        setUser(updatedData);
      })
      .catch((error) => console.error(error))

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <BackButton />
      <Container className='user-tasks-container'>
          <h3> {user.firstname} {user.lastname} info</h3>
          {
            user.userid ? 
            <BootstrapTable heatherItems={Object.keys(user)} rows={[user]} /> : 
            <Container>...loading</Container>
          }
      </Container>
    </>
  )
}

export default User;