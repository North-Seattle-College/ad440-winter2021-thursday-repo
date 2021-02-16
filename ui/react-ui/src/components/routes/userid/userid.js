import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Container from 'react-bootstrap/esm/Container';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';
import PageTitle from '../../PageTitle/PageTitle.js'
import {is404} from '../../../utils.js';

const User = () => {
  let state = [{
    title: '...Loading', 
    subtitle: ''
  }];

  let [user, setUser] = useState(state);

  let {userId} = useParams();

  useEffect(() => {
    (async function getUser() {
      const response = await fetch(`https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/${userId}?`)
      if(response.ok) {
        const resJson = await response.clone().json();
        setUser([
          {
          title: `User ${resJson.userId}`,
          subtitle: `${resJson.firstName} ${resJson.lastName}`
          },
          response,
          resJson
        ])
      } else {
        setUser([
          {
          title: response.status,
          subtitle: response.statusText
          },
          response
        ])
      }
    })()
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
        ? <BootstrapTable heatherItems={Object.keys(user[2])} rows={user} /> 
        : <h3>User {userId} {user[0].subtitle}</h3>}
      </Container>
    </>
  )
}

export default User;