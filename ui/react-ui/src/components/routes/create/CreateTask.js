
import axios from 'axios';
import React, { Component, useState, useRef } from 'react';
import { NavLink } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Form from 'react-bootstrap/Form'
import './Create.css';



function CreateTask() {
    grabURLid();
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
        if (response.status !== 201) { 
            throw new Error(`Request failed: ${response.status}`);
        }
    }



     function grabURLid() {

            let url_str = 'http://localhost:3000/users/1/tasks';
            let url = new URL(url_str);
            let hrefUrl = url.href
            let jsonUrl = JSON.stringify(hrefUrl);
            let splitUrl = jsonUrl.split("/")
            console.log(splitUrl)


         //   console.log(url2)
       
            // let search_params = url.searchParams; 
            // console.log(search_params.getAll(''));
}


    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await saveFormData();
            alert('Task input complete');
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
            alert(`Creating a task has failed. ${e.message}`);
        }
    }

    return (
        
        <form className="taskForm" onSubmit={handleSubmit}>
        <NavLink to={`/`} onClick={null}>
                    <Button variant="outline-primary" size="sm">Home</Button>
                </NavLink>
            <h2>Create Task</h2>

            <label>taskId: &nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.taskId} onChange={set('taskId')}
                />
            </label>

            <label>userId: &nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.userId} onChange={set('userId')}
                />
            </label>

            <label>title: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.title} onChange={set('title')}
                />
            </label>

            <label>description: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.description} onChange={set('description')}
                />
            </label>

            <label>createdDate: &nbsp;&nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.createdDate} onChange={set('createdDate')}
                />
            </label>
            <label>duedate: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.duedate} onChange={set('duedate')}
                />
            </label>
            <label>completed: &nbsp;&nbsp;&nbsp;
            <input
                    type="text" required
                    value={values.completed} onChange={set('completed')}
                />
            </label>
            <label>completedDate: &nbsp;&nbsp;&nbsp;
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