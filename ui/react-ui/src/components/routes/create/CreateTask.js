
import axios from 'axios';
import React, { Component } from 'react';
import { NavLink } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import './Create.css';



// const Create = () => {

//     const [firstName, setFirstName] = useState();
//     const [lastName, setLastName] = useState();
//     const [email, setEmail] = useState();
//     const [validated, setValidated] = useState();
//     const [userCreateSuccess, setUserCreateSuccess] = useState(false);
//     const [isVisible, setIsVisible] = useState(false);
// };

class CreateTask extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
             taskId: '',
             userId: '',
             title: '',
             description: '',
             createdDate: '',
             duedate: '',
             completed: '',
             completedDate: ''

        }
    }

    changerHandler = (e) => {
        this.setState({[e.target.name]: e.target.value })

    }
    
    submitHandler = (e) => {
        e.preventDefault()
        console.log(this.state)
        axios.post('https://jsonplaceholder.typicode.com/posts', this.state)
        .then(response =>{
            console.log(response)
        })
        .catch(error =>{
            console.log(error)
        })
    }
    

    render() {
        const { taskId, userId, title, description, createdDate, duedate, completed, completedDate} = this.state
        return (
            <div className="formContainer">
                <NavLink to={`/`} onClick={null}>
                    <Button variant="outline-primary" size="sm">Home</Button>
                </NavLink>
            
            <div>
             <form onSubmit={this.submitHandler}>
                <div>
                    <input type="text" 
                    name='taskId' 
                    value= {taskId}
                    onChange={this.changerHandler} />
                </div>
                <div>
                    <input type="text" 
                    name='userId' 
                    value= {userId}
                    onChange={this.changerHandler} />
                </div>
                <div>
                    <input type="text" 
                    name='title' 
                    value= {title}
                    onChange={this.changerHandler}  />
                </div>
                <div>
                    <input type="text" 
                    name='description' 
                    value= {description}
                    onChange={this.changerHandler}  />
                </div>
                <div>
                    <input type="text" 
                    name='createdDate' 
                    alue= {createdDate}
                    onChange={this.changerHandler}  />
                </div>
                <div>
                    <input type="text"  
                    name='duedate' 
                    value= {duedate}
                    onChange={this.changerHandler}  />
                </div>
                <div>
                    <input type="text"  
                    name='completed' 
                    value= {completed}
                    onChange={this.changerHandler}  />
                </div>
                <div>
                    <input type="text"  
                    name='completedDate' 
                    value= {completedDate}
                    onChange={this.changerHandler}  />
                </div>
                <button type="submit">Submit</button>
             </form>                
            </div>
            </div>
        )
    }
}

export default CreateTask
