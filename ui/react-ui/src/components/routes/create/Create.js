import React, { useState, useRef } from 'react';
import { NavLink } from "react-router-dom";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import './Create.css';

const Create = () => {

    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [validated, setValidated] = useState();
    const [userCreateSuccess, setUserCreateSuccess] = useState(false);
    const [isVisible, setIsVisible] = useState(false);

    const formRef = useRef(null);

    const handleChange = (e) => {
        const fieldName = e.target.name;
        const fieldValue = e.target.value;

        // Save fields to state
        if (fieldName === 'firstName') {
            setFirstName(fieldValue);
        } else if (fieldName === 'lastName') {
            setLastName(fieldValue);
        } else if (fieldName === 'email') {
            setEmail(fieldValue);
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const form = formRef.current;

        // Form is invalid
        if (form.checkValidity() === false) {
            setValidated(true);
        } 
        // Form is good to go
        else {
            await createUser(); // Call function to create user
            form.reset();
        }
    }

    const createUser = async () => {
        const body = { firstName, lastName, email };
        await fetch('https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/', {
            method: 'post', 
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        }).then((response) => {
            setIsVisible(true);
            // User has been created succsesfully
            if (response.status === 200 || response.status === 201) { // Can also use created user response userId instead
                setUserCreateSuccess(true);
            } 
            // There was an error creating the user
            else {
                setUserCreateSuccess(false);
            }
        });
        //// Alternative if using userId of created user instead of response code
        // .then((response) => {
        //     response.json()
        //         .then((data) => {
        //             console.log(data.userId)
        //         })
    }
        return (
            <div className="formContainer">
                <NavLink to={`/`} onClick={null}>
                    <Button variant="outline-primary" size="sm">Home</Button>
                </NavLink>
                <Alert show={isVisible} dismissible variant={userCreateSuccess ? "success" : "danger"} onClose={() => setIsVisible(false)}>
                    {userCreateSuccess ? <Alert.Heading>User Successfully Created</Alert.Heading> : <Alert.Heading>Error Creating User</Alert.Heading> }
                </Alert>
                <h2 className='title'>Create User</h2>
                <Form noValidate validated={validated} onSubmit={handleSubmit} onChange={handleChange} ref={formRef}>
                    <Form.Group>
                        <Form.Label>First Name: </Form.Label>
                        <Form.Control required as="input" type="text" placeholder="John" name="firstName" />
                        <Form.Control.Feedback type="invalid">
                            Invalid First Name
                        </Form.Control.Feedback>
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Last Name: </Form.Label>
                        <Form.Control required as="input" type="text" placeholder="Smith"  name="lastName" />
                        <Form.Control.Feedback type="invalid">
                            Invalid Last Name
                        </Form.Control.Feedback>
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Email: </Form.Label>
                        <Form.Control required type="email" placeholder="test@example.com"  name="email" />
                        <Form.Control.Feedback type="invalid">
                            Invalid Email
                        </Form.Control.Feedback>
                    </Form.Group>
                    <Button variant="primary" type="submit">
                        Create
                    </Button>
                </Form>
            </div>
        )
}

export default Create;