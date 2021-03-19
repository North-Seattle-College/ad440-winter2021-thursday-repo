import React,{ useEffect, useState } from 'react';

import axios from 'axios';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator';
import * as ReactBootStrap from 'react-bootstrap';
import { ToastMessage } from './ToastMessage';
import { ConfirmDeleteUserModal } from './ConfirmDeleteUserModal';
import { Trash } from 'react-bootstrap-icons';

const UsersPaginated = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [userToDelete, setUserToDelete] = useState();
    const [toastMessage, setToastMessage] = useState();
    
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
        {dataField: "email", text: "Email"},
        
    ]

    const handleDelete = (userId) => {
      const url = 'https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/users/' + userId
      console.log("delete user request: " + url);
  
      fetch(url, {
        method: 'DELETE',
      })
      .then(response => {
        if (!response.ok) {
          response.text().then(text => {
            let msg = `Delete request Error!: ${text}`;
            console.log(msg);  
            setToastMessage( msg);
            setUserToDelete();
          })
        } else {
          setToastMessage( "Deleted userId: " + userId + " successfully!");
          setUserToDelete();
          setUsers(removeUserFromList(userId)); 
        }
      });
    }

    const  removeUserFromList = (id) =>{ 
        return users.filter(function(user){ 
              return user.userId !== id; 
          });
      }

    const  handleClose = () => {
        setUserToDelete();
        console.log("dialouge closed");
      }
    
    const closeToast = () => {
        setToastMessage();
        console.log("toast closed");
      }
    

    useEffect(()=>{ 
        getUserData();
    }, []);

    const selectRow = {
      mode: 'radio',
      clickToSelect: true,
      onSelect:(row) => setUserToDelete(row),
      headerColumnStyle: {width: '70px'},
      selectColumnStyle: {textAlign: 'center'},
      selectionHeaderRenderer: ({mode, checked, indeterminate}) => {
        return (<span>Delete</span>)
      },
      selectionRenderer: ({ mode, checked, disabled }) => {
        return (<Trash/>)
      }
    };

    return <div className="pagination" >
      
        {loading? (
            <div
            aria-live="polite"
            aria-atomic="true"
            style={{
              position: 'relative',
              minHeight: '100px',
            }}
          >
            {
            toastMessage ? 
            ( <ToastMessage 
                message={toastMessage}
                closeToast={closeToast}/>)
                : null
            }
            {
            userToDelete ? 
              <ConfirmDeleteUserModal 
                user={userToDelete}
                handleClose={handleClose}
                handleDelete={handleDelete}/> 
              : null
            }
              <div className="table-wrapper" >
                <BootstrapTable 
                  rowStyle={ { backgroundColor: 'white' } }
                      selectRow = {selectRow}
                      className="table"
                      keyField="userId"
                      data={users}
                      columns={columns}
                      pagination={paginationFactory()}/>
              </div>
            </div>
        ): (<ReactBootStrap.Spinner animation="border"/>)}
    </div>
            
                   
};


export default UsersPaginated;