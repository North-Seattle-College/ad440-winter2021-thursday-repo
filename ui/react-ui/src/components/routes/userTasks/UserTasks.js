import React, {useState, useEffect} from 'react';
import Container from 'react-bootstrap/esm/Container';
import {useParams} from "react-router-dom";
import BootstrapTable from '../../bootstrapTable/BootstrapTable.js';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';
import PageTitle from '../../PageTitle/PageTitle.js'
import {fetchSetTblState} from '../../../utils.js' 


const UserTasks = () => {
  let state = [{
    title: '...Loading', 
    subtitle: ''
  }];
  let [userTasks, setUserTasks] = useState(state);
  let {userId} = useParams();



  useEffect(() => {
    const response = fetchSetTblState(`users/${userId}/tasks`, setUserTasks)
    .catch((error) => console.error(error))
  }, [userId]);

  function deleteTask(taskId){
    const messages = this.state.messages.filter((_, index) => index !== i)
    this.setState({ messages });

  }

  return (
    <>
      <BackButton />
      <PageTitle title={userTasks[0].title} subtitle={userTasks[0].subtitle} />
      <Container>
      {userTasks.length > 2 
        ? <BootstrapTable heatherItems={Object.keys(userTasks[2][0])} rows={userTasks[2]} /> 
        : <h3>User {userId} Tasks Not Found</h3>
      }
      <button onClick={() => this.deleteTask()}>Delete Task</button>
      </Container>
    </>
  )
}



export default UserTasks;
