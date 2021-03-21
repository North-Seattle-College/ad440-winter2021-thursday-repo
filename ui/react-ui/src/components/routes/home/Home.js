import React from 'react';
import Alert from 'react-bootstrap/esm/Alert';
import Button from 'react-bootstrap/Button';
import { withRouter, NavLink} from "react-router-dom";
import './Home.css';
import logo from '../home/collaborating.png';

class Home extends React.Component {
  state = {
    // to add new endpoints, the only thing you need to do is to add your endpoint into this object, 
    // every thing will be done automatically for you. ;)
    endpointsByMethods: {
      GET: [
        {key: '/users', params: [], renderType: ['/users']}, 
        {key: '/users/{userId}', params: [{key: 'userId', value: 0, type: 'number', regex: /{userId}/g}], renderType: ['/users/', '{userId}']},
        {key: '/users/{userId}/tasks', params: [{key: 'userId', value: 0, type: 'number', regex: /{userId}/g}], renderType: ['/users/', '{userId}', '/tasks/']},
        {
          key: '/users/{userId}/tasks/{taskId}', 
          params: [
            {key: 'userId', value: 0, type: 'number', regex: /{userId}/g},
            {key: 'taskId', value: 0, type: 'number', regex: /{taskId}/g},
          ],
          renderType: ['/users/', '{userId}', '/tasks', '{taskId}']
        }
      ],
      REPORTS: [
        {key: '/reports/userId', params: [], renderType: ['/reports/userId']}, 
        {key: '/reports/taskId', params: [], renderType: ['/reports/taskId']}, 
        {key: '/reports/users', params: [], renderType: ['/reports/users']}, 
        {key: '/reports/tasks', params: [], renderType: ['/reports/tasks']}
      ]
    },
    badInputAlert: '',
    emptyInputAlert: ''
  };

  handleParamInputChange({method, endpointKey, paramKey, value}) {
    var endpointsByMethods = {...this.state.endpointsByMethods};
    var endpoints = endpointsByMethods[method];
    var endpoint = endpoints.find(endpoint => endpoint.key === endpointKey);
    var param = endpoint.params.find(param => param.key === paramKey);

    // validate user input
    if (value && param.type === 'number' && isNaN(parseInt(value))) {
      this.setState({badInputAlert: "wrong input!! pay attention to the param's type."});

      var input = document.getElementById(endpointKey);

      input.value = '';
    }
    else {
      param.value = param.type === 'number' ? parseInt(value) : value;

      this.setState({endpointsByMethods});
    }
  }

  triggerEndpoint({method, endpointKey}) {
    var {history} = this.props;
    var {endpointsByMethods} = this.state;
    var endpoints = endpointsByMethods[method];
    var {params} = endpoints.find(endpoint => endpoint.key === endpointKey);
    var endpoint = endpointKey;
    var updatedEndpoint = endpoint;
    var readyToTrigger = true;

    if (params.length > 0) {
      params.forEach(param => {
        if (param.value) updatedEndpoint = updatedEndpoint.replace(param.regex, param.value);
        else {
          readyToTrigger = false;
          this.setState({emptyInputAlert: 'make sure you fill in all required params!!'});
  
          return;
        }
      });
    }

    // push to history to change the endpoint
    if (readyToTrigger) history.push(updatedEndpoint);
  }

  render() {
    var {endpointsByMethods, badInputAlert, emptyInputAlert} = this.state;
    var methods = Object.keys(endpointsByMethods);

    // what happens here is basically mapping over endpointsByMethods and rendering a method title, endpoints, and params
    return (
      <div>
        <div className="background"></div>
          <h1 className='main-heading'>AD440 CLOUD COMPUTING</h1>
            <div className="home-container">
              <NavLink to={`/create`} onClick={null}>
                <Button variant="success" size="lg">Create User</Button>
              </NavLink>
              <div className="box-wrapper">
                <div className="box-left">
                  <img src={logo} alt="Two people collaborating"></img>
                </div>
                <div className="box-right">
                <h2 className='sub-header'>Endpoints</h2>
                <hr></hr>
                {badInputAlert && <Alert variant="danger" onClose={() => this.setState({badInputAlert: ''})} dismissible>{badInputAlert}</Alert>}
                {emptyInputAlert && <Alert variant="danger" onClose={() => this.setState({emptyInputAlert: ''})} dismissible>{emptyInputAlert}</Alert>}
                {methods.map(method => {
                  return (
                    <div className='method-container' key={method}>
                      <h4 className='method-header'>{method}</h4>
                      {endpointsByMethods[method].map(endpoint => {
                        var triggerEndpointArgs = {method, endpointKey: endpoint.key};
                        return (
                          <div className='endpoints-container' key={endpoint.key}>
                            <div className='endpoint-title'>
                              {endpoint.renderType.map((type, index) => {
                                if (['{userId}', '{taskId}'].includes(type)) {
                                  var handlePramInputChangeArgs = {method, endpointKey: endpoint.key, paramKey: type.split(/([{, }])/)[2]};
                                  return (
                                    <input 
                                      className='param-input' 
                                      id={`${endpoint.key}-${type}`} type='text' 
                                      placeholder={type} 
                                      key={index}
                                      onKeyDown={(event) => event.key === 'Enter' && this.triggerEndpoint(triggerEndpointArgs)}
                                      onChange={(event) => this.handleParamInputChange({value: event.target.value, ...handlePramInputChangeArgs})}
                                    ></input>
                                  )
                                }
                                else {
                                  return <div>{type}</div>
                                }
                              })}
                            </div>
                            <Button className='btn-send' onClick={() => this.triggerEndpoint(triggerEndpointArgs)}>Send</Button>
                          </div>
                        )
                      })}
                    </div>
                  )
                })}      
              </div>
            </div>
            <br/>
          <p className="copyright">&copy; 2021 | North Seattle College | Application Development | with Toddy Mladenov | <a href="https://northseattle.edu/" target="_blank">https://northseattle.edu</a></p>
        </div>
     </div> 
    )
  }
}

export default withRouter(Home);
