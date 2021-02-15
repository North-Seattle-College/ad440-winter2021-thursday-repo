import React, { Component } from 'react';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton.js';

export default class Users extends Component {
	
	state = {
		isLoaded: false,
		users: []
	};

	async componentDidMount() {
		const url = 'https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users?';
		const response = await fetch(url);
		const usersData = await response.json();
		this.setState({
			users: usersData,
			isLoaded: true,
		});
	}

	render() {
		const { isLoaded, users } = this.state;
		if (!isLoaded) {
			return <Container>Loading...</Container>;
		} else {
			return (
        <>
          <BackButton />
          <Container>
            <h3>List of Users</h3>
            <Table striped bordered hover className="text-left">
              <thead>
              <tr>
                <th>User ID #</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
              </tr>
              </thead>
              {users.map((user) => (
              <tbody key={user._id}>
                <tr>
                <td>{user.userId}</td>
                <td>{user.firstName}</td>
                <td>{user.lastName}</td>
                <td>{user.email}</td>
                </tr>
              </tbody>
              ))}
            </Table>
          </Container>
        </>
			);
		}
	}
}