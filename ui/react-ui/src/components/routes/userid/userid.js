import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import Container from 'react-bootstrap/esm/Container';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';

var User = () => {
  let [user, setUser] = useState(['loading']);

  var {userId} = useParams();

  useEffect(() => {
    setUser('loading');

    fetch(`https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/${userId}?`)
      .then((response) => {
        if(response.ok) {
          response = response.json();
        }
        return response
      })
      .then((data) => {
        setUser([data]);
      })
      .catch((error) => {
        console.error(error)
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  let userTable;

  if (user[0] === 'loading') userTable = <Container>...loading</Container>;
  else {
    if (user[0].userId) {
      userTable = <BootstrapTable heatherItems={Object.keys(user[0])} rows={user} />;
    }
  }

  return (
    <>
      <BackButton />
      <Container>
        <h3> {user.firstname} {user.lastname} info</h3>
        {userTable}
      </Container>
    </>
  )
}

export default User;