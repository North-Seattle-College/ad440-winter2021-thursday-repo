import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Container from 'react-bootstrap/esm/Container';

var User = () => {
  const [user, setUser] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    fetch(`https://nsc-functionsapp-team1.azurewebsites.net/api/users/${userId}`)
      .then(response => response.json())
      .then(data => setUser(data))
      .catch((error) => console.error(error))
  }, []);

  return (
    <Container className='user-tasks-container'>
        <h3> {user.firstname} {user.lastname} info</h3>
        <BootstrapTable 
         heatherItems={Object.keys(user)}
         rows={[user]}
        />
    </Container>
  )
}

export default User;