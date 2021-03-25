import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator'
import * as ReactBootStrap from 'react-bootstrap';
import { fetchSetTblState } from '../../../utils';
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

    const getData = async (userId)=>{
        try{
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

    return (
        <div className="pagination">
            {loading
                ?(
                    <div className="table-wrapper">
                        <BootstrapTable
                            rowStyle = {{backgroundColor: 'white'}}
                            className="table"
                            keyField="taskId"
                            data={userTasks}
                            columns={columns}
                        />
                    </div>
                ): (<ReactBootStrap.Spinner animation="border" />)}
        </div>
    )
}

export default UserTasksPaginated;