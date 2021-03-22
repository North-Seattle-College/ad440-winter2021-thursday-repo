import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import ToastHeader from 'react-bootstrap/ToastHeader'
import ToastBody from 'react-bootstrap/ToastBody'
import Button from 'react-bootstrap/Button';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';
import { ToastMessage } from './ToastMessage';
import { ConfirmDeleteUserModal } from './ConfirmDeleteUserModal';

export default class Users extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoaded: false,
      users: [],
      userToDelete: null,
      toastMessage: ""
    };
    this.closeToast = this.closeToast.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }

	async componentDidMount() {
		const url = 'https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users';
		const response = await fetch(url);
		const usersData = await response.json();

		this.setState({
			users: usersData,
			isLoaded: true,
		});
	}

  showDeleteUserConfirmation(user){
    this.setState({userToDelete: user});
  }

  handleDelete(userId) {
    const url = 'https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/' + userId
    console.log("delete user request: " + url);

    fetch(url, {
      method: 'DELETE',
    })
    .then(response => {
      if (!response.ok) {
        response.text().then(text => {
          let msg = `Delete request Error!: ${text}`;
          console.log(msg)  
          this.setState({
            toastMessage: msg,
            userToDelete: null,
          })
        })
      } else {
        this.setState({
          userToDelete: null,
          users: this.removeUserFromList(userId),
          toastMessage: "Deleted userId: " + userId + " successfully!"
        });  
      }
    });
  }

  removeUserFromList(id) { 
    return this.state.users.filter(function(user){ 
          return user.userId !== id; 
      });
  }

  handleClose() {
    this.setState({userToDelete: null});
    console.log("dialouge closed");
  }

  closeToast() {
    this.setState({toastMessage: ""});
    console.log("toast closed");
  }

	render() {
		const { isLoaded, users } = this.state;
		if (!isLoaded) {
			return <Container>Loading...</Container>;
		} else {
			return (
        <>
            <div
              aria-live="polite"
              aria-atomic="true"
              style={{
                position: 'relative',
                minHeight: '100px',
              }}
            >
            {this.state.toastMessage ? 
              (<ToastMessage 
                message={this.state.toastMessage}
                closeToast={this.closeToast}/>)
              : null
            }
          <BackButton />
          <Container>
          {
            this.state.userToDelete ? 
            <ConfirmDeleteUserModal 
              user={this.state.userToDelete}
              handleClose={this.handleClose}
              handleDelete={this.handleDelete}/> 
            : null
          }

            <h3>List of Users</h3>
            <Table striped bordered hover className="text-left">
              <thead>
              <tr>
                <th>User ID #</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
                <th>Remove User</th>
              </tr>
              </thead>
              {users.map((user) => (
                <tbody key={user._id}>
                  <tr>
                  <td>{user.userId}</td>
                  <td>{user.firstName}</td>
                  <td>{user.lastName}</td>
                  <td>{user.email}</td>
                  <td><Button onClick={() => this.showDeleteUserConfirmation(user)}>delete</Button></td>
                  </tr>
                </tbody>
                ))}
            </Table>
          </Container>
          </div> 
        </>
			);
		}
	}
}


