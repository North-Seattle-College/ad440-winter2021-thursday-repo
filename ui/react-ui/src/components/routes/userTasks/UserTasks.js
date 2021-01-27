import React, {useState, useEffect} from 'react';
import {useParams} from "react-router-dom";
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';

var UserTasks = () => {
  const [userTasks, setUserTasks] = useState([]);

  var {userId} = useParams();

  useEffect(() => {
    // thsi url is going to get replace with => https://nsc-functionsapp-team1.azurewebsites.net/api/{userId:int?}/tasks?
    // to get the API function's url you should go to the Azure portal
    fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
      .then(response => response.json())
      .then(data => setUserTasks(data))
      .catch((error) => console.error(error))
  }, []);

  // for now and untill we get the correct URL, I'm using this dummy data =>
  var dummyUserTasks = [
    {taskId: 1, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''},
    {taskId: 2, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''},
    {taskId: 3, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 1, completedDate: ''},
    {taskId: 5, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''},
    {taskId: 7, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''},
    {taskId: 11, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 1, completedDate: ''},
    {taskId: 19, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''},
    {taskId: 22, userId: 1, title: 'react', description: 'js', createdDate: '2021-05-07T05:46:38.0000000', dueDate: '', completed: 0, completedDate: ''}
  ]; 

  //after getting the URL, replace dummyUserTasks with userTasks
  return (
    <div className='user-tasks-container'>
      <Container>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>taskId</th>
              <th>userId</th>
              <th>title</th>
              <th>description</th>
              <th>createdDate</th>
              <th>dueDate</th>
              <th>completed</th>
              <th>completedDate</th>
            </tr>
          </thead>
          {dummyUserTasks.map(userTask => (
            <tbody key={userTask.taskId}>
              <tr >
                <td>{userTask.taskId}</td>
                <td>{userTask.userId}</td>
                <td>{userTask.title}</td>
                <td>{userTask.description}</td>
                <td>{userTask.createdDate}</td>
                <td>{userTask.dueDate}</td>
                <td>{userTask.completed}</td>
                <td>{userTask.completedDate}</td>
              </tr>
            </tbody>
          ))}
        </Table>
      </Container>
    </div>
  )
}

export default UserTasks;