import React,{ useEffect, useState } from 'react';

import axios from 'axios';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator';
import * as ReactBootStrap from 'react-bootstrap';


const UsersPaginated = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const getUserData = async ()=>{
        try {
            const data = await axios.get(
                "https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users"
            );
            console.log(data)
            setUsers(data.data)
            setLoading(true)
        } catch (e) {
            console.log(e);
            
        }
    };

    const columns = [
        {dataField: "userId", text: "ID"},
        {dataField: "firstName", text: "First Name"},
        {dataField: "lastName", text: "Last Name"},
        {dataField: "email", text: "Email"}
        
    ]

    useEffect(()=>{ 
        getUserData();
    }, []);

    return <div className="pagination" >
      
        {loading? (
            <div className="table-wrapper" >
                <BootstrapTable 
                rowStyle={ { backgroundColor: 'white' } }
          
                    className="table"
                    keyField="userId"
                    data={users}
                    columns={columns}
                    pagination={paginationFactory()}/>
            </div>

        ): (<ReactBootStrap.Spinner animation="border"/>)}
    </div>
           
};


export default UsersPaginated;