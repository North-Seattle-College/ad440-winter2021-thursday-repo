
import axios from 'axios';
import React, { Component, useState, useRef } from 'react';
import { NavLink } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Form from 'react-bootstrap/Form'
import './Create.css';


/*              taskId: '',
             userId: '',
             title: '',
             description: '',
             createdDate: '',
             duedate: '',
             completed: '',
             completedDate: ''


    changerHandler = (e) => {
        this.setState({[e.target.name]: e.target.value })

 https://nsc-func-dev-usw2-thursday.azurewebsites.net/api/users/:userId/task
    
    submitHandler = (e) => {
        e.preventDefault()
        console.log(this.state)
        axios.post('https://jsonplaceholder.typicode.com/posts', this.state)
        .then(response =>{


            userId: '',
            title: '',
            body: ''


             <label>userId: &nbsp;
            <input
                    type="text" required
                    value={values.userId} onChange={set('userId')}
                />
            </label>
            <label>title: &nbsp;
            <input
                    type="text" required
                    value={values.title} onChange={set('title')}
                />
            </label>
            <label>body: &nbsp;
            <input
                    type="text" required
                    value={values.body} onChange={set('body')}
                />
            </label>










 */


// userId": 1,
// "id": 1,
// "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
// "body

function CreateTask() {
    const [values, setValues] = useState({
        taskId: '',
        userId: '',
        title: '',
        description: '',
        createdDate: '',
        duedate: '',
        completed: '',
        completedDate: ''
    });

    const onChange = (event) => {
        setValues(event.target.value);
    };

    const set = name => {
        return ({ target: { value } }) => {
            setValues(oldValues => ({ ...oldValues, [name]: value }));
        }
    };

    const saveFormData = async () => {
        console.log(JSON.stringify(values));
        const response = await fetch('https://jsonplaceholder.typicode.com/posts', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(values)
        });
        if (response.status !== 200) {
            throw new Error(`Request failed: ${response.status}`);
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await saveFormData();
            alert('Your task has successfully been entered!');
            setValues({
                taskId: '',
                userId: '',
                title: '',
                description: '',
                createdDate: '',
                duedate: '',
                completed: '',
                completedDate: ''
            });
        } catch (e) {
            alert(`Task creation failed! ${e.message}`);
        }
    }

    return (
        
        <form className="taskForm" onSubmit={handleSubmit}>
        <NavLink to={`/`} onClick={null}>
                    <Button variant="outline-primary" size="sm">Home</Button>
                </NavLink>
            <h2>Create Task</h2>

            <label>taskId: &nbsp;
            <input
                    type="text" required
                    value={values.taskId} onChange={set('taskId')}
                />
            </label>

            <label>userId: &nbsp;
            <input
                    type="text" required
                    value={values.userId} onChange={set('userId')}
                />
            </label>

            <label>title: &nbsp;
            <input
                    type="text" required
                    value={values.title} onChange={set('title')}
                />
            </label>

            <label>description: &nbsp;
            <input
                    type="text" required
                    value={values.description} onChange={set('description')}
                />
            </label>

            <label>createdDate: &nbsp;
            <input
                    type="text" required
                    value={values.createdDate} onChange={set('createdDate')}
                />
            </label>
            <label>duedate: &nbsp;
            <input
                    type="text" required
                    value={values.duedate} onChange={set('duedate')}
                />
            </label>
            <label>completed: &nbsp;
            <input
                    type="text" required
                    value={values.completed} onChange={set('completed')}
                />
            </label>
            <label>completedDate: &nbsp;
            <input
                    type="text" required
                    value={values.completedDate} onChange={set('completedDate')}
                />
            </label>

            <button className="taskButton" variant="outline-primary" type="submit">Submit</button>
        </form>
    );
}

export default CreateTask;