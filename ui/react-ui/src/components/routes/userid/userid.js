import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Container from 'react-bootstrap/esm/Container';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';
import PageTitle from '../../PageTitle/PageTitle.js'
import {fetchSetTblState} from '../../../utils.js';

const User = () => {
  let state = [{
    title: '...Loading', 
    subtitle: ''
  }];
  
  let [user, setUser] = useState(state);

  const {userId} = useParams();

  useEffect(() => {
    const response = fetchSetTblState('users', setUser, userId)
    .catch((error) => {
      console.error(error)
    });
  }, [userId]);
  

  return (
    <>
      <BackButton />
      <PageTitle title={user[0].title} subtitle={user[0].subtitle} />
      <Container>
      {user.length > 2 
        ? <BootstrapTable heatherItems={Object.keys(user[2])} rows={[user[2]]} /> 
        : <h3>User {userId} {user[0].subtitle}</h3>
      }
      </Container>
    </>
  )
}

export default User;