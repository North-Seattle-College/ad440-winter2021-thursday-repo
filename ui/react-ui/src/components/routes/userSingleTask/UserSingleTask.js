import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/esm/Container';
import { useParams } from "react-router-dom";
import Table from 'react-bootstrap/Table';

var UserSingleTask = () => {
  const [userSingleTask, setUserSingleTask] = useState([]);

  var { userId, taskId } = useParams();
  console.log(userId, taskId)

  useEffect(() => {
    fetch(`https://nsc-functionsapp-team1.azurewebsites.net/api/users/${userId}/tasks/${taskId}`)
    .then(response => response.json())
    .then(data => setUserSingleTask(data))
    .catch((error) => console.error(error))
  }, [userId, taskId]);

  return (
    <Container>
      <h3>Selected task</h3>
      <Table striped bordered hover className="text-left">
        <thead>
          <tr>
            <th>Task ID #</th>
            <th>Task Description</th>
          </tr>
        </thead>
          <tbody>
          <tr>
            <td>{ taskId }</td>
            <td>{ userSingleTask.description }</td>
          </tr>
        </tbody>
      </Table>
    </Container>
  )
}

export default UserSingleTask;
