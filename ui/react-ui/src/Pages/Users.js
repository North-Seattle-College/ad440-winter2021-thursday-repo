import React, {Component} from 'react'

class Users extends Component{

    constructor(props){
      super(props)
      this.state={
        users:[],
        isLoading:false,
        isError: false
      }
    }
    // Async function to get request 
    async componentDidMount(){
      this.setState({isLoading:true})
      const response = await fetch("https://nate-temp-bucket.s3-us-west-2.amazonaws.com/nate_sample.json")
      if(response.ok){
        const users = await response.json()
        console.log(users)
        this.setState({users, isLoading:false})
      }else{
        this.setState({isError:true, isLoading:false})
      }
    }

    renderTableHeader= () => {
      return Object.keys(this.state.users[0]).map(attr=><th key = {attr}>
        {attr.toUpperCase()}
      </th>)
      
    }

    renderTableRows = () =>{
      return this.state.users.map(user=>{
        return(
          <tr key={user.userId}>
            <td>{user.userId}</td>
            <td>{user.firstName}</td>
            <td>{user.lastName}</td>
            <td>{user.email}</td>

          </tr>
        )
      })
    }

    render(){
      const {users, isLoading, isError} = this.state
      if(isLoading){
        return <div>Loading...</div>
      }
      
      if(isError){
        return <div>Error...</div>
      }

      return users.length > 0
      ?(
        <table>
          <thead>
            <tr>{this.renderTableHeader()}</tr>
          </thead>
          <tbody>{this.renderTableRows()}</tbody>
        </table>

      ):(
        <div>No Users</div>
      )
    }
}

export default Users;