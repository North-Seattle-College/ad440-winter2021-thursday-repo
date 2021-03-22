import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/esm/Container';
import { useParams } from "react-router-dom";
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';
import PageTitle from '../../PageTitle/PageTitle.js'
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import {fetchSetTblState} from '../../../utils.js'

let UserSingleTask = () => {
  let state = [{
    title: '...Loading', 
    subtitle: ''
  }];
  let [userSingleTask, setUserSingleTask] = useState(state);

  let { userId, taskId } = useParams();

  useEffect(() => {
    const response = fetchSetTblState(`users/${userId}/tasks/`, setUserSingleTask, taskId)
    .catch((error) => console.error(error))
  }, [userId, taskId]);



  return (
    <>
      <BackButton />
      <PageTitle title={userSingleTask[0].title} subtitle={userSingleTask[0].subtitle} />
      <Container>
      {userSingleTask.length > 2 
        ? <BootstrapTable heatherItems={Object.keys(userSingleTask[2])} rows={[userSingleTask[2]]} /> 
        : <h3>User {userId} Tasks Not Found</h3>
      }
      </Container>
    </>
  )
}

export default UserSingleTask;
