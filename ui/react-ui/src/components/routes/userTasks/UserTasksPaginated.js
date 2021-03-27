import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import BackButton from '../../bootstrapBackButton/BootstrapBackButton'
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator'
import * as ReactBootStrap from 'react-bootstrap';
import axios from 'axios';

const UserTasksPaginated = () => {
    let [userTasks, setUserTasks] = useState([]);
    let [loading, setLoading] = useState(false);
    let {userId} = useParams();

    const columns = [
        {dataField: "taskId", text: "Task ID"},
        {dataField: "title", text: "Task"},
        {dataField: "description", text: "Description"},
        {dataField: "createdDate", text: "Date Created"},
        {dataField: "dueDate", text: "Due Date"},
        {dataField: "completed", text: "Is Complete"},
        {dataField: "completedDate", text: "Date Completed"}
    ]

    // TODO:
    // Add options to delete a task
    // sort of present in original UserTasks.js but didn't really work

    const getData = async (userId)=>{
        try{
            /*
             * I wanted to use the fetchTableState from ../../utils
             * But it just returned the data in a really unhelpful way with an incorrect
             * "title" and "subtitle" tacked onto the front  
             */
            const data = await axios.get(
                `https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/${userId}/tasks`
            );
            console.log(data);
            setUserTasks(data.data);
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        getData(userId);
        setLoading(true);
    }, [userId]);

    // TODO:
    // Table spacing is bad in narrow windows

    return (
        <div className="pagination">
            <div><BackButton /></div>
            {loading
                ?(
                    <div className="table-wrapper">
                        <BootstrapTable
                            rowStyle = {{backgroundColor: 'white'}}
                            className="table"
                            keyField="taskId"
                            data={userTasks}
                            columns={columns}
                            pagination={paginationFactory()}
                        />
                    </div>
                ): (<ReactBootStrap.Spinner animation="border" />)}
        </div>
    )
}

export default UserTasksPaginated;