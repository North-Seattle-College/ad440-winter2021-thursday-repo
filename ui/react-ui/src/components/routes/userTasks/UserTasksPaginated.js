import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator'
import * as ReactBootStrap from 'react-bootstrap';
import { fetchSetTblState } from '../../../utils';

const UserTasksPaginated = () => {
    let [userTasks, setUserTasks] = useState([]);
    let [loading, setLoading] = useState(false);
    let {userId} = useParams();

    useEffect(() => {
        try{
            const response = fetchSetTblState(`users/${userId}/tasks`, setUserTasks)
            setLoading(true)
        } catch (error) {
            console.error(error);
        }
    }, [userId]);

    return (
        <div className="pagination">
            {loading
                ?(
                    <div><pre>{JSON.stringify(userTasks, null, 5)}</pre></div>
                ): (<ReactBootStrap.Spinner animation="border" />)}
        </div>
    )
}

export default UserTasksPaginated;